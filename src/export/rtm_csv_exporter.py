import io
from src.p2_design_contract.models.contract import HardwareSpecificationContract
from src.p2_design_contract.traceability.rtm_matrix import generate_traceability_matrix


def export_rtm_to_csv(contract: HardwareSpecificationContract, reqs: list) -> str:
    """Exports the requirements traceability matrix as CSV text."""
    df = generate_traceability_matrix(contract, reqs)
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue()
