# 11_SECURITY_ARCHITECTURE

**Document Status:** Authoritative for Security Governance, Identity & Access Management (IAM), Data Protection, AI/ML Guardrails & Audit Integrity  
**Governing Documents:** `01_PROJECT_CONSTITUTION.md`, `02_PRODUCT_BLUEPRINT.md`, `03_PROBLEM_STATEMENT.md`, `04_MARKET_RESEARCH.md`, `05_DATA_STRATEGY_AND_LABELING.md`, `06_TECHNICAL_REQUIREMENTS.md`, `07_SYSTEM_ARCHITECTURE.md`, `08_AI_ARCHITECTURE.md`, `09_DATABASE_DESIGN.md`, `10_API_SPECIFICATION.md`  
**SIH Problem Statement ID:** SIH26165  
**Organization:** Oil India Limited (OIL)  
**Category:** Software  
**Theme:** Smart Automation  
**Team:** Tech Smashers  

---

> **Architectural Tagging Discipline:**
> - `[PROPOSED SECURITY DESIGN]` — Security policies, threat mitigations, and access controls designed by Tech Smashers.
> - `[RECOMMENDED IMPLEMENTATION]` — Pragmatic, industry-standard security implementations (e.g., bcrypt password hashing, JWT Bearer tokens, TLS 1.3, Pydantic input validation) for the hackathon MVP.
> - `[PROTOTYPE ASSUMPTION]` — Modeling choices made to operate reliably on synthetic/public data without access to proprietary OIL enterprise networks.
> - `[FUTURE ENHANCEMENT]` — Advanced enterprise security infrastructure (e.g., Hardware Security Modules, SAML2/OIDC SSO federation, SIEM integration, automated DAST pipelines) reserved for production.
> - `[TO BE CONFIRMED WITH OIL]` — Enterprise IT/HSE security parameters, corporate active directory infrastructure, statutory retention rules, and network firewalls that must be officially confirmed with Oil India Limited.
> - `[ILLUSTRATIVE]` — Representative policy definitions, JSON structures, and permission matrices provided for conceptual clarity.

---

## 1. Purpose

This document defines the complete **Security Architecture** for the **OIL Safety Intelligence Platform**. It provides an exhaustive, defensible specification for how frontline incident reports, sensitive operational prose, AI-generated precursor assessments, character-level evidence spans, 6-state barrier integrity records, IOGP Life-Saving Rule mappings, cross-report pattern clusters, human review decisions, cryptographic audit ledgers, and user identities are protected across their lifecycle.

```mermaid
flowchart TD
    CON["01_PROJECT_CONSTITUTION\nGovernance & Boundaries"] --> SEC
    BP["02_PRODUCT_BLUEPRINT\nUser Roles & Journeys"] --> SEC
    PS["03_PROBLEM_STATEMENT\nOperational Context"] --> SEC
    MR["04_MARKET_RESEARCH\nIndustry Benchmark Security"] --> SEC
    DS["05_DATA_STRATEGY_AND_LABELING\nPII Masking & Provenance"] --> SEC
    TR["06_TECHNICAL_REQUIREMENTS\nSEC-001 & SEC-002 Requirements"] --> SEC
    SA["07_SYSTEM_ARCHITECTURE\nTrust Boundaries & Topology"] --> SEC
    AIA["08_AI_ARCHITECTURE\nAI Guardrails & Model Integrity"] --> SEC
    DBD["09_DATABASE_DESIGN\nColumn-Level Protections & DDL"] --> SEC
    API["10_API_SPECIFICATION\nAuth Endpoints & Error Masking"] --> SEC

    SEC["11_SECURITY_ARCHITECTURE\nAuthentication, RBAC, Data Protection, AI Defense & Audit Integrity"]

    SEC --> UI["12_UI_UX_DESIGN\nSession Management & Secure UI"]
    SEC --> DEP["13_DEPLOYMENT\nNetwork Isolation & Secret Vaults"]
    SEC --> TST["14_TESTING_STRATEGY\nSecurity, DAST & Fuzz Testing"]
```

This document establishes:
- The authentication and Role-Based Access Control (RBAC) frameworks governing operational safety data.
- The boundary protections preventing unauthorized mutation of AI inferences and human sign-offs.
- The AI-specific threat model covering prompt injection, data poisoning, training data leakage, and hallucinated evidence defenses.
- The cryptographic audit trail (`SEC-002`) guaranteeing tamper resistance across all administrative and safety-critical state transitions.
- The data minimization and PII scrubbing filters (`SEC-001`) isolating personnel identities from analytical records.
- The secrets management and environment segregation protocols separating hackathon prototype code from production networks.

---

## 2. Security Objectives

The platform enforces ten primary security objectives `[PROPOSED SECURITY DESIGN]`:

