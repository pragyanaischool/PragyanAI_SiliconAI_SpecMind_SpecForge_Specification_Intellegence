import pytest
from unittest.mock import MagicMock, patch
from src.p4_engineering_copilot.agents.state import CopilotState
from src.p4_engineering_copilot.agents.contract_synthesizer import run_contract_synthesizer_node
from src.p4_engineering_copilot.agents.router import route_next_action
from src.p4_engineering_copilot.copilot_services.conflict_detector import audit_specification_conflicts
from src.p4_engineering_copilot.copilot_services.hitl_manager import apply_port_override, apply_corner_case_injection
from src.p2_design_contract.models.contract import HardwareSpecificationContract
from src.p2_design_contract.models.ports import PortModel
from src.p2_design_contract.models.timing import TimingModel
from src.p2_design_contract.models.constraints import CornerCaseModel


def test_contract_synthesizer_node():
    state: CopilotState = {
        "rag_context": "",
        "user_query": "Extract axi_fifo_module specification",
        "spec_text": "Sample text",
        "extracted_ports": [
            {"name": "aclk", "direction": "input", "width": "[0:0]", "clock_domain": "aclk", "active_level": "edge", "description": "Clock"},
            {"name": "s_valid", "direction": "input", "width": "[0:0]", "clock_domain": "aclk", "active_level": "high", "description": "Valid"}
        ],
        "extracted_timing": {"fmax_mhz": 200.0, "latency_cycles": "1", "throughput_cycles": "1"},
        "extracted_fsms": [],
        "extracted_corners": [],
        "contract": None,
        "review_notes": [],
        "conflicts_detected": [],
        "hitl_overrides": [],
        "execution_step": "Initialized"
    }

    result = run_contract_synthesizer_node(state)

    contract = result.get("contract")
    assert contract is not None
    assert isinstance(contract, HardwareSpecificationContract)
    assert contract.module_name == "axi_fifo_module"
    assert len(contract.ports) == 2
    assert contract.timing.fmax_mhz == 200.0


def test_router_branching():
    # 1. Branch to hitl_hold if conflicts detected
    state_conflicts: CopilotState = {
        "rag_context": "", "user_query": "", "spec_text": "",
        "extracted_ports": [], "extracted_timing": {}, "extracted_fsms": [], "extracted_corners": [],
        "contract": None, "review_notes": [], "conflicts_detected": ["CRITICAL: Duplicate port name"],
        "hitl_overrides": [], "execution_step": ""
    }
    assert route_next_action(state_conflicts) == "hitl_hold"

    # 2. Branch to synthesize if contract is missing
    state_no_contract: CopilotState = {
        "rag_context": "", "user_query": "", "spec_text": "",
        "extracted_ports": [], "extracted_timing": {}, "extracted_fsms": [], "extracted_corners": [],
        "contract": None, "review_notes": [], "conflicts_detected": [],
        "hitl_overrides": [], "execution_step": ""
    }
    assert route_next_action(state_no_contract) == "synthesize"


def test_conflict_detector_polarity_mismatch():
    contract = HardwareSpecificationContract(
        module_name="reset_conflict_mod",
        reset_type="async_low",
        ports=[
            PortModel(name="clk", direction="input", width="[0:0]"),
            PortModel(name="rst_n", direction="input", width="[0:0]", active_level="high")
        ]
    )
    conflicts = audit_specification_conflicts(contract)
    assert len(conflicts) >= 1
    assert "POLARITY CLASH" in conflicts[0]


def test_conflict_detector_cdc_without_two_clocks():
    contract = HardwareSpecificationContract(
        module_name="cdc_fail_mod",
        reset_type="async_low",
        ports=[PortModel(name="clk", direction="input", width="[0:0]")],
        timing=TimingModel(is_cdc=True)
    )
    conflicts = audit_specification_conflicts(contract)
    assert any("CDC INCONSISTENCY" in c for c in conflicts)


def test_hitl_port_override_and_injection():
    contract = HardwareSpecificationContract(
        module_name="override_mod",
        ports=[PortModel(name="clk", direction="input", width="[0:0]")]
    )
    # 1. Inject new port
    new_port = PortModel(name="dbg_strobe", direction="output", width="[0:0]")
    contract = apply_port_override(contract, new_port)
    assert len(contract.ports) == 2
    assert contract.ports[1].name == "dbg_strobe"

    # 2. Override existing port width
    overridden_port = PortModel(name="dbg_strobe", direction="output", width="[7:0]")
    contract = apply_port_override(contract, overridden_port)
    assert len(contract.ports) == 2
    assert contract.ports[1].width == "[7:0]"


def test_hitl_corner_case_injection():
    contract = HardwareSpecificationContract(module_name="corner_mod")
    corner = CornerCaseModel(
        scenario_id="CC_MANUAL_01",
        title="Custom stall",
        hazard_description="Sink drops ready during packet burst",
        expected_hardware_behavior="Hold valid and retain current data",
        sva_property="property p_stall; @(posedge clk) valid && !ready |=> valid; endproperty"
    )
    contract = apply_corner_case_injection(contract, corner)
    assert len(contract.corner_cases) == 1
    assert contract.corner_cases[0].scenario_id == "CC_MANUAL_01"
