# Automark Scripts – CPS Activities

This repository contains automated marking scripts developed for Cyber-Physical Systems (CPS) lab activities. These scripts are designed to help validate and assess the configuration and functionality of industrial control system environments including Factory I/O, OpenPLC, ICSim, pfSense, Suricata, Splunk, and ICS pentesting tools.

---

# Activities Covered

- Activity 2 – Factory I/O Logic Validation
- Activity 3 – OpenPLC & Modbus Communication
- Activity 4 – CAN Bus (ICSim) Simulation & Analysis
- Activity 5 – Secure OT Environment (pfSense + Suricata)
- Activity 6 – Splunk & Threat Hunting
- Activity 7 – ICS Scanning & Vulnerability Identification
- Activity 8 – Industrial Network Attacks & Pentesting Validation

---

# Features

These scripts can automatically check:

- PLC communication and Modbus mapping
- Factory I/O configuration
- CAN traffic and replay activity
- pfSense firewall and network segmentation
- Suricata IDS alerts and logging
- Splunk log monitoring
- OpenPLC connectivity
- Metasploit, Nmap, and ICS scanning tools
- Nessus and Wireshark evidence files

The scripts provide:
- PASS / FAIL results
- Final scores
- Improvement recommendations
- Troubleshooting suggestions

---

# Requirements

Before running the scripts, ensure the following tools/services are installed depending on the activity:

- Python 3
- Factory I/O
- OpenPLC Runtime
- ICSim
- can-utils
- pfSense
- Suricata
- Splunk
- Metasploit Framework
- Nmap
- Modbus-cli
- Nessus (optional)
- Wireshark

---

# How to Download

Clone the repository:

```bash
git clone https://github.com/yeksonbagau/Automark-Script-CPS3010ICT.git
```

Open the project folder:

```bash
cd Automark-Script-CPS3010ICT
```

---

# How to Run

Open a terminal in the activity folder and run the Python script.

Example (Activity 2):

```bash
cd Activity2
python3 automark2.py
```

Example (Activity 3):

```bash
cd Activity3
python3 automark3.py
```

Example (Activity 4):

```bash
cd Activity4
python3 automark_activity4.py
```

Example (Activity 5):

```bash
cd Activity5
python3 automark_activity5.py
```

Example (Activity 6):

```bash
cd Activity6
python3 automark_activity6.py
```

Example (Activity 7):

```bash
cd Activity7
python3 automark_activity7.py
```

Example (Activity 8):

```bash
cd Activity8
python3 automark_activity8.py
```

---

# Example Output

```text
[PASS] OpenPLC Runtime reachable (+5)
[PASS] Modbus communication detected (+5)
[WARN] Suricata alert not detected
FINAL SCORE: 24/30
STATUS: PASS
```

---

# Purpose

The purpose of these scripts is to automate lab validation and assist students in verifying whether their CPS lab activities are configured correctly. These scripts are designed for educational and testing environments only.

---

# Disclaimer

These scripts are intended only for authorised educational lab environments and local virtual machines. They are not designed for attacking real industrial systems or public infrastructure.

---

# Author

Yekson Bagau  
Bachelor of Information Technology (Network&Cybersecurity)  
Griffith University
