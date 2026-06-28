"""
AGL - Mock Negotiation
Simule une negociation complete sans appel API.
Utilise pour documenter le README et tester le pipeline complet.
"""

import json
import os
import sys

sys.path.insert(0, os.getcwd())

from src.core.contract_writer import ContractWriter
from src.core.negotiation_engine import NegotiationResult
from src.core.convergence import ConvergenceEvaluator

# Transcript de negociation simule
MOCK_LOG = [
    {
        "turn": 0,
        "speaker": "Buyer_Counsel",
        "timestamp": "2026-06-28T09:00:00",
        "content": """POSITION: TechCorp Solutions Inc. proposes the following terms:

Clause 3 (IP Ownership): All jointly developed IP shall vest EXCLUSIVELY in TechCorp.
InnovateSoft receives a limited, non-exclusive, non-sublicensable license only.

Clause 4 (License Grant): License period limited to 90 days from execution date.
No royalties owed to InnovateSoft.

Clause 5 (Term): 5-year agreement. 60-day written termination notice.

Clause 6 (Governing Law): State of Delaware, USA. Non-negotiable.

RATIONALE: TechCorp is the primary capital investor in this collaboration.
Exclusive IP ownership reflects the economic reality of both parties contributions
and protects our shareholders interests.

PROPOSAL: We invite InnovateSoft counsel to respond to these terms."""
    },
    {
        "turn": 1,
        "speaker": "Seller_Counsel",
        "timestamp": "2026-06-28T09:01:00",
        "content": """COUNTER-POSITION: InnovateSoft firmly rejects exclusive IP ownership by TechCorp.

Clause 3 (IP Ownership): Jointly developed IP must be co-owned 50/50 with independent
exploitation rights for each party. InnovateSoft retains full ownership of all
improvements to its pre-existing technology stack.

Clause 4 (License Grant): License to Buyer is non-exclusive only. InnovateSoft retains
the right to license its technology to other clients independently.
License term must be tied to the Agreement term, not fixed at 90 days.

Clause 5 (Term): 2-year maximum term with 30-day termination notice.
A 5-year lock-in is commercially unacceptable for InnovateSoft.

Clause 6 (Governing Law): England and Wales - neutral common law jurisdiction
recognised internationally for IP enforcement.

RATIONALE: InnovateSoft technology is the core value driver of this partnership.
Under TRIPS Agreement Article 28, IP co-ownership with independent exploitation
rights is standard practice in technology licensing partnerships.

REVISED PROPOSAL: 50/50 co-ownership, non-exclusive licenses, 2-year term,
England and Wales governing law.

ACCEPTANCE: We accept Clause 1 and 2 as drafted."""
    },
    {
        "turn": 1,
        "speaker": "Arbitrator",
        "timestamp": "2026-06-28T09:02:00",
        "content": """STATUS: NEGOTIATING
TURN: 1
OPEN CLAUSES: Clause 3 (IP Ownership), Clause 4 (License), Clause 5 (Term), Clause 6 (Governing Law)
AGREED CLAUSES: Clause 1 (Definition), Clause 2 (Obligations), Clause 7 (Remedies)
ARBITRATOR NOTE: Both parties have presented clear opening positions. Clause 3 remains
the primary point of contention with exclusive ownership vs 50/50 co-ownership.
Meaningful movement will be required from both sides on IP split and term duration.
NEXT SPEAKER: Buyer_Counsel"""
    },
    {
        "turn": 2,
        "speaker": "Buyer_Counsel",
        "timestamp": "2026-06-28T09:03:00",
        "content": """POSITION: TechCorp acknowledges InnovateSoft's position and offers a structured concession.

Clause 3 (IP Ownership): TechCorp proposes a 70/30 split (TechCorp/InnovateSoft)
with InnovateSoft retaining independent exploitation rights for its pre-existing
technology derivatives only. New jointly developed IP remains 70/30.

Clause 4 (License Grant): TechCorp accepts extending the license term to 180 days
with a renewable option. No royalties remain non-negotiable.

Clause 5 (Term): TechCorp can accept 3 years with 45-day termination notice
as a compromise position.

Clause 6 (Governing Law): TechCorp maintains Delaware as primary preference
but will consider New York as an alternative US jurisdiction.

RATIONALE: The 70/30 split reflects TechCorp's capital contribution while
acknowledging InnovateSoft's technology value. This is a significant concession
from our opening exclusive ownership position.

PROPOSAL: 70/30 IP split, 180-day renewable license, 3-year term, New York law.

CONCESSION: Term reduced from 5 to 3 years. License extended from 90 to 180 days."""
    },
    {
        "turn": 2,
        "speaker": "Seller_Counsel",
        "timestamp": "2026-06-28T09:04:00",
        "content": """COUNTER-POSITION: InnovateSoft acknowledges TechCorp's movement on term and license duration.

Clause 3 (IP Ownership): InnovateSoft cannot accept 70/30. Minimum acceptable
is 45/55 (Seller/Buyer) with full independent exploitation rights for both parties.
This reflects standard technology partnership practice under UK commercial law.

Clause 4 (License Grant): InnovateSoft accepts 180-day renewable license as a
workable compromise. We withdraw the royalty demand in exchange.

Clause 5 (Term): InnovateSoft accepts 3 years with 45-day notice. Agreed.

Clause 6 (Governing Law): InnovateSoft proposes Singapore ICC Arbitration as
a neutral alternative acceptable to both US and UK parties.

RATIONALE: The 45/55 split with independent exploitation rights is the minimum
that protects InnovateSoft's ability to continue operating its core business.
Singapore ICC is internationally recognised and removes jurisdictional bias.

REVISED PROPOSAL: 45/55 IP split, 180-day renewable license, 3-year term,
Singapore ICC Arbitration.

ACCEPTANCE: Clause 4 (180-day license, no royalties). Clause 5 (3 years, 45 days)."""
    },
    {
        "turn": 2,
        "speaker": "Arbitrator",
        "timestamp": "2026-06-28T09:05:00",
        "content": """STATUS: CONVERGING
TURN: 2
OPEN CLAUSES: Clause 3 (IP split: 70/30 vs 45/55), Clause 6 (New York vs Singapore)
AGREED CLAUSES: Clause 1, Clause 2, Clause 4 (180-day renewable, no royalties), Clause 5 (3 years, 45 days), Clause 7
ARBITRATOR NOTE: Significant progress achieved. Clause 4 and 5 are now agreed.
The gap on Clause 3 has narrowed from exclusive vs 50/50 to 70/30 vs 45/55.
A compromise at 60/40 appears mathematically viable. Clause 6 may resolve via
Singapore ICC as a neutral forum. One more exchange should achieve resolution.
NEXT SPEAKER: Buyer_Counsel"""
    },
    {
        "turn": 3,
        "speaker": "Buyer_Counsel",
        "timestamp": "2026-06-28T09:06:00",
        "content": """POSITION: TechCorp accepts the Arbitrator's framing and proposes final resolution.

Clause 3 (IP Ownership): TechCorp proposes 60/40 (TechCorp/InnovateSoft) with
full independent exploitation rights for both parties on jointly developed IP.
Each party retains 100% ownership of pre-existing IP and derivatives thereof.

Clause 6 (Governing Law): TechCorp accepts Singapore ICC International Arbitration
as a neutral forum. This is a significant concession from our Delaware position.

RATIONALE: The 60/40 split with mutual independent exploitation rights represents
a fair reflection of capital vs technology contributions to this partnership.
Singapore ICC provides internationally enforceable IP protection for both parties.

PROPOSAL: 60/40 IP split with independent exploitation, Singapore ICC. Final offer.

CONCESSION: Governing law moved from Delaware/New York to Singapore ICC.
IP split moved from exclusive to 60/40 with full exploitation rights."""
    },
    {
        "turn": 3,
        "speaker": "Seller_Counsel",
        "timestamp": "2026-06-28T09:07:00",
        "content": """COUNTER-POSITION: InnovateSoft accepts TechCorp final proposal with one clarification.

Clause 3 (IP Ownership): InnovateSoft accepts 60/40 (TechCorp/InnovateSoft)
with full independent exploitation rights for both parties. We confirm that
pre-existing IP and all derivatives remain 100% owned by the originating party.

Clause 6 (Governing Law): InnovateSoft accepts Singapore ICC International
Arbitration. This is a fair neutral forum for both parties.

RATIONALE: The 60/40 split with independent exploitation rights and Singapore ICC
represents a commercially viable and legally sound resolution for InnovateSoft.
Both parties can independently exploit the jointly developed IP without
accounting to each other.

REVISED PROPOSAL: FULL AGREEMENT on all clauses.

ACCEPTANCE: Clause 3 (60/40, independent exploitation). Clause 6 (Singapore ICC).
All other clauses previously agreed. InnovateSoft signals readiness to execute."""
    },
    {
        "turn": 3,
        "speaker": "Arbitrator",
        "timestamp": "2026-06-28T09:08:00",
        "content": """STATUS: AGREEMENT REACHED
TURN: 3
OPEN CLAUSES: None
AGREED CLAUSES: All clauses (1, 2, 3, 4, 5, 6, 7)
ARBITRATOR NOTE: Full agreement achieved in 3 turns. Final terms:
- Clause 3: 60/40 IP split (TechCorp/InnovateSoft) with independent exploitation rights
- Clause 4: 180-day renewable license, no royalties
- Clause 5: 3-year term, 45-day termination notice
- Clause 6: Singapore ICC International Arbitration
Both parties have signaled readiness to execute. Negotiation concluded successfully.
NEXT SPEAKER: None - Agreement reached."""
    },
]

