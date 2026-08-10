\# AI Component Catalogue

\| Property \| Value \|

\|---\|---\|

\| Document ID \| ACC-001 \|

\| Version \| 1.0 \|

\| Status \| Active Reference \|

\| Document Owner \| @domannand95 \|

\| Effective Date \| 2026-08-07 \|

\> \*\*Purpose\*\*

\>

\> Provide a centralized inventory of all artificial intelligence
platforms, local models, APIs, software components, and supporting
technologies utilised within the Knowledge Infrastructure Bootstrap Kit,
Digital Archive, Sovereign OS, and associated research environments.

---

\# Overview

The AI Component Catalogue serves as the authoritative inventory for all
operational AI resources.

Unlike the AI Ecosystem Roadmap, Commissioning Manual, and Operations
Manual, this document does not define architecture or workflow. Instead,
it records what components exist, why they are used, their operational
role, and their current lifecycle status.

This catalogue should be updated whenever AI platforms, models, or
infrastructure components are added, modified, retired, or replaced.

---

\# Objectives

The catalogue aims to:

\- maintain an authoritative inventory of AI components;

\- document operational responsibilities;

\- support commissioning and recovery;

\- simplify maintenance;

\- preserve historical configuration records;

\- minimise undocumented software dependencies.

---

\# Scope

This document includes:

\- cloud AI platforms;

\- local language models;

\- embedding models;

\- APIs;

\- development tools;

\- orchestration software;

\- vector databases;

\- speech and vision systems;

\- future research components.

---

\# Dependencies

This catalogue should be used alongside:

\- Knowledge Governance Framework

\- AI Ecosystem & Infrastructure Roadmap

\- AI Platform Commissioning Manual

\- AI Operations Manual

\- Workstation Profile

\- Sovereign OS

---

\# Lifecycle Status

Components progress through the following lifecycle:

Proposed

↓

Evaluation

↓

Operational

↓

Maintenance

↓

Deprecated

↓

Retired

↓

Archived

---

\# Cloud AI Services

\| Platform \| Primary Purpose \| Status \|

\|---\|---\|---\|

\| ChatGPT \| Architecture, engineering, documentation \| Operational \|

\| Gemini Deep Research \| Literature review and external research \|
Operational \|

\| NotebookLM \| Source-grounded document reasoning \| Operational \|

\| Grok API \| Alternative reasoning and critique \| Operational \|

\| Claude (Collaborator) \| Collaborative engineering review \|
Operational \|

---

\# Local AI Infrastructure

\| Component \| Purpose \| Status \|

\|---\|---\|---\|

\| Ollama \| Local inference engine \| Operational \|

\| Open WebUI \| Browser interface for local models \| Planned \|

\| Hugging Face \| Model and dataset repository \| Operational \|

---

\# Installed Local Models

\| Model \| Primary Role \| Status \|

\|---\|---\|---\|

\| Llama 3.2 \| General reasoning \| Operational \|

\| Qwen 2.5 \| General reasoning \| Operational \|

\| Qwen 2.5 Coder \| Software engineering \| Operational \|

\| DeepSeek Coder \| Code review and debugging \| Operational \|

\| Phi-4 Mini \| Lightweight reasoning \| Operational \|

\| Mistral Small \| Architecture and planning \| Operational \|

---

\# Embedding Models

\| Model \| Purpose \| Status \|

\|---\|---\|---\|

\| nomic-embed-text \| Semantic embeddings and RAG \| Planned \|

---

\# Vector Databases

\| Component \| Purpose \| Status \|

\|---\|---\|---\|

\| ChromaDB \| Local semantic search \| Planned \|

\| Qdrant \| Scalable vector storage \| Future Evaluation \|

---

\# Speech Processing

\| Component \| Purpose \| Status \|

\|---\|---\|---\|

\| Whisper \| Speech-to-text transcription \| Planned \|

---

\# Vision & OCR

\| Component \| Purpose \| Status \|

\|---\|---\|---\|

\| OCR Engine \| Document digitisation \| Future Evaluation \|

\| Vision Models \| Image understanding \| Future Evaluation \|

---

\# Development Environment

\| Component \| Purpose \| Status \|

\|---\|---\|---\|

\| VS Code \| Primary development environment \| Operational \|

\| Git \| Version control \| Operational \|

\| GitHub \| Repository hosting \| Operational \|

\| Rust \| Systems development \| Operational \|

\| Python \| Automation and AI tooling \| Operational \|

---

\# Knowledge Infrastructure

\| Component \| Purpose \| Status \|

\|---\|---\|---\|

\| Knowledge Infrastructure Bootstrap Kit \| Governance \| Operational
\|

\| Digital Archive \| Long-term knowledge preservation \| Operational \|

\| Sovereign OS \| Future orchestration platform \| Active Development
\|

---

\# API Services

\| API \| Purpose \| Status \|

\|---\|---\|---\|

\| Grok API \| Cloud reasoning \| Operational \|

\| GitHub API \| Repository integration \| Operational \|

\| Hugging Face API \| Model ecosystem \| Available \|

---

\# Storage Components

\| Component \| Purpose \| Status \|

\|---\|---\|---\|

\| Internal SSD \| Active workspace \| Operational \|

\| External SSD \| Archive and backups \| Planned \|

\| Cloud Storage \| Off-site redundancy \| Operational \|

\| Cold Archive \| Long-term preservation \| Planned \|

---

\# Planned Components

The following technologies remain under evaluation and should only be
adopted when justified by operational evidence:

\- Open WebUI

\- ChromaDB

\- Qdrant

\- Whisper

\- Local RAG

\- Embedding services

\- Automated document indexing

\- Local AI agents

\- Multi-agent orchestration

\- Sovereign OS AI integration

---

\# Component Review Criteria

Before a component progresses to Operational status, it should
demonstrate:

\- operational necessity;

\- measurable productivity improvement;

\- acceptable maintenance burden;

\- compatibility with existing workflows;

\- reproducible installation;

\- security review;

\- governance compliance.

---

\# Retirement Policy

Components should be retired when:

\- no longer actively used;

\- superseded by a superior alternative;

\- incompatible with current infrastructure;

\- unsupported or insecure.

Retirement should preserve historical configuration records where
appropriate.

---

\# Maintenance Schedule

Monthly

\- Review updates.

\- Remove obsolete models.

\- Review storage utilisation.

Quarterly

\- Benchmark local models.

\- Review AI subscriptions.

\- Evaluate new releases.

Annually

\- Audit the complete AI ecosystem.

\- Review architecture.

\- Update the catalogue.

---

\# Component Relationships

\`\`\`text

Knowledge Governance Framework

│

▼

AI Ecosystem Roadmap

│

▼

AI Platform Commissioning

│

▼

AI Operations Manual

│

▼

AI Component Catalogue

│

▼

Operational AI Environment

│

▼

Digital Archive

│

▼

Sovereign OS

\`\`\`

---

\# Revision History

\| Version \| Date \| Summary \|

\|---\|---\|---\|

\| 1.0 \| 2026-08-07 \| Initial AI component inventory. \|

---

\# Design Principle

The AI ecosystem should remain modular, observable, and replaceable.

Individual models, APIs, and software platforms will evolve over time.
The catalogue preserves a clear inventory of operational capability
while ensuring that governance, knowledge, and engineering practices
remain independent of any specific technology.
