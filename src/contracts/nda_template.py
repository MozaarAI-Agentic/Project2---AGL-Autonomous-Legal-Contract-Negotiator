"""
AGL - NDA Template
"""

NDA_BASE = {
    "title": "MUTUAL NON-DISCLOSURE AND IP OWNERSHIP AGREEMENT",
    "parties": {
        "buyer":  "TechCorp Solutions Inc. (Disclosing Party / Buyer)",
        "seller": "InnovateSoft Ltd. (Receiving Party / Seller)",
    },
    "clauses": {
        "1_definition": {
            "title": "Definition of Confidential Information",
            "text": "Confidential Information means any non-public information disclosed by either party, including technical data, trade secrets, know-how, research, product plans, software, customer lists, financial information, or business plans.",
            "disputed": False,
        },
        "2_obligations": {
            "title": "Obligations of Receiving Party",
            "text": "The Receiving Party agrees to: (a) hold Confidential Information in strict confidence; (b) not disclose to third parties without consent; (c) use solely for evaluating a potential business relationship.",
            "disputed": False,
        },
        "3_ip_ownership": {
            "title": "Intellectual Property Ownership",
            "text": "All IP developed jointly shall be owned [TO BE NEGOTIATED]. Each party retains ownership of its pre-existing IP. Derivative works shall be owned by [TO BE NEGOTIATED].",
            "disputed": True,
            "key_terms": ["ownership split", "derivative works", "pre-existing IP"],
        },
        "4_ip_license": {
            "title": "License Grant",
            "text": "Each party grants the other a [TO BE NEGOTIATED] license to use its Confidential Information for the evaluation period of [DURATION TO BE NEGOTIATED].",
            "disputed": True,
            "key_terms": ["license type", "duration", "sublicense rights", "royalties"],
        },
        "5_term": {
            "title": "Term and Termination",
            "text": "This Agreement shall remain in effect for [DURATION TO BE NEGOTIATED]. Either party may terminate upon [NOTICE PERIOD TO BE NEGOTIATED] written notice.",
            "disputed": True,
            "key_terms": ["duration", "notice period"],
        },
        "6_governing_law": {
            "title": "Governing Law",
            "text": "This Agreement shall be governed by the laws of [JURISDICTION TO BE NEGOTIATED], without regard to its conflict of law provisions.",
            "disputed": True,
            "key_terms": ["jurisdiction", "court"],
        },
        "7_remedies": {
            "title": "Remedies",
            "text": "The parties acknowledge that breach may cause irreparable harm. The non-breaching party shall be entitled to seek equitable relief, including injunction, in addition to all other remedies.",
            "disputed": False,
        },
    },
}

BUYER_INITIAL_POSITION = {
    "clause_3": {
        "label": "IP Ownership",
        "position": "exclusive",
        "text": "ALL jointly developed IP shall be owned EXCLUSIVELY by TechCorp Solutions Inc. InnovateSoft receives only a limited, non-exclusive, non-transferable license. InnovateSoft pre-existing IP used in the collaboration must be licensed to TechCorp royalty-free.",
        "redline": "exclusive ownership to TechCorp",
        "minimum_acceptable": "70/30 split in TechCorp favor",
        "hard_limit": True,
    },
    "clause_4": {
        "label": "License Grant",
        "position": "restrictive",
        "text": "License granted to InnovateSoft: non-exclusive, revocable, 90-day term. No sublicensing rights. No royalties owed to InnovateSoft for TechCorp exploitation of jointly developed IP.",
        "redline": "90-day license, no royalties",
        "minimum_acceptable": "180-day license",
        "hard_limit": False,
    },
    "clause_5": {
        "label": "Term",
        "position": "long",
        "text": "Agreement term: 5 years. Termination notice: 60 days written notice.",
        "redline": "5 years / 60-day notice",
        "minimum_acceptable": "3 years / 45-day notice",
        "hard_limit": False,
    },
    "clause_6": {
        "label": "Governing Law",
        "position": "delaware",
        "text": "Governing Law: State of Delaware, USA. Non-negotiable given TechCorp corporate domicile and board requirements.",
        "redline": "Delaware, USA",
        "minimum_acceptable": "New York, USA",
        "hard_limit": True,
    },
}

SELLER_INITIAL_POSITION = {
    "clause_3": {
        "label": "IP Ownership",
        "position": "co-ownership",
        "text": "Jointly developed IP shall be co-owned 50/50 with independent exploitation rights for each party. InnovateSoft retains FULL ownership of all improvements and derivatives of its pre-existing technology.",
        "redline": "50/50 co-ownership, independent exploitation",
        "minimum_acceptable": "40/60 split Seller/Buyer with exploitation rights",
        "hard_limit": True,
    },
    "clause_4": {
        "label": "License Grant",
        "position": "flexible",
        "text": "License to Buyer: non-exclusive only. InnovateSoft retains full right to license its technology independently to other clients. License term tied to Agreement term, not fixed at 90 days.",
        "redline": "non-exclusive, full-term license",
        "minimum_acceptable": "non-exclusive, 1-year minimum term",
        "hard_limit": False,
    },
    "clause_5": {
        "label": "Term",
        "position": "short",
        "text": "Agreement term: 2 years maximum. Termination notice: 30 days standard commercial practice.",
        "redline": "2 years / 30-day notice",
        "minimum_acceptable": "3 years / 45-day notice",
        "hard_limit": False,
    },
    "clause_6": {
        "label": "Governing Law",
        "position": "england",
        "text": "Governing Law: England and Wales. Neutral common law jurisdiction acceptable to both parties. Internationally recognised IP enforcement framework.",
        "redline": "England and Wales",
        "minimum_acceptable": "Singapore or ICC Arbitration",
        "hard_limit": False,
    },
}


def get_disputed_clauses() -> list:
    return [
        key for key, val in NDA_BASE["clauses"].items()
        if val.get("disputed", False)
    ]


def get_clause_text(clause_key: str) -> str:
    return NDA_BASE["clauses"].get(clause_key, {}).get("text", "")


def get_buyer_redline(clause_key: str) -> str:
    short_key = clause_key.split("_")[0]
    return BUYER_INITIAL_POSITION.get("clause_" + short_key, {}).get("redline", "")


def get_seller_redline(clause_key: str) -> str:
    short_key = clause_key.split("_")[0]
    return SELLER_INITIAL_POSITION.get("clause_" + short_key, {}).get("redline", "")
