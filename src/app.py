"""
AGL - Autonomous Legal Contract Negotiator
Entry point principal du projet.

Usage :
    python src/app.py              # negociation complete
    python src/app.py --dry-run    # validation architecture sans LLM
"""

import argparse
import logging
import os
import sys
from datetime import datetime

from src.config import OUTPUT_DIR, ANTHROPIC_API_KEY

# Configuration du logging
os.makedirs(OUTPUT_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
            os.path.join(
                OUTPUT_DIR,
                "agl_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".log"
            )
        ),
    ],
)
logger = logging.getLogger("AGL")


def run_dry_check() -> None:
    """Valide les imports et l architecture sans appel LLM."""
    logger.info("Dry-run : validation de l architecture...")
    try:
        from src.contracts.nda_template import NDA_BASE, get_disputed_clauses
        from src.agents.buyer_agent import get_buyer_opening_statement
        from src.agents.seller_agent import create_seller_agent
        from src.agents.arbitrator import parse_arbitrator_status
        from src.core.convergence import ConvergenceEvaluator
        from src.core.contract_writer import ContractWriter

        logger.info("Imports OK")
        logger.info("Clauses disputees : " + str(get_disputed_clauses()))
        logger.info("Dry-run PASSE - systeme pret")
        print("")
        print("=" * 55)
        print("  DRY-RUN PASSE - AGL pret a negocier")
        print("=" * 55)
    except ImportError as e:
        logger.error("Import error : " + str(e))
        sys.exit(1)


def run_negotiation() -> None:
    """Lance la negociation complete et genere le DOCX."""
    from src.core.negotiation_engine import NegotiationEngine
    from src.core.contract_writer import ContractWriter

    print("")
    print("=" * 55)
    print("  AGL - Autonomous Legal Contract Negotiator")
    print("  Agent vs Agent Arena | NDA + IP Ownership")
    print("=" * 55)
    print("")

    # Negociation
    engine = NegotiationEngine()
    result = engine.run()

    print("")
    print("=" * 55)
    print("  NEGOCIATION TERMINEE")
    print("  Session  : " + result.session_id)
    print("  Tours    : " + str(result.total_turns))
    print("  Status   : " + result.final_status)
    print("  Raison   : " + result.termination_reason)
    print("=" * 55)

    # Generation DOCX
    writer = ContractWriter(result)
    docx_path = writer.generate()

    # Export metriques convergence
    metrics_path = os.path.join(
        OUTPUT_DIR,
        "convergence_" + result.session_id + ".json"
    )
    engine.evaluator.export_json(metrics_path)

    print("")
    print("Fichiers generes :")
    print("  DOCX     : " + docx_path)
    print("  JSON log : " + os.path.join(OUTPUT_DIR, "negotiation_" + result.session_id + ".json"))
    print("  Metriques: " + metrics_path)
    print("")


def main():
    parser = argparse.ArgumentParser(
        description="AGL - Autonomous Legal Contract Negotiator"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Valide l architecture sans appel LLM"
    )
    args = parser.parse_args()

    if args.dry_run:
        run_dry_check()
    else:
        if not ANTHROPIC_API_KEY:
            logger.error("ANTHROPIC_API_KEY manquante. Verifie ton fichier .env")
            sys.exit(1)
        run_negotiation()


if __name__ == "__main__":
    main()
