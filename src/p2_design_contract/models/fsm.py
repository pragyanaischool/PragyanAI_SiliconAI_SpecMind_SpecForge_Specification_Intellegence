from typing import List, Literal
from pydantic import BaseModel, Field


class FSMTransitionModel(BaseModel):
    from_state: str = Field(description="Originating FSM state")
    to_state: str = Field(description="Destination FSM state")
    condition: str = Field(description="Boolean logic condition causing the state jump")


class FSMModel(BaseModel):
    name: str = Field(default="MAIN_FSM", description="State machine name")
    encoding: Literal["binary", "one-hot", "gray", "auto"] = "binary"
    states: List[str] = Field(default_factory=list, description="Unique states")
    transitions: List[FSMTransitionModel] = Field(default_factory=list, description="State transition arcs")
    reset_state: str = Field(default="IDLE", description="Default state upon reset assertion")
