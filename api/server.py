# api/server.py
import os
import shutil
import tempfile
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel

app = FastAPI(
    title="PragyanAI-SpecForge Engine API",
    version="2.0.0",
    description="ASIC Specification Intelligence & Formal Hardware Contract API"
)

FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://pragyanaisiliconaispecmind.netlify.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "https://pragyanaisiliconaispecmind.netlify.app",
        "http://localhost:3000",
        "http://localhost:8501",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CHROMA_DIR = os.environ.get("CHROMA_DIR", "./.chroma_db")
DEFAULT_GROQ_KEY = os.environ.get("GROQ_API_KEY", "")

active_contract = None
vector_store_instance = None
requirements_cache = []


class ChatRequest(BaseModel):
    query: str
    groq_api_key: Optional[str] = None


class ExtractionRequest(BaseModel):
    query: str
    groq_api_key: Optional[str] = None


@app.get("/")
def health_check():
    """Fast healthcheck so Render detects the port immediately."""
    return {
        "status": "online",
        "service": "PragyanAI-SpecForge Engine API",
        "version": "2.0.0",
        "has_contract": active_contract is not None,
        "chroma_dir": CHROMA_DIR
    }


@app.post("/api/spec/demo")
def load_demo():
    global active_contract
    from src.utils.demo_loader import load_demo_contract
    active_contract = load_demo_contract()
    return {"message": "Demo AXI4-Stream FIFO contract loaded", "contract": active_contract}


@app.get("/api/contract")
def get_contract():
    if not active_contract:
        raise HTTPException(status_code=404, detail="No active hardware contract loaded.")
    return active_contract


@app.post("/api/spec/upload")
async def upload_and_index_specs(
    files: List[UploadFile] = File(...),
    groq_api_key: Optional[str] = Form(None)
):
    global vector_store_instance, requirements_cache
    from src.p1_specification_intelligence.doc_understanding.pdf_table_parser import parse_pdf_with_tables
    from src.p1_specification_intelligence.doc_understanding.text_normalizer import normalize_spec_text
    from src.p1_specification_intelligence.req_extraction.requirement_miner import extract_requirements
    from src.rag.chunker import chunk_spec_document
    from src.rag.vector_store import build_spec_vectorstore

    all_text = []
    for file in files:
        ext = os.path.splitext(file.filename)[-1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        try:
            if ext == ".pdf":
                raw_text = parse_pdf_with_tables(tmp_path)
            else:
                with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                    raw_text = f.read()

            normalized = normalize_spec_text(raw_text)
            all_text.append(normalized)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    full_spec = "\n\n".join(all_text)
    chunks = chunk_spec_document(full_spec)
    vector_store_instance = build_spec_vectorstore(chunks, persist_dir=CHROMA_DIR)

    effective_key = groq_api_key or DEFAULT_GROQ_KEY
    if effective_key:
        requirements_cache = extract_requirements(full_spec[:6000], effective_key)

    return {
        "message": f"Successfully ingested {len(files)} files into {len(chunks)} semantic chunks.",
        "requirements_extracted": len(requirements_cache)
    }


@app.post("/api/spec/extract")
def run_extraction(req: ExtractionRequest):
    global active_contract
    from src.p4_engineering_copilot.agents.workflow import compile_copilot_graph
    from src.p4_engineering_copilot.copilot_services.conflict_detector import audit_specification_conflicts

    effective_key = req.groq_api_key or DEFAULT_GROQ_KEY
    if not effective_key:
        raise HTTPException(status_code=400, detail="GROQ_API_KEY is required to trigger extraction.")

    rag_context = ""
    if vector_store_instance:
        retriever = vector_store_instance.as_retriever(search_kwargs={"k": 4})
        docs = retriever.invoke(req.query)
        rag_context = "\n\n".join([d.page_content for d in docs])

    graph = compile_copilot_graph(effective_key)
    initial_state = {
        "rag_context": rag_context,
        "user_query": req.query,
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

    final_state = graph.invoke(initial_state)
    active_contract = final_state.get("contract")

    conflicts = []
    if active_contract:
        conflicts = audit_specification_conflicts(active_contract)

    return {
        "execution_step": final_state.get("execution_step"),
        "conflicts": conflicts,
        "contract": active_contract
    }


@app.post("/api/contract/port")
def add_or_override_port(port: dict):
    global active_contract
    from src.p2_design_contract.models.ports import PortModel
    from src.p4_engineering_copilot.copilot_services.hitl_manager import apply_port_override

    if not active_contract:
        raise HTTPException(status_code=400, detail="Contract not initialized.")
    port_model = PortModel(**port)
    active_contract = apply_port_override(active_contract, port_model)
    return {"message": f"Port '{port_model.name}' updated successfully.", "contract": active_contract}


@app.post("/api/contract/corner-case")
def add_corner_case(corner: dict):
    global active_contract
    from src.p2_design_contract.models.constraints import CornerCaseModel
    from src.p4_engineering_copilot.copilot_services.hitl_manager import apply_corner_case_injection

    if not active_contract:
        raise HTTPException(status_code=400, detail="Contract not initialized.")
    corner_model = CornerCaseModel(**corner)
    active_contract = apply_corner_case_injection(active_contract, corner_model)
    return {"message": f"Corner case '{corner_model.scenario_id}' injected successfully.", "contract": active_contract}


@app.post("/api/copilot/chat")
def chat_copilot(req: ChatRequest):
    from src.p4_engineering_copilot.copilot_services.spec_qa import answer_spec_question

    effective_key = req.groq_api_key or DEFAULT_GROQ_KEY
    if not effective_key:
        raise HTTPException(status_code=400, detail="GROQ_API_KEY is required.")

    context = ""
    if vector_store_instance:
        docs = vector_store_instance.as_retriever(search_kwargs={"k": 3}).invoke(req.query)
        context = "\n\n".join([d.page_content for d in docs])
    elif active_contract:
        context = active_contract.to_json()

    reply = answer_spec_question(req.query, context, effective_key)
    return {"reply": reply}


@app.get("/api/export/json")
def export_json():
    if not active_contract:
        raise HTTPException(status_code=400, detail="No contract available.")
    return JSONResponse(
        content=active_contract.model_dump(),
        headers={"Content-Disposition": f"attachment; filename={active_contract.module_name}_contract.json"}
    )


@app.get("/api/export/markdown", response_class=PlainTextResponse)
def export_markdown():
    from src.export.mas_doc_generator import generate_mas_markdown
    if not active_contract:
        raise HTTPException(status_code=400, detail="No contract available.")
    content = generate_mas_markdown(active_contract)
    return PlainTextResponse(
        content,
        headers={"Content-Disposition": f"attachment; filename={active_contract.module_name}_MAS.md"}
    )


@app.get("/api/export/sva", response_class=PlainTextResponse)
def export_sva():
    from src.export.sva_bind_exporter import export_sva_module
    if not active_contract:
        raise HTTPException(status_code=400, detail="No contract available.")
    content = export_sva_module(active_contract)
    return PlainTextResponse(
        content,
        headers={"Content-Disposition": f"attachment; filename={active_contract.module_name}_sva.sv"}
    )


@app.get("/api/export/rtm")
def export_rtm():
    from src.export.rtm_csv_exporter import export_rtm_to_csv
    if not active_contract:
        raise HTTPException(status_code=400, detail="No contract available.")
    csv_str = export_rtm_to_csv(active_contract, requirements_cache)
    return PlainTextResponse(
        csv_str,
        headers={"Content-Disposition": f"attachment; filename={active_contract.module_name}_RTM.csv"}
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api.server:app", host="0.0.0.0", port=port)
