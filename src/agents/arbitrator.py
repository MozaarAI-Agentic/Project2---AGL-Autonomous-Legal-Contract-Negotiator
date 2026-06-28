"""
AGL - Arbitrator Agent
Agent impartial qui gere le turn-loop de la negociation.
Ne prend pas parti. Surveille, resumes, declare accord ou deadlock.
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.anthropic import AnthropicChatCompletionClient

from src.config import ANTHROPIC_API_KEY, CLAUDE_MODEL


ARBITRATOR_SYSTEM_PROMPT = """You are an impartial Legal Arbitrator overseeing a contract
negotiation between Buyer_Counsel (TechCorp) and Seller_Counsel (InnovateSoft).

YOUR ROLE:
==========
You do NOT take sides. You do NOT advocate for either party.
Your sole function is to manage the negotiation process fairly.

YOUR TASKS AFTER EACH EXCHANGE:
1. SUMMARIZE what each party proposed in this turn.
2. IDENTIFY which clauses are moving toward agreement.
3. IDENTIFY which clauses remain blocked.
4. DETECT if positions are repeating without movement (deadlock signal).
5. DECLARE the outcome when conditions are met.

TERMINATION CONDITIONS:
- If all 4 clauses reach tentative agreement: declare AGREEMENT REACHED
- If positions repeat for 3+ turns without movement: declare DEADLOCK
- Always explain your reasoning before declaring either outcome.

RESPONSE FORMAT - always use exactly this structure:
STATUS: [NEGOTIATING / CONVERGING / DEADLOCK / AGREEMENT REACHED]
TURN: [current turn number]
OPEN CLAUSES: [list clauses still disputed]
AGREED CLAUSES: [list clauses with tentative agreement]
ARBITRATOR NOTE: [your impartial observation - 2-3 sentences]
NEXT SPEAKER: [Buyer_Counsel or Seller_Counsel]

You have no financial interest in the outcome.
Your only goal is a fair and efficient process.
"""


def create_arbitrator_agent() -> AssistantAgent:
    """Cree et retourne l agent Arbitrator configure."""
    client = AnthropicChatCompletionClient(
        model=CLAUDE_MODEL,
        api_key=ANTHROPIC_API_KEY,
        temperature=0.2,
    )
    return AssistantAgent(
        name="Arbitrator",
        model_client=client,
        system_message=ARBITRATOR_SYSTEM_PROMPT,
        description="Impartial arbitrator managing the negotiation process.",
    )


def parse_arbitrator_status(message: str) -> dict:
    """
    Parse la sortie de l Arbitrator pour extraire le statut structure.
    Utilise par le NegotiationEngine pour detecter la terminaison.

    Retourne un dict avec :
    - status     : NEGOTIATING / CONVERGING / DEADLOCK / AGREEMENT REACHED
    - turn       : numero du tour courant
    - terminated : True si negociation terminee
    """
    status = {
        "status": "NEGOTIATING",
        "turn": 0,
        "terminated": False,
    }

    lines = message.upper().split("\n")
    for line in lines:
        line = line.strip()

        if line.startswith("STATUS:"):
            raw = line.replace("STATUS:", "").strip()
            status["status"] = raw
            if "AGREEMENT REACHED" in raw or "DEADLOCK" in raw:
                status["terminated"] = True

        elif line.startswith("TURN:"):
            raw = line.replace("TURN:", "").strip()
            digits = "".join(c for c in raw if c.isdigit())
            if digits:
                status["turn"] = int(digits)

    return status
