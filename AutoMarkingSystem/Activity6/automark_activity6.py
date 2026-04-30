import subprocess
import os

score = 0
total = 56

print("=== Auto Marker: Activity 6 – Splunk + Suricata + Threat Hunting ===\n")

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode(errors="ignore")
    except:
        return ""

# =========================
# 1. Interface / IP checks
# =========================
ip_info = run("ip a")

if "192.168.2.5" in ip_info:
    print("[PASS] HMI has Operations IP 192.168.2.5 (+2)")
    score += 2
else:
    print("[FAIL] HMI IP 192.168.2.5 not found")

if "eth1" in ip_info:
    print("[PASS] Monitoring interface eth1 exists (+2)")
    score += 2
else:
    print("[FAIL] eth1 monitoring interface not found")

# =========================
# 2. Network connectivity
# =========================
if "bytes from" in run("ping -c 2 192.168.1.5"):
    print("[PASS] HMI can reach PLC 192.168.1.5 (+3)")
    score += 3
else:
    print("[FAIL] HMI cannot reach PLC 192.168.1.5")

if "bytes from" in run("ping -c 2 192.168.1.6"):
    print("[PASS] HMI can reach Factory 192.168.1.6 (+3)")
    score += 3
else:
    print("[FAIL] HMI cannot reach Factory 192.168.1.6")

# =========================
# 3. Suricata service
# =========================
if run("systemctl is-active suricata").strip() == "active":
    print("[PASS] Suricata is running (+4)")
    score += 4
else:
    print("[FAIL] Suricata is not running")

# =========================
# 4. Suricata interface config
# =========================
suricata_conf = run("cat /etc/suricata/suricata.yaml")

if "interface: eth1" in suricata_conf:
    print("[PASS] Suricata is configured to monitor eth1 (+4)")
    score += 4
else:
    print("[FAIL] Suricata is not configured for eth1")

# =========================
# 5. Rule file check
# =========================
local_rules = run("cat /var/lib/suricata/rules/local.rules")

if "alert icmp" in local_rules and "ICMP" in local_rules:
    print("[PASS] ICMP custom rule exists in local.rules (+3)")
    score += 3
else:
    print("[FAIL] ICMP custom rule missing from local.rules")

# =========================
# 6. Log file checks
# =========================
if os.path.exists("/var/log/suricata/fast.log"):
    print("[PASS] fast.log exists (+2)")
    score += 2
else:
    print("[FAIL] fast.log missing")

if os.path.exists("/var/log/suricata/eve.json"):
    print("[PASS] eve.json exists (+2)")
    score += 2
else:
    print("[FAIL] eve.json missing")

# =========================
# 7. Suricata alert checks
# =========================
fast_alerts = run("grep -i 'ICMP' /var/log/suricata/fast.log | tail -20")

if fast_alerts:
    print("[PASS] ICMP alerts found in fast.log (+5)")
    score += 5
else:
    print("[FAIL] No ICMP alerts found in fast.log")

ipv4_alerts = run("grep '192.168.1.' /var/log/suricata/fast.log | tail -20")

if ipv4_alerts:
    print("[PASS] IPv4 OT traffic detected in fast.log (+5)")
    score += 5
else:
    print("[WARN] No IPv4 192.168.1.x alerts found in fast.log")

# =========================
# 8. eve.json alert checks
# =========================
eve_alerts = run("grep '\"event_type\":\"alert\"' /var/log/suricata/eve.json | tail -20")

if eve_alerts:
    print("[PASS] Alert events exist in eve.json (+5)")
    score += 5
else:
    print("[FAIL] No alert events found in eve.json")

eve_icmp = run("grep '\"proto\":\"ICMP\"' /var/log/suricata/eve.json | tail -20")

if eve_icmp:
    print("[PASS] ICMP events found in eve.json (+4)")
    score += 4
else:
    print("[FAIL] No ICMP events found in eve.json")

# =========================
# 9. Splunk service check
# =========================
splunk_process = run("ps aux | grep splunk | grep -v grep")

if splunk_process:
    print("[PASS] Splunk is running (+4)")
    score += 4
else:
    print("[FAIL] Splunk is not running")

if run("ss -tulnp | grep 8000"):
    print("[PASS] Splunk Web is listening on port 8000 (+2)")
    score += 2
else:
    print("[FAIL] Splunk Web port 8000 not listening")

# =========================
# 10. Malware file check
# =========================
malware_locations = [
    "./BeaconMalware.py",
    "/home/openplc/BeaconMalware.py",
    "/home/hmi/BeaconMalware.py",
    "/home/student/BeaconMalware.py"
]

malware_found = False
for path in malware_locations:
    if os.path.exists(path):
        malware_found = True
        break

if malware_found:
    print("[PASS] BeaconMalware.py found (+3)")
    score += 3
else:
    print("[WARN] BeaconMalware.py not found in checked locations")

# =========================
# 11. Threat hunting IOC checks
# Activity 6 IOC:
# PLC 192.168.1.5 -> suspicious IP 192.168.2.254 on TCP/80
# =========================
ioc_ip = run("grep '192.168.2.254' /var/log/suricata/eve.json | tail -20")

if ioc_ip:
    print("[PASS] IOC IP 192.168.2.254 found in eve.json (+5)")
    score += 5
else:
    print("[FAIL] IOC IP 192.168.2.254 not found in eve.json")

plc_to_ioc = run("grep '192.168.1.5' /var/log/suricata/eve.json | grep '192.168.2.254' | tail -20")

if plc_to_ioc:
    print("[PASS] PLC beacon traffic detected: 192.168.1.5 -> 192.168.2.254 (+5)")
    score += 5
else:
    print("[FAIL] PLC beacon traffic not found")

port_80 = run("grep '\"dest_port\":80' /var/log/suricata/eve.json | tail -20")

if port_80:
    print("[PASS] TCP destination port 80 activity found (+3)")
    score += 3
else:
    print("[WARN] No destination port 80 activity found")

# =========================
# FINAL SCORE
# =========================
print("\n=== FINAL RESULT ===")
print(f"Score: {score}/{total}")

percentage = (score / total) * 100
print(f"Percentage: {percentage:.1f}%")

if score >= 50:
    print(" Excellent – Activity 6 is ready to demonstrate.")
elif score >= 40:
    print(" Good – mostly ready, check warnings/fails.")
elif score >= 30:
    print(" Partial – some core parts work, but fix failed checks.")
else:
    print(" Needs work – review network, Suricata, Splunk, and malware traffic.")

print("\n=== Suggested Splunk Searches ===")
print('1) source="/var/log/suricata/eve.json" event_type=alert')
print('2) source="/var/log/suricata/eve.json" proto=ICMP')
print('3) source="/var/log/suricata/eve.json" 192.168.2.254')
print('4) source="/var/log/suricata/eve.json" (src_ip="192.168.1.5" OR src_ip="192.168.2.5") | stats count by src_ip,dest_ip,dest_port | sort - count')