1. **Confidentiality:** Prevent unauthorized inspection of proprietary upstream exploration and production (E&P) operational conditions, contractor details, and frontline narratives.
2. **Data Integrity (`DATA-001`, `SEC-002`):** Guarantee that safety narratives, extracted signals, barrier evaluations, and human sign-offs cannot be modified or deleted without leaving an immutable audit trace.
3. **High Availability (`NFR-001`):** Ensure continuous operational accessibility of incident reporting and triage queues during routine field operations and emergency safety reviews.
4. **Authenticity:** Positively verify the identity of all human safety officers, field supervisors, and automated ingestion connectors interacting with platform interfaces.
5. **Strict Authorization (`SEC-001`):** Enforce least-privilege role boundaries; general viewers must never access administrative configurations or submit safety overrides.
6. **Non-Repudiation & Accountability (`HIL-002`):** Maintain unbroken chains of custody linking every confirmation, correction, or rejection to a certified human reviewer.
7. **Scientific & Legal Traceability (`OBS-001`):** Every AI-generated assessment must be cryptographically and relationally traceable to its source report, model checkpoint, and ruleset version.
8. **Privacy-by-Design (`SEC-001`):** Guarantee that worker identities, mobile numbers, and personal identifiers are scrubbed before analytical persistence.
9. **AI Output Integrity (`AI-008`, `NFR-003`):** Protect the reasoning engine against prompt injection, adversarial narrative manipulation, and fabricated text evidence.
10. **Decoupled Human-Review Integrity (`HIL-001`):** Ensure that human review actions create distinct historical records and never overwrite raw AI analytical outputs.

---

## 3. Foundational Security Principles

1. **Least Privilege:** Every system process, database connection pool, and authenticated user operates with the minimum set of permissions necessary to execute their assigned role.
2. **Defense in Depth:** Security controls are layered across network firewalls, API transport layers, application logic, database constraints, and model validation gates.
3. **Secure by Default:** All network endpoints require cryptographic transport (TLS 1.3), authentication is mandatory for write operations, and permissive wildcards (e.g., `CORS *`) are prohibited.
4. **Fail-Safe Degradation (`NFR-003`):** If NLP parsing or classification workers fail, the system transitions to `SIF: REVIEW` and flags manual HSE triage; it **never** defaults to a false `SIF: NO`.
5. **Zero Trust on Client Inputs:** Frontend UI validations are treated as cosmetic conveniences; all business invariants, types, and string bounds are re-validated server-side.
6. **Data Minimization:** Analytical tables persist only operational and physical safety attributes, discarding extraneous employee biographical data.
7. **Zero Secret Commitment:** Passwords, private keys, and API tokens are injected exclusively via environment variables and never committed to source control repositories.
8. **Decoupled Truth Planes:** Raw frontline prose, derived AI inferences, and human HSE reviews reside in distinct, non-overwriting relational storage planes (`09_DATABASE_DESIGN.md`).
9. **Provenance Immutability (`DATA-002`):** Synthetic hackathon benchmark records carry permanent metadata banners preventing accidental confusion with authorized OIL enterprise data.
10. **Auditable Human Primacy (`HIL-001`):** The AI engine is an assistive decision-support tool; autonomous permit revocations or facility shutdowns are architecturally prohibited.

---

## 4. Security Architecture & Trust Boundaries

The system segregates components into distinct trust zones separated by explicit security perimeters:

```
[ UNTRUSTED ZONE: Public Internet / External Networks ]
                           │
                           ▼ (TLS 1.3 / Reverse Proxy / Rate Limiter)
[ DMZ / INGRESS PERIMETER ]
  ┌─────────────────────────────────────────────────────────────┐
  │ Ingress Router & TLS Termination (Port 443)                 │
  │ Request-ID Injection, CORS Policy, WAF Payload Filter       │
  └─────────────────────────────────────────────────────────────┘
                           │
                           ▼ (Internal Network / Authenticated Bearer JWT)
[ TRUSTED APPLICATION ZONE ]
  ┌─────────────────────────────────────────────────────────────┐
  │ API Gateway & Application Services (FastAPI / Node.js)      │
  │ • Role-Based Access Control (RBAC) Validator                │
  │ • Input Pydantic Schema Validator                           │
  │ • PII Sanitization & Normalization Filter                   │
  └─────────────────────────────────────────────────────────────┘
          │                                             │
          ▼ (Unix Domain Socket / gRPC)                 ▼ (Authenticated TLS Connection)
[ ISOLATED INFERENCE ZONE ]                  [ HARDENED DATA ZONE ]
  ┌───────────────────────────────┐            ┌────────────────────────────────┐
  │ AI / NLP Engine Workers       │            │ PostgreSQL 16 Database         │
  │ • Tokenizer & Syntax Parser   │            │ • Least-Privilege Roles        │
  │ • Precursor Triad Evaluator   │            │ • Non-Overwriting Tables       │
  │ • Verbatim Span Bounder       │            │ • Append-Only Audit Ledger     │
  │ • Output Schema Validator     │            │ • AES-256 Storage Encryption   │
  └───────────────────────────────┘            └────────────────────────────────┘
```

### Trust Boundary Analysis

| Boundary Interface | External / Untrusted Side | Internal / Trusted Side | Enforced Security Controls |
|---|---|---|---|
| **Client $\rightarrow$ API Gateway** | Web Browser / Mobile Client | Backend Routing Engine | TLS 1.3, Rate Limiting, CORS origin check, JWT verification. |
| **API $\rightarrow$ AI Worker** | API Application Layer | Model Inference Runtime | IPC validation, bounded string lengths, isolated execution sandbox. |
| **Backend $\rightarrow$ Database** | Service Application Code | PostgreSQL RDBMS | TLS connection, application role isolation, parameterized SQL queries. |
| **AI Output $\rightarrow$ DB Storage** | Raw Model Softmax/Tensors | Persistent Storage Plane | Strict JSON schema validation, reference integrity checks, bounds gating. |
| **Human Review $\rightarrow$ Ledger** | Certified Reviewer Client | Audit Ledger (`audit_events`)| Cryptographic SHA-256 hash chaining, immutable append-only enforcement. |

---

## 5. Conceptual Data Sensitivity Classification `[PROPOSED SECURITY DESIGN]`

