import streamlit as st
from src.export.json_exporter import export_contract_to_json
from src.export.mas_doc_generator import generate_mas_markdown
from src.export.sva_bind_exporter import export_sva_module
from src.export.rtm_csv_exporter import export_rtm_to_csv


def render_tab_export():
    contract = st.session_state.get("contract")
    if not contract:
        st.info("No active contract to export.")
        return

    st.subheader("💾 Export Specification & Verification Artifacts")
    st.caption("Generate immutable machine-readable manifests and synthesizable formal modules with one click.")

    col1, col2, col3, col4 = st.columns(4)

    # 1. JSON Contract
    with col1:
        st.markdown("#### 1. JSON Contract")
        json_data = export_contract_to_json(contract)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name=f"{contract.module_name}_contract.json",
            mime="application/json",
            use_container_width=True
        )

    # 2. Markdown MAS Doc
    with col2:
        st.markdown("#### 2. MAS Spec (.md)")
        md_data = generate_mas_markdown(contract)
        st.download_button(
            label="📄 Download MAS",
            data=md_data,
            file_name=f"{contract.module_name}_spec.md",
            mime="text/markdown",
            use_container_width=True
        )

    # 3. SystemVerilog SVA Module
    with col3:
        st.markdown("#### 3. SVA Bind (.sv)")
        sva_data = export_sva_module(contract)
        st.download_button(
            label="🛡️ Download SVA",
            data=sva_data,
            file_name=f"{contract.module_name}_sva.sv",
            mime="text/plain",
            use_container_width=True
        )

    # 4. RTM Matrix (.csv)
    with col4:
        st.markdown("#### 4. RTM Matrix (.csv)")
        reqs = st.session_state.get("requirements", [])
        rtm_data = export_rtm_to_csv(contract, reqs)
        st.download_button(
            label="📊 Download RTM",
            data=rtm_data,
            file_name=f"{contract.module_name}_RTM.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.markdown("---")
    st.markdown("### 📄 Micro-Architecture Specification Live Preview")
    st.markdown(md_data)
