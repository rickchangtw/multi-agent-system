# Multi-Agent Community Management System - Deployment Guide

## System Overview

This document describes the complete multi-agent system for managing a 600-unit community with specialized AI agents for different management domains.

## System Architecture

### Core Components

1. **Agent Configurations** (`agents/`)
   - 6 specialized agents with distinct roles
   - YAML-based configuration with role, capabilities, and knowledge bases

2. **Communication Protocol** (`protocols/`)
   - Structured message format for agent-to-agent communication
   - Escalation paths and routing rules
   - Priority-based delivery mechanisms

3. **Event Definitions** (`events/`)
   - 4 event types with defined handlers
   - Action-based event processing logic

4. **State Schema** (`state/`)
   - Shared state structure for all agents
   - Agent states, event logs, and system time

### Agent Roles

| Agent | Role | Description |
|-------|------|-------------|
| admin | Total Director (總幹事) | Central authority, manages all operations |
| property | Property Manager (物業管理) | Maintenance, vendors, space management |
| security | Security Officer (保全) | Access control, threat detection, incident response |
| fire | Fire Safety Officer (消防) | Fire detection, suppression, egress management |
| energy | Energy Manager (節能管理) | Load balancing, grid interaction, efficiency |
| notify | Notification Center (通知中心) | Broadcast delivery, message routing, alerts |

## Deployment Steps

### 1. System Setup

```bash
# Navigate to the multi-agent system directory
cd /home/rick/shared-wiki/multi-agent-system

# Validate the system
python3 test_complete_system.py
```

### 2. Server Deployment

```bash
# Start the server
cd /home/rick/shared-wiki/multi-agent-system
python3 server.py

# Server starts on port 3021
# Endpoints available:
# - GET /api/health
# - GET /api/agents
# - GET /api/agent/{name}
# - POST /api/message
# - POST /api/event
# - GET /api/state
# - GET /api/events
# - POST /api/system/restart
```

### 3. Testing

#### Unit Tests
```bash
# Run complete system validation
python3 test_complete_system.py

# Run communication protocol tests
python3 tests/test_communication.py
```

#### Integration Tests
```bash
# Test API endpoints
curl http://127.0.0.1:3021/api/health
curl http://127.0.0.1:3021/api/agents
curl http://127.0.0.1:3021/api/agent/admin
curl http://127.0.0.1:3021/api/health
```

## File Structure

```
multi-agent-system/
├── agents/
│   ├── admin.yaml
│   ├── energy.yaml
│   ├── fire.yaml
│   ├── notify.yaml
│   ├── property.yaml
│   └── security.yaml
├── events/
│   └── events.yaml
├── protocols/
│   └── communication.yaml
├── state/
│   └── state-schema.md
├── tests/
│   └── test_communication.py
├── wiki/
│   ├── multi-agent-system.md
│   ├── infrastructure.md
│   ├── operations.md
│   ├── data.md
│   └── log.md
├── server.py
├── test_complete_system.py
├── DEPLOYMENT-GUIDE.md
└── VALIDATION_REPORT.md
```

## Configuration Examples

### Agent Configuration (admin.yaml)

```yaml
name: admin
role: "Total Director (總幹事)"
description: "The admin agent is the central authority in the community management system..."
capabilities:
  - "Manage resident lifecycle"
  - "Enforce policies"
  - "Make decisions"
  - "Coordinate agents"
  - "System administration"
```

### Event Definition (events.yaml)

```yaml
events:
  - name: incident.escalation
    description: "Escalate an incident to the admin agent for decision-making"
    priority: high
    from:
      - "fire.agent"
      - "security.agent"
    to: "admin.agent"
    data:
      building: string
      floor: integer
      sensor_id: string
      validated: boolean
      suppression_active: boolean
    actions:
      - "Acknowledge incident"
      - "Assign response team"
      - "Update incident status"
```

### Communication Protocol (communication.yaml)

```yaml
message_format:
  from: agent_name
  to: agent_name
  type: message_type
  priority: critical|high|normal|low
  subject: brief subject line
  data: message-specific data
  timestamp: ISO 8601 format
  correlation_id: unique-identifier

message_types:
  incident_escalation:
    from: "fire.agent / security.agent"
    to: "admin.agent"
    type: "incident.escalation"
    priority: "critical"
    data: "incident details"
```

## Validation Results

### System Validation

✅ **All agent configurations valid**
- 6 agents: admin, energy, fire, notify, property, security

✅ **Communication protocol valid**
- Message format: Valid
- Message types: 4 types defined
- Escalation paths: 2 paths defined
- Communication channels: 3 channels defined
- Routing rules: 5 rules defined

✅ **Event definitions valid**
- 4 events: incident.escalation, emergency.broadcast, maintenance.requested, access.denied

✅ **State schema valid**
- Agent states, event log, shared state, system time

✅ **Multi-agent scenarios validated**
- Fire Emergency: 4 messages validated
- Maintenance Request: 4 messages validated
- Access Control: 3 messages validated

✅ **Event handlers valid**
- incident.escalation: 2 actions
- emergency.broadcast: 2 actions
- maintenance.requested: 2 actions
- access.denied: 2 actions

## Next Steps

1. **Deploy to Production**
   - Use Docker Compose for containerized deployment
   - Configure environment variables
   - Set up monitoring

2. **Integrate with LLaMA.cpp**
   - Connect to local LLaMA.cpp server
   - Implement agent AI capabilities

3. **Add OpenWiki Integration**
   - Integrate with OpenWiki for knowledge base
   - Implement `openwiki personal --update` queries

4. **Implement Communication Channels**
   - Set up push notifications
   - Configure email/SMS integration
   - Implement voice call capabilities

5. **Monitor and Optimize**
   - Set up logging
   - Monitor message routing
   - Track event processing

## Troubleshooting

### Common Issues

1. **YAML Parsing Errors**
   - Ensure YAML files are valid
   - Use `yaml.safe_load()` for parsing
   - Check for special characters (→, etc.)

2. **Server Not Starting**
   - Check port availability
   - Ensure Python dependencies are installed
   - Verify configuration files exist

3. **Message Routing Issues**
   - Check agent configurations
   - Verify escalation paths
   - Review priority levels

4. **State Sync Issues**
   - Check shared state schema
   - Verify agent state updates
   - Review event logging

## Contact

For issues or questions, refer to the wiki documentation:
- `wiki/multi-agent-system.md`
- `wiki/infrastructure.md`
- `wiki/operations.md`
- `wiki/data.md`

---

**Deployment Date**: 2026-07-20
**System Version**: 1.0.0
**Status**: ✅ Validated and Ready