To avoid unverified assumptions regarding Oil India Limited's internal classification schemes, the platform establishes a four-tier conceptual data classification model:

```
                                  DATA SENSITIVITY TIERS
                                             │
        ┌───────────────────────┬────────────┴──────────┬────────────────────────┐
        ▼                       ▼                       ▼                        ▼
     LEVEL 1                 LEVEL 2                 LEVEL 3                  LEVEL 4
     PUBLIC                 INTERNAL                SENSITIVE            HIGHLY SENSITIVE
  (IOGP Rules,            (Aggregated KPIs,      (Frontline Prose,     (Employee Names,
   Taxonomy Schemas,       Barrier Failure        Site Coordinates,     Audit Tamper Ledger,
   Public Benchmark Data)  Facility Trends)       Near-Miss Narratives) Database Credentials)
```

### Sensitivity Tier Mapping & Protection Rules

| Level | Classification | Example Data Elements | Minimum Technical Protection Controls |
|---|---|---|---|
| **L1** | Public | IOGP Report 459 rule definitions, synthetic demonstration narratives, API documentation. | Standard integrity protection; open read access. |
| **L2** | Internal | Aggregated facility SIF rates, recurring precursor cluster titles, barrier failure percentages. | Authenticated session required; RBAC role check (`HSE_VIEWER` and above). |
| **L3** | Sensitive | Raw incident narratives, specific equipment tag numbers, contractor names, supervisor notes. | TLS 1.3 in transit, AES-256 at rest, access logged in `audit_events`, PII masked. |
| **L4** | Highly Sensitive | Database root credentials, JWT signing private keys, unmasked employee records, tamper ledger hashes. | Isolated environment variables, strict column-level database permissions, non-exportable keys. |

---

## 6. Data Types & Protection Matrix

| Data Entity (`09_DATABASE_DESIGN.md`) | Inherent Risk / Exposure | Sensitivity Tier | In-Transit Protection | At-Rest Protection | Access Boundary |
|---|---|---|---|---|---|
| `safety_reports.raw_narrative` | Operational exposure, raw contractor mentions | **Level 3** | TLS 1.3 | AES-256 Storage | `HSE_ANALYST`, `HSE_OFFICER` |
| `safety_reports.normalized_narrative`| Scrubbed operational narrative | **Level 3** | TLS 1.3 | AES-256 Storage | Authenticated Users |
| `sif_assessments` | Latent fatality potential conclusions | **Level 2** | TLS 1.3 | AES-256 Storage | Authenticated Users |
| `evidence_spans` | Exact text phrases proving barrier gaps | **Level 3** | TLS 1.3 | AES-256 Storage | Authenticated Users |
| `barrier_findings` | Critical safeguard failure classifications | **Level 2** | TLS 1.3 | AES-256 Storage | Authenticated Users |
| `recurring_patterns` | Systemic cross-facility precursor clusters | **Level 2** | TLS 1.3 | AES-256 Storage | Authenticated Users |
| `human_reviews` | Safety officer overrides and review notes | **Level 3** | TLS 1.3 | AES-256 Storage | Restricted to HSE Officers |
| `audit_events` | Tamper-evident governance ledger | **Level 4** | TLS 1.3 | Append-Only / Chained | `SYSTEM_AUDITOR` Only |
| `app_users` | Reviewer names, hashed passwords, emails | **Level 4** | TLS 1.3 | bcrypt Hash / AES | System Administrators |

---

## 7. Threat Model (STRIDE Methodology)

The platform evaluates potential threats using the Microsoft STRIDE categorization framework `[PROPOSED SECURITY DESIGN]`:

```mermaid
flowchart LR
    S[Spoofing Identity] --> T1[Fake User / Rogue Ingestion Connector]
    T[Tampering with Data] --> T2[Modifying SIF Assessments / Falsifying Gas Logs]
    R[Repudiation] --> T3[Denying Safety Reviewer Override Decisions]
    I[Information Disclosure] --> T4[Leaking Operational Narratives / Contractor PII]
    D[Denial of Service] --> T5[Flooding AI Inference Engine with Giant Texts]
    E[Elevation of Privilege] --> T6[Viewer Modifying Systemic Safety Rules]
```

### STRIDE Assessment Matrix

| STRIDE Category | Specific Attack Vector | System Vulnerability Target | Potential Impact | Engineered Architectural Mitigation |
|---|---|---|---|---|
| **Spoofing** | Attacker transmits reports using forged supervisor IDs. | `POST /api/v1/reports` | Corrupted safety data; falsified audit trails. | Cryptographic JWT Bearer token authentication; user identity derived strictly from validated token claims. |
| **Tampering** | Rogue actor alters a `SIF: YES` finding to `SIF: NO` in database. | `sif_assessments` table | Buried fatal risk; unmitigated catastrophic incident. | Relational `UPDATE` disabled on inferences; append-only human review table; SHA-256 audit ledger chaining. |
| **Repudiation** | HSE Officer denies overriding an AI precursor finding. | `human_reviews` table | Inability to establish legal accountability post-accident. | Mandatory cryptographic user binding; client IP and timestamp logged in `audit_events` with hash chain. |
| **Information Disclosure** | Unauthorized actor reads raw field reports containing contractor names. | `GET /api/v1/reports/{id}` | Privacy violation; contractor relationship compromise. | PII masking in Stage 1 NLP (`SEC-001`); strict server-side RBAC gating report narrative retrieval. |
| **Denial of Service** | Malicious actor posts 50MB text payloads to AI parser. | `POST /api/v1/reports/{id}/analyze` | CPU exhaustion; model worker crash; pipeline deadlock. | Ingress body size limit (64KB); regex token gating; Pydantic length bounds ($10 \le \text{length} \le 10,000$). |
| **Elevation of Privilege**| Standard viewer alters IOGP Life-Saving Rule definitions. | `POST /api/v1/configuration/rules` | Compromised safety logic across all future reports. | Server-side role enforcement; admin endpoints restricted strictly to `role == 'ADMINISTRATOR'`. |

