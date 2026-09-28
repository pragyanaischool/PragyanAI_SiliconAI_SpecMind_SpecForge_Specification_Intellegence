import streamlit as st
from src.3_verification_intelligence.sva_generation.sva_builder import generate_sva_bind_file
from src.3_verification_intelligence.coverage_recommendations.covergroup_suggester import generate_systemverilog_covergroups


def render_tab_verification():
    contract = st.session_state.get("contract")
    if not contract:
        st.info("No active contract to verify.")
        return

    st.subheader("🛡️ Verification Intelligence & Formal SVA Collateral")

    tab_sva, tab_coverage, tab_plan = st.tabs([
        "Formal SVA Properties",
        "SystemVerilog Covergroups",
        "Verification Plan"
    ])

    with tab_sva:
        st.markdown("#### ⚠️ Identified Corner Cases & Concurrent SVA Bindings")
        if not contract.corner_cases:
            st.warning("No corner cases registered in the contract.")
        else:
            for cc in contract.corner_cases:
                with st.expander(f"🛑 {cc.scenario_id}: {cc.title}"):
                    st.markdown(f"**Hazard Description:** {cc.hazard_description}")
                    st.markdown(f"**Expected Hardware Action:** {cc.expected_hardware_behavior}")
                    st.code(cc.sva_property, language="systemverilog")

            st.markdown("#### Full SystemVerilog Bind Module")
            sva_full_module = generate_sva_bind_file(contract)
            st.code(sva_full_module, language="systemverilog")

    with tab_coverage:
        st.markdown("#### 🎯 Functional Coverage Model")
        cg_code = generate_systemverilog_covergroups(contract)
        st.code(cg_code, language="systemverilog")

    with tab_plan:
        st.markdown("#### 📋 Directed & Stress Verification Checklist")
        st.markdown(f"""
        1. **Smoke / Power-On Reset:** Hold `{contract.reset_type}` for 10 cycles, ensure all internal counters and valid flags initialize to zero.
        2. **Backpressure Stall Test:** Assert and drop valid/ready lines randomly to confirm no pipeline data drops occur.
        3. **Throughput Verification:** Confirm continuous transfers sustain target throughput `{contract.timing.throughput_cycles}` without bubble insertion.
        4. **FSM Illegal State Recovery:** Force illegal binary states via formal engine; assert design restores `{contract.fsms[0].reset_state if contract.fsms else 'IDLE'}` within 1 clock cycle.
        """)
