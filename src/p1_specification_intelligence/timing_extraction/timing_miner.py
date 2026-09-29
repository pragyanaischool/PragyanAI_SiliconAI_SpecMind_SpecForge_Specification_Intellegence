from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from src.2_design_contract.models.timing import TimingModel


def extract_timing_constraints(
    spec_text: str,
    groq_api_key: str,
    model_name: str = "llama-3.3-70b-versatile"
) -> TimingModel:
    """Extracts clock operating frequencies, setup/hold margins, and CDC requirements."""
    llm = ChatGroq(model_name=model_name, groq_api_key=groq_api_key, temperature=0.0)
    structured_llm = llm.with_structured_output(TimingModel)

    system_prompt = (
        "You are a Principal Static Timing Analysis (STA) and Clock Domain Crossing (CDC) Architect. "
        "Extract Fmax, setup/hold constraints, cycle latencies, and clock domain crossing schemes."
    )

    try:
        res = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Specification:\n{spec_text}")
        ])
        return res if isinstance(res, TimingModel) else TimingModel(latency_cycles="1", throughput_cycles="1")
    except Exception:
        return TimingModel(latency_cycles="1", throughput_cycles="1")
