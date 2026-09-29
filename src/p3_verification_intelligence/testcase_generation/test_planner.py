from typing import List, Dict, Any
from src.p2_design_contract.models.contract import HardwareSpecificationContract


def generate_test_plan(contract: HardwareSpecificationContract) -> List[Dict[str, Any]]:
    """Synthesizes a structured verification test plan."""
    test_plan = [
        {
            "test_id": "TEST_001_POWER_ON_RESET",
            "type": "Sanity",
            "description": f"Verify proper reset initialization across all registers in {contract.module_name}.",
            "stimulus": f"Assert {contract.reset_type} reset for 10 cycles, sample output flags for zero states.",
            "pass_criteria": "All status outputs deasserted, zero unknown (X) states."
        }
    ]

    for cc in contract.corner_cases:
        test_plan.append({
            "test_id": f"TEST_CORNER_{cc.scenario_id}",
            "type": "Directed Edge-Case",
            "description": cc.title,
            "stimulus": f"Target scenario: {cc.hazard_description}",
            "pass_criteria": f"Hardware requirement: {cc.expected_hardware_behavior}"
        })

    if contract.protocols:
        test_plan.append({
            "test_id": "TEST_STRESS_BACKPRESSURE",
            "type": "Randomized Stress",
            "description": "Randomized toggle of ready/valid handshakes with zero-delay burst injection.",
            "stimulus": "Continuous transaction bursts with randomized slave stalls.",
            "pass_criteria": "Zero data payload drops, zero protocol handshake violations."
        })

    return test_plan
