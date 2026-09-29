from src.p2_design_contract.models.contract import HardwareSpecificationContract


def export_contract_to_json(contract: HardwareSpecificationContract) -> str:
    """Serializes the hardware contract to formatted JSON."""
    return contract.to_json(indent=2)
