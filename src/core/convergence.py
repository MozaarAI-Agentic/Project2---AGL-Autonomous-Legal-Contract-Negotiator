"""
AGL - Convergence Evaluator
Mesure la similarite semantique entre les positions successives des agents.
Detecte la convergence (accord) et le flatline (blocage).
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import List, Optional

import numpy as np
from sentence_transformers import SentenceTransformer

from src.config import (
    CONVERGENCE_THRESHOLD,
    FLATLINE_TURNS,
    MIN_TURNS,
    EMBEDDING_MODEL,
)

logger = logging.getLogger(__name__)


@dataclass
class TurnRecord:
    turn_number: int
    speaker: str
    content: str
    embedding: Optional[np.ndarray] = field(default=None, repr=False)
    similarity_to_prev: Optional[float] = None
    delta: Optional[float] = None


class ConvergenceEvaluator:

    def __init__(self):
        logger.info("Chargement du modele : " + EMBEDDING_MODEL)
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.history: List[TurnRecord] = []
        self.flatline_count: int = 0
        self.convergence_reached: bool = False
        self.flatline_triggered: bool = False

    def add_turn(self, turn_number: int, speaker: str, content: str) -> TurnRecord:
        embedding = self.model.encode(content, normalize_embeddings=True)

        record = TurnRecord(
            turn_number=turn_number,
            speaker=speaker,
            content=content,
            embedding=embedding,
        )

        prev = self._get_last_by_speaker(speaker)

        if prev is not None and prev.embedding is not None:
            similarity = float(np.dot(embedding, prev.embedding))
            record.similarity_to_prev = similarity

            if prev.similarity_to_prev is not None:
                record.delta = abs(similarity - prev.similarity_to_prev)

            delta_str = str(round(record.delta, 4)) if record.delta is not None else "N/A"
            logger.info(
                "Tour " + str(turn_number) + " [" + speaker + "] "
                "similarite=" + str(round(similarity, 4)) + " "
                "delta=" + delta_str
            )

        self.history.append(record)
        self._update_state(turn_number)
        return record

    def _get_last_by_speaker(self, speaker: str) -> Optional[TurnRecord]:
        for record in reversed(self.history):
            if record.speaker == speaker:
                return record
        return None

    def _update_state(self, current_turn: int) -> None:
        if current_turn < MIN_TURNS:
            return

        recent = [r for r in self.history if r.similarity_to_prev is not None]
        if len(recent) < 2:
            return

        last_similarity = recent[-1].similarity_to_prev
        if last_similarity is not None and last_similarity >= CONVERGENCE_THRESHOLD:
            self.convergence_reached = True
            logger.info("CONVERGENCE tour " + str(current_turn))
            return

        recent_deltas = [
            r.delta for r in recent[-FLATLINE_TURNS:]
            if r.delta is not None
        ]

        if len(recent_deltas) >= FLATLINE_TURNS:
            if all(d < 0.01 for d in recent_deltas):
                self.flatline_count += 1
                if self.flatline_count >= FLATLINE_TURNS:
                    self.flatline_triggered = True
                    logger.warning("FLATLINE tour " + str(current_turn))
            else:
                self.flatline_count = 0

    @property
    def should_terminate(self) -> bool:
        return self.convergence_reached or self.flatline_triggered

    @property
    def termination_reason(self) -> str:
        if self.convergence_reached:
            return "CONVERGENCE"
        if self.flatline_triggered:
            return "FLATLINE - protection budget tokens"
        return "ONGOING"

    def get_summary(self) -> dict:
        similarities = [
            r.similarity_to_prev for r in self.history
            if r.similarity_to_prev is not None
        ]
        return {
            "total_turns": len(self.history),
            "convergence_reached": self.convergence_reached,
            "flatline_triggered": self.flatline_triggered,
            "termination_reason": self.termination_reason,
            "avg_similarity": float(np.mean(similarities)) if similarities else 0.0,
            "max_similarity": float(np.max(similarities)) if similarities else 0.0,
            "final_similarity": float(similarities[-1]) if similarities else 0.0,
            "turn_by_turn": [
                {
                    "turn": r.turn_number,
                    "speaker": r.speaker,
                    "similarity": r.similarity_to_prev,
                    "delta": r.delta,
                }
                for r in self.history
            ],
        }

    def export_json(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.get_summary(), f, indent=2, default=str)
        logger.info("Metriques exportees : " + path)
