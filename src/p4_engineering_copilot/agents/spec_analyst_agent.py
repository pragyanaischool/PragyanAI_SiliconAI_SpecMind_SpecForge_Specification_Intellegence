from src.4_engineering_copilot.agents.state import CopilotState
from src.1_specification_intelligence.interface_extraction.interface_miner import extract_interfaces
from src.1_specification_intelligence.timing_extraction.timing_miner import extract_timing_constraints
from src.1_specification_intelligence.fsm_extraction.fsm_miner import extract_fsm_structures
from src.1_specification_intelligence.corner_case_discovery.hazard_analyzer import discover_corner_cases


def run_spec_analyst_node(state: CopilotState, groq_api_key: str) -> dict:
    """Executes parallel extraction miners across the ingested specification context."""
    text = state.get("rag_context") or state.get("spec_text") or ""

    ports = extract_interfaces(text, groq_api_key)
    timing = extract_timing_constraints(text, groq_api_key)
    fsms = extract_fsm_structures(text, groq_api_key)
    corners = discover_corner_cases(text, groq_api_key)

    return {
        "extracted_ports": [p.model_dump() for p in ports],
        "extracted_timing": timing.model_dump(),
        "extracted_fsms": [f.model_dump() for f in fsms],
        "extracted_corners": [c.model_dump() for c in corners],
        "execution_step": "Spec Extraction Complete"
    }
