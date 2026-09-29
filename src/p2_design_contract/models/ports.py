import re
from typing import Literal
from pydantic import BaseModel, Field, field_validator


class PortModel(BaseModel):
    name: str = Field(description="Signal identifier (e.g., s_axis_tdata)")
    direction: Literal["input", "output", "inout"] = Field(description="Signal port direction")
    width: str = Field(default="[0:0]", description="Verilog bit width slice notation, e.g. [31:0] or [0:0]")
    clock_domain: str = Field(default="clk", description="Primary clock domain name")
    active_level: Literal["high", "low", "edge", "n/a"] = Field(default="high")
    description: str = Field(default="", description="Functional purpose of the signal")

    @field_validator("name")
    @classmethod
    def validate_identifier(cls, v: str) -> str:
        clean = v.strip()
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_$]*$", clean):
            raise ValueError(f"Invalid Verilog signal identifier: '{clean}'")
        return clean

    @field_validator("width")
    @classmethod
    def validate_verilog_width(cls, v: str) -> str:
        clean = v.strip().replace(" ", "")
        if not clean.startswith("[") or not clean.endswith("]"):
            clean = f"[{clean}]" if ":" in clean else f"[{clean}:0]"
        return clean
