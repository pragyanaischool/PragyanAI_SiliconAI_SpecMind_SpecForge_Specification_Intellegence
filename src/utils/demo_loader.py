from src.2_design_contract.models.contract import HardwareSpecificationContract
from src.2_design_contract.models.ports import PortModel
from src.2_design_contract.models.timing import TimingModel
from src.2_design_contract.models.fsm import FSMModel, FSMTransitionModel
from src.2_design_contract.models.constraints import CornerCaseModel


def load_demo_contract() -> HardwareSpecificationContract:
    """Provides a reference golden contract for an AXI4-Stream FIFO."""
    return HardwareSpecificationContract(
        module_name="axis_sync_fifo_demo",
        description="Reference Parameterized AXI4-Stream Synchronous FIFO with Watermark Flags",
        reset_type="async_low",
        ports=[
            PortModel(name="aclk", direction="input", width="[0:0]", clock_domain="aclk", active_level="edge", description="Core Clock"),
            PortModel(name="aresetn", direction="input", width="[0:0]", clock_domain="aclk", active_level="low", description="Active-low Reset"),
            PortModel(name="s_axis_tdata", direction="input", width="[31:0]", clock_domain="aclk", active_level="high", description="Slave Inbound Payload"),
            PortModel(name="s_axis_tvalid", direction="input", width="[0:0]", clock_domain="aclk", active_level="high", description="Slave Data Valid"),
            PortModel(name="s_axis_tready", direction="output", width="[0:0]", clock_domain="aclk", active_level="high", description="Slave Ready for Write"),
            PortModel(name="m_axis_tdata", direction="output", width="[31:0]", clock_domain="aclk", active_level="high", description="Master Outbound Payload"),
            PortModel(name="m_axis_tvalid", direction="output", width="[0:0]", clock_domain="aclk", active_level="high", description="Master Data Valid"),
            PortModel(name="m_axis_tready", direction="input", width="[0:0]", clock_domain="aclk", active_level="high", description="Downstream Sink Ready"),
        ],
        timing=TimingModel(
            fmax_mhz=250.0,
            setup_time_ns=0.4,
            hold_time_ns=0.1,
            latency_cycles="0 (FWFT Mode)",
            throughput_cycles="1 transaction/cycle",
            is_cdc=False
        ),
        fsms=[
            FSMModel(
                name="FWFT_CTRL_FSM",
                encoding="one-hot",
                states=["ST_EMPTY", "ST_FILLING", "ST_VALID"],
                transitions=[
                    FSMTransitionModel(from_state="ST_EMPTY", to_state="ST_VALID", condition="s_axis_tvalid && s_axis_tready"),
                    FSMTransitionModel(from_state="ST_VALID", to_state="ST_EMPTY", condition="m_axis_tready && fifo_count == 1"),
                ],
                reset_state="ST_EMPTY"
            )
        ],
        corner_cases=[
            CornerCaseModel(
                scenario_id="CC_AXIS_01",
                title="Full-1 Boundary Simultaneous R/W",
                hazard_description="Simultaneous read and write when FIFO has exactly 1 open space remaining.",
                expected_hardware_behavior="Occupancy counter remains stable; s_axis_tready remains asserted.",
                sva_property="property p_simul_rw;\n  @(posedge aclk) disable iff (!aresetn)\n  (count == DEPTH-1 && s_axis_tvalid && s_axis_tready && m_axis_tvalid && m_axis_tready) |=> (count == DEPTH-1);\nendproperty\nassert property (p_simul_rw);"
            )
        ]
    )
