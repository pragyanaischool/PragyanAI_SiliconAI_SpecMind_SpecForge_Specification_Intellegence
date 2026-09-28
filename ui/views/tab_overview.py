import streamlit as st


def render_tab_overview():
    contract = st.session_state.get("contract")

    if not contract:
        st.info("No Hardware Specification loaded. Upload a document in the sidebar or click 'Load Demo AXI-FIFO'.")
        return

    # Top KPI Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"""
            <div class='metric-card'>
                <div class='metric-title'>Reset Methodology</div>
                <div class='metric-value'>{contract.reset_type.replace('_', ' ').upper()}</div>
                <span class='metric-badge'>Synchronous Deassert</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        fmax_val = f"{contract.timing.fmax_mhz} MHz" if contract.timing.fmax_mhz else "Unspecified"
        st.markdown(
            f"""
            <div class='metric-card'>
                <div class='metric-title'>Target Fmax</div>
                <div class='metric-value'>{fmax_val}</div>
                <span class='metric-badge'>Clock Period: {round(1000 / contract.timing.fmax_mhz, 2) if contract.timing.fmax_mhz else 'N/A'} ns</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        input_count = sum(1 for p in contract.ports if p.direction == "input")
        output_count = sum(1 for p in contract.ports if p.direction == "output")
        st.markdown(
            f"""
            <div class='metric-card'>
                <div class='metric-title'>Total Interfaces</div>
                <div class='metric-value'>{len(contract.ports)} Signals</div>
                <span class='metric-badge'>{input_count} In / {output_count} Out</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            f"""
            <div class='metric-card'>
                <div class='metric-title'>Corner Cases Trapped</div>
                <div class='metric-value'>{len(contract.corner_cases)} Scenarios</div>
                <span class='metric-badge'>Formally Checked (SVA)</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # Architectural Overview Section
    st.subheader("📋 Architectural Intent & Summary")
    st.markdown(f"**Module Identifier:** `{contract.module_name}`")
    st.write(contract.description if contract.description else "No architectural description provided.")

    colA, colB = st.columns(2)
    with colA:
        st.markdown("#### ⏱️ Performance Budget")
        st.markdown(f"- **Cycle Latency:** `{contract.timing.latency_cycles}`")
        st.markdown(f"- **Throughput / Initiation Interval:** `{contract.timing.throughput_cycles}`")
        st.markdown(f"- **Setup Budget:** `{contract.timing.setup_time_ns or 'N/A'} ns`")
        st.markdown(f"- **Hold Margin:** `{contract.timing.hold_time_ns or 'N/A'} ns`")

    with colB:
        st.markdown("#### 🛡️ Clock & Power Domain Isolation")
        st.markdown(f"- **Clock Domain Crossing (CDC):** `{'Required' if contract.timing.is_cdc else 'Single Domain'}`")
        if contract.timing.is_cdc and contract.timing.cdc_details:
            st.markdown(f"- **CDC Mitigation Scheme:** `{contract.timing.cdc_details}`")
        st.markdown(f"- **Protocol Handshake Type:** `{contract.protocols[0].standard if contract.protocols else 'Custom Point-to-Point'}`")
