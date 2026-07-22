# Multi-Agent System - 600-Resident Smart Community

## Overview

A multi-agent system for managing a 600-resident community with 6 autonomous agents:
- **admin** — Resident lifecycle, policy enforcement, decision authority
- **property** — Maintenance scheduling, vendor management, space management
- **security** — Access control, threat detection, incident response
- **fire** — Fire detection, suppression systems, egress management
- **energy** — Load management, grid interaction, efficiency optimization
- **notify** — Broadcast delivery, message routing, alert management

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Event Bus (Redis/RabbitMQ)                │
└──────────┬──────────────────────────────────────────────────┘
           │
    ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
    │   Admin     │  │  Property   │  │   Security   │
    └─────────────┘  └─────────────┘  └─────────────┘
           │              │                │
    ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
    │    Fire     │  │    Energy   │  │    Notify    │
    └─────────────┘  └─────────────┘  └─────────────┘
           │              │                │
    ┌──────▼──────────────────────────────────────▼──────┐
    │              PostgreSQL (Shared State)               │
    └─────────────────────────────────────────────────────┘
```

## Directory Structure

```
multi-agent-system/
├── README.md                 # This file
├── agents/                   # Agent system prompts and configurations
│   ├── admin.yaml
│   ├── property.yaml
│   ├── security.yaml
│   ├── fire.yaml
│   ├── energy.yaml
│   └── notify.yaml
├── protocols/                # Communication protocols
│   └── communication.yaml
├── events/                   # Event definitions and handling
│   └── events.yaml
├── state/                    # Shared state management
│   └── state-schema.md
└── tests/                    # Test scripts
    └── test-agents.sh
```

## Quick Start

1. Configure agents in `agents/` directory
2. Define communication protocols in `protocols/`
3. Set up event handling in `events/`
4. Run tests in `tests/`

## Knowledge Base

The system is based on the OpenWiki personal brain at `~/.openwiki/wiki/`:
- `agents.md` — Agent architecture
- `infrastructure.md` — Physical infrastructure
- `residents.md` — Resident management
- `operations.md` — Operational workflows
- `data.md` — Data architecture and APIs
- `quickstart.md` — System overview