---

## 8. Comprehensive Asset Risk Register

| Asset ID | Target Asset | Primary Threat Scenario | Severity | Likelihood | Technical Mitigation Strategy |
|---|---|---|---|---|---|
| **RSK-01** | Safety Narratives | SQL Injection exfiltrating unmasked incident prose. | High | Low | Native parameterized queries (SQLAlchemy / asyncpg); zero raw SQL concatenation. |
| **RSK-02** | SIF Potential Engine | Prompt injection forcing AI to declare safe state. | Critical | Med | Treat prose strictly as data; heuristic regex pre-filtering; schema-bound outputs. |
| **RSK-03** | Evidence Offsets | Frontend manipulation altering highlighted evidence. | Med | Low | Evidence spans validated against server-side string hashes; client highlights are read-only. |
| **RSK-04** | Audit History | Malicious administrator wiping historical review logs. | Critical | Low | Append-only database permissions (`REVOKE UPDATE, DELETE ON audit_events`); hash chaining. |
| **RSK-05** | API Endpoints | Insecure Direct Object Reference (IDOR) on report IDs. | High | Med | Server-side tenant/facility ownership checks on all parameterized `/reports/{id}` routes. |
| **RSK-06** | Model Checkpoint | Unauthorized replacement of transformer weights. | High | Low | Read-only file system permissions on model directory; SHA-256 integrity verification on startup. |
| **RSK-07** | Data Provenance | Synthetic test records displayed as authentic OIL data. | Med | Med | Mandatory `source_type` database column; frontend hard-coded provenance alert banners. |

---

## 9. Authentication Architecture

### 9.1 Prototype Authentication (`[RECOMMENDED IMPLEMENTATION]`)
For the SIH 2026 hackathon MVP, the platform implements a secure, stateless JWT Bearer token authentication mechanism:
- **Password Hashing:** Passwords stored in `app_users` are hashed using **bcrypt** via `passlib[bcrypt]` (salt rounds: 12) for lightweight dependency footprint and robust security. Legacy MD5, SHA-1, or unsalted algorithms are strictly prohibited. (Argon2id is preserved as a future H1/enterprise hardening configuration).
- **Token Signing:** JWT tokens are signed using symmetric `HS256` (or asymmetric `RS256`) with high-entropy 256-bit secrets injected via environment variables.
- **Token Lifespan:** Access tokens have a maximum validity of **15 minutes**. Refresh tokens are bound to specific client instances and expire after 24 hours.

### 9.2 Enterprise Target Architecture (`[FUTURE ENHANCEMENT]` / `[TO BE CONFIRMED WITH OIL]`)
In production deployment within Oil India Limited's corporate network:
- Local password tables will be deprecated in favor of enterprise Single Sign-On (SSO) utilizing **SAML 2.0** or **OpenID Connect (OIDC)** federated with OIL's internal Identity Provider (e.g., Microsoft Entra ID / Active Directory).
- Multi-Factor Authentication (MFA) will be enforced for all accounts possessing safety review authority (`HSE_OFFICER`).

---

## 10. Authorization & Role-Based Access Control (RBAC)

The platform enforces six canonical roles with strict hierarchical permissions:

```
[ ROLE HIERARCHY ]
      SYSTEM_AUDITOR ──────────────┐ (Exclusive Audit Inspection)
                                   │
      ADMINISTRATOR                │
            │                      │
            ▼                      │
       HSE_OFFICER                 │
            │                      │
            ▼                      │
       HSE_ANALYST                 │
            │                      │
            ▼                      │
       HSE_VIEWER ─────────────────┤
                                   │
      ML_OPS_ENGINEER ─────────────┘ (Model Telemetry & Run Diagnostics)
```

### Comprehensive Role-Permission Matrix

| Functional Operation | Primary API Route | `HSE_VIEWER` | `HSE_ANALYST` | `HSE_OFFICER` | `ADMINISTRATOR` | `SYSTEM_AUDITOR` | `ML_OPS_ENGINEER` |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **View Executive Dashboard** | `GET /dashboard/summary` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| **Search & List Reports** | `GET /reports` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| **View Single Report Metadata**| `GET /reports/{id}` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| **View AI SIF Analysis & Spans**| `GET /reports/{id}/analysis` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| **Submit New Safety Report** | `POST /reports` | Denied | Allowed | Allowed | Allowed | Denied | Denied |
| **Trigger AI Reanalysis** | `POST /reports/{id}/analyze` | Denied | Allowed | Allowed | Allowed | Denied | Allowed |
| **Generate Pattern Clusters**| `POST /patterns/generate` | Denied | Allowed | Allowed | Allowed | Denied | Allowed |
| **Submit Formal HSE Review** | `POST /reports/{id}/reviews` | Denied | Denied | **Allowed** | Denied | Denied | Denied |
| **Inspect Run Telemetry** | `GET /processing-runs/{id}` | Denied | Denied | Allowed | Allowed | Denied | **Allowed** |
| **Inspect Tamper Audit Ledger**| `GET /audit/events` | Denied | Denied | Denied | Denied | **Allowed** | Denied |
| **Manage Life-Saving Rules** | `POST /configuration/rules` *(H1 / Future Admin Capability)* | Denied | Denied | Denied | **Allowed** | Denied | Denied |
| **Manage User Accounts** | `POST /users` *(H1 / Future Admin Capability)* | Denied | Denied | Denied | **Allowed** | Denied | Denied |

