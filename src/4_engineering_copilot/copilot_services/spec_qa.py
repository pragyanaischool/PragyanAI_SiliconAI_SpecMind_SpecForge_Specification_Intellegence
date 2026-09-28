from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage


def answer_spec_question(query: str, context: str, groq_api_key: str) -> str:
    """Answers hardware questions strictly grounded in the ingested specification document."""
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", groq_api_key=groq_api_key, temperature=0.1)

    prompt = f"""You are a Principal Hardware Co-Designer. Answer the user query strictly using the specification context below.
Cite the relevant section or signal table whenever stating facts. If unknown or missing, state that it is not specified.

Specification Context:
\"\"\"{context}\"\"\"

User Question: {query}
"""
    res = llm.invoke([SystemMessage(content=prompt)])
    return str(res.content)
