from src.p2_design_contract.models.contract import HardwareSpecificationContract
from src.p2_design_contract.models.ports import PortModel
from src.p2_design_contract.models.constraints import CornerCaseModel
from src.p2_design_contract.models.fsm import FSMModel
from src.p3_verification_intelligence.sva_generation.sva_builder import generate_sva_bind_file
from src.p3_verification_intelligence.coverage_recommendations.covergroup_suggester import generate_systemverilog_covergroups
from src.p3_verification_intelligence.testcase_generation.test_planner import generate_test_plan
from src.p3_verification_intelligence.boundary_conditions.boundary_tester import extract_boundary_scenarios


def test_generate_sva_bind_file_structure():
    contract = HardwareSpecificationContract(
        module_name="axi_stream_buffer",
        reset_type="async_low",
        ports=[
            PortModel(name="aclk", direction="input", width="[0:0]", clock_domain="aclk", active_level="edge"),
            PortModel(name="aresetn", direction="input", width="[0:0]", clock_domain="aclk", active_level="low"),
            PortModel(name="tvalid", direction="input", width="[0:0]", clock_domain="aclk", active_level="high"),
            PortModel(name="tready", direction="output", width="[0:0]", clock_domain="aclk", active_level="high")
        ],
        corner_cases=[
            CornerCaseModel(
                scenario_id="CC_AXIS_01",
                title="Ready Drop Protocol Check",
                hazard_description="tready drops mid-transaction",
                expected_hardware_behavior="tvalid must remain stable",
                sva_property="property p_valid_hold; @(posedge aclk) tvalid && !tready |=> tvalid; endproperty\nassert property (p_valid_hold);"
            )
        ]
    )

    sva_code = generate_sva_bind_file(contract)

    # 1. Check module definition and timescale
    assert "`timescale 1ns / 1ps" in sva_code
    assert "module axi_stream_buffer_sva (" in sva_code

    # 2. Check port declarations
    assert "input wire [0:0]" in sva_code
    assert "aclk" in sva_code
    assert "aresetn" in sva_code

    # 3. Check clocking and disable conditions
    assert "default clocking cb_clk @(posedge aclk); endclocking;" in sva_code
    assert "default disable iff (!aresetn);" in sva_code

    # 4. Check formal properties and bind statement
    assert "property p_valid_hold;" in sva_code
    assert "bind axi_stream_buffer axi_stream_buffer_sva inst_axi_stream_buffer_sva" in sva_code


def test_generate_systemverilog_covergroups():
    contract = HardwareSpecificationContract(
        module_name="fifo_core",
        ports=[
            PortModel(name="clk", direction="input", width="[0:0]"),
            PortModel(name="wr_valid", direction="input", width="[0:0]"),
            PortModel(name="wr_ready", direction="output", width="[0:0]")
        ],
        fsms=[
            FSMModel(
                name="FIFO_FSM",
                states=["EMPTY", "PARTIAL", "FULL"]
            )
        ]
    )

    cg_code = generate_systemverilog_covergroups(contract)

    assert "covergroup cg_fifo_core @(posedge clk);" in cg_code
    assert "cp_wr_valid: coverpoint wr_valid" in cg_code
    assert "cp_wr_ready: coverpoint wr_ready" in cg_code
    assert "cp_fsm_fifo_fsm: coverpoint state_fifo_fsm" in cg_code
    assert "bins empty = {EMPTY};" in cg_code
    assert "endgroup" in cg_code


def test_testcase_planner_and_boundaries():
    contract = HardwareSpecificationContract(
        module_name="uart_rx",
        reset_type="async_low",
        ports=[
            PortModel(name="clk", direction="input", width="[0:0]"),
            PortModel(name="rx_data", direction="output", width="[7:0]")
        ],
        corner_cases=[
            CornerCaseModel(
                scenario_id="CC_UART_01",
                title="Framing Error",
                hazard_description="Stop bit low",
                expected_hardware_behavior="Flag error",
                sva_property="assert property (p_stop);"
            )
        ]
    )

    plan = generate_test_plan(contract)
    assert len(plan) == 2
    assert plan[0]["test_id"] == "TEST_001_POWER_ON_RESET"
    assert plan[1]["test_id"] == "TEST_CORNER_CC_UART_01"

    boundaries = extract_boundary_scenarios(contract)
    assert len(boundaries) == 1
    assert boundaries[0]["signal"] == "rx_data"
    assert "0xff" in boundaries[0]["boundary_test"].lower()