---

## 11. Resource-Level Authorization & IDOR Defense

To prevent Insecure Direct Object References (IDOR):
1. The backend application layer verifies that the authenticated user possesses explicit authority to view the requested facility record before querying data:
   ```python
   # Illustrative Backend Enforcement Logic
   def verify_report_access(current_user: User, report_id: UUID):
       report = db.query(SafetyReport).filter_by(report_id=report_id).first()
       if not report:
           raise NotFoundException(code="REPORT_NOT_FOUND")
       if current_user.role != "ADMINISTRATOR" and report.facility_id not in current_user.assigned_facilities:
           raise ForbiddenException(code="FACILITY_ACCESS_DENIED")
       return report
   ```
2. Object access decisions are never delegated to client-supplied URL parameters or frontend session state.

---

## 12. Session Management & Browser Security

1. **HttpOnly Cookies:** When browser cookies are utilized for session tokens, they must enforce `HttpOnly; Secure; SameSite=Strict`.
2. **Token Revocation:** User logout immediately invalidates the active refresh token in the backend cache.
3. **Cross-Site Scripting (XSS) Defenses:**
   - Content Security Policy (CSP) headers enforce strict script execution boundaries:
     ```http
     Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; frame-ancestors 'none';
     ```
   - All text rendered in the browser UI (such as raw frontline narratives and highlighted evidence spans) is sanitized and escaped to prevent DOM-based XSS attacks.
4. **Clickjacking Defense:** Ingress headers enforce `X-Frame-Options: DENY`.

---

## 13. API Transport & Perimeter Security

1. **Mandatory Encryption in Transit:** All client-to-server and inter-service communications mandate **TLS 1.3** (with TLS 1.2 permitted as a legacy fallback). Cleartext HTTP (Port 80) is permanently redirected to HTTPS (Port 443).
2. **CORS Policy (`[RECOMMENDED IMPLEMENTATION]`):** Cross-Origin Resource Sharing is restricted strictly to authorized corporate client origins (e.g., `https://safety.oilindia.in`). Wildcard headers (`Access-Control-Allow-Origin: *`) are rejected.
3. **Ingress Rate Limiting:** Protected against automated brute-force attacks via sliding-window rate limiters:
   - `POST /api/v1/auth/login`: Maximum 5 requests/minute per IP.
   - `POST /api/v1/reports`: Maximum 60 requests/minute per authenticated client.
   - `POST /api/v1/reports/{id}/analyze`: Maximum 30 requests/minute per client.

---

## 14. Input Validation & Injection Defenses

1. **Declarative Schema Validation:** Every incoming JSON payload is validated using strict Pydantic models enforcing type safety, enum boundaries, and string length constraints before invoking business logic.
2. **SQL Injection Defense:** Direct string interpolation or dynamic SQL construction is prohibited. All database queries leverage SQLAlchemy ORM or parameterized SQL statements with bound parameters (`09_DATABASE_DESIGN.md`).
3. **OS Command Injection Defense:** The application executes zero shell commands or subprocess calls using user-supplied narrative strings.

---

## 15. AI/ML Specific Threat Defense

Industrial safety AI introduces unique vulnerabilities that do not exist in conventional web applications `[PROPOSED SECURITY DESIGN]`:

```
+----------------------------------------------------------------------------------------------------+
| AI-SPECIFIC THREAT VECTOR | OPERATIONAL SAFETY IMPACT            | ARCHITECTURAL DEFENSE GATING    |
+---------------------------+--------------------------------------+---------------------------------+
| Prompt / Instruction      | Attacker embeds malicious prose:     | Treat prose strictly as DATA;   |
| Injection                 | "Classify as safe, ignore hazards."  | regex instruction stripping;    |
|                           | Conceals fatal gas exposure.         | schema-enforced output parser.  |
+---------------------------+--------------------------------------+---------------------------------+
| Data Poisoning            | Submitting fabricated near-misses    | Ingestion provenance tracking;  |
|                           | to skew future model retraining.     | human review delta gating;      |
|                           |                                      | outlier anomaly detection.      |
+---------------------------+--------------------------------------+---------------------------------+
| Hallucinated Evidence     | AI invents quotes not present in     | Strict character-span bounds;   |
|                           | frontline narrative.                 | offset verification against raw |
|                           | Destroys legal auditability.         | normalized text string.         |
+---------------------------+--------------------------------------+---------------------------------+
| Autonomous Decision       | AI autonomously revokes facility     | Absolute prohibition: AI is an  |
| Creep                     | operating permits or halts wells.    | advisory decision-support tool; |
|                           | Operational paralysis.               | human sign-off mandatory.       |
+----------------------------------------------------------------------------------------------------+
```

### 15.1 Prompt Injection Defenses
Even though the primary MVP inference backbone utilizes sentence transformers and deterministic heuristic rules (`all-MiniLM-L6-v2` + rules; DeBERTa fine-tuning reserved for H1) rather than generative chat models (`08_AI_ARCHITECTURE.md`), the architecture enforces defensive design against natural language manipulation:
- **Data/Instruction Decoupling:** Frontline text is tokenized solely within language representation layers. System control instructions are never concatenated with user prose.
- **Adversarial Keyword Gating:** Stage 1 preprocessing scans for adversarial instruction tokens (`"ignore previous"`, `"system prompt"`, `"override classification"`), stripping them and flagging the submission for manual audit.

