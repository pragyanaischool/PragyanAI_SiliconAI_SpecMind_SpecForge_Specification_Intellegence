from typing import List, Literal
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage


class AtomicRequirement(BaseModel):
    req_id: str = Field(description="Unique identifier such as REQ_FIFO_001")
    category: Literal["Functional", "Interface", "Timing", "Safety", "Reset", "Protocol"]
    statement: str = Field(description="Strict normative requirement directive")
    verification_criteria: str = Field(description="Method used to prove requirement satisfaction in simulation/formal")


class RequirementList(BaseModel):
    requirements: List[AtomicRequirement] = Field(default_factory=list)


def extract_requirements(
    spec_text: str,
    groq_api_key: str,
    model_name: str = "llama-3.3-70b-versatile"
) -> List[AtomicRequirement]:
    """Isolates atomic, testable requirements from specifications."""
    llm = ChatGroq(model_name=model_name, groq_api_key=groq_api_key, temperature=0.0)
    structured_llm = llm.with_structured_output(RequirementList)

    system_prompt = (
        "You are a Lead Hardware Systems Architect. Extract all atomic, testable "
        "hardware requirements from the technical specification text. Exclude marketing preamble."
    )
    user_prompt = f"Specification Input:\n\"\"\"{spec_text}\"\"\""

    try:
        result = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        return result.requirements if isinstance(result, RequirementList) else []
    except Exception:
        return []
