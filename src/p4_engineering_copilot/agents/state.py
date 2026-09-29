from typing import TypedDict, List, Optional
from src.p2_design_contract.models.contract import HardwareSpecificationContract


class CopilotState(TypedDict):
    rag_context: str
    user_query: str
    spec_text: str
    extracted_ports: List[dict]
    extracted_timing: dict
    extracted_fsms: List[dict]
    extracted_corners: List[dict]
    contract: Optional[HardwareSpecificationContract]
    review_notes: List[str]
    conflicts_detected: List[str]
    hitl_overrides: List[dict]
    execution_step: str
