import streamlit as st
from src.2_design_contract.models.ports import PortModel
from src.2_design_contract.models.constraints import CornerCaseModel
from src.4_engineering_copilot.copilot_services.hitl_manager import apply_port_override, apply_corner_case_injection


def render_tab_editor():
    contract = st.session_state.get("contract")
    if not contract:
        st.info("No active contract to modify. Load a demo or run an extraction first.")
        return

    st.subheader("✏️ Human-in-the-Loop (HITL) Contract Modification")
    st.caption("Apply manual overrides or add proprietary constraints without corrupting the verified contract.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔌 Add / Override Interface Port")
        with st.form("form_add_port"):
            p_name = st.text_input("Port Name", "dbg_status_flag")
            p_dir = st.selectbox("Direction", ["input", "output", "inout"], index=1)
            p_width = st.text_input("Bit Width", "[0:0]")
            p_clk = st.text_input("Clock Domain", "clk")
            p_pol = st.selectbox("Active Level", ["high", "low", "edge", "n/a"], index=0)
            p_desc = st.text_area("Functional Purpose", "Internal debug error indicator")

            if st.form_submit_button("Inject Port Definition"):
                try:
                    new_port = PortModel(
                        name=p_name,
                        direction=p_dir,
                        width=p_width,
                        clock_domain=p_clk,
                        active_level=p_pol,
                        description=p_desc
                    )
                    st.session_state.contract = apply_port_override(st.session_state.contract, new_port)
                    st.success(f"Port '{p_name}' successfully injected into contract.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Validation failed: {str(e)}")

    with col2:
        st.markdown("#### 🛑 Inject Custom Corner Case & SVA")
        with st.form("form_add_corner"):
            cid = st.text_input("Scenario ID", "CC_MANUAL_01")
            ctitle = st.text_input("Scenario Title", "Simultaneous Flush on Active Burst")
            chazard = st.text_area("Hazard Description", "Flush strobe asserted while transfer is mid-burst")
            cbehavior = st.text_area("Expected Action", "Cleanly abort burst, reset pointers, drop valid")
            csva = st.text_area("SystemVerilog Assertion (SVA)", "property p_flush;\n  @(posedge clk) flush |-> ##1 !valid;\nendproperty\nassert property (p_flush);")

            if st.form_submit_button("Inject Verification Constraint"):
                try:
                    new_cc = CornerCaseModel(
                        scenario_id=cid,
                        title=ctitle,
                        hazard_description=chazard,
                        expected_hardware_behavior=cbehavior,
                        sva_property=csva
                    )
                    st.session_state.contract = apply_corner_case_injection(st.session_state.contract, new_cc)
                    st.success(f"Corner Case '{cid}' injected successfully.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Validation failed: {str(e)}")
