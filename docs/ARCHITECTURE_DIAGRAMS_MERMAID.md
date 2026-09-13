# End-to-End System & AI Architecture Diagrams (Mermaid)
**Project:** AI/NLP Engine to Detect Serious Injury & Fatality (SIF) Precursors  
**Problem Statement ID:** SIH26165 (Oil India Limited - OIL)  
**Team:** Tech Smashers  
**Target Usage:** SIH 2026 Presentation Slides (PowerPoint / Keynote), Technical Defense & Evaluation

---

## Quick Presentation Guide (How to use in PowerPoint)
1. **Option A (Instant High-Res Image for Slides):** Copy any diagram block below, paste it into [mermaid.live](https://mermaid.live), and click **Download PNG (High Res)** or **Download SVG**. Insert directly into your PowerPoint slide!
2. **Option B (Native PowerPoint Add-in):** If you use the *Mermaid Previewer* add-in or Office 365 Mermaid extension, you can paste the Mermaid code directly into PowerPoint.
3. **Option C (Markdown Presentation Tools):** If using Marp, Slidev, or Obsidian Slides, these diagrams render natively with full vector clarity.

---

## Slide Diagram Index
- **Diagram 1:** [Master End-to-End System & Dataflow Architecture](#diagram-1-master-end-to-end-system--dataflow-architecture)
- **Diagram 2:** [Deep-Dive AI/NLP Dual-Track Safety Intelligence Engine](#diagram-2-deep-dive-ainlp-dual-track-safety-intelligence-engine)
- **Diagram 3:** [Incident Report Lifecycle & Human-in-the-Loop (HIL) Governance](#diagram-3-incident-report-lifecycle--human-in-the-loop-hil-governance)
- **Diagram 4:** [Physical Deployment & Container Infrastructure Topology](#diagram-4-physical-deployment--container-infrastructure-topology)
- **Diagram 5:** [Zero-Trust Security, PII Masking & Audit Trail Boundary](#diagram-5-zero-trust-security-pii-masking--audit-trail-boundary)
- **Diagram 6:** [Cross-Report Precursor Pattern Clustering & Hotspot Synthesis](#diagram-6-cross-report-precursor-pattern-clustering--hotspot-synthesis)

---

### Diagram 1: Master End-to-End System & Dataflow Architecture
> **Slide Title:** End-to-End Platform Architecture: From Field Observation to Explainable SIF Prevention  
> **Key Message:** Demonstrates how raw, messy field prose transitions through sanitization, 11 logical processing layers, dual-path reasoning, and human verification into actionable frontline alerts.

```mermaid
flowchart TD
    %% Global Styling
    classDef clientStyle fill:#EBF3FB,stroke:#0B6BB3,stroke-width:2px,color:#0B2545;
    classDef ingestStyle fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20;
    classDef aiStyle fill:#FFF8E1,stroke:#F57F17,stroke-width:2px,color:#B78103;
    classDef dbStyle fill:#EDE7F6,stroke:#512DA8,stroke-width:2px,color:#311B92;
    classDef hilStyle fill:#FCE4EC,stroke:#C2185B,stroke-width:2px,color:#880E4F;
    classDef outStyle fill:#E0F7FA,stroke:#00838F,stroke-width:2px,color:#006064;

    %% Client Ingestion Sources
    subgraph S1 ["1. Frontline Data Ingestion & Sources"]
        direction TB
        SRC_M["📱 Field Mobile App / PWA\n(Frontline Operators / Rig Workers)"]:::clientStyle
        SRC_W["💻 Web Portal Form\n(Safety Supervisors / Drillers)"]:::clientStyle
        SRC_B["📄 Bulk CSV / Excel Batch Ingest\n(Historical Incident Logs)"]:::clientStyle
        SRC_ERP["🏢 Future OIL Enterprise Connector\n(SAP HSSE / Open Industrial APIs)"]:::clientStyle
    end

    %% Ingestion & Sanitization Gateway
    subgraph S2 ["2. Secure Ingestion & Sanitization Gateway (Layer 3)"]
        direction TB
        GATE["API Gateway & Ingestion Controller\n(FastAPI / Payload Schema Validation)"]:::ingestStyle
        PII["Regex PII Scrubbing Engine\n(Worker Names, Badges, Phone Numbers Masked)"]:::ingestStyle
        HASH["Cryptographic SHA-256 Provenance Hasher\n(Immutable Content Verification & De-duplication)"]:::ingestStyle
        GATE --> PII --> HASH
    end

    %% AI Safety Intelligence Pipeline
    subgraph S3 ["3. AI / NLP Safety Intelligence Engine (Layers 4, 5, 6, 7)"]
        direction TB
        PRE["Domain Preprocessing\n(O&G Abbreviation Expansion & Normalization)"]:::aiStyle
        LING["Contextual NLP Parser (spaCy)\n(Tokenization, Dependency Parsing, Negation Scopes)"]:::aiStyle
        SIG["Physical Safety Signal Extractor\n(Activity, Energy Hazard, Equipment, Exposure Reality)"]:::aiStyle
        
        subgraph DUAL ["Dual-Path Hybrid Reasoning Core"]
            RULE["Deterministic Energy-Barrier Rules\n(Known Physical Hazard Matrix)"]:::aiStyle
            SEM["Semantic Vector Classifier\n(Transformer all-MiniLM-L6-v2; DeBERTa H1)"]:::aiStyle
        end

        BAR["6-State Barrier Integrity Evaluator\n(Present/Verified, Missing, Incomplete, Failed, Bypassed, Unknown)"]:::aiStyle
        LSR["IOGP 9 Life-Saving Rule Classifier\n(Contextual Mapping to Global O&G Standards)"]:::aiStyle
        SIF_DEC["SIF Potential Arbiter & Confidence Scorer\n(Output: SIF YES / NO / REVIEW | Tier: P1, P2, P3)"]:::aiStyle
        EVID["Verbatim Character-Span Evidence Binder\n(Zero-Hallucination Exact Text Grounding)"]:::aiStyle

        PRE --> LING --> SIG
        SIG --> RULE & SEM
        RULE & SEM --> BAR & LSR --> SIF_DEC --> EVID
    end

    %% Persistence & Analytical Engine
    subgraph S4 ["4. Data & Pattern Discovery Persistence (Layers 8 & 10)"]
        direction TB
        PG[("PostgreSQL 16 Enterprise Relational DB\n(Canonical Reports, Findings, Audits)")]:::dbStyle
        VEC[("pgvector Semantic Store\n(Report Embeddings & Similarity Index)")]:::dbStyle
        PAT["Cross-Report Pattern Discovery Engine\n(Multi-Dimensional Hotspot Clustering: N >= 3)"]:::dbStyle
        PG <--> VEC
        PG --> PAT
    end

    %% Human Governance & Action Tier
    subgraph S5 ["5. Human-in-the-Loop Governance & Action (Layers 9 & 11)"]
        direction TB
        QUEUE["HSE Attention Queue & Priority Triage\n(P1 Critical: <15m, P2 High: <4h, P3: <24h)"]:::hilStyle
        REV_UI["HSE Officer Validation Console\n(Inspect Verbatim Evidence, Confirm / Overrule / Correct)"]:::hilStyle
        AUDIT["Immutable Audit Ledger\n(Chained SHA-256 Logs of all Inferences & Overrides)"]:::hilStyle
        QUEUE --> REV_UI --> AUDIT
    end

    %% Executive Dashboards & Alerting
    subgraph S6 ["6. Decision Intelligence & Executive Dashboards (Layer 1)"]
        direction TB
        DASH["HSE Executive Command Center\n(Site Risk Matrix, Precursor Hotspots, Barrier Gaps)"]:::outStyle
        ALERT["Real-Time Critical Alerts\n(Email / SMS / Webhooks for P1 Precursors)"]:::outStyle
        CAPA["Targeted Preventative Action Dispatch\n(Toolbox Talks, Rig Audits, Equipment Servicing)"]:::outStyle
    end

    %% Cross-Subsystem Connections
    SRC_M & SRC_W & SRC_B -.-> GATE
    SRC_ERP -.->|Authorized Connector| GATE
    HASH --> PRE
    EVID --> PG
    EVID --> QUEUE
    PAT --> DASH
    REV_UI -.->|Reviewer Delta Feedback| RULE
    REV_UI --> CAPA
    SIF_DEC -.->|P1 Trigger| ALERT
```

---

### Diagram 2: Deep-Dive AI/NLP Dual-Track Safety Intelligence Engine
> **Slide Title:** Dual-Path AI Engine: Hybrid Deterministic & Semantic SIF Reasoning  
> **Key Message:** Solves the black-box AI problem. High-risk petroleum engineering decisions cannot rely on unexplainable neural networks alone; our dual-path architecture marries deterministic physics-based barrier rules with contextual deep NLP.

```mermaid
flowchart TD
    classDef raw fill:#ECEFF1,stroke:#455A64,stroke-width:2px,color:#263238;
    classDef nlp fill:#E1F5FE,stroke:#0288D1,stroke-width:2px,color:#01579B;
    classDef dual fill:#FFF9C4,stroke:#FBC02D,stroke-width:2px,color:#F57F17;
    classDef rule fill:#E8F5E9,stroke:#388E3C,stroke-width:2px,color:#1B5E20;
    classDef ml fill:#EDE7F6,stroke:#7E57C2,stroke-width:2px,color:#311B92;
    classDef out fill:#FBE9E7,stroke:#D84315,stroke-width:2px,color:#BF360C;
    classDef exp fill:#E0F2F1,stroke:#00897B,stroke-width:2px,color:#004D40;

    RAW["Raw Unstructured Frontline Narrative\ne.g., 'Tk entered CS @ Dk-4 bfr gas test. No standby guy. Job stpd by supv.'"]:::raw

    subgraph STAGE_A ["Phase 1: Linguistic Normalization & PII Sanitization"]
        PII_M["1. PII Regex Masker\n([NAME_MASKED], [BADGE_MASKED])"]:::nlp
        NORM["2. Oilfield Abbreviation Expander\n('CS' -> Confined Space, 'Dk-4' -> Derrick 4, 'Tk' -> Technician)"]:::nlp
        PARS["3. Contextual Syntax & Negation Parser (spaCy)\nDependency Parsing ('without', 'before', 'failed')"]:::nlp
        PII_M --> NORM --> PARS
    end

    RAW --> PII_M

    subgraph STAGE_B ["Phase 2: Physical Safety Signal Extraction"]
        ACT["Activity Signal: Confined Space Entry"]:::nlp
        HAZ["Hazard Energy: Toxic Atmospheric Gas / Asphyxiation"]:::nlp
        EXP["Worker Exposure: Active Physical Presence Inside Cellar"]:::nlp
        CTL["Control State: Gas Detector Omitted, Standby Attendant Absent"]:::nlp
        PARS --> ACT & HAZ & EXP & CTL
    end

    subgraph STAGE_C ["Phase 3: Dual-Track Reasoning Architecture"]
        subgraph PATH_1 ["Path 1: Deterministic Energy-Barrier Rules"]
            E_MAT["Hazard Energy Matrix\n(CSRA & EEI High-Energy Protocol)"]:::rule
            B_LOG["6-State Barrier Evaluation Logic\n(Present/Verified / Missing / Incomplete / Failed / Bypassed / Unknown)"]:::rule
            E_MAT --> B_LOG
        end

        subgraph PATH_2 ["Path 2: Semantic Representation & Similarity"]
            EMB["Contextual Dense Embedding\n(sentence-transformers/all-MiniLM-L6-v2)"]:::ml
            CLF["Semantic Rule & LSR Matcher\n(Cosine Similarity on 384d Embeddings; DeBERTa fine-tuning H1)"]:::ml
            EMB --> CLF
        end

        ACT & HAZ & EXP & CTL --> PATH_1
        ACT & HAZ & EXP & CTL --> PATH_2
    end

    subgraph STAGE_D ["Phase 4: Synthesis, SIF Arbitration & Standards Mapping"]
        ARB["Hybrid Arbiter & SIF Potential Assessor\nDecouples Recorded Injury from Latent Potential\n(Asymmetric Tuning: Zero Missed High-Energy Events)"]:::dual
        LSR_MAP["IOGP Life-Saving Rules Classifier\n(Rule 2: Confined Space Entry, Rule 6: Energy Isolation)"]:::dual
        PATH_1 & PATH_2 --> ARB
        PATH_1 & PATH_2 --> LSR_MAP
    end

    subgraph STAGE_E ["Phase 5: Verbatim Explainability & Output Contract"]
        EXP_B["Verbatim Evidence Span Binder\nExtracts Exact [start_offset, end_offset] from Narrative"]:::exp
        OUT_JSON["Explainable Safety Intelligence Record\n• SIF Potential: YES (Confidence: 0.94)\n• Priority Tier: P1 - CRITICAL (<15m SLA)\n• Life-Saving Rule: IOGP Rule 2 (Confined Space)\n• Degraded Barrier: Atmospheric Testing (FAILED / BYPASSED)\n• Verbatim Evidence: 'entered CS ... before gas test'"]:::out
        ARB & LSR_MAP --> EXP_B --> OUT_JSON
    end
```

---

### Diagram 3: Incident Report Lifecycle & Human-in-the-Loop (HIL) Governance
> **Slide Title:** Report Lifecycle & Human-in-the-Loop Governance Workflow  
> **Key Message:** No AI recommendation is final without human oversight. This workflow demonstrates how reports move through triage, human verification, corrective action, and immutable audit logging.

```mermaid
stateDiagram-v2
    classDef initial fill:#ECEFF1,stroke:#607D8B,color:#263238;
    classDef processing fill:#FFF8E1,stroke:#FFA000,color:#FF6F00;
    classDef review fill:#FCE4EC,stroke:#D81B60,color:#880E4F;
    classDef verified fill:#E8F5E9,stroke:#43A047,color:#1B5E20;
    classDef closed fill:#EDE7F6,stroke:#5E35B1,color:#311B92;

    [*] --> SUBMITTED : Frontline Worker / Field Supervisor submits Observation Report
    
    SUBMITTED --> INGESTING : Ingestion Gateway validates JSON/CSV Schema
    INGESTING --> SANITIZED : Automated PII Scrubbing + SHA-256 Hash Generated
    
    state "AI Reasoning Engine Pipeline" as AI_PIPELINE {
        SANITIZED --> EXTRACTING_SIGNALS : spaCy parses Activity, Hazard, Controls
        EXTRACTING_SIGNALS --> INFERRING_SIF : Dual-Path Rule + Transformer Inference
        INFERRING_SIF --> BOUND_EVIDENCE : Character-level narrative evidence attached
    }

    BOUND_EVIDENCE --> TRIAGED : System assigns SIF Status & Priority Tier

    state TRIAGED <<choice>>
    TRIAGED --> P1_CRITICAL : SIF Potential = YES (High Energy, No Barrier)
    TRIAGED --> P2_HIGH : SIF Potential = REVIEW (Ambiguous Barrier Data)
    TRIAGED --> P3_STANDARD : SIF Potential = NO (Low Energy / Housekeeping)

    P1_CRITICAL --> PENDING_HSE_REVIEW : Real-Time Alert to HSE Field Officer (<15 min SLA)
    P2_HIGH --> PENDING_HSE_REVIEW : Dispatched to Daily Safety Triage Queue (<4 hr SLA)
    P3_STANDARD --> PENDING_HSE_REVIEW : Added to Weekly Aggregate Queue (<24 hr SLA)

    state "Human Safety Officer Governance Console" as HSE_REVIEW {
        PENDING_HSE_REVIEW --> INSPECTION : Safety Officer inspects verbatim evidence & barriers
        
        state INSPECTION <<choice>>
        INSPECTION --> CONFIRMED : Agree with AI SIF Assessment & Rule Mapping
        INSPECTION --> CORRECTED : Adjust Barrier Status or SIF Rating with Domain Justification
        INSPECTION --> REJECTED : False Alarm / Inconsequential Observation
    }

    CONFIRMED --> AUDITED : Write Immutable Delta to Audit Ledger (SEC-002)
    CORRECTED --> AUDITED : Record Correction Delta for Model Drift & Continuous Learning
    REJECTED --> AUDITED : Log Reason Code & Archive Record

    AUDITED --> ACTION_DISPATCHED : Generate Preventative Action (CAPA / Rig Inspection)
    ACTION_DISPATCHED --> CLOSED : Field Corrective Action Executed & Verified
    CLOSED --> [*]
```

---

### Diagram 4: Physical Deployment & Container Infrastructure Topology
> **Slide Title:** Production-Grade Deployment Architecture: 3-Container Containerized Topology  
> **Key Message:** Designed for zero-downtime, local air-gapped field capability, and seamless enterprise migration. One single command `docker compose up` spins up the entire isolated stack.

```mermaid
flowchart TD
    classDef user fill:#E3F2FD,stroke:#1E88E5,stroke-width:2px,color:#0D47A1;
    classDef edge fill:#EDE7F6,stroke:#5E35B1,stroke-width:2px,color:#311B92;
    classDef app fill:#FFF3E0,stroke:#FB8C00,stroke-width:2px,color:#E65100;
    classDef db fill:#E8F5E9,stroke:#43A047,stroke-width:2px,color:#1B5E20;
    classDef store fill:#ECEFF1,stroke:#546E7A,stroke-width:2px,color:#263238;

    subgraph CLIENT_TIER ["Client & Field Access Layer"]
        CLI_PWA["Operator PWA / Tablet\n(Field Rigs / Remote GGS)"]:::user
        CLI_WEB["HSE Management Browser\n(Corporate Desktop / Ops Room)"]:::user
    end

    subgraph HOST ["Single Node Host / Cloud VPS / On-Prem Rig Server (Ubuntu 22.04 LTS / RHEL)"]
        direction TB

        subgraph FRONTEND ["Presentation & Reverse Proxy Container (sih-frontend)"]
            NGINX["Nginx Web Server (Port 80 / 3000)\n• React 18 + Vite Static Assets\n• Reverse Proxy (/api/v1 -> Backend:8000)\n• Rate Limiting & Gzip"]:::edge
        end

        subgraph BACKEND ["Application & Inference Container (backend-api)"]
            direction TB
            FASTAPI["FastAPI / Python 3.11 Runtime (Port 8000)\n• Uvicorn ASGI Multi-Worker Server\n• Modular Router /api/v1/*\n• PII Sanitizer & SHA-256 Hasher"]:::app
            
            subgraph EMBEDDED_AI ["In-Memory Lightweight AI Engine"]
                SPACY["spaCy 3.7 (en_core_web_sm)\nSyntactic & Dependency NLP"]:::app
                TRANS["sentence-transformers (all-MiniLM-L6-v2)\nSemantic Embedding Engine (Local CPU Optimized)"]:::app
                RULE_MOD["Heuristic Causal & Energy Ruleset\n(CSRA / EEI Energy Category Logic)"]:::app
            end

            FASTAPI --- EMBEDDED_AI
        end

        subgraph PERSISTENCE ["Persistence & Data Container (database)"]
            PG_DB["PostgreSQL 16 Enterprise Relational DB (Port 5432)\n• 11 Normalized Core Tables (3NF)\n• pgvector Extension (Vector Embeddings & Search)\n• Native JSONB Semi-Structured Signal Storage\n• B-Tree & GIN Inverted Indexes"]:::db
        end

        subgraph STORAGE ["Isolated Host Volumes (Persistent SSD)"]
            VOL_PG[("Volume: ./data/postgres\n(Persistent DB Files)")]:::store
            VOL_LOG[("Volume: ./data/audit_events\n(Immutable Chained Logs)")]:::store
        end
    end

    %% Network Connections
    CLI_PWA & CLI_WEB -->|HTTPS / WSS| NGINX
    NGINX -->|Reverse Proxy /| VITE_NODE
    NGINX -->|Reverse Proxy /api/*| FASTAPI
    FASTAPI -->|Async SQLAlchemy 2.0 / Pool Size 20| PG_DB
    PG_DB --- VOL_PG
    FASTAPI --- VOL_LOG
```

---

### Diagram 5: Zero-Trust Security, PII Masking & Audit Trail Boundary
> **Slide Title:** Defense-in-Depth Security & Data Sovereignty Architecture  
> **Key Message:** Guarantees 100% data sovereignty. All AI inference is performed locally on-premise without external public cloud leaks, protected by cryptographic audit chains and strict Role-Based Access Control (RBAC).

```mermaid
flowchart LR
    classDef boundary fill:#FFEBEE,stroke:#C62828,stroke-width:2px,color:#B71C1C;
    classDef rbac fill:#E8EAF6,stroke:#3949AB,stroke-width:2px,color:#1A237E;
    classDef pii fill:#FFF8E1,stroke:#F57F17,stroke-width:2px,color:#E65100;
    classDef audit fill:#E0F2F1,stroke:#00695C,stroke-width:2px,color:#004D40;
    classDef data fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px,color:#4A148C;

    subgraph EXTERNAL ["External Ingestion Boundary"]
        RAW_IN["Raw Frontline Narrative\n(Contains Names, Phone Numbers, Contractor IDs)"]
    end

    subgraph SECURITY_PERIMETER ["Air-Gapped On-Premises Security Perimeter (SEC-001)"]
        direction TB

        subgraph PII_LAYER ["1. Automatic PII Scrubbing Engine"]
            SCRUB["Regex & NER PII Masker\n• Worker Names -> [WORKER_1]\n• Mobile Numbers -> [PHONE_MASKED]\n• Vehicle Numbers -> [VEHICLE_MASKED]"]:::pii
            PROV["Provenance Stamp (DATA-002)\n• Tag: AUTHORIZED_OIL / SYNTHETIC\n• Hash: SHA-256 of Raw Content"]:::pii
            SCRUB --> PROV
        end

        subgraph RBAC_LAYER ["2. Role-Based Access Control (RBAC Matrix)"]
            direction TB
            R1["Frontline Worker: Submit Reports, View Own Status"]:::rbac
            R2["HSE Field Officer: Review Queue, Validate Evidence, Override"]:::rbac
            R3["HSE Manager / Lead: Cross-Site Heatmaps, Export CAPA, Audit"]:::rbac
            R4["System Admin: Manage Users, Monitor Health Probes"]:::rbac
        end

        subgraph CRYPTO_AUDIT ["3. Cryptographic Audit Ledger (SEC-002)"]
            direction TB
            LOG_A["Block N: Report Ingested (Hash: a1b2...)"]:::audit
            LOG_B["Block N+1: AI Inferred SIF YES (Hash: c3d4...)"]:::audit
            LOG_C["Block N+2: Officer Confirmed with Note (Hash: e5f6...)"]:::audit
            LOG_A -->|Chained SHA-256| LOG_B -->|Chained SHA-256| LOG_C
        end

        subgraph ISOLATED_STORE ["4. Encrypted Data Persistence"]
            DB_ENC[("AES-256 Encrypted Database\n• Sanitized Narratives Only\n• Tokenized Evidence Offsets\n• Separation of Raw & Derived State")]:::data
        end
    end

    RAW_IN --> SCRUB
    PROV --> DB_ENC
    RBAC_LAYER <-->|JWT Bearer Token / Role Enforcement| DB_ENC
    DB_ENC -.->|State Transitions| CRYPTO_AUDIT
```

---

### Diagram 6: Cross-Report Precursor Pattern Clustering & Hotspot Synthesis
> **Slide Title:** Cross-Report Pattern Intelligence: Uncovering Latent Systemic Risk  
> **Key Message:** Single incident reporting misses the big picture. Our multi-dimensional clustering algorithm analyzes recurring precursor combinations across rigs and time windows to identify systemic organizational vulnerabilities before an incident occurs.

```mermaid
flowchart TD
    classDef input fill:#EFEBE9,stroke:#4E342E,stroke-width:2px,color:#3E2723;
    classDef cluster fill:#E1F5FE,stroke:#0277BD,stroke-width:2px,color:#01579B;
    classDef metric fill:#FFF3E0,stroke:#EF6C00,stroke-width:2px,color:#E65100;
    classDef action fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20;

    subgraph REPORT_STREAM ["Individual Analyzed Safety Reports (Last 90 Days)"]
        R1["Report #104: Rig-07 | Winch Cable Frayed | Mechanical Energy | Barrier: Failed Inspection"]:::input
        R2["Report #189: Rig-07 | Slings Overloaded | Heavy Lifting | Barrier: Incomplete Rigging Plan"]:::input
        R3["Report #245: Rig-07 | Dropped Object from Mast | Gravity Energy | Barrier: Missing Tether"]:::input
        RN["Reports #...: Other Facilities across OIL Operations"]:::input
    end

    subgraph MULTI_DIM_CLUSTER ["Multi-Dimensional Clustering Engine (Layer 8 - AI-007)"]
        direction TB
        TUPLE["4-Tuple Aggregator:\n⟨ Installation, Activity, Hazard Energy, Degraded Barrier ⟩"]:::cluster
        WINDOW["Sliding Temporal Window:\nRolling 90-Day Operational Time Horizon"]:::cluster
        THRESHOLD["Precursor Hotspot Threshold Gate:\nCluster Occurrence Count N >= 3 Reports"]:::cluster
        TUPLE --> WINDOW --> THRESHOLD
    end

    REPORT_STREAM --> TUPLE

    subgraph PATTERN_SYNTHESIS ["Precursor Pattern & Risk Metric Computation"]
        direction TB
        HOTSPOT["🔥 Identified Precursor Cluster:\n'Rig-07 Lifting & Mechanical Energy Barrier Degradation'"]:::metric
        METRICS["Cluster Risk Metrics:\n• Frequency: 3 Near-Misses in 42 Days\n• Latent Consequence: High Potential SIF (P1)\n• Common Root Barrier: Pre-Use Inspection Bypass"]:::metric
        HOTSPOT --> METRICS
    end

    THRESHOLD -->|Condition Met: N >= 3| HOTSPOT

    subgraph PREVENTATIVE_ACTIONS ["Automated Decision-Support Interventions (CAPA)"]
        direction TB
        ACT1["1. Immediate Action:\nDispatch Rig-07 Hoisting & Rigging Third-Party Safety Audit"]:::action
        ACT2["2. Targeted Engineering Control:\nMandate Digital Pre-Use Checklists for all Crane Winch Lines"]:::action
        ACT3["3. Workforce Intervention:\nStand-Down & Targeted Toolbox Talk on IOGP Life-Saving Rule #5"]:::action
        ACT1 --- ACT2 --- ACT3
    end

    METRICS --> PREVENTATIVE_ACTIONS
```

---

## PPT Presentation Alignment & Speaking Points

| Slide / Diagram | Primary Objective | Suggested Hackathon Jury Speaking Pitch |
|---|---|---|
| **Diagram 1: Master Architecture** | Establish technical depth and end-to-end viability. | *"Judges, our architecture covers the full journey: from field ingestion to real-time PII scrubbing, through an 11-layer intelligence engine, down to verifiable database persistence and executive alerting."* |
| **Diagram 2: Dual-Path AI Engine** | Prove explainability & safety rigor. | *"In high-risk oilfield operations, black-box deep learning is unacceptable. We use a dual-track engine: deterministic energy-barrier rules guarantee physical safety boundaries, while dense semantic models handle dirty frontline phrasing—grounded by verbatim text spans."* |
| **Diagram 3: Report Lifecycle & HIL** | Showcase ethical AI & governance. | *"We enforce strict Human-in-the-Loop governance: the AI is an assistive decision-support engine, not an autonomous field officer. High-consequence SIF cases are triaged to human experts under strict SLAs with an immutable audit trail."* |
| **Diagram 4: Deployment Topology** | Demonstrate feasibility & lightweight deployment. | *"The prototype runs completely containerized via Docker Compose. It is local, air-gapped, and runs on CPU without expensive cloud GPUs, making it 100% compliant with OIL's on-premises security policy."* |
| **Diagram 5: Security & Provenance** | Address data sovereignty & enterprise security. | *"We ensure zero data leakage. Automatic PII scrubbing strips personal identities at the gateway, cryptographic SHA-256 hashes link all inferences, and strict RBAC controls govern visibility."* |
| **Diagram 6: Cross-Report Patterns** | Highlight proactive prevention vs. reactive reporting. | *"We don't just classify single reports—our system clusters recurring failures across 4-tuple operational dimensions. When 3 or more near-misses hit the same barrier within 90 days, it automatically sounds the alarm to prevent a catastrophic blowout or fatality."* |

---
*Created by Team Tech Smashers for Smart India Hackathon (SIH 2026) | Problem Statement SIH26165 (Oil India Limited)*
