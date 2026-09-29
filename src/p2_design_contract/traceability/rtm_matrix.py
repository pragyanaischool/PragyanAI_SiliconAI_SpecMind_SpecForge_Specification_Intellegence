import pandas as pd
from typing import List
from src.p2_design_contract.models.contract import HardwareSpecificationContract
from src.p1_specification_intelligence.req_extraction.requirement_miner import AtomicRequirement


def generate_traceability_matrix(
    contract: HardwareSpecificationContract,
    requirements: List[AtomicRequirement]
) -> pd.DataFrame:
    """Builds a bidirectional requirements traceability matrix mapping spec directives to hardware elements."""
    records = []

    for req in requirements:
        mapped_targets = []

        for p in contract.ports:
            if p.name.lower() in req.statement.lower():
                mapped_targets.append(f"Port:{p.name}")

        for cc in contract.corner_cases:
            if req.req_id.lower() in cc.scenario_id.lower() or cc.title.lower() in req.statement.lower():
                mapped_targets.append(f"CornerCase:{cc.scenario_id}")

        records.append({
            "Requirement ID": req.req_id,
            "Category": req.category,
            "Requirement Statement": req.statement,
            "Mapped Design Element": ", ".join(mapped_targets) if mapped_targets else "General RTL Architecture",
            "Verification Proof Method": req.verification_criteria
        })

    return pd.DataFrame(records)
