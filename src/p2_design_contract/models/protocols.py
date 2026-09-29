from typing import Literal, List, Optional
from pydantic import BaseModel, Field


class ProtocolModel(BaseModel):
    standard: Literal["AXI4", "AXI4-Lite", "AXI4-Stream", "APB4", "AHB-Lite", "TileLink", "Custom"]
    role: Literal["master", "slave", "source", "sink", "peer"] = "slave"
    clock_signal: str = "aclk"
    reset_signal: str = "aresetn"
    handshake_type: Literal["ready_valid", "credit_based", "request_grant", "strobe"] = "ready_valid"
    associated_ports: List[str] = Field(default_factory=list)
    description: Optional[str] = None
