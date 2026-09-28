from typing import Literal
from src.4_engineering_copilot.agents.state import CopilotState


def route_next_action(state: CopilotState) -> Literal["synthesize", "hitl_hold", "finalize"]:
    """Determines subsequent agent node transitions."""
    if state.get("conflicts_detected"):
        return "hitl_hold"
    if not state.get("contract"):
        return "synthesize"
    return "finalize"
