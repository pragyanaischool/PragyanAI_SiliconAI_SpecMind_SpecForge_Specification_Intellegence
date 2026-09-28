from langgraph.graph import StateGraph, END
from src.4_engineering_copilot.agents.state import CopilotState
from src.4_engineering_copilot.agents.spec_analyst_agent import run_spec_analyst_node
from src.4_engineering_copilot.agents.contract_synthesizer import run_contract_synthesizer_node
from src.4_engineering_copilot.agents.dv_intelligence_agent import run_dv_intelligence_node


def compile_copilot_graph(groq_api_key: str):
    """Compiles the LangGraph multi-agent execution pipeline."""
    graph = StateGraph(CopilotState)

    def analyst_node(state: CopilotState):
        return run_spec_analyst_node(state, groq_api_key)

    def synthesizer_node(state: CopilotState):
        return run_contract_synthesizer_node(state)

    def dv_node(state: CopilotState):
        return run_dv_intelligence_node(state)

    graph.add_node("spec_analyst", analyst_node)
    graph.add_node("synthesizer", synthesizer_node)
    graph.add_node("dv_intelligence", dv_node)

    graph.set_entry_point("spec_analyst")
    graph.add_edge("spec_analyst", "synthesizer")
    graph.add_edge("synthesizer", "dv_intelligence")
    graph.add_edge("dv_intelligence", END)

    return graph.compile()
