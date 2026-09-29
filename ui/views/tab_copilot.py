import streamlit as st
from src.p4_engineering_copilot.agents.workflow import compile_copilot_graph
from src.p4_engineering_copilot.copilot_services.spec_qa import answer_spec_question
from src.p4_engineering_copilot.copilot_services.conflict_detector import audit_specification_conflicts


def render_tab_copilot():
    st.subheader("🤖 Hardware Engineering Multi-Agent Copilot")
    st.caption("Coordinate the Spec Analyst, STA Architect, and DV Agents with grounded document retrieval.")

    chat_col, right_col = st.columns([3, 2])

    with right_col:
        st.markdown("#### 📡 Agent Execution Telemetry")
        log_box = st.empty()
        log_box.info("Agent cluster idle. Submit a query below to trigger multi-agent analysis.")

        if st.session_state.get("contract"):
            conflicts = audit_specification_conflicts(st.session_state.contract)
            if conflicts:
                st.markdown("#### ⚠️ Conflict & Polarity Alerts")
                for c in conflicts:
                    st.markdown(f"<div class='conflict-box'>{c}</div>", unsafe_allow_html=True)

    with chat_col:
        # Display conversation history
        for msg in st.session_state.get("chat_history", []):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("E.g., Extract full hardware contract for an AXI4-Stream FIFO...")

        if user_input:
            api_key = st.session_state.get("groq_api_key")
            if not api_key:
                st.error("Please supply a valid Groq API Key in the sidebar.")
                return

            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            # RAG Context Retrieval
            rag_context = ""
            if st.session_state.get("vectorstore"):
                retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 4})
                retrieved_chunks = retriever.invoke(user_input)
                rag_context = "\n\n".join([c.page_content for c in retrieved_chunks])

            # Determine if this is a general Q&A or a synthesis/extraction command
            is_extraction = any(w in user_input.lower() for w in ["extract", "contract", "synthesize", "generate", "deconstruct"])

            if is_extraction:
                with right_col:
                    with st.status("Executing Multi-Agent StateGraph...", expanded=True) as status_box:
                        graph = compile_copilot_graph(api_key)
                        initial_state = {
                            "rag_context": rag_context,
                            "user_query": user_input,
                            "spec_text": rag_context[:3000],
                            "extracted_ports": [],
                            "extracted_timing": {},
                            "extracted_fsms": [],
                            "extracted_corners": [],
                            "contract": None,
                            "review_notes": [],
                            "conflicts_detected": [],
                            "hitl_overrides": [],
                            "execution_step": "Initialized"
                        }

                        for step in graph.stream(initial_state):
                            for node_name, updates in step.items():
                                if node_name == "spec_analyst":
                                    st.markdown("<div class='agent-pill'>🔌 <b>Spec Analyst:</b> Mined ports, widths & timing limits.</div>", unsafe_allow_html=True)
                                elif node_name == "synthesizer":
                                    st.markdown("<div class='agent-pill'>📦 <b>Synthesizer:</b> Reconciled Pydantic contract.</div>", unsafe_allow_html=True)
                                    if updates.get("contract"):
                                        st.session_state.contract = updates["contract"]
                                elif node_name == "dv_intelligence":
                                    st.markdown("<div class='agent-pill'>🛡️ <b>DV Lead:</b> Compiled SVAs & coverage model.</div>", unsafe_allow_html=True)

                        status_box.update(label="Hardware Contract Synthesized!", state="complete")

                response_text = f"Hardware contract synthesized for **{st.session_state.contract.module_name}**. Inspect the contract in the **Ports & FSMs** or **Verification** tabs."
            else:
                # Direct Grounded Q&A
                context_source = rag_context if rag_context else (st.session_state.contract.to_json() if st.session_state.get("contract") else "No context available.")
                response_text = answer_spec_question(user_input, context_source, api_key)

            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
            with st.chat_message("assistant"):
                st.markdown(response_text)