# Metriques de convergence simulees
MOCK_CONVERGENCE = {
    "total_turns": 3,
    "convergence_reached": True,
    "flatline_triggered": False,
    "termination_reason": "CONVERGENCE",
    "avg_similarity": 0.847,
    "max_similarity": 0.923,
    "final_similarity": 0.923,
    "turn_by_turn": [
        {"turn": 0, "speaker": "Buyer_Counsel",  "similarity": None,  "delta": None},
        {"turn": 1, "speaker": "Seller_Counsel",  "similarity": None,  "delta": None},
        {"turn": 1, "speaker": "Arbitrator",      "similarity": None,  "delta": None},
        {"turn": 2, "speaker": "Buyer_Counsel",   "similarity": 0.781, "delta": None},
        {"turn": 2, "speaker": "Seller_Counsel",  "similarity": 0.803, "delta": 0.022},
        {"turn": 2, "speaker": "Arbitrator",      "similarity": 0.812, "delta": 0.009},
        {"turn": 3, "speaker": "Buyer_Counsel",   "similarity": 0.887, "delta": 0.106},
        {"turn": 3, "speaker": "Seller_Counsel",  "similarity": 0.923, "delta": 0.036},
        {"turn": 3, "speaker": "Arbitrator",      "similarity": 0.931, "delta": 0.008},
    ],
}


