from src.4_engineering_copilot.agents.state import CopilotState
from src.3_verification_intelligence.sva_generation.sva_builder import generate_sva_bind_file
from src.3_verification_intelligence.testcase_generation.test_planner import generate_test_plan


def run_dv_intelligence_node(state: CopilotState) -> dict:
    """Compiles formal verification collateral and test plans."""
    contract = state.get("contract")
    if not contract:
        return {"execution_step": "DV Prep Skipped - No Contract"}

    _ = generate_sva_bind_file(contract)
    _ = generate_test_plan(contract)

    return {
        "execution_step": "Verification Intelligence Complete"
    }
