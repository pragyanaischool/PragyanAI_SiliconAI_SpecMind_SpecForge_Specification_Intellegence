from typing import List, Dict
from src.p2_design_contract.models.contract import HardwareSpecificationContract


def extract_boundary_scenarios(contract: HardwareSpecificationContract) -> List[Dict[str, str]]:
    """Identifies boundary saturation points and pointer overflow checks."""
    scenarios = []

    for port in contract.ports:
        if "[" in port.width and ":" in port.width:
            try:
                high_bit = int(port.width.replace("[", "").split(":")[0])
                if high_bit >= 1:
                    max_val = hex((1 << (high_bit + 1)) - 1)
                    scenarios.append({
                        "signal": port.name,
                        "boundary_test": f"Test boundary rollover: inject 0x0, {max_val}, and alternating walking 1s.",
                        "expected_action": "No arithmetic saturation failure or unintended latch activation."
                    })
            except ValueError:
                continue

    return scenarios
