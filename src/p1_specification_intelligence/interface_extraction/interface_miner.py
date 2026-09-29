from typing import List
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from src.2_design_contract.models.ports import PortModel


class PortContainer(BaseModel):
    ports: List[PortModel] = Field(default_factory=list)


def extract_interfaces(
    spec_text: str,
    groq_api_key: str,
    model_name: str = "llama-3.3-70b-versatile"
) -> List[PortModel]:
    """Extracts hardware interface signals, directions, widths, and clock affiliations."""
    llm = ChatGroq(model_name=model_name, groq_api_key=groq_api_key, temperature=0.0)
    structured_llm = llm.with_structured_output(PortContainer)

    system_prompt = (
        "You are an ASIC Pinout and Interface Specialist. Deconstruct all hardware interface signals, "
        "busses, clock ports, and resets from the text. Assign explicit Verilog bit widths (e.g. [31:0] "
        "or [0:0]) and active polarity levels."
    )

    try:
        res = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Datasheet Excerpt:\n{spec_text}")
        ])
        return res.ports if isinstance(res, PortContainer) else []
    except Exception:
        return []
