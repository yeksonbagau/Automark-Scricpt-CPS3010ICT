import json
import socket
from urllib.parse import urlparse

score = 0
total = 20

EXPECTED_VARIABLES = {
    "IN": "%IX100.0",
    "OUT": "%QX100.0",
    "WL": "%IW100",
    "FV": "%QW100",
    "DV": "%QW101"
}

def check_port(host, port, timeout=3):
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False

print("=== Auto Marker: Activity 3 - Factory I/O to OpenPLC Runtime ===\n")

try:
    with open("activity3_output.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("[ERROR] activity3_output.json not found")
    raise SystemExit
except json.JSONDecodeError as e:
    print(f"[ERROR] Invalid JSON: {e}")
    raise SystemExit

# 1. Factory I/O driver
if data.get("factoryio_driver") == "Modbus TCP/IP Server":
    print("[PASS] Factory I/O driver is Modbus TCP/IP Server")
    score += 3
else:
    print("[FAIL] Incorrect Factory I/O driver")

# 2. OpenPLC Runtime reachable
runtime_url = data.get("openplc_runtime_url", "")
parsed = urlparse(runtime_url)
host = parsed.hostname
port = parsed.port or 80

if host and check_port(host, port):
    print(f"[PASS] OpenPLC Runtime reachable at {host}:{port}")
    score += 3
else:
    print("[FAIL] OpenPLC Runtime not reachable")

# 3. plc.st uploaded
if data.get("plc_st_uploaded") is True:
    print("[PASS] plc.st uploaded")
    score += 2
else:
    print("[FAIL] plc.st not uploaded")

# 4. Compile success
if data.get("compile_success") is True:
    print("[PASS] Program compiled successfully")
    score += 2
else:
    print("[FAIL] Program compilation failed")

# 5. PLC running
if data.get("plc_running") is True:
    print("[PASS] PLC is running")
    score += 3
else:
    print("[FAIL] PLC is not running")

# 6. Variable mapping
student_vars = data.get("variables", {})
missing_or_wrong = []

for name, expected in EXPECTED_VARIABLES.items():
    actual = student_vars.get(name)
    if actual != expected:
        missing_or_wrong.append(f"{name} expected {expected} got {actual}")

if not missing_or_wrong:
    print("[PASS] Variable mappings are correct")
    score += 3
else:
    print("[FAIL] Variable mapping errors:")
    for item in missing_or_wrong:
        print("   -", item)

# 7. Monitoring values exist
monitor = data.get("monitoring_values", {})
required_monitor_keys = {"IN", "OUT", "WL", "FV", "DV"}

if required_monitor_keys.issubset(set(monitor.keys())):
    print("[PASS] Monitoring values present for IN, OUT, WL, FV, DV")
    score += 2
else:
    print("[FAIL] Missing monitoring values")

# 8. Communication confirmed
if data.get("communication_confirmed") is True:
    print("[PASS] Factory I/O communication with OpenPLC confirmed")
    score += 2
else:
    print("[FAIL] Communication not confirmed")

print(f"\nFinal Score: {score}/{total}")

if score >= 16:
    print("Result: PASS")
else:
    print("Result: NEEDS IMPROVEMENT")