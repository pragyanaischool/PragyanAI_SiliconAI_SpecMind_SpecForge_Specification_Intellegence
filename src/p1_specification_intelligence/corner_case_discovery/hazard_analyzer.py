from typing import List
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from src.2_design_contract.models.constraints import CornerCaseModel


class CornerCaseContainer(BaseModel):
    corner_cases: List[CornerCaseModel] = Field(default_factory=list)


def discover_corner_cases(
    spec_text: str,
    groq_api_key: str,
    model_name: str = "llama-3.3-70b-versatile"
) -> List[CornerCaseModel]:
    """Discovers race conditions, boundary stalls, and protocol edge cases."""
    llm = ChatGroq(model_name=model_name, groq_api_key=groq_api_key, temperature=0.2)
    structured_llm = llm.with_structured_output(CornerCaseContainer)

    system_prompt = (
        "You are a Principal Hardware Verification Architect. Scrutinize the specification for "
        "race conditions, simultaneous read/write collisions at boundaries (full/empty), backpressure stalls, "
        "and unexpected reset assertions during transactions. Formulate a SystemVerilog Assertion (SVA) for each."
    )

    try:
        res = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Specification Excerpt:\n{spec_text}")
        ])
        return res.corner_cases if isinstance(res, CornerCaseContainer) else []
    except Exception:
        return []