def run_mock():
    print("")
    print("=" * 55)
    print("  AGL - MOCK NEGOTIATION RUN")
    print("  Pipeline complet sans appel API")
    print("=" * 55)
    print("")

    # Construction du NegotiationResult
    result = NegotiationResult(
        session_id="mock_20260628_090000",
        started_at="2026-06-28T09:00:00",
        ended_at="2026-06-28T09:08:00",
        total_turns=3,
        termination_reason="CONVERGENCE",
        final_status="AGREEMENT REACHED",
        agreed_clauses={
            "clause_3": "60/40 split (TechCorp/InnovateSoft) with independent exploitation rights",
            "clause_4": "180-day renewable license, no royalties",
            "clause_5": "3-year term, 45-day termination notice",
            "clause_6": "Singapore ICC International Arbitration",
        },
        negotiation_log=MOCK_LOG,
        convergence_summary=MOCK_CONVERGENCE,
    )

    # Export JSON
    os.makedirs("output", exist_ok=True)
    json_path = "output/negotiation_mock_20260628_090000.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
    print("JSON log genere   : " + json_path)

    # Generation DOCX
    writer = ContractWriter(result)
    docx_path = writer.generate("output/negotiated_nda_mock_20260628.docx")
    print("DOCX genere       : " + docx_path)

    # Export metriques convergence
    metrics_path = "output/convergence_mock_20260628.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(MOCK_CONVERGENCE, f, indent=2)
    print("Metriques generees: " + metrics_path)

    print("")
    print("=" * 55)
    print("  MOCK RUN COMPLET")
    print("  Status  : " + result.final_status)
    print("  Tours   : " + str(result.total_turns))
    print("  Accord  : 60/40 IP | Singapore ICC | 3 ans")
    print("=" * 55)
    print("")
    print("Ouvre le DOCX pour documenter le README :")
    print("output/negotiated_nda_mock_20260628.docx")


if __name__ == "__main__":
    run_mock()
