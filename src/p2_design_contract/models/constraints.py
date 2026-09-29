from pydantic import BaseModel, Field


class CornerCaseModel(BaseModel):
    scenario_id: str = Field(description="Unique scenario code (e.g. CC_AXIS_01)")
    title: str = Field(description="Concise description of the edge case")
    hazard_description: str = Field(description="Detailed physical or logical failure mechanism")
    expected_hardware_behavior: str = Field(description="Exact RTL response required to prevent data loss or lockup")
    sva_property: str = Field(description="SystemVerilog Assertion (SVA) checking this property")
