import socket
import requests
from pymodbus.client import ModbusTcpClient

# --- FINAL VERIFIED CONFIGURATION ---
OPENPLC_IP = "192.168.10.100"  # Corrected based on your browser screenshot
FACTORYIO_IP = "192.168.10.107" # Your Windows VM IP
WEB_PORT = 8080
MODBUS_PORT = 503

def run_assessment():
    score = 0
    total = 20
    print("=== FINAL ASSESSMENT: ACTIVITY 3 (AZURE VM LINK) ===\n")

    # 1. Connectivity to OpenPLC (Ubuntu)
    print(f"[*] Testing connection to OpenPLC Dashboard ({OPENPLC_IP})...")
    try:
        r = requests.get(f"http://{OPENPLC_IP}:{WEB_PORT}/monitoring", timeout=3)
        if r.status_code == 200:
            print("[PASS] OpenPLC Monitoring Page is LIVE (+5 pts)")
            score += 5
    except Exception as e:
        print(f"[FAIL] OpenPLC unreachable. Error: {e}")

    # 2. Connectivity to Factory I/O Modbus Server (Windows)
    print(f"[*] Testing Modbus Server on Port {MODBUS_PORT}...")
    client = ModbusTcpClient(FACTORYIO_IP, port=MODBUS_PORT)
    if client.connect():
        print(f"[PASS] Factory I/O Modbus Server is active (+5 pts)")
        score += 5
        
        # 3. Live Data Validation (Reading WL Register 100)
        # We use read_input_registers for %IW100
        res = client.read_input_registers(100, 1)
        if not res.isError():
            wl_val = res.registers[0]
            print(f"[PASS] Successfully read live WL Value: {wl_val} (+5 pts)")
            score += 5
            
            # 4. State Validation (Is the simulation actually moving?)
            if wl_val > 0:
                print("[PASS] Verified: Live data exchange is functional (+5 pts)")
                score += 5
            else:
                print("[WARN] WL is 0. Ensure the water tank has started filling.")
        else:
            print("[FAIL] Modbus Read Error. Check if tags are mapped to 100.")
        client.close()
    else:
        print(f"[FAIL] Could not connect to Modbus on {FACTORYIO_IP}:{MODBUS_PORT}")

    # --- FINAL SCORE ---
    print("\n" + "="*40)
    print(f"FINAL SCORE: {score}/{total}")
    print("="*40)
    if score == 20:
        print("STATUS: SUCCESS - Communication Link Fully Verified")
    else:
        print("STATUS: INCOMPLETE - Check Network or Port 503 Settings")

if __name__ == "__main__":
    run_assessment()