from typing import List
from src.2_design_contract.models.contract import HardwareSpecificationContract


def review_contract_rules(contract: HardwareSpecificationContract) -> List[str]:
    """Reviews the HardwareSpecificationContract against standard tapeout rules."""
    notes = []

    if not contract.ports:
        notes.append("WARNING: Contract contains zero ports.")

    if not contract.corner_cases:
        notes.append("WARNING: No critical corner cases or SVAs generated.")

    if contract.timing.fmax_mhz and contract.timing.fmax_mhz > 500:
        notes.append("STA NOTICE: Fmax exceeds 500 MHz. Multicycle/retiming considerations recommended.")

    return notes
