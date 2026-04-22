import json

score = 0
total = 20

required_tags = {
    "Tank 1 Level Meter",
    "Tank 1 Fill Valve",
    "Tank 1 Discharge Valve",
    "<=",
    ">=",
    "SR",
    "BOOL",
    "AND"
}

print("=== Auto Marker: Activity 2 - Factory I/O Water Treatment Plant ===\n")

try:
    with open("student_output.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("[ERROR] student_output.json not found")
    exit()

# 1. Scene loaded
if "water treatment" in data.get("scene_loaded", "").lower():
    print("[PASS] Correct scene loaded")
    score += 3
else:
    print("[FAIL] Incorrect scene")

# 2. Tank configuration
if data.get("tank_config", "").lower() == "analog":
    print("[PASS] Tank set to Analog")
    score += 3
else:
    print("[FAIL] Tank not set to Analog")

# 3. Controller
if data.get("controller") == "Control I/O":
    print("[PASS] Control I/O selected")
    score += 3
else:
    print("[FAIL] Incorrect controller")

# 4. Required tags/blocks
student_tags = set(data.get("tags_present", []))
missing = required_tags - student_tags
if not missing:
    print("[PASS] All required tags/blocks present")
    score += 4
else:
    print(f"[FAIL] Missing tags/blocks: {', '.join(sorted(missing))}")

# 5. Logic behaviour
logic = data.get("logic_behaviour", {})
logic_ok = (
    logic.get("low_level_fill_on") is True and
    logic.get("low_level_discharge_off") is True and
    logic.get("high_level_fill_off") is True and
    logic.get("high_level_discharge_on") is True
)

if logic_ok:
    print("[PASS] Low/high level control logic correct")
    score += 4
else:
    print("[FAIL] Control logic behaviour incorrect")

# 6. System run
if data.get("system_running") is True and data.get("tank_fills_automatically") is True:
    print("[PASS] System runs and tank fills automatically")
    score += 3
else:
    print("[FAIL] System did not run correctly")

# 7. Emergency challenge
if data.get("emergency_button_added") is True and data.get("emergency_shutdown_working") is True:
    print("[PASS] Emergency shutdown implemented")
    score += 3
else:
    print("[FAIL] Emergency shutdown missing or not working")

print(f"\nFinal Score: {score}/{total}")

if score >= 16:
    print("Result: PASS")
else:
    print("Result: NEEDS IMPROVEMENT")