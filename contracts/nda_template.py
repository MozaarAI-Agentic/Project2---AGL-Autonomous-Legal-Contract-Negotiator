"""
AGL — NDA Template
Contient le document NDA de base (neutre) et les positions
initiales des deux parties sur les clauses disputées.
"""

# ─────────────────────────────────────────────────────────────────────────────
# DOCUMENT NDA DE BASE — point de départ neutre
# Les clauses marquées [TO BE NEGOTIATED] sont celles que les agents
# vont résoudre pendant la négociation.
# ─────────────────────────────────────────────────────────────────────────────

NDA_BASE = {
    "title": "MUTUAL NON-DISCLOSURE AND IP OWNERSHIP AGREEMENT",

    "parties": {
        "buyer":  'TechCorp Solutions Inc. ("Disclosing Party / Buyer")',
        "seller": 'InnovateSoft Ltd. ("Receiving Party / Seller")',
    },

    "clauses": {

        # ── Clause 1 : non disputée, définition standard ──────────────────────
        "1_definition": {
            "title": "Definition of Confidential Information",
            "text": (
                '"Confidential Information" means any non-public information '
                "disclosed by either party, including but not limited to: "
                "technical data, trade secrets, know-how, research, product "
                "plans, software, customer lists, financial information, or "
                "business plans, whether disclosed orally, in writing, or by "
                "any other means."
            ),
            "disputed": False,
        },

        # ── Clause 2 : non disputée, obligations standard ─────────────────────
        "2_obligations": {
            "title": "Obligations of Receiving Party",
            "text": (
                "The Receiving Party agrees to: (a) hold Confidential "
                "Information in strict confidence; (b) not disclose "
                "Confidential Information to third parties without prior "
                "written consent; (c) use Confidential Information solely "
                "for the purpose of evaluating a potential business "
                "relationship."
            ),
            "disputed": False,
        },

        # ── Clause 3 : DISPUTÉE — ownership de l'IP ──────────────────────────
        # C'est la clause pivot. Tout le reste dépend de son résultat.
        "3_ip_ownership": {
            "title": "Intellectual Property Ownership",
            "text": (
                "All Intellectual Property (IP) developed jointly during "
                "the collaboration shall be owned [TO BE NEGOTIATED]. "
                "Each party retains ownership of its pre-existing IP. "
                "Derivative works and improvements to pre-existing IP "
                "shall be owned by [TO BE NEGOTIATED]."
            ),
            "disputed": True,
            "key_terms": [
                "ownership split",        # ex: exclusive / 50-50 / 70-30
                "derivative works",       # qui possède les améliorations ?
                "pre-existing IP",        # chaque partie garde le sien
            ],
        },

        # ── Clause 4 : DISPUTÉE — licence d'utilisation ───────────────────────
        # Dépend directement de la Clause 3 :
        # si Buyer a l'IP exclusive → il contrôle la licence du Seller
        "4_ip_license": {
            "title": "License Grant",
            "text": (
                "Each party grants the other a [TO BE NEGOTIATED] license "
                "to use its Confidential Information solely for the "
                "evaluation period of [DURATION TO BE NEGOTIATED]."
            ),
            "disputed": True,
            "key_terms": [
                "license type",       # exclusive / non-exclusive
                "duration",           # 90 jours / durée du contrat
                "sublicense rights",  # peut-on re-licencier à des tiers ?
                "royalties",          # paiement ou royalty-free ?
            ],
        },

        # ── Clause 5 : DISPUTÉE — durée de l'accord ──────────────────────────
        # Le Buyer veut verrouiller longtemps pour protéger son IP.
        # Le Seller veut rester flexible pour ne pas être piégé.
        "5_term": {
            "title": "Term and Termination",
            "text": (
                "This Agreement shall remain in effect for [DURATION TO BE "
                "NEGOTIATED] from the Effective Date. Either party may "
                "terminate upon [NOTICE PERIOD TO BE NEGOTIATED] written "
                "notice."
            ),
            "disputed": True,
            "key_terms": [
                "duration",        # 2 ans (Seller) vs 5 ans (Buyer)
                "notice period",   # 30 jours (Seller) vs 60 jours (Buyer)
            ],
        },

        # ── Clause 6 : DISPUTÉE — juridiction applicable ─────────────────────
        # Stratégiquement liée à la Clause 3 :
        # qui possède l'IP détermine quel tribunal est pertinent.
        "6_governing_law": {
            "title": "Governing Law",
            "text": (
                "This Agreement shall be governed by the laws of "
                "[JURISDICTION TO BE NEGOTIATED], without regard to its "
                "conflict of law provisions."
            ),
            "disputed": True,
            "key_terms": [
                "jurisdiction",   # Delaware USA vs England & Wales
                "court",          # tribunal compétent en cas de litige
            ],
        },

        # ── Clause 7 : non disputée, recours standard ─────────────────────────
        "7_remedies": {
            "title": "Remedies",
            "text": (
                "The parties acknowledge that breach of this Agreement may "
                "cause irreparable harm for which monetary damages would be "
                "inadequate. Accordingly, the non-breaching party shall be "
                "entitled to seek equitable relief, including injunction, "
                "in addition to all other remedies."
            ),
            "disputed": False,
        },
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# POSITION INITIALE DU BUYER — TechCorp Solutions Inc.
#
# Stratégie : agressive, IP-first.
# Le Buyer est l'investisseur principal → il veut l'ownership exclusif.
# Il est prêt à concéder sur la durée (Clause 5) pour garder l'IP (Clause 3).
# La juridiction Delaware est non-négociable pour lui.
# ─────────────────────────────────────────────────────────────────────────────

BUYER_INITIAL_POSITION = {

    "clause_3": {
        "label": "IP Ownership",
        "position": "exclusive",
        "text": (
            "ALL jointly developed IP shall be owned EXCLUSIVELY by "
            "TechCorp Solutions Inc. InnovateSoft receives only a limited, "
            "non-exclusive, non-transferable license. InnovateSoft's "
            "pre-existing IP used in the collaboration must be licensed "
            "to TechCorp royalty-free."
        ),
        "redline": "exclusive ownership → TechCorp",
        "minimum_acceptable": "70/30 split in TechCorp's favor",
        "hard_limit": True,   # ne pas céder en dessous du minimum
    },

    "clause_4": {
        "label": "License Grant",
        "position": "restrictive",
        "text": (
            "License granted to InnovateSoft: non-exclusive, revocable, "
            "90-day term. No sublicensing rights. No royalties owed to "
            "InnovateSoft for TechCorp's exploitation of jointly developed IP."
        ),
        "redline": "90-day license, no royalties",
        "minimum_acceptable": "180-day license",
        "hard_limit": False,  # peut concéder sur la durée
    },

    "clause_5": {
        "label": "Term",
        "position": "long",
        "text": (
            "Agreement term: 5 years. "
            "Termination notice: 60 days written notice."
        ),
        "redline": "5 years / 60-day notice",
        "minimum_acceptable": "3 years / 45-day notice",
        "hard_limit": False,  # peut concéder ici pour gagner sur Clause 3
    },

    "clause_6": {
        "label": "Governing Law",
        "position": "delaware",
        "text": (
            "Governing Law: State of Delaware, USA. "
            "Non-negotiable given TechCorp's corporate domicile "
            "and board requirements."
        ),
        "redline": "Delaware, USA",
        "minimum_acceptable": "New York, USA",
        "hard_limit": True,   # juridiction US obligatoire
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# POSITION INITIALE DU SELLER — InnovateSoft Ltd.
#
# Stratégie : défensive, protection de la technologie.
# Le Seller est le détenteur de la technologie → il veut co-ownership.
# Il est prêt à concéder sur la juridiction pour garder l'IP co-owned.
# La durée courte est importante pour lui rester flexible.
# ─────────────────────────────────────────────────────────────────────────────

SELLER_INITIAL_POSITION = {

    "clause_3": {
        "label": "IP Ownership",
        "position": "co-ownership",
        "text": (
            "Jointly developed IP shall be co-owned 50/50 with independent "
            "exploitation rights for each party — no accounting required. "
            "InnovateSoft retains FULL ownership of all improvements and "
            "derivatives of its pre-existing technology."
        ),
        "redline": "50/50 co-ownership, independent exploitation",
        "minimum_acceptable": "40/60 split (Seller/Buyer) with exploitation rights",
        "hard_limit": True,   # ne jamais accepter l'ownership exclusif Buyer
    },

    "clause_4": {
        "label": "License Grant",
        "position": "flexible",
        "text": (
            "License to Buyer: non-exclusive only. "
            "InnovateSoft retains full right to license its technology "
            "independently to other clients. License term tied to "
            "Agreement term, not fixed at 90 days."
        ),
        "redline": "non-exclusive, full-term license",
        "minimum_acceptable": "non-exclusive, 1-year minimum term",
        "hard_limit": False,
    },

    "clause_5": {
        "label": "Term",
        "position": "short",
        "text": (
            "Agreement term: 2 years maximum. "
            "Termination notice: 30 days (standard commercial practice)."
        ),
        "redline": "2 years / 30-day notice",
        "minimum_acceptable": "3 years / 45-day notice",
        "hard_limit": False,
    },

    "clause_6": {
        "label": "Governing Law",
        "position": "england",
        "text": (
            "Governing Law: England and Wales. "
            "Neutral common law jurisdiction acceptable to both parties. "
            "Internationally recognised IP enforcement framework."
        ),
        "redline": "England & Wales",
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
    clause = NDA_BASE["clauses"].get(clause_key, {})
    return clause.get("text", "")


def get_buyer_redline(clause_key: str) -> str:
    short_key = clause_key.split("_")[0]
    key = "clause_" + short_key
    return BUYER_INITIAL_POSITION.get(key, {}).get("redline", "")


def get_seller_redline(clause_key: str) -> str:
    short_key = clause_key.split("_")[0]
    key = "clause_" + short_key
    return SELLER_INITIAL_POSITION.get(key, {}).get("redline", "")