import os
import tempfile
import streamlit as st

from src.utils.session_manager import init_session_state
from src.utils.demo_loader import load_demo_contract
from src.p1_specification_intelligence.doc_understanding.pdf_table_parser import parse_pdf_with_tables
from src.p1_specification_intelligence.doc_understanding.text_normalizer import normalize_spec_text
from src.p1_specification_intelligence.req_extraction.requirement_miner import extract_requirements
from src.rag.chunker import chunk_spec_document
from src.rag.vector_store import build_spec_vectorstore

from ui.views.tab_overview import render_tab_overview
from ui.views.tab_specification import render_tab_specification
from ui.views.tab_contract import render_tab_contract
from ui.views.tab_verification import render_tab_verification
from ui.views.tab_copilot import render_tab_copilot
from ui.views.tab_editor import render_tab_editor
from ui.views.tab_export import render_tab_export

# 1. Page Configuration
st.set_page_config(
    page_title="PragyanAI-SpecForge | Hardware Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Custom EDA Dark Theme
css_path = os.path.join(os.path.dirname(__file__), "ui", "styles", "custom.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 3. Initialize State
init_session_state()

# 4. Header Bar
header_left, header_right = st.columns([3, 1])
with header_left:
    st.markdown(
        """
        <div style='display: flex; align-items: center; gap: 12px;'>
            <div style='background: rgba(0, 242, 254, 0.15); border: 1px solid #00F2FE; border-radius: 8px; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; color: #00F2FE; font-size: 20px;'>⚡</div>
            <div>
                <h2 style='margin: 0; padding: 0; font-size: 1.5rem; font-weight: 800; letter-spacing: 0.05em;'>
                    PRAGYANAI <span style='color: #00F2FE;'>SPECFORGE</span>
                </h2>
                <p style='margin: 0; color: #94A3B8; font-size: 0.8rem;'>
                    Autonomous Hardware Specification Intelligence & Design Contract Studio
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
with header_right:
    contract = st.session_state.get("contract")
    if contract:
        st.markdown(
            f"""
            <div style='text-align: right; padding-top: 6px;'>
                <span class='metric-badge' style='font-size: 0.8rem; padding: 4px 10px;'>
                    Active Block: <b>{contract.module_name}</b>
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<hr style='border: 0; border-top: 1px solid #1E293B; margin: 14px 0 20px 0;'/>", unsafe_allow_html=True)

# 5. Sidebar Controls & Ingestion
with st.sidebar:
    st.markdown("### ⚙️ Engine Parameters")
    api_key_input = st.text_input(
        "Groq API Key",
        type="password",
        value=st.session_state.get("groq_api_key", os.environ.get("GROQ_API_KEY", "")),
        help="Inference engine key for Llama-3.3-70B analytical reasoning."
    )
    if api_key_input:
        st.session_state.groq_api_key = api_key_input

    st.markdown("<hr style='border: 0; border-top: 1px solid #1E293B; margin: 12px 0;'/>", unsafe_allow_html=True)
    st.markdown("### 📄 Datasheet / Spec Ingestion")

    uploaded_files = st.file_uploader(
        "Upload Hardware Docs",
        type=["pdf", "docx", "txt", "md"],
        accept_multiple_files=True,
        help="Select protocol sheets, architectural register tables, or interface docs."
    )

    if st.button("⚡ Index Specs to Knowledge Base", use_container_width=True, disabled=not uploaded_files):
        with st.status("Ingesting & Vectorizing Specification Chunks...", expanded=True) as status_box:
            all_text = []
            for up_file in uploaded_files:
                ext = os.path.splitext(up_file.name)[-1].lower()
                with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                    tmp.write(up_file.read())
                    tmp_path = tmp.name

                try:
                    if ext == ".pdf":
                        raw_text = parse_pdf_with_tables(tmp_path)
                    else:
                        with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                            raw_text = f.read()

                    clean_text = normalize_spec_text(raw_text)
                    all_text.append(clean_text)
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)

            full_spec_corpus = "\n\n".join(all_text)
            chunks = chunk_spec_document(full_spec_corpus)
            st.session_state.vectorstore = build_spec_vectorstore(chunks, persist_dir="./.chroma_db")

            active_key = st.session_state.get("groq_api_key")
            if active_key:
                st.write("Extracting atomic normative requirements...")
                st.session_state.requirements = extract_requirements(full_spec_corpus[:6000], active_key)

            status_box.update(label="Specification Knowledge Base Ready!", state="complete")
        st.toast(f"Successfully indexed {len(chunks)} chunks!", icon="🚀")

    st.markdown("<hr style='border: 0; border-top: 1px solid #1E293B; margin: 12px 0;'/>", unsafe_allow_html=True)
    if st.button("🧪 Load Golden AXI4-Stream Demo", use_container_width=True):
        st.session_state.contract = load_demo_contract()
        st.rerun()

# 6. Primary View Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📐 Overview",
    "📑 Traceability (RTM)",
    "🔌 Ports & FSMs",
    "🛡️ Verification & SVA",
    "🤖 Multi-Agent Copilot",
    "✏️ HITL Editor",
    "💾 Export Studio"
])

with tab1:
    render_tab_overview()
with tab2:
    render_tab_specification()
with tab3:
    render_tab_contract()
with tab4:
    render_tab_verification()
with tab5:
    render_tab_copilot()
with tab6:
    render_tab_editor()
with tab7:
    render_tab_export()
