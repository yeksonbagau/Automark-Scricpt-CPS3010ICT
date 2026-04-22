import subprocess

score = 0
total = 20

print("=== Auto Marker: Activity 4 - CAN Simulation & Analysis ===\n")

# =========================
# 1. Check vcan0 interface
# =========================
try:
    result = subprocess.check_output("ip link show vcan0", shell=True).decode()
    print("[PASS] vcan0 interface is active (+5 pts)")
    score += 5
except:
    print("[FAIL] vcan0 interface not found")

# =========================
# 2. Check ICSim running
# =========================
try:
    result = subprocess.check_output("ps aux | grep icsim | grep -v grep", shell=True).decode()
    if result:
        print("[PASS] ICSim simulator is running (+3 pts)")
        score += 3
    else:
        print("[FAIL] ICSim not running")
except:
    print("[FAIL] ICSim check error")

# =========================
# 3. Check controls running
# =========================
try:
    result = subprocess.check_output("ps aux | grep controls | grep -v grep", shell=True).decode()
    if result:
        print("[PASS] Controls app is running (+3 pts)")
        score += 3
    else:
        print("[FAIL] Controls not running")
except:
    print("[FAIL] Controls check error")

# =========================
# 4. Check CAN traffic (candump)
# =========================
try:
    result = subprocess.check_output("timeout 3 candump vcan0", shell=True).decode()
    if result.strip() != "":
        print("[PASS] CAN traffic detected on vcan0 (+5 pts)")
        score += 5
    else:
        print("[FAIL] No CAN traffic detected")
except:
    print("[FAIL] candump failed")

# =========================
# 5. Wireshark (manual check)
# =========================
print("[INFO] Wireshark capture should be verified manually (vcan0 interface)")
score += 4  # give marks if completed manually

# =========================
# FINAL SCORE
# =========================
print("\n==============================")
print(f"FINAL SCORE: {score}/{total}")

if score >= 15:
    print("STATUS: PASS")
else:
    print("STATUS: INCOMPLETE")