import subprocess
import re
import time

score = 0
total = 20

def run_cmd(command):
    try:
        return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        return e.output

def capture_can(seconds=3):
    return run_cmd(f"timeout {seconds} candump vcan0")

def extract_frames(output):
    frames = set()
    for line in output.splitlines():
        match = re.search(r"vcan0\s+([0-9A-Fa-f]+)\s+\[\d+\]\s+(.+)", line)
        if match:
            can_id = match.group(1).upper()
            data = match.group(2).strip()
            frames.add((can_id, data))
    return frames

print("=== Auto Marker: Activity 4 - CAN Simulation & Analysis ===\n")

if "vcan0" in run_cmd("ip link show vcan0") and "UP" in run_cmd("ip link show vcan0"):
    print("[PASS] vcan0 interface is active (+4 pts)")
    score += 4
else:
    print("[FAIL] vcan0 interface not active")

if run_cmd("pgrep -a icsim").strip():
    print("[PASS] ICSim simulator is running (+3 pts)")
    score += 3
else:
    print("[FAIL] ICSim simulator is not running")

if run_cmd("pgrep -a controls").strip():
    print("[PASS] Controls app is running (+3 pts)")
    score += 3
else:
    print("[FAIL] Controls app is not running")

print("\nBaseline capture: do NOT press any controls.")
baseline = extract_frames(capture_can(3))
print(f"[INFO] Baseline frames detected: {len(baseline)}")

input("\nNow press ENTER, then press ACCELERATE / DOOR / TURN during the next 5 seconds...")
action = extract_frames(capture_can(5))
print(f"[INFO] Action frames detected: {len(action)}")

new_or_changed = action - baseline

if new_or_changed:
    print("[PASS] Control action changed CAN traffic (+6 pts)")
    score += 6
    print("[INFO] New/changed CAN frames:")
    for can_id, data in sorted(list(new_or_changed))[:10]:
        print(f"  CAN ID: {can_id}, DATA: {data}")
else:
    print("[FAIL] No clear CAN frame change detected after control action")

print("\n[INFO] Wireshark manual check: open Wireshark, select vcan0, and confirm CAN packets.")
score += 4

print("\n==============================")
print(f"FINAL SCORE: {score}/{total}")

if score >= 15:
    print("STATUS: PASS")
else:
    print("STATUS: INCOMPLETE")
