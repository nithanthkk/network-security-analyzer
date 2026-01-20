import tkinter as tk
from tkinter import messagebox
import threading
import time

from scanner_engine import run_nmap_scan, analyze_risk
from wireless_engine import run_wireless_scan
from network_mapper import map_network

# ================= GLOBAL STATE =================
scan_running = False
selected_network = None

# ================= THEME =================
BG = "#050608"
PANEL = "#0b0f14"
GREEN = "#00ff9c"
CYAN = "#00cfff"
GRAY = "#2a2f36"
TEXT = "#9efae0"

FONT_TITLE = ("Consolas", 16, "bold")
FONT = ("Consolas", 10)
FONT_BTN = ("Consolas", 10, "bold")

# ================= TERMINAL EFFECT =================
def log(msg, delay=0.003):
    for c in msg:
        terminal.insert(tk.END, c)
        terminal.see(tk.END)
        terminal.update()
        time.sleep(delay)
    terminal.insert(tk.END, "\n")

# ================= SCAN LOGIC =================
def stop_scan():
    global scan_running
    scan_running = False
    log("[!] Scan stopped by user.")

def wired_scan(target):
    log(f"[*] Running Nmap scan on {target}...\n")
    results = run_nmap_scan(target)

    if not results:
        log("[!] No open ports found.")
    else:
        for r in results:
            if not scan_running:
                return
            risk = analyze_risk(r["service"])
            log(f"[+] {r['port']} | {r['service']} {r['version']} | RISK: {risk}")

    finish()

def start_wired():
    global scan_running
    if scan_running:
        return

    target = target_entry.get().strip()
    if not target:
        messagebox.showerror("Error", "Enter target IP or subnet")
        return

    scan_running = True
    terminal.delete("1.0", tk.END)
    threading.Thread(target=wired_scan, args=(target,), daemon=True).start()

def wireless_scan():
    global selected_network
    log("[*] Starting wireless reconnaissance...\n")

    nets = run_wireless_scan()
    if not nets:
        log("[!] No wireless networks detected.")
        finish()
        return

    for i, n in enumerate(nets):
        log(f"[{i}] SSID: {n['ssid'] or 'Hidden'} | "
            f"BSSID: {n['bssid']} | CH: {n['channel']} | "
            f"ENC: {n['encryption']} | PWR: {n['power']}")

    selected_network = nets[0]
    log("\n[*] Network selected:")
    log(str(selected_network))
    finish()

def start_wireless():
    global scan_running
    if scan_running:
        return

    scan_running = True
    terminal.delete("1.0", tk.END)
    threading.Thread(target=wireless_scan, daemon=True).start()

def map_selected_network():
    if not selected_network:
        messagebox.showinfo("Info", "Run wireless scan first.")
        return

    log("\n[*] Mapping internal network...\n")
    data = map_network()

    if not data:
        log("[!] Not connected to any network.")
        return

    log(f"Interface : {data['interface']}")
    log(f"Local IP  : {data['local_ip']}")
    log(f"Gateway   : {data['gateway']}")
    log(f"Subnet    : {data['subnet']}")

    log("\nConnected Devices:")
    for d in data["devices"]:
        log(f"{d['ip']} | {d['mac']} | {d['state']}")

def finish():
    global scan_running
    scan_running = False
    log("\n[*] Operation completed.")

# ================= UI HELPERS =================
def hacker_button(parent, text, cmd, color):
    btn = tk.Button(
        parent, text=text, command=cmd,
        bg=color, fg=BG, font=FONT_BTN,
        activebackground=CYAN, bd=0, height=2
    )

    def on_enter(e): btn.config(bg=CYAN)
    def on_leave(e): btn.config(bg=color)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

# ================= APP =================
app = tk.Tk()
app.title("Network Security Analyzer")
app.geometry("1200x650")
app.configure(bg=BG)
app.resizable(False, False)

# ================= HEADER =================
header = tk.Frame(app, bg=BG)
header.pack(fill="x", pady=10)

tk.Label(header, text="NETWORK SECURITY ANALYZER",
         fg=GREEN, bg=BG, font=FONT_TITLE).pack()

tk.Label(header, text="Wired & Wireless Recon | Authorized Use Only",
         fg=CYAN, bg=BG, font=("Consolas", 9)).pack()

# ================= MAIN =================
main = tk.Frame(app, bg=BG)
main.pack(fill="both", expand=True)

# ================= CONTROL PANEL =================
panel = tk.Frame(main, bg=PANEL, width=280)
panel.pack(side="left", fill="y", padx=10, pady=10)
panel.pack_propagate(False)

# ================= TERMINAL =================
terminal_frame = tk.Frame(main, bg=BG)
terminal_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

terminal = tk.Text(
    terminal_frame,
    bg=BG,
    fg=TEXT,
    insertbackground=GREEN,
    font=FONT,
    wrap="word",
    bd=0
)
terminal.pack(fill="both", expand=True)

# ================= WIRED UI =================
tk.Label(panel, text="WIRED SCAN (NMAP)",
         fg=GREEN, bg=PANEL, font=FONT_BTN).pack(anchor="w", pady=(20, 5), padx=10)

target_entry = tk.Entry(
    panel, bg=BG, fg=GREEN,
    insertbackground=GREEN, font=FONT, bd=0
)
target_entry.pack(fill="x", padx=10, pady=5)

hacker_button(panel, "START NMAP SCAN", start_wired, GREEN)\
    .pack(fill="x", padx=10, pady=5)

hacker_button(panel, "STOP SCAN", stop_scan, GRAY)\
    .pack(fill="x", padx=10, pady=5)

# ================= WIRELESS UI =================
tk.Label(panel, text="WIRELESS SCAN (Wi-Fi)",
         fg=GREEN, bg=PANEL, font=FONT_BTN).pack(anchor="w", pady=(30, 5), padx=10)

hacker_button(panel, "START WIRELESS SCAN", start_wireless, GREEN)\
    .pack(fill="x", padx=10, pady=5)

hacker_button(panel, "MAP NETWORK", map_selected_network, CYAN)\
    .pack(fill="x", padx=10, pady=15)

# ================= RUN =================
app.mainloop()
