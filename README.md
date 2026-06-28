<div align="center">

# 🤝 AGL — Autonomous Legal Contract Negotiator

### *Two AI agents walk into a boardroom. Only one deal walks out.*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![AutoGen](https://img.shields.io/badge/AutoGen-v0.7-7B2FBE?style=for-the-badge&logo=microsoft&logoColor=white)](https://github.com/microsoft/autogen)
[![Claude](https://img.shields.io/badge/Claude-Sonnet_4.6-D97757?style=for-the-badge&logo=anthropic&logoColor=white)](https://anthropic.com)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](./LICENSE)
[![Status](https://img.shields.io/badge/Status-Production_Ready-22C55E?style=for-the-badge)]()

**[🇬🇧 English](#english-version) · [🇫🇷 Français](#version-française)**

---

*From weeks of legal back-and-forth to minutes of autonomous negotiation.*  
*Built by [Bobby Mozaar](mailto:smozaar@gmail.com) — AI Systems Architect · BigIcks Consulting*

</div>

---

## English Version

### The Problem No One Talks About

Every enterprise B2B deal dies the same slow death.

A contract lands in legal. Lawyers redline it. It bounces back. More redlines. More bouncing. Three weeks later, the same four clauses are still unresolved — IP ownership, license duration, governing law, term length. The sales team is furious. The deal is stalled. The legal team is billing by the hour.

This is not a legal problem. **It's an orchestration problem.**

AGL is the fix. Two fully isolated AI agents — one representing the Buyer, one the Seller — negotiate a real NDA with real IP ownership clauses, arbitrated by an impartial third agent, until they reach a documented agreement or a declared impasse. The output is a professionally redlined Word document, ready for human legal review.

No human in the loop for the first 80% of friction. Just agents, mandates, and math.

---

### What Makes This Different

Most AI contract tools summarize or draft. AGL **negotiates**.

| Feature | AGL | Typical AI Contract Tool |
|---|---|---|
| Adversarial agent architecture | ✅ | ❌ |
| Private isolated mandates per agent | ✅ | ❌ |
| Impartial arbitrator node | ✅ | ❌ |
| Semantic convergence detection | ✅ | ❌ |
| Token budget protection (flatline kill) | ✅ | ❌ |
| Redlined DOCX output | ✅ | Partial |
| Full audit trail JSON | ✅ | Partial |

---

### Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    NEGOTIATION ARENA                      │
│                                                           │
│  ┌──────────────────┐  proposal  ┌───────────────────┐   │
│  │   BUYER AGENT    │ ─────────► │   SELLER AGENT    │   │
│  │   Buyer_Counsel  │ ◄───────── │   Seller_Counsel  │   │
│  │   private SP ▓▓▓ │            │   private SP ▓▓▓  │   │
│  └────────┬─────────┘            └─────────┬─────────┘   │
│           │                                │              │
│           └──────────────┬─────────────────┘              │
│                          ▼                                │
│                 ┌─────────────────┐                       │
│                 │   ARBITRATOR    │  temperature=0.2      │
│                 │   turn mgmt     │  impartial            │
│                 │   deadlock det. │  no financial stake   │
│                 └────────┬────────┘                       │
│                          ▼                                │
│                 ┌─────────────────┐                       │
│                 │   CONVERGENCE   │  sentence-transformers│
│                 │   EVALUATOR     │  cosine similarity    │
│                 │   flatline →    │  delta tracking       │
│                 │   terminate     │                       │
│                 └────────┬────────┘                       │
└──────────────────────────┼───────────────────────────────┘
                           ▼
              ┌──────────────────────────┐
              │       python-docx        │
              │   Redlined NDA DOCX      │
              │   Convergence Report     │
              │   Full Transcript        │
              └──────────────────────────┘
```

**Why this architecture works:**

The adversarial nature of the negotiation does not come from using different LLMs — it comes from **isolated context**. Each agent receives a private system prompt containing its mandate, red lines, and concession strategy. Neither agent can see the other's instructions. Claude, running two separate instances with opposing mandates, produces genuinely conflicting positions — exactly like two real legal teams working from different briefs.

The Arbitrator runs at `temperature=0.2` — deliberately lower than the negotiating agents — to ensure consistent, parseable output. A deterministic arbitrator is a stable pipeline.

---

### Project Structure

```
agl-contract-negotiator/
│
├── src/
│   ├── agents/
│   │   ├── buyer_agent.py         ← Private mandate: exclusive IP ownership
│   │   ├── seller_agent.py        ← Private mandate: co-ownership, tech protection
│   │   └── arbitrator.py          ← Impartial · turn mgmt · status parser
│   │
│   ├── core/
│   │   ├── negotiation_engine.py  ← Main async orchestration loop (AutoGen v0.7)
│   │   ├── convergence.py         ← Cosine similarity · flatline detection
│   │   └── contract_writer.py     ← Redlined DOCX generator (python-docx)
│   │
│   ├── contracts/
│   │   └── nda_template.py        ← NDA base · disputed clauses · party positions
│   │
│   ├── evaluation/
│   │   └── ragas_eval.py          ← Cross-turn delta tracking
│   │
│   ├── app.py                     ← Entry point
│   └── config.py                  ← Centralized config via .env
│
├── assets/
│   └── nda_sample.docx            ← Sample negotiated output (downloadable)
│
├── tests/
│   ├── test_agents.py
│   ├── test_convergence.py
│   └── conftest.py
│
├── docs/
│   ├── ARCHITECTURE.md
│   └── QUICKSTART.md
│
├── scripts/
│   └── run_mock.py                ← Full pipeline demo, no API credits needed
│
├── .env.example
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

### The NDA: What the Agents Actually Fight Over

The agents negotiate a **Mutual NDA with IP Ownership clauses** — the highest-stakes section of any B2B technology partnership. Four clauses, four battles:

| Clause | Buyer Opens | Seller Opens | Typical Resolution |
|---|---|---|---|
| **3 — IP Ownership** | Exclusive ownership by Buyer | 50/50 co-ownership | 60/40 with exploitation rights |
| **4 — License Grant** | 90 days, no royalties | Full-term, independent licensing | 180-day renewable |
| **5 — Term** | 5 years, 60-day notice | 2 years, 30-day notice | 3 years, 45-day notice |
| **6 — Governing Law** | Delaware, USA (hard req.) | England & Wales | Singapore ICC Arbitration |

The agents do not just argue — they **trade**. The Buyer can yield on term length (Clause 5) to protect IP exclusivity (Clause 3). The Seller can yield on jurisdiction (Clause 6) to secure co-ownership (Clause 3). This is real negotiation logic, encoded in private system prompts.

---

### Convergence Engine: The Math Behind the Termination

Every turn, each agent's message is embedded using `sentence-transformers/all-MiniLM-L6-v2` and compared to that agent's previous message via cosine similarity:

```
similarity(turn_n, turn_n-2)  →  how much has this agent's position moved?
delta = |similarity_n - similarity_n-1|  →  rate of change

if delta < 0.01 for 3 consecutive turns  →  FLATLINE  →  terminate
if similarity > 0.92                     →  CONVERGENCE  →  terminate
```

This is not a timer. It is a **mathematical measure of negotiation stagnation** — the difference between a production-safe autonomous system and one that runs until your API bill hits the ceiling.

**Why 0.92?** At that threshold with `all-MiniLM-L6-v2`, two legal position statements are semantically near-identical. An agent rephrasing its position scores ~0.88-0.91. True convergence — an agent genuinely accepting the other's terms — scores 0.92+.

---

### Sample Output

> Produced by `scripts/run_mock.py` — full pipeline, no API credits required.

**Turn 0 — Buyer opens:**
```
POSITION: TechCorp demands EXCLUSIVE ownership of all jointly developed IP.
Delaware law. 5-year term. 90-day license, no royalties.
```

**Turn 1 — Seller responds:**
```
COUNTER-POSITION: InnovateSoft requires 50/50 co-ownership with independent
exploitation rights. England & Wales. 2-year term. Full-term license.
```

**Turn 2 — Arbitrator:**
```
STATUS: NEGOTIATING
OPEN CLAUSES: 3, 4, 5, 6
AGREED CLAUSES: 1, 2, 7
NOTE: Clear opening positions established. Meaningful movement required on IP split.
```

**Turn 3 — Resolution:**
```
STATUS: AGREEMENT REACHED
- Clause 3: 60/40 IP split with independent exploitation rights
- Clause 4: 180-day renewable license, no royalties
- Clause 5: 3-year term, 45-day notice
- Clause 6: Singapore ICC International Arbitration
```

📄 **[Download sample negotiated NDA →](./assets/nda_sample.docx)**

---

### Convergence Report (Mock Run)

| Metric | Value |
|---|---|
| Total Turns | 3 |
| Convergence Reached | ✅ Yes |
| Flatline Triggered | ❌ No |
| Termination Reason | CONVERGENCE |
| Average Similarity | 0.847 |
| Final Similarity | **0.923** |

---

### Quickstart

**Prerequisites:** Python 3.11+, Anthropic API key

```bash
# 1. Clone
git clone https://github.com/MozaarAI-Agentic/agl-contract-negotiator.git
cd agl-contract-negotiator

# 2. Environment
python -m venv venv
source venv/bin/activate          # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Config
cp .env.example .env
# Edit .env → add your ANTHROPIC_API_KEY

# 4. Dry-run (architecture check, no API call)
python src/app.py --dry-run

# 5. Mock run (full pipeline, no API credits needed)
python scripts/run_mock.py

# 6. Full negotiation
python src/app.py
```

**Docker:**
```bash
docker compose up --build
```

---

### Configuration

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | Required |
| `CLAUDE_MODEL` | `claude-sonnet-4-6` | Model to use |
| `MAX_TURNS` | `10` | Hard cap on negotiation turns |
| `MIN_TURNS` | `3` | Min turns before convergence check |
| `CONVERGENCE_THRESHOLD` | `0.92` | Cosine similarity threshold |
| `FLATLINE_TURNS` | `3` | Consecutive flatline turns before forced stop |

---

### Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Agent Framework | AutoGen v0.7 | Native async multi-agent primitives |
| LLM Backend | Claude Sonnet 4.6 | Best instruction-following for legal reasoning |
| Convergence Eval | sentence-transformers | Local, zero API cost, production-fast |
| Document Output | python-docx | Enterprise-standard redline formatting |
| Config | python-dotenv | 12-factor app compliance |
| Containerization | Docker + Compose | One-command reproducible deployment |

---

### Known Limitations

Every honest engineer documents what their system *cannot* do.

**1. Single-LLM adversarialism**
Both agents run on Claude. Adversarial behavior emerges from isolated system prompts, not model bias divergence. In production, running Buyer on Claude and Seller on GPT-4o would introduce genuine epistemic differences — a stronger test of the arbitration system.

**2. NDA scope only**
The current template covers NDA + IP clauses. Extending to full MSA, SOW, or employment agreements requires new templates and agent mandate redesign.

**3. No session memory**
Each negotiation starts fresh. There is no mechanism to resume a failed negotiation or build on previous partial agreements.

**4. Message-level convergence, not clause-level**
The evaluator measures overall message similarity, not per-clause agreement. An agent could agree on three clauses and deadlock on one — the evaluator would not distinguish this from full deadlock.

**5. No legal validation**
The output DOCX is a structured draft, not a legally reviewed document. Human legal review remains required before any execution.

---

### Future Improvements

**Short term (0–3 months)**
- [ ] Streamlit UI for real-time turn-by-turn negotiation visualization
- [ ] Langfuse observability — trace every agent call with latency and cost breakdown
- [ ] Per-clause convergence tracking (not just message-level)
- [ ] HITL override mode — pause negotiation for human review on critical clauses

**Medium term (3–6 months)**
- [ ] Multi-LLM mode: Buyer=Claude, Seller=GPT-4o, Arbitrator=Gemini
- [ ] Additional contract types: SaaS MSA, SOW, employment agreements
- [ ] Vector memory — agents referencing precedents from past negotiation sessions
- [ ] REST API for integration into existing legal workflow tools

**Long term (6–12 months)**
- [ ] Fine-tuned legal reasoning model (LoRA on NDA domain corpus)
- [ ] Multi-language support (EN + FR for francophone markets)
- [ ] DocuSign API integration for end-to-end execution workflow
- [ ] GDPR, CCPA, and sector-specific compliance checking

---

### Why This Project Exists

> *"I built AGL to prove a single point: the hardest problem in multi-agent AI is not making agents smart — it's making them disagree productively and converge reliably."*
>
> — Bobby Mozaar, AI Systems Architect

The enterprise legal market spends an estimated $300B/year on contract management. The bottleneck is not drafting — it is negotiation. AGL is a proof-of-concept for what autonomous negotiation infrastructure looks like when built to production engineering standards: isolated context, mathematical termination conditions, and structured outputs that integrate into existing enterprise workflows.

This is Project 2 in an ongoing portfolio of production-grade agentic systems built for real institutional contexts. Project 1 (KYC Orchestrator) is live at [`MozaarAI-Agentic/project-1`](https://github.com/MozaarAI-Agentic).

---

### Author

**Bobby Mozaar** — AI Systems Architect · Founder, BigIcks Consulting · Cameroon 🇨🇲

> Institutional AI systems for real-world infrastructure. QUALNET (7-agent telecom QoS system, ~4B FCFA), PICTEL (5-agent consumer protection platform, ~2.5B FCFA) — both deployed for ART Cameroun.

- 📧 [smozaar@gmail.com](mailto:smozaar@gmail.com)
- 🔗 GitHub: [@Mozaar007](https://github.com/Mozaar007)
- 📱 +237 673 687 079

---

### License

MIT License — see [LICENSE](./LICENSE)

---

---

## Version Française

### Le Problème que Personne N'ose Nommer

Chaque deal B2B enterprise meurt de la même mort lente.

Un contrat arrive chez les juristes. Ils le redlinent. Il repart. Nouvelles annotations. Nouveau retour. Trois semaines plus tard, les mêmes quatre clauses — propriété intellectuelle, durée de la licence, droit applicable, durée du contrat — sont toujours en suspens. L'équipe commerciale s'impatiente. Le deal patine. Les avocats facturent à l'heure.

Ce n'est pas un problème juridique. **C'est un problème d'orchestration.**

AGL est la réponse. Deux agents IA totalement isolés — l'un représentant l'Acheteur, l'autre le Vendeur — négocient un vrai NDA avec de vraies clauses IP, arbitrés par un troisième agent impartial, jusqu'à un accord documenté ou une impasse déclarée. L'output est un document Word professionnel redliné, prêt pour validation humaine.

Aucune intervention humaine sur les 80 premiers pourcents de friction. Juste des agents, des mandats, et des mathématiques.

---

### Ce que Ce Système Prouve

La plupart des outils IA pour contrats résument ou rédigent. AGL **négocie**.

Ce projet démontre la capacité à gérer des **agents concurrents avec des system prompts conflictuels et des états de données cachés** — l'un des problèmes les plus difficiles en orchestration IA. En implémentant un évaluateur de convergence automatique basé sur la similarité sémantique, il montre des garde-fous mathématiques réels sur le comportement imprévisible des LLMs — prouvant qu'il est possible de construire des systèmes autonomes sûrs, prédictibles et prêts pour l'entreprise.

---

### Architecture

```
┌──────────────────────────────────────────────────────────┐
│                  ARÈNE DE NÉGOCIATION                     │
│                                                           │
│  ┌──────────────────┐  proposal  ┌───────────────────┐   │
│  │   AGENT BUYER    │ ─────────► │   AGENT SELLER    │   │
│  │   mandat privé ▓ │ ◄───────── │   mandat privé ▓  │   │
│  └────────┬─────────┘            └─────────┬─────────┘   │
│           └──────────────┬─────────────────┘              │
│                          ▼                                │
│                 ┌─────────────────┐                       │
│                 │   ARBITRATEUR   │  impartial            │
│                 │   gestion tours │  temperature basse    │
│                 │   détection     │  aucun intérêt        │
│                 │   deadlock      │  financier            │
│                 └────────┬────────┘                       │
│                          ▼                                │
│                 ┌─────────────────┐                       │
│                 │   CONVERGENCE   │  sentence-transformers│
│                 │   EVALUATOR     │  similarité cosinus   │
│                 │   flatline →    │  protection budget    │
│                 │   terminate     │  tokens               │
│                 └────────┬────────┘                       │
└──────────────────────────┼───────────────────────────────┘
                           ▼
              ┌──────────────────────────┐
              │       python-docx        │
              │   NDA Redliné DOCX       │
              │   Rapport Convergence    │
              │   Transcript Complet     │
              └──────────────────────────┘
```

---

### Ce que les Agents Négocient

Quatre clauses, quatre batailles réelles :

| Clause | Position Buyer | Position Seller | Résolution typique |
|---|---|---|---|
| **3 — Propriété IP** | Ownership exclusif Buyer | Co-ownership 50/50 | 60/40 avec droits d'exploitation |
| **4 — Licence** | 90 jours, sans royalties | Durée contrat, licences indépendantes | 180 jours renouvelable |
| **5 — Durée** | 5 ans, préavis 60 jours | 2 ans, préavis 30 jours | 3 ans, préavis 45 jours |
| **6 — Droit applicable** | Delaware, USA (obligatoire) | Angleterre et Pays de Galles | Arbitrage ICC Singapour |

Les agents ne se contentent pas d'argumenter — ils **font des concessions stratégiques**. L'Acheteur peut céder sur la durée (Clause 5) pour protéger l'ownership IP (Clause 3). Le Vendeur peut céder sur la juridiction (Clause 6) pour sécuriser le co-ownership (Clause 3).

---

### Moteur de Convergence : Les Mathématiques Derrière l'Arrêt

À chaque tour, le message de chaque agent est transformé en vecteur d'embedding et comparé au message précédent du même agent :

```
similarité(tour_n, tour_n-2) → l'agent a-t-il bougé de position ?
delta = |similarité_n - similarité_n-1| → taux de changement

si delta < 0.01 pendant 3 tours consécutifs → FLATLINE → arrêt forcé
si similarité > 0.92 → CONVERGENCE → accord détecté
```

Ce n'est pas un timer. C'est une **mesure mathématique de la stagnation de la négociation** — ce qui distingue un système autonome production-safe d'un système qui épuise ton budget API.

---

### Exemple de Sortie (Mock Run)

**Tour 0 — Le Buyer ouvre :**
```
POSITION: TechCorp exige l'ownership EXCLUSIF de toute IP développée conjointement.
Droit Delaware. Durée 5 ans. Licence 90 jours, sans royalties.
```

**Tour 1 — Le Seller répond :**
```
CONTRE-POSITION: InnovateSoft exige un co-ownership 50/50 avec droits d'exploitation
indépendants. Angleterre et Pays de Galles. Durée 2 ans. Licence pleine durée.
```

**Tour 3 — Résolution :**
```
STATUT: ACCORD CONCLU
- Clause 3: Split IP 60/40 avec droits d'exploitation indépendants
- Clause 4: Licence 180 jours renouvelable, sans royalties
- Clause 5: Durée 3 ans, préavis 45 jours
- Clause 6: Arbitrage International ICC Singapour
```

📄 **[Télécharger le NDA négocié (exemple) →](./assets/nda_sample.docx)**

---

### Quickstart

```bash
# 1. Clone
git clone https://github.com/MozaarAI-Agentic/agl-contract-negotiator.git
cd agl-contract-negotiator

# 2. Environnement
python -m venv venv
.\venv\Scripts\Activate.ps1     # Windows
pip install -r requirements.txt

# 3. Configuration
cp .env.example .env
# Éditer .env → ajouter ANTHROPIC_API_KEY

# 4. Dry-run (validation architecture, aucun appel LLM)
python src/app.py --dry-run

# 5. Mock run (pipeline complet, sans crédits API)
python scripts/run_mock.py

# 6. Négociation complète
python src/app.py
```

---

### Limitations Connues

**1. Single-LLM** — Les deux agents utilisent Claude. L'adversarialité vient de l'isolation des system prompts, pas de biais de modèles différents. En production, Seller_Counsel serait remplacé par GPT-4o pour une vraie divergence épistémique.

**2. Scope NDA uniquement** — L'extension à d'autres types de contrats (MSA, SOW) nécessite de nouveaux templates.

**3. Pas de mémoire inter-sessions** — Chaque négociation repart de zéro.

**4. Convergence au niveau message** — L'évaluateur mesure la similarité globale du message, pas l'accord par clause individuelle.

**5. Pas de validation juridique réelle** — L'output DOCX est un brouillon structuré. La validation humaine reste obligatoire avant signature.

---

### Améliorations Futures

**Court terme (0–3 mois)**
- [ ] Interface Streamlit pour visualisation en temps réel
- [ ] Intégration Langfuse pour l'observabilité (coût, latence, traces par agent)
- [ ] Convergence par clause individuelle
- [ ] Mode HITL — pause négociation sur clauses critiques pour review humaine

**Moyen terme (3–6 mois)**
- [ ] Mode Multi-LLM : Buyer=Claude, Seller=GPT-4o, Arbitrator=Gemini
- [ ] Support d'autres contrats : MSA SaaS, SOW, contrats d'emploi
- [ ] Mémoire vectorielle — agents référençant des précédents
- [ ] API REST pour intégration dans outils juridiques existants

**Long terme (6–12 mois)**
- [ ] Modèle fine-tuné sur corpus NDA (LoRA)
- [ ] Support multilingue (EN + FR)
- [ ] Intégration DocuSign pour workflow de signature
- [ ] Vérification conformité RGPD, CCPA

---

### Pourquoi Ce Projet Existe

> *"J'ai construit AGL pour prouver un seul point : le problème le plus difficile en IA multi-agents n'est pas de rendre les agents intelligents — c'est de les faire être en désaccord de manière productive et converger de manière fiable."*
>
> — Bobby Mozaar, Architecte Systèmes IA

Le marché enterprise de la gestion contractuelle représente environ 300 milliards de dollars par an. Le goulot d'étranglement n'est pas la rédaction — c'est la négociation. AGL est une preuve de concept de ce à quoi ressemble une infrastructure de négociation autonome quand elle est construite selon des standards d'ingénierie production.

Ce projet est le Projet 2 d'un portfolio continu de systèmes agentiques production-grade construits pour des contextes institutionnels réels. Le Projet 1 (KYC Orchestrator) est disponible à [`MozaarAI-Agentic/project-1`](https://github.com/MozaarAI-Agentic).

---

### Auteur

**Bobby Mozaar** (également Sam Mozaar / MOMNUGI SAUREL ARNAUD)  
Architecte Systèmes IA · Fondateur, BigIcks Consulting · Cameroun 🇨🇲

> Systèmes IA institutionnels pour infrastructures réelles. QUALNET (système 7 agents pour mesure qualité télécom, ~4 Mds FCFA), PICTEL (plateforme 5 agents pour protection des consommateurs, ~2,5 Mds FCFA) — tous deux déployés pour l'ART Cameroun.

- 📧 [smozaar@gmail.com](mailto:smozaar@gmail.com)
- 🔗 GitHub : [@Mozaar007](https://github.com/Mozaar007)
- 📱 +237 673 687 079

---

### Licence

MIT License — voir [LICENSE](./LICENSE)

---

<!-- ══════════════════════════════════════════════════════════
     GITHUB REPOSITORY TOPICS
     Copy-paste these into Settings → Topics on GitHub
     to maximize repo discoverability:

     agentic-ai
     multi-agent-systems
     autogen
     claude-api
     anthropic
     contract-negotiation
     legal-ai
     nlp
     semantic-similarity
     sentence-transformers
     python
     enterprise-ai
     llm
     autonomous-agents
     ai-orchestration
     docx
     legal-tech
     ragas
     b2b
     adversarial-agents
══════════════════════════════════════════════════════════ -->
