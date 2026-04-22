import subprocess

score = 0
total = 30

def run_cmd(cmd):
    try:
        return subprocess.check_output(
            cmd, shell=True, stderr=subprocess.STDOUT, text=True
        )
    except subprocess.CalledProcessError as e:
        return e.output

print("=== Auto Marker: Activity 5 - Secure OT Environment ===\n")

# ---------------------------
# Task 1: Network Segmentation
# ---------------------------
print("---- Task 1: Network Segmentation ----")

ip_output = run_cmd("ip a")

# HMI should be on Operations Level 192.168.2.0/24
if "192.168.2.5/24" in ip_output:
    print("[PASS] HMI Operations Level IP detected (192.168.2.5/24) (+4)")
    score += 4
elif "192.168.2." in ip_output:
    print("[PASS] Operations Level network detected on HMI (192.168.2.x) (+3)")
    score += 3
else:
    print("[FAIL] Operations Level network not detected on HMI")

# Extra adapter for monitoring / TAP
if "eth1:" in ip_output or "enp0s8:" in ip_output or "enp0s9:" in ip_output:
    print("[PASS] Additional monitoring adapter detected for TAP/mirroring (+2)")
    score += 2
else:
    print("[WARN] No second adapter detected for TAP/mirroring")

# ---------------------------
# Task 2: pfSense Firewall
# ---------------------------
print("\n---- Task 2: pfSense Firewall ----")

# Use HTTPS to test pfSense reachability because web UI is at 192.168.2.1
pfsense_web = run_cmd("curl -k -I --max-time 5 https://192.168.2.1")

if "HTTP/" in pfsense_web:
    print("[PASS] pfSense web interface reachable at https://192.168.2.1 (+4)")
    score += 4
else:
    print("[FAIL] Cannot reach pfSense web interface")

# HTTP outbound should be allowed
http_test = run_cmd("curl -I --max-time 5 http://example.com")
if "HTTP/" in http_test:
    print("[PASS] HTTP allowed through firewall (+3)")
    score += 3
else:
    print("[FAIL] HTTP blocked")

# DNS outbound should be allowed
dns_test = run_cmd("getent hosts example.com")
if dns_test.strip():
    print("[PASS] DNS resolution working through firewall (+3)")
    score += 3
else:
    print("[FAIL] DNS resolution failed")

# ICMP block test
icmp_result = subprocess.run(
    "ping -c 1 192.168.1.5",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

if icmp_result.returncode != 0:
    print("[PASS] ICMP blocking rule working (+2)")
    score += 2
else:
    print("[INFO] ICMP reachable (this may be expected if the temporary ICMP block rule was removed)")

# ---------------------------
# Task 3: Suricata IDS
# ---------------------------
print("\n---- Task 3: Suricata IDS ----")

suricata_status = run_cmd("systemctl is-active suricata").strip()
if suricata_status == "active":
    print("[PASS] Suricata service is running (+4)")
    score += 4
else:
    print("[FAIL] Suricata service is not running")

suricata_yaml = run_cmd("cat /etc/suricata/suricata.yaml")

# Check af-packet config
if "af-packet:" in suricata_yaml and (
    "interface: eth0" in suricata_yaml or
    "interface: enp0s3" in suricata_yaml or
    "interface: eth1" in suricata_yaml or
    "interface: enp0s8" in suricata_yaml
):
    print("[PASS] Suricata af-packet interface configured (+2)")
    score += 2
else:
    print("[FAIL] Suricata af-packet interface not configured correctly")

# Check rule files
if "local.rules" in suricata_yaml and "modbus.rules" in suricata_yaml:
    print("[PASS] Suricata custom rule files configured (+2)")
    score += 2
else:
    print("[FAIL] local.rules / modbus.rules not configured")

# Check startup logs
suricata_log = run_cmd("tail -n 50 /var/log/suricata/suricata.log")
if "engine started" in suricata_log.lower() or "packet processing threads" in suricata_log.lower():
    print("[PASS] Suricata engine startup confirmed in logs (+2)")
    score += 2
else:
    print("[WARN] Suricata startup confirmation not found in recent logs")

# Generate ICMP traffic to trigger alert
print("\nGenerating ICMP test traffic...")
run_cmd("ping -c 2 192.168.1.5")

fast_log_after = run_cmd("tail -n 50 /var/log/suricata/fast.log")
if "ICMP test" in fast_log_after or "ICMP" in fast_log_after:
    print("[PASS] Suricata detected ICMP alert (+4)")
    score += 4
else:
    print("[FAIL] No ICMP alert detected in Suricata logs")

# ---------------------------
# Final result
# ---------------------------
print("\n==============================")
print(f"FINAL SCORE: {score}/{total}")

if score >= 22:
    print("STATUS: PASS")
else:
    print("STATUS: NEEDS IMPROVEMENT")