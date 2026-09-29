from src.2_design_contract.models.contract import HardwareSpecificationContract
from src.2_design_contract.models.ports import PortModel
from src.2_design_contract.models.constraints import CornerCaseModel


def apply_port_override(
    contract: HardwareSpecificationContract,
    new_port: PortModel
) -> HardwareSpecificationContract:
    """Safely updates or injects a port definition via Human-in-the-Loop."""
    existing_idx = next((i for i, p in enumerate(contract.ports) if p.name == new_port.name), None)
    if existing_idx is not None:
        contract.ports[existing_idx] = new_port
    else:
        contract.ports.append(new_port)
    return contract


def apply_corner_case_injection(
    contract: HardwareSpecificationContract,
    corner: CornerCaseModel
) -> HardwareSpecificationContract:
    """Injects human-entered corner cases and assertions into the contract."""
    contract.corner_cases.append(corner)
    return contract
