from typing import List
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from src.2_design_contract.models.fsm import FSMModel


class FSMContainer(BaseModel):
    fsms: List[FSMModel] = Field(default_factory=list)


def extract_fsm_structures(
    spec_text: str,
    groq_api_key: str,
    model_name: str = "llama-3.3-70b-versatile"
) -> List[FSMModel]:
    """Reconstructs state machines, transitions, triggers, and encodings."""
    llm = ChatGroq(model_name=model_name, groq_api_key=groq_api_key, temperature=0.0)
    structured_llm = llm.with_structured_output(FSMContainer)

    system_prompt = (
        "You are an ASIC Control Path Architect. Identify all sequential Finite State Machines (FSMs), "
        "their explicit state names, trigger conditions, reset default states, and state transition matrices."
    )

    try:
        res = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Specification:\n{spec_text}")
        ])
        return res.fsms if isinstance(res, FSMContainer) else []
    except Exception:
        return []
