import subprocess
import os
import glob
import re

score = 0
total = 60
issues = []
fixes = []

def run_cmd(cmd, timeout=20):
    try:
        return subprocess.check_output(
            cmd,
            shell=True,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout
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

print("=== Auto Marker: Activity 8 - Attacking Industrial Networks ===\n")

# =====================================================
# Task 1 / 2: Metasploit + S7 / Modbus testbed
# =====================================================
print("---- Task 1 & 2: Metasploit, S7, and Modbus Testbed ----")

if run_cmd("which msfconsole").strip():
    pass_check("Metasploit Framework installed", 4)
else:
    fail_check("Metasploit not found", "Install or start Kali Metasploit tools.")

if run_cmd("which searchsploit").strip():
    pass_check("Searchsploit available", 2)
else:
    warn_check("searchsploit not found", "Install exploitdb: sudo apt install exploitdb")

ports = run_cmd("ss -lntu")

if ":102" in ports:
    pass_check("Siemens S7 port 102 is listening", 4)
else:
    warn_check("S7 port 102 not detected", "Start the Siemens/S7 simulator or snap7 server.")

if ":502" in ports:
    pass_check("Modbus port 502 is listening", 4)
else:
    fail_check("Modbus port 502 not detected", "Start Modbus simulator: ./diagslave -m tcp or ModbusPal.")

# Check Metasploit external Siemens exploit file
msf_s7_paths = [
    "/usr/share/metasploit-framework/modules/exploits/hardware/remote/38964.rb",
    "/usr/share/metasploit-framework/modules/exploits/hardware/remot/38964.rb"
]

if any(os.path.exists(path) for path in msf_s7_paths):
    pass_check("Siemens S7 exploit module 38964.rb copied into Metasploit", 3)
else:
    warn_check(
        "Siemens S7 exploit module not found in Metasploit path",
        "Copy 38964.rb into /usr/share/metasploit-framework/modules/exploits/hardware/remote/"
    )

# =====================================================
# Task 3: ModbusPal / Modbus-cli
# =====================================================
print("\n---- Task 3: Modbus Protocol Testing ----")

if run_cmd("which ruby").strip():
    pass_check("Ruby installed for modbus-cli", 2)
else:
    warn_check("Ruby not found", "Install Ruby: sudo apt-get install ruby-full")

if run_cmd("which modbus").strip():
    pass_check("modbus-cli installed", 4)
else:
    fail_check("modbus-cli not found", "Install it: sudo gem install modbus-cli")

# Read Modbus registers safely
modbus_read = run_cmd("timeout 8 modbus read 127.0.0.1 %MW1 10", timeout=12)

if "ERROR" not in modbus_read.upper() and modbus_read.strip():
    pass_check("modbus-cli can read holding registers from localhost", 5)
    print("[INFO] Sample Modbus read output:")
    print("\n".join(modbus_read.splitlines()[:6]))
else:
    fail_check(
        "modbus-cli read test failed",
        "Ensure ModbusPal/diagslave is running on 127.0.0.1:502."
    )

# Evidence of ModbusPal jar
modbuspal_files = glob.glob("**/ModbusPal.jar", recursive=True)
if modbuspal_files:
    pass_check("ModbusPal.jar found", 2)
else:
    warn_check("ModbusPal.jar not found", "Place ModbusPal.jar in the activity folder if used.")

# =====================================================
# Task 4: CAN attack / replay environment
# =====================================================
print("\n---- Task 4: CAN Protocol Attack and Replay ----")

if run_cmd("which cansend").strip():
    pass_check("cansend available", 3)
else:
    fail_check("cansend not found", "Install can-utils: sudo apt install can-utils")

if run_cmd("which candump").strip():
    pass_check("candump available", 3)
else:
    fail_check("candump not found", "Install can-utils: sudo apt install can-utils")

if run_cmd("which canplayer").strip():
    pass_check("canplayer available", 3)
else:
    fail_check("canplayer not found", "Install can-utils: sudo apt install can-utils")

vcan = run_cmd("ip link show vcan0")
if "vcan0" in vcan and "UP" in vcan:
    pass_check("vcan0 interface is active", 4)
else:
    fail_check(
        "vcan0 is not active",
        "Run: sudo modprobe can && sudo modprobe vcan && sudo ip link add dev vcan0 type vcan && sudo ip link set up vcan0"
    )

if run_cmd("pgrep -a icsim").strip():
    pass_check("ICSim is running", 3)
else:
    warn_check("ICSim not running", "Start it: ./icsim vcan0 &")

if run_cmd("pgrep -a controls").strip():
    pass_check("ICSim controls are running", 3)
else:
    warn_check("ICSim controls not running", "Start it: ./controls vcan0 &")

# Check CAN traffic
can_traffic = run_cmd("timeout 4 candump vcan0", timeout=8)

if can_traffic.strip():
    pass_check("CAN traffic detected on vcan0", 4)
    ids = set()
    for line in can_traffic.splitlines():
        m = re.search(r"vcan0\s+([0-9A-Fa-f]+)\s+\[\d+\]", line)
        if m:
            ids.add(m.group(1).upper())
    if ids:
        print("[INFO] Detected CAN IDs:", ", ".join(sorted(ids)))
else:
    warn_check("No CAN traffic detected", "Start ICSim/controls and press buttons during capture.")

# Check replay files
canlogs_exists = os.path.isdir("CANLogs")
candump_logs = glob.glob("CANLogs/candump-*.log") + glob.glob("candump-*.log")
replay_logs = glob.glob("CANLogs/can.*.log") + glob.glob("can.*.log")

if canlogs_exists:
    pass_check("CANLogs directory exists", 2)
else:
    warn_check("CANLogs directory not found", "Create it: mkdir CANLogs")

if candump_logs:
    pass_check("candump replay log found", 3)
else:
    warn_check("No candump replay log found", "Run: candump -c vcan0 -l inside CANLogs.")

if replay_logs:
    pass_check("Filtered replay logs found", 3)
else:
    warn_check(
        "Filtered replay logs not found",
        "Create logs such as can.acceleration.log, can.turnright.log, and can.turnleft.log using grep."
    )

# =====================================================
# Task 5: ICS Environment Pentesting Evidence
# =====================================================
print("\n---- Task 5: ICS Environment Reconnaissance and Evidence ----")

ip_info = run_cmd("ip a")

if "192.168.2.254" in ip_info:
    pass_check("Kali has expected Operations Level IP 192.168.2.254", 4)
else:
    warn_check(
        "Kali IP 192.168.2.254 not detected",
        "Set Kali adapter to Operations Level and assign 192.168.2.254/24 with gateway 192.168.2.1."
    )

# Check key hosts
for host, name, pts in [
    ("192.168.2.1", "pfSense firewall", 2),
    ("192.168.1.5", "PLC/OpenPLC", 3),
    ("192.168.2.5", "HMI", 2),
]:
    ping = run_cmd(f"ping -c 1 -W 2 {host}", timeout=5)
    if "bytes from" in ping:
        pass_check(f"{name} reachable at {host}", pts)
    else:
        warn_check(f"{name} not reachable at {host}", f"Check VM power/network/firewall for {host}.")

# OpenPLC web interface check
openplc = run_cmd("curl -I --max-time 5 http://192.168.1.5:8080", timeout=8)
if "HTTP/" in openplc:
    pass_check("OpenPLC web interface reachable on 192.168.1.5:8080", 4)
else:
    warn_check(
        "OpenPLC web interface not reachable",
        "Ensure OpenPLC runtime is running and port 8080 is allowed through pfSense."
    )

# Modbus port check on real PLC target
modbus_target = run_cmd("timeout 8 nc -zv 192.168.1.5 502", timeout=10)
if "succeeded" in modbus_target.lower() or "open" in modbus_target.lower():
    pass_check("PLC Modbus port 502 reachable", 4)
else:
    warn_check(
        "PLC Modbus port 502 not reachable",
        "Check OpenPLC Modbus port, pfSense rules, and PLC runtime."
    )

# Evidence files: Nessus / pcap / report
nessus_files = glob.glob("*.nessus") + glob.glob("*.html") + glob.glob("*.csv")
pcap_files = glob.glob("*.pcap") + glob.glob("*.pcapng")
report_files = glob.glob("*report*.txt") + glob.glob("*report*.md") + glob.glob("*findings*.txt")

if nessus_files:
    pass_check("Nessus scan evidence file found", 3)
else:
    warn_check("No Nessus evidence file found", "Export Nessus results as .nessus, .html, or .csv into this folder.")

if pcap_files:
    pass_check("Wireshark packet capture evidence found", 3)
else:
    warn_check("No Wireshark pcap evidence found", "Save the OpenPLC HTTP capture as .pcapng in this folder.")

if report_files:
    pass_check("Pentest findings/report evidence found", 2)
else:
    warn_check("No findings/report file found", "Create report_findings.txt or report_findings.md summarising results.")

# =====================================================
# Final Result
# =====================================================
print("\n==============================")
print(f"FINAL SCORE: {score}/{total}")

percentage = (score / total) * 100
print(f"PERCENTAGE: {percentage:.1f}%")

if score >= 48:
    print("STATUS: EXCELLENT - Activity 8 is ready to demonstrate.")
elif score >= 38:
    print("STATUS: PASS - Most Activity 8 requirements are working.")
else:
    print("STATUS: NEEDS IMPROVEMENT - Review failed/warning items.")

print("\n---- Issues / Improvements ----")
if not issues:
    print("No major issues detected.")
else:
    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue}")

print("\n---- Recommended Fixes ----")
if not fixes:
    print("No fixes required.")
else:
    for i, fix in enumerate(fixes, 1):
        print(f"{i}. {fix}")

print("\n---- Suggested Manual Evidence to Show Tutor ----")
print("1. Metasploit search results for Modbus/S7 modules.")
print("2. modbus-cli read/write output.")
print("3. cansend/candump/canplayer replay evidence.")
print("4. Nessus scan results showing discovered hosts/services.")
print("5. Wireshark HTTP capture showing OpenPLC login traffic.")
