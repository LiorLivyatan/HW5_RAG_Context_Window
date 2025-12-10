# Deployment Architecture

This document describes the deployment architecture of the Context Windows Lab.

## Deployment Diagram

The system is designed for local deployment to ensure privacy and eliminate API costs.

```mermaid
graph TD
    User[User / Researcher] -->|CLI Commands| App[Context Windows Lab\n(Python Application)]
    
    subgraph "Local Workstation"
        App -->|Read/Write| Config[Configuration Files\n(YAML, .env)]
        App -->|Read/Write| Data[Data Directory\n(Raw Documents)]
        App -->|Write| Results[Results Directory\n(JSON, PNG)]
        
        App -->|HTTP API| Ollama[Ollama Service\n(Local LLM Server)]
        
        App -->|Embed/Query| Chroma[ChromaDB\n(Embedded Vector Store)]
        
        subgraph "Ollama Service"
            Llama2[Llama 2 Model]
            TinyLlama[TinyLlama Model]
        end
    end
    
    classDef component fill:#f9f,stroke:#333,stroke-width:2px;
    classDef storage fill:#ff9,stroke:#333,stroke-width:2px;
    classDef actor fill:#9ff,stroke:#333,stroke-width:2px;
    
    class User actor;
    class App component;
    class Config,Data,Results,Chroma storage;
    class Ollama component;
```

## Comparisons

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Compute** | Local CPU/GPU | Privacy, zero cost, reproducibility |
| **LLM Provider** | Ollama | Easy local model management, OpenAI-compatible API |
| **Vector Store** | ChromaDB | Embedded (no separate process), simple, fast |
| **Storage** | Local Filesystem | Simple, transparent, easy to backup |
