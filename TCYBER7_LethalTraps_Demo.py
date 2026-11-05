#!/usr/bin/env python3
"""
===============================================================================
TCYBER7 - THE 10 LETHAL CYBER TRAPS SUITE (SAFE DEMO VERSION)
===============================================================================
Author      : TCYBER7
Version     : 1.0.0 (Demo Release)
License     : Demo / Educational & Evaluation Purpose Only
Description : Fully automated, multi-threaded active defense simulation.
              Runs safely on Windows, macOS, and Android (Pydroid) without root.
              No system changes are made.
===============================================================================
"""

import os
import sys
import time
import socket
import shutil
import logging
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

# =============================================================================
# CONFIGURATION & SETUP
# =============================================================================
LOG_PATH = 'tcyber7_traps_demo.log'

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [DEMO-TRAP-%(name)s] %(message)s'
)

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

# =============================================================================
# CORE DEMO ENGINE
# =============================================================================
class LethalCyberTrapsDemo:
    def __init__(self):
        self.running = True
        self.active_threads = []

    def log(self, trap_name, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = Colors.YELLOW if level == "ALERT" else Colors.CYAN
        print(f"[{timestamp}] [{color}DEMO: {trap_name}{Colors.RESET}] {message}")
        logging.info(f"{trap_name}: {message}")

    # 1. PUNJI STICK PIT (Directory Sinkhole Simulation)
    def trap_punji_pit(self):
        base_path = "./demo_hidden_pit"
        try:
            target_dir = os.path.join(base_path, "void_1", "void_2")
            os.makedirs(target_dir, exist_ok=True)
            with open(os.path.join(target_dir, "secret_payload.txt"), "w") as f:
                f.write("[SIMULATION] You have fallen into the demo Punji Stick Pit.\n")
            self.log("Punji Stick Pit", f"Simulated sinkhole deployed at {base_path}")
        except Exception as e:
            self.log("Punji Stick Pit", f"Error: {e}", "ALERT")

    # 2. FLAGPOLE MINE (Honey-Credential Tripwire)
    def trap_bouncing_betty(self):
        def monitor_file():
            filepath = "./demo_db_config.bak"
            try:
                with open(filepath, "w") as f:
                    f.write("DB_USER=root\nDB_PASS=DEMO_HONEY_TRAP_PASSWORD\n")
                self.log("Bouncing Betty", f"Tripwire planted at {filepath}. Monitoring...")
                initial_atime = os.path.getatime(filepath)
                
                while self.running:
                    time.sleep(3)
                    if not os.path.exists(filepath): continue
                    current_atime = os.path.getatime(filepath)
                    if current_atime != initial_atime:
                        self.log("Bouncing Betty", f"ALERT! Unauthorized read access detected on {filepath}", "ALERT")
                        initial_atime = current_atime
            except Exception:
                pass
        
        t = threading.Thread(target=monitor_file, daemon=True)
        t.start()
        self.active_threads.append(t)

    # 3. MACE / SPIKE BALL (Resource Exhaustion Defender)
    def trap_mace(self):
        def process_hunter():
            self.log("Mace Trap", "Monitoring for CPU abusers (Simulation Mode)...")
            while self.running:
                time.sleep(15)
                self.log("Mace Trap", "[SIMULATION] Scanned processes. No rogue CPU spikes detected.")
        
        t = threading.Thread(target=process_hunter, daemon=True)
        t.start()
        self.active_threads.append(t)

    # 4. TOE POPPER (Instant IP Banishment Port)
    def trap_toe_popper(self, port=1337):
        def listener():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(("0.0.0.0", port))
                s.listen(1)
                s.settimeout(2.0)
                self.log("Toe Popper", f"Listening on simulated bait port {port}...")
                while self.running:
                    try:
                        conn, addr = s.accept()
                        ip = addr[0]
                        self.log("Toe Popper", f"Intruder from {ip} on port {port}! [SIMULATING iptables DROP]", "ALERT")
                        conn.send(b"WARNING: IP Logged by TCYBER7 Sentinels.\n")
                        conn.close()
                    except socket.timeout:
                        continue
            except Exception:
                self.log("Toe Popper", f"Failed to bind port {port}. Port may be in use.")
            finally:
                s.close()

        t = threading.Thread(target=listener, daemon=True)
        t.start()
        self.active_threads.append(t)

    # 5. GRENADE IN A CAN (Quarantine Trigger)
    def trap_grenade(self):
        watch_dir = "./demo_uploads"
        quarantine_dir = "./demo_quarantine"
        
        def directory_watcher():
            os.makedirs(watch_dir, exist_ok=True)
            os.makedirs(quarantine_dir, exist_ok=True)
            self.log("Grenade in a Can", f"Armed! Drop any .php or .exe file in {watch_dir} to test quarantine.")
            while self.running:
                time.sleep(3)
                try:
                    for filename in os.listdir(watch_dir):
                        if filename.endswith(('.php', '.sh', '.elf', '.exe', '.txt')):
                            file_path = os.path.join(watch_dir, filename)
                            dest_path = os.path.join(quarantine_dir, filename + ".quarantined")
                            shutil.move(file_path, dest_path)
                            self.log("Grenade in a Can", f"Malicious drop detected! Quarantined: {filename}", "ALERT")
                except Exception:
                    pass

        t = threading.Thread(target=directory_watcher, daemon=True)
        t.start()
        self.active_threads.append(t)

    # 6. DOORWAY BOOBY TRAP (Fake Admin Portal HTTP Server)
    def trap_doorway(self, port=8080):
        class FakeLoginHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                html = "<html><body><h1>Admin Web Portal (Demo Mode)</h1><form method='POST'><input type='text' name='user' placeholder='Username'/><input type='password' name='pass' placeholder='Password'/><input type='submit'/></form></body></html>"
                self.wfile.write(html.encode())
                
            def do_POST(self):
                client_ip = self.client_address[0]
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode()
                print(f"[{Colors.YELLOW}DEMO: Doorway Trap{Colors.RESET}] Captured Fake Credentials from {client_ip}: {post_data}")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Access Denied. Demo Incident Logged.")
                
            def log_message(self, format, *args):
                pass 

        def run_server():
            try:
                server = HTTPServer(('0.0.0.0', port), FakeLoginHandler)
                server.timeout = 2.0
                self.log("Doorway Trap", f"Fake Admin Portal deployed on HTTP port {port}. Test via browser at http://localhost:{port}")
                while self.running:
                    server.handle_request()
            except Exception:
                pass
                
        t = threading.Thread(target=run_server, daemon=True)
        t.start()
        self.active_threads.append(t)

    # 7. SNAKE PIT (Tar Pit / Connection Slowdown)
    def trap_snake_pit(self, port=8888):
        def tarpit():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(("0.0.0.0", port))
                s.listen(5)
                s.settimeout(2.0)
                self.log("Snake Pit", f"Tar Pit active on port {port}. Ready to entangle scanners...")
                while self.running:
                    try:
                        conn, addr = s.accept()
                        self.log("Snake Pit", f"Trapped scanner from {addr[0]}. [SIMULATING Infinite Socket Hold]", "ALERT")
                        # We close it after 5 seconds in demo mode to prevent overloading Pydroid
                        time.sleep(5)
                        conn.close()
                    except socket.timeout:
                        continue
            except Exception:
                pass
            finally:
                s.close()
                
        t = threading.Thread(target=tarpit, daemon=True)
        t.start()
        self.active_threads.append(t)

    # 8. FIRE TRAP (Automated Panic Lockdown)
    def trap_fire(self):
        self.log("Fire Trap", "[SIMULATION] System threat threshold normal. Firewall purge standing by.")

    # 9. AMBUSH ENVELOPMENT (Log Counter-Audit)
    def trap_ambush(self):
        self.log("Ambush Envelopment", "[SIMULATION] Correlating mock telemetry from auth, syslog, and web server.")

    # 10. FALSE ABANDONED EQUIPMENT (Honey-Tokens)
    def trap_equipment(self):
        token_dir = "./demo_aws_keys"
        token_file = os.path.join(token_dir, "credentials")
        try:
            os.makedirs(token_dir, exist_ok=True)
            with open(token_file, "w") as f:
                f.write("[default]\naws_access_key_id = DEMO_AKIA_HONEY_TOKEN\naws_secret_access_key = SIMULATED_TRAP_SECRET_KEY\n")
            self.log("False Equipment", f"AWS Honey-credentials planted at {token_file}")
        except Exception:
            pass

    # SYSTEM START/STOP
    def arm_all(self):
        self.trap_punji_pit()
        self.trap_bouncing_betty()
        self.trap_mace()
        self.trap_toe_popper()
        self.trap_grenade()
        self.trap_doorway()
        self.trap_snake_pit()
        self.trap_fire()
        self.trap_ambush()
        self.trap_equipment()
        
    def stop_all(self):
        self.running = False
        print(f"\n{Colors.YELLOW}[TCYBER7] Disarming Demo Traps and shutting down cleanly...{Colors.RESET}")
        time.sleep(2) 

# =============================================================================
# MAIN EXECUTION ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colors.CYAN + "=" * 75)
    print("    TCYBER7 - THE 10 LETHAL CYBER TRAPS DEFENSE SUITE (SAFE DEMO)    ")
    print("=" * 75 + Colors.RESET)
    
    demo = LethalCyberTrapsDemo()
    demo.arm_all()
    
    print("-" * 75)
    print(f"[{Colors.GREEN}DEMO ARMED{Colors.RESET}] All 10 Sentinels are running safely in simulation mode.")
    print("Try opening http://localhost:8080 in your browser to trigger the Doorway Trap.")
    print(f"Try creating a .txt file inside the './demo_uploads' folder to trigger the Grenade Trap.")
    print("Press Ctrl+C (or Stop button) to terminate.")
    print("-" * 75)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        demo.stop_all()
        print(f"[{Colors.GREEN}OFFLINE{Colors.RESET}] Demo terminated safely. Log saved to: {os.path.abspath(LOG_PATH)}")
        sys.exit(0)