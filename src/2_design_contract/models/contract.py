import json
from typing import List, Literal
from pydantic import BaseModel, Field, model_validator

from .ports import PortModel
from .protocols import ProtocolModel
from .timing import TimingModel
from .fsm import FSMModel
from .constraints import CornerCaseModel


class RTMItem(BaseModel):
    req_id: str
    target_element: str
    description: str


class HardwareSpecificationContract(BaseModel):
    module_name: str = Field(description="Top-level synthesizable RTL module name")
    description: str = Field(default="", description="High-level architectural overview")
    reset_type: Literal["sync_high", "sync_low", "async_high", "async_low"] = "async_low"
    ports: List[PortModel] = Field(default_factory=list)
    protocols: List[ProtocolModel] = Field(default_factory=list)
    timing: TimingModel = Field(default_factory=TimingModel)
    fsms: List[FSMModel] = Field(default_factory=list)
    corner_cases: List[CornerCaseModel] = Field(default_factory=list)
    traceability_records: List[RTMItem] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_clock_presence(self) -> "HardwareSpecificationContract":
        clock_found = any("clk" in p.name.lower() for p in self.ports)
        if self.ports and not clock_found:
            self.ports.insert(
                0,
                PortModel(
                    name="clk",
                    direction="input",
                    width="[0:0]",
                    clock_domain="clk",
                    active_level="edge",
                    description="Default system clock",
                ),
            )
        return self

    def to_json(self, indent: int = 2) -> str:
        return self.model_dump_json(indent=indent)

    @classmethod
    def from_json(cls, json_str: str) -> "HardwareSpecificationContract":
        return cls.model_validate_json(json_str)
