"""
AGL - Negotiation Engine
Orchestre la boucle de negociation entre Buyer, Seller et Arbitrator.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

from src.agents.buyer_agent import create_buyer_agent, get_buyer_opening_statement
from src.agents.seller_agent import create_seller_agent
from src.agents.arbitrator import create_arbitrator_agent, parse_arbitrator_status
from src.core.convergence import ConvergenceEvaluator
from src.config import MAX_TURNS, MIN_TURNS, OUTPUT_DIR

logger = logging.getLogger(__name__)


@dataclass
class NegotiationResult:
    """Resultat complet d une session de negociation."""
    session_id: str
    started_at: str
    ended_at: str
    total_turns: int
    termination_reason: str
    final_status: str
    agreed_clauses: dict = field(default_factory=dict)
    negotiation_log: List[dict] = field(default_factory=list)
    convergence_summary: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "total_turns": self.total_turns,
            "termination_reason": self.termination_reason,
            "final_status": self.final_status,
            "agreed_clauses": self.agreed_clauses,
            "convergence_summary": self.convergence_summary,
            "negotiation_log": self.negotiation_log,
        }


class NegotiationEngine:
    """
    Orchestre la boucle Agent vs Agent.

    Flux par tour :
    1. Buyer propose / contre-propose
    2. Seller repond
    3. Arbitrator evalue et resumes
    4. Convergence evaluator verifie si on doit terminer
    5. Repete jusqu a : convergence | flatline | accord | max turns
    """

    def __init__(self):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.started_at = datetime.now().isoformat()

        logger.info("Initialisation des agents...")
        self.buyer = create_buyer_agent()
        self.seller = create_seller_agent()
        self.arbitrator = create_arbitrator_agent()
        self.evaluator = ConvergenceEvaluator()

        self.turn_count = 0
        self.negotiation_log: List[dict] = []
        self.final_status = "ONGOING"
        self.agreed_clauses: dict = {}

        logger.info("Session " + self.session_id + " prete | Max turns : " + str(MAX_TURNS))

    def _log_turn(self, speaker: str, content: str, metadata: Optional[dict] = None) -> None:
        """Enregistre un tour dans le log de negociation."""
        entry = {
            "turn": self.turn_count,
            "timestamp": datetime.now().isoformat(),
            "speaker": speaker,
            "content": content,
        }
        if metadata:
            entry.update(metadata)
        self.negotiation_log.append(entry)
        preview = content[:150].replace("\n", " ")
        logger.info("[Tour " + str(self.turn_count) + "] " + speaker + " : " + preview + "...")

    async def _ask_agent(self, agent, message: str) -> str:
        """Envoie un message a un agent et retourne sa reponse texte."""
        token = CancellationToken()
        response = await agent.on_messages(
            [TextMessage(content=message, source="orchestrator")],
            cancellation_token=token,
        )
        reply = response.chat_message.content
        return reply if isinstance(reply, str) else str(reply)

    async def _run_async(self) -> NegotiationResult:
        """Boucle de negociation asynchrone."""
        logger.info("Demarrage de la negociation AGL...")

        # Tour 0 : Buyer ouvre la negociation
        self.turn_count = 0
        buyer_opening = get_buyer_opening_statement()
        self._log_turn("Buyer_Counsel", buyer_opening)
        self.evaluator.add_turn(0, "Buyer_Counsel", buyer_opening)
        current_buyer_msg = buyer_opening

        # Boucle principale
        for turn in range(1, MAX_TURNS + 1):
            self.turn_count = turn

            # Seller repond
            seller_prompt = (
                "Tour " + str(turn) + " - Position du Buyer :\n\n"
                + current_buyer_msg
                + "\n\nVeuillez fournir votre contre-position."
            )
            seller_reply = await self._ask_agent(self.seller, seller_prompt)
            self._log_turn("Seller_Counsel", seller_reply)
            seller_rec = self.evaluator.add_turn(turn, "Seller_Counsel", seller_reply)

            # Arbitrator evalue apres le Seller
            sim_str = str(round(seller_rec.similarity_to_prev, 4)) if seller_rec.similarity_to_prev is not None else "N/A"
            arb_prompt = (
                "Tour " + str(turn) + " - Echange a evaluer :\n\n"
                "BUYER :\n" + current_buyer_msg + "\n\n"
                "SELLER :\n" + seller_reply + "\n\n"
                "Stabilite position Seller (similarite cosinus) : " + sim_str + "\n\n"
                "Fournissez votre resume d arbitrage."
            )
            arb_reply = await self._ask_agent(self.arbitrator, arb_prompt)
            self._log_turn("Arbitrator", arb_reply)
            arb_status = parse_arbitrator_status(arb_reply)

            if arb_status["terminated"]:
                self.final_status = arb_status["status"]
                logger.info("Arbitrator declare : " + self.final_status)
                break

            if self.evaluator.should_terminate and turn >= MIN_TURNS:
                self.final_status = self.evaluator.termination_reason
                logger.info("Convergence : " + self.final_status)
                break

            # Buyer contre-propose
            buyer_prompt = (
                "Tour " + str(turn) + " - Contre-position du Seller :\n\n"
                + seller_reply + "\n\n"
                "Note Arbitrator :\n" + arb_reply + "\n\n"
                "Fournissez votre reponse."
            )
            buyer_reply = await self._ask_agent(self.buyer, buyer_prompt)
            current_buyer_msg = buyer_reply
            self._log_turn("Buyer_Counsel", buyer_reply)
            self.evaluator.add_turn(turn, "Buyer_Counsel", buyer_reply)

            if self.evaluator.should_terminate and turn >= MIN_TURNS:
                self.final_status = self.evaluator.termination_reason
                logger.info("Convergence : " + self.final_status)
                break

        else:
            self.final_status = "MAX_TURNS_REACHED"
            logger.warning("Max turns atteint sans convergence.")

        # Construction du resultat
        result = NegotiationResult(
            session_id=self.session_id,
            started_at=self.started_at,
            ended_at=datetime.now().isoformat(),
            total_turns=self.turn_count,
            termination_reason=self.evaluator.termination_reason,
            final_status=self.final_status,
            agreed_clauses=self.agreed_clauses,
            negotiation_log=self.negotiation_log,
            convergence_summary=self.evaluator.get_summary(),
        )

        # Export JSON
        log_path = os.path.join(OUTPUT_DIR, "negotiation_" + self.session_id + ".json")
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
        logger.info("Log exporte : " + log_path)

        return result

    def run(self) -> NegotiationResult:
        """Point d entree synchrone - encapsule la boucle async."""
        return asyncio.run(self._run_async())