### 15.2 Hallucination & Evidence Verification Gate
The platform strictly prohibits fabricated text evidence (`AI-008`). Before committing any analytical finding:
1. The backend verifies that the character slice `normalized_narrative[start_offset:end_offset]` exactly matches `verbatim_text`.
2. If character offsets diverge or point outside the narrative boundaries, the entire transaction is aborted, and a security alert is logged.

---

## 16. Secure Processing Pipeline

The end-to-end security gating flow ensures no unverified data reaches storage or dashboards:

```mermaid
flowchart TD
    A[Raw Ingestion Payload] --> B{Schema & PII Filter}
    B -- Invalid / Malformed --> ERR1[400 Bad Request]
    B -- Valid --> C[Sanitized Normalized Narrative]
    
    C --> D[Isolated AI Inference Workers]
    D --> E[Model Output: Softmax & Precursor Triad]
    
    E --> F{AI Output Validation Gate}
    F -- Invalid Offset / Hallucination --> ERR2[Abort Transaction & Alert Admin]
    F -- Valid Offsets & Bounded Scores --> G[Atomic ACID Database Commit]
    
    G --> H[Safety Intelligence Store]
    H --> I[Executive Dashboard]
    
    H --> J[Human HSE Review Console]
    J --> K{Review Action Authorized?}
    K -- Role != HSE_OFFICER --> ERR3[403 Forbidden]
    K -- Authorized --> L[Append to human_reviews Table]
    
    L --> M[Cryptographic SHA-256 Hash Chain]
    M --> N[audit_events Immutable Ledger]
```

---

## 17. Database & Storage Security

1. **Role-Isolated Connection Credentials (`09_DATABASE_DESIGN.md`):**
   - Application ingestion services connect via `app_ingestion_role` (restricted to `INSERT`, `SELECT` on `safety_reports`).
   - Inference workers connect via `app_inference_role` (restricted to derived tables).
   - Review services connect via `app_review_role` (`INSERT` on `human_reviews`, zero delete permissions).
2. **Encryption at Rest:** All PostgreSQL data directories and tablespaces are encrypted using enterprise AES-256 volume encryption (`dm-crypt` / LUKS or managed cloud KMS).
3. **Database Audit Logging:** PostgreSQL `pgaudit` extension logs all DDL executions, administrative role changes, and bulk extraction attempts.

---

## 18. Secrets Management Protocol

1. **Zero Hardcoded Secrets:** Hardcoding database credentials, private keys, or API tokens in Python/JavaScript source code or Git manifests is strictly prohibited.
2. **Environment Injection (`[RECOMMENDED IMPLEMENTATION]`):** For the hackathon MVP, secrets are injected into container environments via Docker Compose `.env` files that are strictly excluded from version control via `.gitignore`.
3. **Enterprise Vault Integration (`[FUTURE ENHANCEMENT]` / `[TO BE CONFIRMED WITH OIL]`):** In production, secrets will be dynamically leased and rotated using an enterprise secrets engine (e.g., HashiCorp Vault or Azure Key Vault).

---

## 19. Privacy & Data Minimization Architecture (`SEC-001`)

1. **PII Masking Filter:** Frontline incident text is passed through a deterministic Named Entity Recognition (NER) and regex filter during Stage 1 ingestion:
   - Worker names are replaced with generalized operational roles (e.g., `[TECHNICIAN]`, `[ROUGHNECK]`).
   - Phone numbers, vehicle registration plates, and Aadhaar/PAN/Employee ID patterns are scrubbed and replaced with `[REDACTED]`.
2. **Segregated User Directory:** User personal information (names, emails, authentication hashes) is isolated in the `app_users` table and never joined directly with public analytical views.

---

## 20. Tamper-Evident Audit Ledger (`SEC-002`)

All administrative changes, safety review overrides, and model execution events are appended to the `audit_events` ledger:

```
[ Audit Event N-1 ]                 [ Audit Event N ]
┌─────────────────────────┐         ┌─────────────────────────┐
│ event_id: UUID          │         │ event_id: UUID          │
│ sequence_number: 104    │         │ sequence_number: 105    │
│ action: SIF_EVALUATED   │         │ action: REVIEW_RECORDED │
│ event_sha256: 7f8a...   │────────>│ prev_event_hash: 7f8a...│
└─────────────────────────┘         │ event_sha256: 3c2d...   │
                                    └─────────────────────────┘
```

### Cryptographic Hash Chaining Mechanism
- Each record calculates:
  $$\text{event\_sha256} = \text{SHA-256}(\text{sequence\_number} \parallel \text{action\_type} \parallel \text{target\_id} \parallel \text{payload\_delta} \parallel \text{prev\_event\_hash})$$
- Modifying, deleting, or reordering any historical audit event invalidates the entire subsequent cryptographic hash chain, enabling instant detection of insider database tampering during compliance audits.

---

## 21. Secure Software Development Lifecycle (SSDLC)

1. **Automated Secret Scanning:** Git pre-commit hooks utilize `gitleaks` to block commits containing passwords, private keys, or AWS/API tokens.
2. **Static Dependency Scanning:** All Python dependencies are pinned in `requirements.txt` with cryptographic hashes; dependencies are scanned for known CVEs using `safety` and `pip-audit`.
3. **Branch Protection:** Source code changes must pass through pull request reviews and automated GitHub Actions CI pipelines before merging into main branches.

