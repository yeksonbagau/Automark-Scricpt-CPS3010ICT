import subprocess
import os

score = 0
total = 25
issues = []
fixes = []

def run_cmd(cmd):
    try:
        return subprocess.check_output(
            cmd, shell=True, stderr=subprocess.STDOUT, text=True, timeout=25
        )
    except subprocess.CalledProcessError as e:
        return e.output
    except subprocess.TimeoutExpired:
        return "[TIMEOUT]"

def pass_check(msg, pts):
    global score
    print(f"[PASS] {msg} (+{pts})")
    score += pts

def fail_check(msg, fix):
    print(f"[FAIL] {msg}")
    issues.append(msg)
    fixes.append(fix)

def warn_check(msg, fix):
    print(f"[WARN] {msg}")
    issues.append(msg)
    fixes.append(fix)

print("=== Auto Marker: Activity 7 - ICS Scanning & Probing ===\n")

# ---------------------------
# 1. Tool checks
# ---------------------------
print("---- Tool Checks ----")

if run_cmd("which nmap").strip():
    pass_check("Nmap installed", 3)
else:
    fail_check("Nmap not installed", "Install using: sudo apt install nmap")

if run_cmd("which ss").strip():
    pass_check("ss command available", 2)
else:
    fail_check("ss not available", "Install iproute2: sudo apt install iproute2")

# ---------------------------
# 2. Check open ports
# ---------------------------
print("\n---- Local ICS Ports ----")

ports = run_cmd("ss -lntu")

if ":502" in ports:
    pass_check("Modbus port 502 detected", 5)
else:
    fail_check(
        "Modbus port 502 not found",
        "Run Modbus simulator: ./diagslave -m tcp"
    )

if ":102" in ports:
    pass_check("S7 port 102 detected", 5)
else:
    fail_check(
        "S7 port 102 not found",
        "Ensure Siemens/S7 simulator is running (snap7)"
    )

# ---------------------------
# 3. Nmap Modbus scan
# ---------------------------
print("\n---- Nmap Modbus Scan ----")

modbus = run_cmd("nmap --script modbus-discover.nse -p 502 127.0.0.1")

if "502/tcp" in modbus and ("open" in modbus or "Modbus" in modbus):
    pass_check("Modbus scan successful", 5)
else:
    fail_check(
        "Modbus scan failed",
        "Check Modbus simulator is running and port 502 is open"
    )

# ---------------------------
# 4. Nmap S7 scan
# ---------------------------
print("\n---- Nmap S7 Scan ----")

s7 = run_cmd("nmap --script s7-info.nse -p 102 127.0.0.1")

if "102/tcp" in s7 and ("S7" in s7 or "Siemens" in s7 or "SIMATIC" in s7):
    pass_check("S7 scan successful (Siemens detected)", 5)
else:
    warn_check(
        "S7 scan did not confirm Siemens device",
        "Port 102 is open but S7 service not responding correctly. Check snap7 or simulator."
    )

# ---------------------------
# 5. plcscan check
# ---------------------------
print("\n---- PLCScan Check ----")

if os.path.exists("plcscan") or os.path.exists("./plcscan.py") or os.path.exists("plcscan/plcscan.py"):
    pass_check("plcscan tool found", 2)
else:
    warn_check(
        "plcscan not found",
        "Optional: git clone https://github.com/meeas/plcscan"
    )

# ---------------------------
# FINAL
# ---------------------------
print("\n==============================")
print(f"FINAL SCORE: {score}/{total}")

if score >= 18:
    print("STATUS: PASS")
else:
    print("STATUS: NEEDS IMPROVEMENT")

# ---------------------------
# IMPROVEMENT REPORT
# ---------------------------
print("\n---- Issues Detected ----")

if not issues:
    print("No issues detected. All checks passed.")
else:
    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue}")

print("\n---- Recommended Fixes ----")

if not fixes:
    print("No fixes needed.")
else:
    for i, fix in enumerate(fixes, 1):
        print(f"{i}. {fix}")
