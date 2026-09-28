import pytest
from pydantic import ValidationError
from src.2_design_contract.models.ports import PortModel
from src.2_design_contract.models.timing import TimingModel
from src.2_design_contract.models.fsm import FSMModel, FSMTransitionModel
from src.2_design_contract.models.constraints import CornerCaseModel
from src.2_design_contract.models.contract import HardwareSpecificationContract
from src.2_design_contract.models.protocols import ProtocolModel


def test_port_model_validation_valid():
    port = PortModel(
        name="s_axis_tdata",
        direction="input",
        width="[31:0]",
        clock_domain="aclk",
        active_level="high",
        description="Data payload"
    )
    assert port.name == "s_axis_tdata"
    assert port.width == "[31:0]"
    assert port.direction == "input"


def test_port_model_slice_auto_formatting():
    # Tests width slice auto-formatting: "31:0" -> "[31:0]"
    p1 = PortModel(name="data_bus", direction="output", width="31:0")
    assert p1.width == "[31:0]"

    # Tests single integer width: "7" -> "[7:0]"
    p2 = PortModel(name="byte_out", direction="output", width="7")
    assert p2.width == "[7:0]"


def test_port_model_invalid_identifier():
    with pytest.raises(ValidationError):
        # Starts with invalid numeric character
        PortModel(name="123_invalid_port", direction="input")

    with pytest.raises(ValidationError):
        # Contains illegal punctuation
        PortModel(name="port-name!", direction="output")


def test_contract_clock_auto_insertion():
    # If a contract is declared with zero clock ports, the model validator inserts clk automatically
    contract = HardwareSpecificationContract(
        module_name="pure_logic_block",
        reset_type="async_low",
        ports=[
            PortModel(name="data_in", direction="input", width="[7:0]"),
            PortModel(name="data_out", direction="output", width="[7:0]")
        ]
    )
    port_names = [p.name for p in contract.ports]
    assert "clk" in port_names
    assert contract.ports[0].name == "clk"
    assert contract.ports[0].direction == "input"


def test_contract_serialization_roundtrip():
    contract = HardwareSpecificationContract(
        module_name="fifo_top",
        description="Synchronous buffer",
        reset_type="sync_low",
        ports=[
            PortModel(name="clk", direction="input", width="[0:0]"),
            PortModel(name="wr_en", direction="input", width="[0:0]")
        ],
        timing=TimingModel(fmax_mhz=300.0, latency_cycles="1"),
        fsms=[
            FSMModel(
                name="CTRL_FSM",
                encoding="one-hot",
                states=["IDLE", "ACTIVE"],
                transitions=[
                    FSMTransitionModel(from_state="IDLE", to_state="ACTIVE", condition="wr_en")
                ]
            )
        ],
        corner_cases=[
            CornerCaseModel(
                scenario_id="CC_01",
                title="Write Overflow",
                hazard_description="Write strobe when full",
                expected_hardware_behavior="Drop write and raise sticky overflow",
                sva_property="property p_ovf; @(posedge clk) full && wr_en |=> ovf; endproperty"
            )
        ]
    )

    json_str = contract.to_json()
    assert '"fifo_top"' in json_str

    deserialized = HardwareSpecificationContract.from_json(json_str)
    assert deserialized.module_name == "fifo_top"
    assert deserialized.timing.fmax_mhz == 300.0
    assert len(deserialized.fsms[0].transitions) == 1
    assert deserialized.corner_cases[0].scenario_id == "CC_01"
