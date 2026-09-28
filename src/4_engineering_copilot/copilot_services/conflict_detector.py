from typing import List
from src.2_design_contract.models.contract import HardwareSpecificationContract


def audit_specification_conflicts(contract: HardwareSpecificationContract) -> List[str]:
    """Inspects the assembled contract for architectural contradictions and polarity mismatches."""
    conflicts = []

    port_names = [p.name for p in contract.ports]
    if len(port_names) != len(set(port_names)):
        conflicts.append("CRITICAL: Duplicate port identifiers discovered in signal interface list.")

    reset_ports = [p for p in contract.ports if "rst" in p.name.lower() or "reset" in p.name.lower()]
    for rp in reset_ports:
        if "low" in contract.reset_type and rp.active_level == "high":
            conflicts.append(
                f"POLARITY CLASH: Contract reset_type is '{contract.reset_type}', "
                f"but port '{rp.name}' has active_level='high'."
            )

    if contract.timing.is_cdc:
        clock_ports = [p for p in contract.ports if "clk" in p.name.lower()]
        if len(clock_ports) < 2:
            conflicts.append(
                "CDC INCONSISTENCY: Module is flagged as Clock Domain Crossing (CDC), "
                "but fewer than 2 clock signals exist."
            )

    return conflicts
