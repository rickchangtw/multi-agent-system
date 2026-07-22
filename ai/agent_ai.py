#!/usr/bin/env python3
"""
Multi-Agent System - AI Integration Module
多 Agent 系統 AI 整合模組
"""

import json
import os
import sys
import time
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "ai_config.yaml"
AI_DIR = BASE_DIR / "ai"
PROMPT_DIR = BASE_DIR / "prompt_templates"

# Load config
try:
    import yaml
except ImportError:
    # Fallback to simple config
    config = {}
else:
    config = yaml.safe_load(open(CONFIG_PATH)) or {}

# AI Client
class AIClient:
    """AI Client for LLaMA.cpp integration"""
    
    def __init__(self, config: dict):
        self.base_url = config.get("model_config", {}).get("base_url", "http://127.0.0.1:9000/v1")
        self.api_key = config.get("model_config", {}).get("api_key", "local")
        self.temperature = config.get("model_config", {}).get("temperature", 0.7)
        self.max_tokens = config.get("model_config", {}).get("max_tokens", 1024)
        self.top_p = config.get("model_config", {}).get("top_p", 0.9)
        self.model_name = config.get("model_config", {}).get("model", "default")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat_completion(self, messages: List[dict], agent_name: str = "default") -> Optional[dict]:
        """Send chat completion request to LLaMA.cpp"""
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "content": data["choices"][0]["message"]["content"],
                    "finish_reason": data["choices"][0]["finish_reason"],
                    "model": data.get("model", self.model_name),
                    "usage": data.get("usage", {})
                }
            else:
                return {
                    "error": f"API Error: {response.status_code}",
                    "details": response.text[:500]
                }
        except Exception as e:
            return {
                "error": str(e),
                "details": "Connection failed"
            }
    
    def stream_completion(self, messages: List[dict], agent_name: str = "default") -> Optional[typing.Generator[str, None, None]]:
        """Stream chat completion response"""
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "stream": True
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                stream=True,
                timeout=30
            )
            
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "choices" in data:
                        delta = data["choices"][0].get("delta", {})
                        if "content" in delta:
                            yield delta["content"]
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def test_connection(self) -> bool:
        """Test AI server connection"""
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception:
            return False

# Knowledge Base Module
class KnowledgeBase:
    """Knowledge Base for community management"""
    
    def __init__(self, wiki_dir: str = "/home/rick/shared-wiki/wiki"):
        self.wiki_dir = Path(wiki_dir)
        self.documents = {}
        self.load_documents()
    
    def load_documents(self):
        """Load all wiki documents"""
        if not self.wiki_dir.exists():
            return
        
        for doc_path in self.wiki_dir.glob("*.md"):
            doc_name = doc_path.stem
            try:
                with open(doc_path, 'r', encoding='utf-8') as f:
                    self.documents[doc_name] = f.read()
            except Exception:
                pass
    
    def search(self, query: str, doc_names: List[str] = None) -> List[dict]:
        """Search knowledge base"""
        results = []
        query_lower = query.lower()
        
        for doc_name, content in self.documents.items():
            if doc_names and doc_name not in doc_names:
                continue
            
            if query_lower in content.lower():
                results.append({
                    "doc_name": doc_name,
                    "content": content[:500],  # First 500 chars
                    "relevance": "high"
                })
        
        return results
    
    def get_document(self, doc_name: str) -> Optional[str]:
        """Get specific document"""
        return self.documents.get(doc_name)
    
    def get_all_documents(self) -> Dict[str, str]:
        """Get all documents"""
        return self.documents

# Agent Prompt Templates
class AgentPrompts:
    """Agent prompt templates"""
    
    def __init__(self):
        self.admin = self._load_prompt("admin")
        self.property = self._load_prompt("property")
        self.security = self._load_prompt("security")
        self.fire = self._load_prompt("fire")
        self.energy = self._load_prompt("energy")
        self.notify = self._load_prompt("notify")
    
    @staticmethod
    def _load_prompt(agent_name: str) -> str:
        """Load prompt template"""
        prompt_path = PROMPT_DIR / f"{agent_name}_prompts.md"
        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        return f"You are a {agent_name} agent in a community management system. Respond in Traditional Chinese."
    
    def get_system_prompt(self, agent_name: str) -> str:
        """Get system prompt for agent"""
        prompt_path = PROMPT_DIR / f"{agent_name}_prompts.md"
        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        return f"You are a {agent_name} agent in a community management system. Respond in Traditional Chinese."

# Main AI Module
class MultiAgentAI:
    """Main AI module for multi-agent system"""
    
    def __init__(self, config_path: str = None):
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
        else:
            config = config
        
        self.ai_client = AIClient(config)
        self.knowledge_base = KnowledgeBase()
        self.agent_prompts = AgentPrompts()
    
    def query(self, question: str, agent_name: str = "admin") -> dict:
        """Query AI with knowledge base"""
        # Build messages
        messages = [
            {"role": "system", "content": self.agent_prompts.get_system_prompt(agent_name)},
            {"role": "user", "content": f"Based on the community knowledge base, answer: {question}"}
        ]
        
        # Add relevant documents
        results = self.knowledge_base.search(question)
        if results:
            docs = "\n\n".join([f"[{r['doc_name']}]: {r['content']}" for r in results[:3]])
            messages.append({"role": "system", "content": f"Relevant knowledge:\n{docs}"})
        
        # Send to AI
        response = self.ai_client.chat_completion(messages, agent_name)
        
        return {
            "question": question,
            "agent": agent_name,
            "answer": response.get("content", "") if response else "",
            "error": response.get("error") if response else None,
            "timestamp": datetime.now().isoformat()
        }
    
    def test_connection(self) -> bool:
        """Test AI connection"""
        return self.ai_client.test_connection()
    
    def search_knowledge(self, query: str, doc_names: List[str] = None) -> List[dict]:
        """Search knowledge base"""
        return self.knowledge_base.search(query, doc_names)
    
    def get_agent_prompts(self, agent_name: str) -> str:
        """Get agent prompt template"""
        return self.agent_prompts.get_system_prompt(agent_name)

# Test
if __name__ == "__main__":
    print("=" * 60)
    print("Multi-Agent AI Integration Test")
    print("=" * 60)
    
    # Test AI client
    print("\n1. Testing AI connection...")
    ai = MultiAgentAI()
    connected = ai.test_connection()
    print(f"   Connection: {'✅ OK' if connected else '❌ Failed'}")
    
    # Test knowledge base
    print("\n2. Testing Knowledge Base...")
    docs = ai.knowledge_base.get_all_documents()
    print(f"   Documents loaded: {len(docs)}")
    for doc_name in docs:
        print(f"   - {doc_name}")
    
    # Test query
    print("\n3. Testing query...")
    result = ai.query("如何申請電梯維修？")
    print(f"   Answer: {result.get('answer', '')[:200]}..." if result.get('answer') else f"   Error: {result.get('error', '')}")
    
    print("\n" + "=" * 60)
    print("✅ AI Integration Test Complete")
    print("=" * 60)
