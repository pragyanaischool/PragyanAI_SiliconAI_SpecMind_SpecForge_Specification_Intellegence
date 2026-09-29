from src.p2_design_contract.models.contract import HardwareSpecificationContract


def generate_mas_markdown(contract: HardwareSpecificationContract) -> str:
    """Compiles a complete Micro-Architecture Specification (MAS) in Markdown."""
    lines = [
        f"# Micro-Architecture Specification: {contract.module_name}",
        f"\n**Module Description:** {contract.description}\n",
        "## 1. Operating Parameters & Constraints",
        f"- **Reset Methodology:** `{contract.reset_type}`",
        f"- **Target Frequency:** `{contract.timing.fmax_mhz or 'Unspecified'} MHz`",
        f"- **Latency / Throughput:** `{contract.timing.latency_cycles}` / `{contract.timing.throughput_cycles}`",
        f"- **CDC Boundaries:** `{'Yes' if contract.timing.is_cdc else 'No'}`\n",
        "## 2. Port Interface Dictionary",
        "| Port Name | Direction | Bit Width | Clock Domain | Active Level | Description |",
        "|---|:---:|:---:|:---:|:---:|---|",
    ]

    for p in contract.ports:
        lines.append(
            f"| `{p.name}` | `{p.direction}` | `{p.width}` | `{p.clock_domain}` | `{p.active_level}` | {p.description} |"
        )

    if contract.fsms:
        lines.append("\n## 3. Finite State Machine (FSM) Architectures")
        for fsm in contract.fsms:
            lines.append(f"### FSM: `{fsm.name}` (Encoding: {fsm.encoding})")
            lines.append(f"**States:** {', '.join(fsm.states)}\n")
            lines.append("| From State | To State | Condition Expression |")
            lines.append("|---|---|---|")
            for t in fsm.transitions:
                lines.append(f"| `{t.from_state}` | `{t.to_state}` | `{t.condition}` |")

    lines.append("\n## 4. Formal Verification Assertions & Corner Cases")
    for cc in contract.corner_cases:
        lines.append(f"### {cc.scenario_id}: {cc.title}")
        lines.append(f"**Hazard Condition:** {cc.hazard_description}\n")
        lines.append(f"**Hardware Behavior:** {cc.expected_hardware_behavior}\n")
        lines.append(f"```systemverilog\n{cc.sva_property}\n```\n")

    return "\n".join(lines)
