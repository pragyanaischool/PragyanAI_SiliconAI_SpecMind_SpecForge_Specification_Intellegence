import streamlit as st
import pandas as pd


def render_tab_contract():
    contract = st.session_state.get("contract")
    if not contract:
        st.info("No active contract loaded. Please synthesize or load a demo contract first.")
        return

    st.subheader(f"🔌 Physical Interface Definitions: `{contract.module_name}`")

    # 1. Port Interface Grid
    port_records = [
        {
            "Name": p.name,
            "Direction": p.direction.upper(),
            "Bit Width": p.width,
            "Domain": p.clock_domain,
            "Active Level": p.active_level,
            "Functional Description": p.description or "-"
        }
        for p in contract.ports
    ]
    st.dataframe(pd.DataFrame(port_records), use_container_width=True, hide_index=True)

    st.markdown("---")

    # 2. Finite State Machine Visualization
    st.subheader("🔄 Control-Path Finite State Machines (FSM)")
    if not contract.fsms:
        st.info("This block contains no sequential FSMs (pure datapath or pipeline architecture).")
        return

    for fsm in contract.fsms:
        st.markdown(f"#### FSM: `{fsm.name}` (Encoding: `{fsm.encoding}`) | Reset: `{fsm.reset_state}`")
        st.write(f"**Identified States:** `{'`, `'.join(fsm.states)}`")

        # Graphviz state-transition visualizer
        try:
            dot_lines = [
                "digraph FSM {",
                '  bgcolor="#0B132B";',
                '  node [shape=circle, fontname="JetBrains Mono", style=filled, fillcolor="#0F172A", fontcolor="#00F2FE", color="#00F2FE"];',
                '  edge [fontname="JetBrains Mono", fontcolor="#94A3B8", color="#38BDF8"];'
            ]
            for t in fsm.transitions:
                dot_lines.append(f'  "{t.from_state}" -> "{t.to_state}" [label="{t.condition}"];')
            dot_lines.append("}")
            st.graphviz_chart("\n".join(dot_lines))
        except Exception:
            # Fallback table if Graphviz runtime unavailable
            t_data = [{"From": t.from_state, "To": t.to_state, "Condition": t.condition} for t in fsm.transitions]
            st.dataframe(pd.DataFrame(t_data), use_container_width=True, hide_index=True)
