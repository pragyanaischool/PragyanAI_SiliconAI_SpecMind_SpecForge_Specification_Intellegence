from src.p4_engineering_copilot.agents.state import CopilotState
from src.p2_design_contract.models.contract import HardwareSpecificationContract
from src.p2_design_contract.models.ports import PortModel
from src.p2_design_contract.models.timing import TimingModel
from src.p2_design_contract.models.fsm import FSMModel
from src.p2_design_contract.models.constraints import CornerCaseModel


def run_contract_synthesizer_node(state: CopilotState) -> dict:
    """Combines mined parameters into a validated Pydantic HardwareSpecificationContract."""
    ports = [PortModel(**p) for p in state.get("extracted_ports", [])]
    timing = TimingModel(**state.get("extracted_timing", {}))
    fsms = [FSMModel(**f) for f in state.get("extracted_fsms", [])]
    corners = [CornerCaseModel(**c) for c in state.get("extracted_corners", [])]

    module_name = "synthesized_hardware_block"
    for term in state.get("user_query", "").split():
        if "_" in term and term.islower():
            module_name = term
            break

    contract = HardwareSpecificationContract(
        module_name=module_name,
        description=f"Synthesized hardware architecture for {module_name}",
        reset_type="async_low",
        ports=ports,
        timing=timing,
        fsms=fsms,
        corner_cases=corners
    )

    return {
        "contract": contract,
        "execution_step": "Contract Synthesized"
    }
