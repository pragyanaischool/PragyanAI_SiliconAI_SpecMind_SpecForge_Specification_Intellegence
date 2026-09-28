import os
import pytest
from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)


def test_api_health_check():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "PragyanAI-SpecForge" in data["service"]


def test_api_load_demo():
    response = client.post("/api/spec/demo")
    assert response.status_code == 200
    data = response.json()
    assert "axis_sync_fifo_demo" in data["contract"]["module_name"]
    assert len(data["contract"]["ports"]) > 0


def test_api_get_contract():
    # First ensure demo is loaded
    client.post("/api/spec/demo")

    response = client.get("/api/contract")
    assert response.status_code == 200
    data = response.json()
    assert data["module_name"] == "axis_sync_fifo_demo"
    assert "timing" in data
    assert "ports" in data


def test_api_add_port_hitl():
    client.post("/api/spec/demo")

    payload = {
        "name": "test_intr_req",
        "direction": "output",
        "width": "[0:0]",
        "clock_domain": "aclk",
        "active_level": "high",
        "description": "Interrupt flag"
    }

    response = client.post("/api/contract/port", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert any(p["name"] == "test_intr_req" for p in data["contract"]["ports"])


def test_api_add_corner_case_hitl():
    client.post("/api/spec/demo")

    payload = {
        "scenario_id": "CC_API_TEST",
        "title": "API Injected Condition",
        "hazard_description": "Simultaneous assert of test and reset",
        "expected_hardware_behavior": "Reset priority overrides test",
        "sva_property": "property p_rst; @(posedge aclk) !aresetn |-> !test_intr_req; endproperty"
    }

    response = client.post("/api/contract/corner-case", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert any(c["scenario_id"] == "CC_API_TEST" for c in data["contract"]["corner_cases"])


def test_api_export_endpoints():
    client.post("/api/spec/demo")

    # 1. Export JSON
    res_json = client.get("/api/export/json")
    assert res_json.status_code == 200
    assert "axis_sync_fifo_demo" in res_json.text

    # 2. Export Markdown MAS
    res_md = client.get("/api/export/markdown")
    assert res_md.status_code == 200
    assert "# Micro-Architecture Specification" in res_md.text

    # 3. Export SystemVerilog SVA
    res_sva = client.get("/api/export/sva")
    assert res_sva.status_code == 200
    assert "module axis_sync_fifo_demo_sva" in res_sva.text

    # 4. Export RTM CSV
    res_rtm = client.get("/api/export/rtm")
    assert res_rtm.status_code == 200
    assert "Requirement ID" in res_rtm.text


def test_api_upload_text_spec():
    sample_content = b"""
    ================================================================================
    SPECIFICATION: SPI Top (spi_top)
    ================================================================================
    Port Name | Dir | Width | Clock | Description
    clk       | in  | [0:0] | clk   | Master Clock
    rst_n     | in  | [0:0] | clk   | Active-low Reset
    mosi      | out | [0:0] | clk   | Master Out Slave In
    """

    files = [("files", ("spi_top.txt", sample_content, "text/plain"))]
    response = client.post("/api/spec/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "Successfully ingested" in data["message"]


def test_api_extraction_without_key_error():
    # If environment variable is absent and no key is sent in payload, should raise HTTP 400
    with pytest.MonkeyPatch.context() as m:
        m.setenv("GROQ_API_KEY", "")
        # Reset local cache variable in server module
        import api.server
        api.server.DEFAULT_GROQ_KEY = ""

        response = client.post("/api/spec/extract", json={"query": "Extract spec", "groq_api_key": ""})
        assert response.status_code == 400
        assert "GROQ_API_KEY is required" in response.json()["detail"]
