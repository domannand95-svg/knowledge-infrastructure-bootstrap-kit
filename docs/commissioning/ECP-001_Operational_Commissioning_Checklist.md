# Operational Commissioning Checklist (`ECP-001` - Execution Phase)

| Property | Value |
| --- | --- |
| **Document ID** | ECP-001 (Execution Checklist Supplement) |
| **Status** | Active Operational Checklist (Temporary / Commissioning Phase) |
| **Target Completion** | Pre-SMART Board Demonstration (Monday) |

---

# Current Operational Status

| Property | Value |
| --- | --- |
| **Phase** | Bootstrap Commissioning |
| **State** | In Progress |
| **Current Stage** | Stage 1 — Bootstrap Kit Audit |
| **Next Milestone** | Validate Local AI Classification Pipeline |

---

# Execution Schedule & Objectives

## Stage 1 — Bootstrap Kit Audit (Priority 1)

Systematically review each top-level repository folder to establish the active operating map.

For every folder, record only three governing attributes:

- **Purpose:** What is the core function of this folder?
- **Contains:** What specific items belong here?
- **Does Not Contain:** What materials are explicitly excluded from this folder?

---

## Stage 2 — Local AI Workflow Test

Execute deterministic processing on a single, real New Waste Order document using the local environment (Mistral/Ollama) and the constitutional classification standard (`NWO-000`).

```text
Single Target Document
           ↓
 Markdown Conversion (.md)
           ↓
Local AI Classification (Ollama / Mistral + NWO-000)
           ↓
    Human Review & Verification
           ↓
Module Assignment OR Refinement Queue
```

---

## Stage 3 — Evidence Package Backlog

Following **initial** local workflow validation, commission focused, bounded research requests rather than broad exploratory queries.

### Evidence Package 1 — `NWO-004` (Organic Resource Library)

- Current literature review
- Evidence gap identification
- Conflicting data analysis
- Recent Australian baseline studies

### Evidence Package 2 — `NWO-012` (Thermal Systems)

- Current reactor designs
- Autothermal operation parameters
- Biochar quality metrics
- Emission controls
- Commercial feasibility

### Evidence Package 3 — `NWO-015` (Ecological Restoration)

- Australian restoration ecology frameworks
- Native species selection and succession
- Long-term monitoring protocols
- Evidence quality assessment

---

# Operational Responsibilities

| Responsibility | Assigned To |
| --- | --- |
| Deterministic organisation, classification, and first-pass document sorting | **Local Ollama (Mistral)** |
| External literature gathering, source comparison, and structured evidence package synthesis | **Gemini Deep Research** |
| Constitutional architecture review, governance critique, workflow verification, and internal consistency testing | **ChatGPT** |
| Final verification, review, and promotion authority | **Human Operator (@domannand95)** |
| Automated file routing, metadata verification, and repository maintenance | **Supporting Tooling (Scripts / Future Rust Utilities)** |

---

# Exit Criteria

`ECP-001` shall be considered complete when:

- Bootstrap Kit folder audit is complete.
- Local AI successfully classifies at least one real document.
- End-to-end workflow has been validated.
- Initial Deep Research backlog has been established.
- SMART Board demonstration environment has been prepared and validated.

Upon successful completion:

- This execution checklist shall be archived as a historical commissioning record.
- Any validated improvements shall be promoted into the Bootstrap Kit through the established governance process.

---

# Design Principle

Commission first. Refine second.

The purpose of this checklist is to validate the engineering workflow in practice rather than expand the governance framework. Reusable improvements discovered during commissioning shall be promoted into the Bootstrap Kit, while execution-specific activities remain part of the historical commissioning record.