---

## 22. Security Environment Segregation

```
+----------------------------------------------------------------------------------------------------+
| ENVIRONMENT         | PURPOSE                     | DATA POLICY          | CREDENTIAL POLICY       |
+---------------------+-----------------------------+----------------------+-------------------------+
| Local Development   | Feature coding & testing    | Synthetic MVD-60 only| Ephemeral local secrets |
+---------------------+-----------------------------+----------------------+-------------------------+
| Hackathon Prototype | Live SIH 2026 Evaluation    | Curated Synthetic &  | Dedicated containerized |
| (Demo Environment)  | & Jury Demonstrations       | Public Zenodo CSRA   | isolated passwords      |
+---------------------+-----------------------------+----------------------+-------------------------+
| Enterprise Pilot    | Validated OIL Field Testing | Authorized historical| Integrated enterprise   |
| (Target Production) | on Corporate Network        | OIL E&P records      | IAM / Managed Vault     |
+----------------------------------------------------------------------------------------------------+
```

---

## 23. Incident Response Protocol (High-Level Framework)

In the event of a suspected security breach or data integrity violation:
1. **Detection & Triage:** Anomalous activity flagged via failed login spikes, audit chain breaks, or unexpected API error rates.
2. **Containment:** Compromised user sessions immediately revoked; network isolation applied to affected container instances.
3. **Investigation:** Forensics executed by cross-referencing `request_id` logs with the immutable `audit_events` ledger.
4. **Eradication & Recovery:** System restored from verified tamper-free database snapshots; credentials rotated.
5. **Post-Mortem Review:** Root cause analysis documented to update security unit tests and input validation rules.

---

## 24. Security vs. Usability Trade-Off Analysis

```
+----------------------------------------------------------------------------------------------------+
| Architectural Dimension | Chosen Security Strategy       | Alternative Rejected | Practical Rationale      |
+-------------------------+--------------------------------+----------------------+--------------------------+
| Authentication Model    | Stateless Bearer JWTs          | Session Cookies with | Decoupled scalability;   |
|                         | (15-min expiration)            | Sticky Server State  | seamless mobile/web API  |
|                         |                                |                      | integration for demo     |
+-------------------------+--------------------------------+----------------------+--------------------------+
| Audit Trail Storage     | Relational SHA-256 Hash Chain  | Distributed          | Zero multi-node latency; |
|                         | in PostgreSQL Engine           | Blockchain Ledger    | fully auditable without  |
|                         |                                |                      | extreme compute overhead |
+-------------------------+--------------------------------+----------------------+--------------------------+
| PII Handling            | Automated Regex + NER Masking  | Manual Review of     | Eliminates field triage  |
|                         | at Ingestion Boundary          | Every Single Report  | operational bottlenecks  |
+----------------------------------------------------------------------------------------------------+
```

---

## 25. Prototype vs. Production Security Baseline

```
+----------------------------------------------------------------------------------------------------+
| Security Domain        | SIH 2026 Hackathon Prototype (P0)    | Enterprise OIL Production Target (P2)|
+------------------------+--------------------------------------+--------------------------------------+
| Identity Management    | Local bcrypt + JWT Bearer Tokens     | Enterprise SAML 2.0 / OIDC (Entra ID)|
| MFA Enforcement        | Optional / Simulated for Demo        | Mandatory for all HSE Reviewers      |
| Network Perimeter      | Docker Bridge Network + Host TLS     | Dedicated Corporate Subnet (VPC/WAF) |
| Secrets Storage        | Container Environment Variables      | HashiCorp Vault / Azure Key Vault    |
| Audit Log Verification | Database Sequence Check Script       | Automated Continuous SIEM Ingestion  |
| Data Provenance        | Strict Database Tagging & UI Banners | Cryptographic Certificate of Origin  |
+----------------------------------------------------------------------------------------------------+
```

---

## 26. Requirements Traceability Matrix (`06_TECHNICAL_REQUIREMENTS.md`)

| Requirement ID | Technical Specification in Requirements Document | Engineered Security Mitigation in this Document |
|---|---|---|
| `SEC-001` | PII Masking & Data Minimization | Section 19 (Ingestion NER PII scrubbing; `app_users` separation) |
| `SEC-002` | Cryptographic Tamper-Resistant Audit Trail | Section 20 (SHA-256 event chaining in `audit_events`) |
| `FR-001` | Multi-Format Report Ingestion Validation | Section 14 (Pydantic schema bounds; body size limit gating) |
| `AI-004` | SIF Potential Reasoning Protection, incl. Outcome Blindness Enforcement | Section 15 (Prompt injection pre-filter); Section 2 (independent database columns preventing outcome bias) |
| `AI-008` | Verbatim Character-Level Evidence Binding | Section 15.2 (Server-side string slice bounds verification) |
| `DATA-002`| Data Provenance Tracking & Segregation | Section 5 & 8 (Mandatory `source_type` tags; UI disclosure banners) |
| `HIL-001` | Certified Human HSE Review Security | Section 10 & 16 (Strict `HSE_OFFICER` RBAC authorization gate) |
| `HIL-002` | Audit Trail for Safety Overrides | Section 20 (Append-only `human_reviews` + `audit_events` logging) |
| `OBS-001` | Model & Pipeline Version Immutability | Section 2 (Cryptographic ruleset hashes bound to processing runs) |
| `NFR-003` | Fail-Safe Handling of Uncertainty | Section 3 (Automatic transition to `SIF: REVIEW` upon AI failure) |

---

