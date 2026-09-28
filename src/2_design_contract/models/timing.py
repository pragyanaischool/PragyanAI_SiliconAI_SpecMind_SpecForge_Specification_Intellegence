from typing import Optional
from pydantic import BaseModel, Field


class TimingModel(BaseModel):
    fmax_mhz: Optional[float] = Field(default=200.0, description="Maximum operating frequency in MHz")
    setup_time_ns: Optional[float] = Field(default=0.5, description="Setup timing budget in nanoseconds")
    hold_time_ns: Optional[float] = Field(default=0.2, description="Hold timing margin in nanoseconds")
    latency_cycles: str = Field(default="1", description="Input-to-output cycle latency")
    throughput_cycles: str = Field(default="1 cycle", description="Transaction throughput rate")
    is_cdc: bool = Field(default=False, description="Module contains asynchronous clock crossings")
    cdc_details: Optional[str] = Field(default=None, description="CDC mitigation synchronization topology")
