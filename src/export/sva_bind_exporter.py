from src.2_design_contract.models.contract import HardwareSpecificationContract
from src.3_verification_intelligence.sva_generation.sva_builder import generate_sva_bind_file


def export_sva_module(contract: HardwareSpecificationContract) -> str:
    """Exports synthesizable SystemVerilog Assertion bind code."""
    return generate_sva_bind_file(contract)
