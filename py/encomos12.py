import os
import sys
import shutil
import tkinter as tk
from datetime import datetime


class EncomOS12(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ENCOM OS-12")
        self.overrideredirect(True)
        self.configure(bg="#05070B")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.bind("<Escape>", lambda event: self.destroy())
        self.bind("<Control-l>", lambda event: self.clear_history())
        self.font_main = ("Courier", 12)
        self.font_small = ("Courier", 11)
        self.cursor_visible = True
        self.animation_queue = []
        self.animation_running = False
        self.create_ui()
        self.after(200, self.run_boot_sequence)
        self.blink_cursor()
        self.draw_scanlines()

    def create_ui(self):
        self.shell_border = tk.Frame(self, bg="#00eaff", highlightthickness=0)
        self.shell_border.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)
        self.shell = tk.Frame(self.shell_border, bg="#05070B")
        self.shell.pack(fill="both", expand=True, padx=2, pady=2)
        self.scanlines_canvas = tk.Canvas(self.shell, bg="#05070B", highlightthickness=0)
        self.scanlines_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.topbar = tk.Frame(self.shell, bg="#0E131F", height=44)
        self.topbar.pack(fill="x", padx=16, pady=(16, 8))
        self.topbar.pack_propagate(False)
        self.title_label = tk.Label(self.topbar, text="ENCOM OS-12 // QUANTUM TERMINAL", fg="#00eaff", bg="#0E131F", font=("Courier", 12, "bold"), anchor="w")
        self.title_label.pack(side="left", padx=12, pady=10)
        self.status_label = tk.Label(self.topbar, text="SECURE LINK ACTIVE", fg="#7dd3fc", bg="#0E131F", font=("Courier", 10))
        self.status_label.pack(side="left", padx=12, pady=10)
        self.close_button = tk.Button(self.topbar, text="[X]", fg="#ffffff", bg="#8b0000", bd=0, highlightthickness=0, activebackground="#b22222", activeforeground="#ffffff", font=("Courier", 11, "bold"), command=self.destroy)
        self.close_button.pack(side="right", padx=10, pady=8)
        self.main_panel = tk.Frame(self.shell, bg="#05070B", highlightbackground="#0E131F", highlightthickness=1)
        self.main_panel.pack(fill="both", expand=True, padx=16, pady=(0, 8))
        self.history = tk.Text(self.main_panel, bg="#05070B", fg="#00eaff", insertbackground="#00eaff", relief="flat", bd=0, wrap="word", font=self.font_small, padx=6, pady=6)
        self.history.pack(fill="both", expand=True)
        self.history.configure(state="disabled")
        self.history.tag_configure("prompt", foreground="#00eaff")
        self.history.tag_configure("output", foreground="#7dd3fc")
        self.history.tag_configure("error", foreground="#ff6b6b")
        self.history.tag_configure("system", foreground="#a7f3d0")
        self.history.tag_configure("warning", foreground="#fbbf24")
        self.input_frame = tk.Frame(self.shell, bg="#0E131F", highlightbackground="#00eaff", highlightthickness=1)
        self.input_frame.pack(fill="x", padx=16, pady=(0, 16))
        self.prompt_label = tk.Label(self.input_frame, text="ENCOM_ADMIN@GRID:~$ ", fg="#00eaff", bg="#0E131F", font=self.font_main, anchor="w")
        self.prompt_label.pack(side="left", padx=8, pady=6)
        self.command_entry = tk.Entry(self.input_frame, bg="#0E131F", fg="#00eaff", insertbackground="#00eaff", relief="flat", highlightthickness=0, font=self.font_main)
        self.command_entry.pack(side="left", fill="x", expand=True, padx=(0, 8), pady=6)
        self.command_entry.focus_set()
        self.command_entry.bind("<Return>", self.handle_command)
        self.bind("<Configure>", lambda event: self.draw_scanlines())

    def blink_cursor(self):
        self.cursor_visible = not self.cursor_visible
        color = "#00eaff" if self.cursor_visible else "#05070B"
        self.command_entry.configure(insertbackground=color)
        self.after(500, self.blink_cursor)

    def draw_scanlines(self):
        self.scanlines_canvas.delete("all")
        width = max(1, self.scanlines_canvas.winfo_width())
        height = max(1, self.scanlines_canvas.winfo_height())
        for y in range(0, height, 4):
            self.scanlines_canvas.create_line(0, y, width, y, fill="#0a0f16", width=1)
        for x in range(0, width, 120):
            self.scanlines_canvas.create_line(x, 0, x, height, fill="#071018", width=1)

    def run_boot_sequence(self):
        sequence = [
            "INITIALIZING QUANTUM CORE MATRIX...",
            "SYNCING NEURAL GRID INTERFACES...",
            "ESTABLISHING SECURE CHANNELS...",
            "LOADING ENCOM OS-12 RUNTIME...",
            "SYSTEM READY. WELCOME, ADMINISTRATOR.",
        ]
        self.write_line("=== ENCOM OS-12 BOOT SEQUENCE ===", "system", animate=False)
        for index, line in enumerate(sequence):
            self.after(index * 220 + 220, lambda value=line: self.write_line(value, "output"))

    def write_line(self, text, tag="output", animate=True):
        if animate:
            self.animation_queue.append((text, tag))
            if not self.animation_running:
                self.animation_running = True
                self._process_animation_queue()
        else:
            self.history.configure(state="normal")
            self.history.insert("end", text + "\n", tag)
            self.history.see("end")
            self.history.configure(state="disabled")

    def _process_animation_queue(self):
        if not self.animation_queue:
            self.animation_running = False
            return
        text, tag = self.animation_queue.pop(0)
        self.history.configure(state="normal")
        self._type_index = 0
        self._type_text = text
        self._type_tag = tag
        self._type_step()

    def _type_step(self):
        if self._type_index < len(self._type_text):
            self.history.insert("end", self._type_text[self._type_index], self._type_tag)
            self.history.see("end")
            self._type_index += 1
            self.after(10, self._type_step)
        else:
            self.history.insert("end", "\n", self._type_tag)
            self.history.see("end")
            self.history.configure(state="disabled")
            self.after(80, self._process_animation_queue)

    def clear_history(self):
        self.history.configure(state="normal")
        self.history.delete("1.0", "end")
        self.history.configure(state="disabled")

    def handle_command(self, event=None):
        command = self.command_entry.get().strip()
        if not command:
            self.command_entry.delete(0, "end")
            return
        self.write_line("ENCOM_ADMIN@GRID:~$ " + command, "prompt", animate=False)
        self.command_entry.delete(0, "end")
        self.process_command(command)

    def process_command(self, command):
        cmd = command.lower()
        if cmd == "help":
            self.write_line("AVAILABLE COMMANDS: help, clear, exit, system_status, whoami, date, reboot, scan, network, matrix, cpu, memory, ping, mkdir, ls, cat, pwd, flynn, tron, mcp, clu", "system")
        elif cmd == "clear":
            self.clear_history()
            self.write_line("HISTORY CLEARED.", "system", animate=False)
        elif cmd == "exit":
            self.destroy()
        elif cmd == "system_status":
            self.write_line("SERVER STATUS: QUANTUM CORE ONLINE", "system")
            self.write_line("CPU LOAD: 27%", "system")
            self.write_line("MEMORY: 63%", "system")
            self.write_line("GRID LATENCY: 4.2 ms", "system")
        elif cmd == "whoami":
            self.write_line("ENCOM ADMINISTRATOR", "system")
        elif cmd == "date":
            self.write_line(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "warning")
        elif cmd == "reboot":
            self.write_line("REBOOTING QUANTUM CORE...", "warning", animate=False)
            self.after(1000, self.restart_system)
        elif cmd == "scan":
            self.write_line("SCAN COMPLETE: 12 NODES ONLINE", "system")
            self.write_line("THREAT LEVEL: LOW", "system")
        elif cmd == "network":
            self.write_line("NETWORK STATUS: SECURE CHANNELS ACTIVE", "system")
            self.write_line("NODE COUNT: 12", "system")
            self.write_line("PACKET LOSS: 0%", "system")
        elif cmd == "matrix":
            self.write_line("MATRIX MODE ENGAGED", "system")
            self.write_line("GRID HARMONICS STABLE", "system")
        elif cmd == "cpu":
            self.write_line("CPU LOAD: 27%", "system")
            self.write_line("THERMAL STATE: OPTIMAL", "system")
        elif cmd == "memory":
            self.write_line("RAM USAGE: 63%", "system")
            self.write_line("CACHE STATUS: NORMAL", "system")
        elif cmd == "ping":
            self.write_line("PINGING GRID NODE 01...", "warning")
            self.write_line("RESPONSE: 4.2 ms", "system")
        elif cmd.startswith("mkdir"):
            parts = cmd.split()
            if len(parts) < 2:
                self.write_line("USAGE: mkdir <name>", "error")
            else:
                path = parts[1]
                try:
                    os.makedirs(path, exist_ok=True)
                    self.write_line(f"DIRECTORY CREATED: {path}", "system")
                except OSError as exc:
                    self.write_line(f"FAILED TO CREATE DIRECTORY: {exc}", "error")
        elif cmd == "ls":
            entries = sorted(os.listdir("."))
            if entries:
                self.write_line(" ".join(entries), "system")
            else:
                self.write_line("NO FILES FOUND", "system")
        elif cmd.startswith("cat"):
            parts = cmd.split(maxsplit=1)
            if len(parts) < 2:
                self.write_line("USAGE: cat <file>", "error")
            else:
                file_path = parts[1]
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    with open(file_path, "r", encoding="utf-8") as handle:
                        self.write_line(handle.read().strip(), "system")
                else:
                    self.write_line("FILE NOT FOUND", "error")
        elif cmd == "pwd":
            self.write_line(os.getcwd(), "system")
        elif cmd == "flynn":
            self.write_line("FLYNN LIVES", "system")
        elif cmd == "tron":
            self.write_line("I fight for the Users!", "system")
        elif cmd == "mcp":
            self.write_line("ALERT: INTRUSION DETECTED IN THE MCP CHANNEL", "error")
        elif cmd == "clu":
            self.write_line("THE SYSTEM IS PERFECT. ERROR IS A HUMAN CONCEPT.", "system")
        else:
            self.write_line("COMMAND NOT FOUND. TYPE help FOR ACCESS", "error")

    def restart_system(self):
        self.destroy()
        os.execv(sys.executable, [sys.executable, __file__] + sys.argv[1:])


if __name__ == "__main__":
    app = EncomOS12()
    app.mainloop()
