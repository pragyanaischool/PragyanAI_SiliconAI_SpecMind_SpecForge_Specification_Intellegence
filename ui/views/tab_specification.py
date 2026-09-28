import streamlit as st
import pandas as pd
from src.2_design_contract.traceability.rtm_matrix import generate_traceability_matrix


def render_tab_specification():
    st.subheader("📑 Specification Ingestion & Traceability Matrix (RTM)")
    
    contract = st.session_state.get("contract")
    requirements = st.session_state.get("requirements", [])

    if not contract:
        st.info("Ingest documents or load a reference contract to inspect traceability.")
        return

    st.markdown("#### 🔍 Automated Requirement Tracing")
    if requirements:
        rtm_df = generate_traceability_matrix(contract, requirements)
        st.dataframe(rtm_df, use_container_width=True, hide_index=True)
    else:
        st.warning("No explicit atomic requirements stored in session. Requirements are automatically extracted during document upload.")
        
        # Display extracted functional items mapped to ports
        st.markdown("#### Signal Trace Summary")
        trace_data = [
            {
                "Signal": p.name,
                "Width": p.width,
                "Domain": p.clock_domain,
                "Active Level": p.active_level,
                "Design Role": p.description or "General functional interface"
            }
            for p in contract.ports
        ]
        st.dataframe(pd.DataFrame(trace_data), use_container_width=True, hide_index=True)