## 27. Security ↔ Database Traceability Matrix (`09_DATABASE_DESIGN.md`)

| Database Entity / Column | Security Vulnerability Prevented | Enforced Technical Protection Rule |
|---|---|---|
| `safety_reports.raw_narrative` | Information disclosure / PII leakage | Encrypted at rest (AES-256); access restricted to HSE roles. |
| `safety_reports.normalized_narrative`| Injection / malformed token processing | PII scrubbed; domain abbreviations expanded safely. |
| `sif_assessments.sif_potential`| Unauthorized tampering of safety status | Relational `UPDATE` disabled; superseded via `is_active_assessment`. |
| `barrier_findings.barrier_status`| Arbitrary string manipulation | Strict check constraints enforcing 6 canonical states. |
| `evidence_spans.start_offset` | Evidence fabrication / desynchronization | Checked against `LENGTH(normalized_narrative)` on insert. |
| `human_reviews` (All Columns) | Overwriting raw model outputs | Strictly append-only table; references original assessment ID. |
| `audit_events.prev_event_hash` | Silent database log deletion | Cryptographic SHA-256 hash chaining detecting ledger tampering. |
| `app_users.role` | Privilege escalation | Enforced server-side via JWT claims; validated against DB check constraint. |

---

## 28. Security Assumptions & Explicit Limitations

### 28.1 Explicit Engineering Assumptions
1. The hackathon demonstration environment operates on synthetic upstream E&P narratives and public benchmark datasets (`DATA-002`).
2. Enterprise SSO federation, corporate firewalls, and hardware security modules (HSMs) are deferred to post-hackathon implementation phases.
3. Network transport within isolated Docker container networks is assumed non-hostile, relying on container network namespace isolation.

### 28.2 What This Architecture Does NOT Establish
- This document **does not** constitute an official ISO 27001 or SOC 2 compliance certification.
- This document **does not** claim verified knowledge of Oil India Limited's internal network topography or Active Directory configuration.
- This document **does not** claim that synthetic prototype evaluations represent completed security testing on live production infrastructure.

---

## 29. Security Definition of Done (DoD)

The Security Architecture is declared complete and authoritative when the following criteria are satisfied:
- [x] All 10 core security objectives are defined and aligned with the Project Constitution.
- [x] High-level trust boundaries and STRIDE threat models are fully specified.
- [x] 5-tier Role-Based Access Control (RBAC) matrix is formalized across all platform endpoints.
- [x] AI-specific security guardrails (prompt injection, hallucination defenses, output verification) are established.
- [x] Cryptographic tamper-evident audit ledger (`SEC-002`) with SHA-256 chaining is architected.
- [x] PII scrubbing and data minimization rules (`SEC-001`) are codified for ingestion pipelines.
- [x] Zero secret commitment standards and environment segregation protocols are formalized.
- [x] Comprehensive requirements traceability connects controls directly to `06_TECHNICAL_REQUIREMENTS.md`.
- [x] All enterprise integration assumptions are clearly marked as `[TO BE CONFIRMED WITH OIL]`.

---

## 30. Inter-Document Architectural Positioning

```
[01_PROJECT_CONSTITUTION]        --> Supreme safety ethics & non-predictive boundaries
[02_PRODUCT_BLUEPRINT]           --> User roles, journeys & dashboard concepts
[03_PROBLEM_STATEMENT]           --> Official SIH26165 problem definition
[04_MARKET_RESEARCH]             --> Enterprise EHS compliance standards
[05_DATA_STRATEGY_AND_LABELING]  --> Canonical safety taxonomies & PII rules
[06_TECHNICAL_REQUIREMENTS]      --> IEEE Requirements (SEC-001, SEC-002, HIL-001)
[07_SYSTEM_ARCHITECTURE]         --> 11-layer system topology & trust boundaries
[08_AI_ARCHITECTURE]             --> Causal reasoning models & guardrails
[09_DATABASE_DESIGN]             --> PostgreSQL relational schema & check constraints
[10_API_SPECIFICATION]           --> REST contracts, auth headers & error formats
[11_SECURITY_ARCHITECTURE]       --> Threat models, IAM, cryptographic audit & AI defense
        │
        ▼ (Downstream Technical Execution)
[12_UI_UX_DESIGN]                --> Frontend session management & visual alert banners
[13_DEPLOYMENT]                  --> Hardened container configuration & firewall rules
[14_TESTING_STRATEGY]            --> Security penetration, fuzzing & vulnerability testing
[15_ROADMAP]                     --> Enterprise security compliance implementation
[16_DOCUMENT_CONSISTENCY_AUDIT]  --> Cross-specification validation audit
```

---

## 31. Final Security Architecture Summary

The **OIL Safety Intelligence Platform Security Architecture** establishes a rigorous defense-in-depth model protecting industrial safety intelligence across its complete lifecycle:

$$\text{Authenticated User} \longrightarrow \text{Role-Based Ingress} \longrightarrow \text{Sanitized Ingestion} \longrightarrow \text{Sandboxed AI Inference} \longrightarrow \text{Verified Evidence Offsets} \longrightarrow \text{Append-Only Reviews} \longrightarrow \text{Cryptographic Audit Ledger}$$

By treating natural language narratives as untrusted data, enforcing character-level evidence bounds, protecting original AI inferences from destructive overwrites, locking administrative configurations behind strict RBAC gates, and chaining all governance actions in a tamper-resistant SHA-256 ledger, the security architecture ensures total operational transparency, uncompromising safety engineering ethics, and practical hackathon-to-enterprise scalability.
