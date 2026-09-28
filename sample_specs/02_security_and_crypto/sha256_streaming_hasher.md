# Micro-Architecture Specification: SHA-256 Streaming Hasher Core
**Document Version:** 2.1 | **Security Standard:** FIPS 180-4 | **Module Name:** `sha256_engine_top`

## 1. Architectural Summary
Hardware acceleration block for SHA-256 secure hash standard. Accepts streaming 512-bit message blocks ($M^{(i)}$), executes 64 iterative compression rounds, updates the 256-bit working state variables ($a, b, c, d, e, f, g, h$), and appends the initial hash vector $H^{(0)}$.

## 2. Port Interface Dictionary
| Signal Name | Direction | Bit Width | Clock Domain | Active Level | Functional Description |
|:---|:---:|:---:|:---:|:---:|:---|
| `clk` | input | `[0:0]` | `clk` | edge | Core cryptographic clock (target: 333 MHz) |
| `rst_n` | input | `[0:0]` | `clk` | low | Synchronous active-low reset |
| `init_cmd` | input | `[0:0]` | `clk` | high | Resets internal hash state to $H^{(0)}$ initial constants |
| `block_valid` | input | `[0:0]` | `clk` | high | Indicates `block_data` contains a valid 512-bit chunk |
| `block_data` | input | `[511:0]`| `clk` | high | 512-bit raw padded input message chunk |
| `block_ready` | output| `[0:0]` | `clk` | high | Core ready for next 512-bit block (deasserted during 64 rounds) |
| `digest_out` | output| `[255:0]`| `clk` | high | Final computed 256-bit cryptographic message digest |
| `digest_valid`| output| `[0:0]` | `clk` | high | 1-cycle strobe indicating hash calculation completion |

## 3. Timing and Performance Characteristics
- **Compression Latency:** Exactly 64 clock cycles per 512-bit block.
- **Throughput:** $5.33 \text{ Gbps}$ at $333 \text{ MHz}$.
- **Message Expansion:** Done on-the-fly via a 16-word circular buffer without external RAM access.

## 4. Finite State Machine
- `STATE_IDLE`: Ready to accept `init_cmd` or `block_data`.
- `STATE_EXPAND_COMPRESS`: Active execution of rounds $t = 0 \text{ to } 63$. `block_ready = 0`.
- `STATE_FINALIZE`: Accumulates intermediate hash values with initial state vector ($H^{(i)} = H^{(i-1)} + \text{Vars}$).
- `STATE_VALID`: Asserts `digest_valid = 1` for 1 clock cycle, updates `digest_out`.

## 5. Critical Hazards & Verification Assertions
- **HAZARD-01 (Init Overwrite):** If `init_cmd` is asserted mid-compression ($t \in [1, 63]$), the core must immediately terminate execution, purge intermediate states, and reload $H^{(0)}$.
- **HAZARD-02 (Backpressure Breach):** If `block_valid` remains asserted while `block_ready = 0`, the current state must not be corrupted.
- **SVA Assertion Reference:**
  ```systemverilog
  property p_block_ready_dropped_during_compression;
    @(posedge clk) disable iff (!rst_n)
    (block_valid && block_ready) |=> (!block_ready [*64]);
  endproperty
  assert property (p_block_ready_dropped_during_compression);
