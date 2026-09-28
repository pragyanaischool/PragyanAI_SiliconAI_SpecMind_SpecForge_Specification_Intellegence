from src.2_design_contract.models.contract import HardwareSpecificationContract


def generate_systemverilog_covergroups(contract: HardwareSpecificationContract) -> str:
    """Generates SystemVerilog functional coverage groups and cross bins."""
    clk_name = next((p.name for p in contract.ports if "clk" in p.name.lower()), "clk")

    code = [
        "// ============================================================================",
        f"// Functional Coverage Model for: {contract.module_name}",
        "// ============================================================================\n",
        f"covergroup cg_{contract.module_name} @(posedge {clk_name});",
        "  option.per_instance = 1;\n",
    ]

    for p in contract.ports:
        if any(term in p.name.lower() for term in ["valid", "ready", "enable", "strobe"]):
            code.append(f"  cp_{p.name}: coverpoint {p.name} {{")
            code.append("    bins deasserted = {0};")
            code.append("    bins asserted   = {1};")
            code.append("  }\n")

    for fsm in contract.fsms:
        code.append(f"  cp_fsm_{fsm.name.lower()}: coverpoint state_{fsm.name.lower()} {{")
        for state in fsm.states:
            code.append(f"    bins {state.lower()} = {{{state}}};")
        code.append("  }\n")

    code.append("endgroup\n")
    return "\n".join(code)
