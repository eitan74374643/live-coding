"""
DavidAI GUI Launcher.
Launches the CustomTkinter interface for the DavidAI ecosystem.
"""
import sys
import threading
import time
import customtkinter as ctk
from davidai.core.orchestrator import DavidAI

# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class DavidAIGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DavidAI Command Center")
        self.geometry("1100x700")

        # Initialize Ecosystem Logic in a separate thread to keep UI responsive
        self.ecosystem = DavidAI()
        self.update_running = False

        # Grid Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()
        self.create_control_panel()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="DavidAI\nEcosystem", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.start_btn = ctk.CTkButton(self.sidebar, text="Start Cycle", command=self.start_ecosystem)
        self.start_btn.grid(row=1, column=0, padx=20, pady=10)

        self.pause_btn = ctk.CTkButton(self.sidebar, text="Pause/Resume", command=self.toggle_pause)
        self.pause_btn.grid(row=2, column=0, padx=20, pady=10)

        self.mode_var = ctk.StringVar(value="Fast")
        self.mode_menu = ctk.CTkOptionMenu(self.sidebar, values=["Fast", "Deep Logic"], variable=self.mode_var)
        self.mode_menu.grid(row=3, column=0, padx=20, pady=10)

        self.sidebar_status = ctk.CTkLabel(self.sidebar, text="Status: Idle")
        self.sidebar_status.grid(row=5, column=0, padx=20, pady=20)

    def create_main_area(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=20, pady=20)

        # Project Tree / File Map
        self.file_tree_label = ctk.CTkLabel(self.main_frame, text="Project Map / Live Feed", font=ctk.CTkFont(size=16, weight="bold"))
        self.file_tree_label.pack(anchor="w", padx=10, pady=5)

        self.file_tree = ctk.CTkTextbox(self.main_frame, font=("Consolas", 12))
        self.file_tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.file_tree.insert("end", "Waiting for ecosystem start...")

    def create_control_panel(self):
        self.metrics_frame = ctk.CTkFrame(self, corner_radius=0)
        self.metrics_frame.grid(row=2, column=1, sticky="nsew", padx=20, pady=(0, 20))

        self.metrics_frame.grid_columnconfigure(0, weight=1)
        self.metrics_frame.grid_columnconfigure(1, weight=1)
        self.metrics_frame.grid_columnconfigure(2, weight=1)

        # Metrics
        self.gpu_label = ctk.CTkLabel(self.metrics_frame, text="GPU: 0/12 GB")
        self.gpu_label.grid(row=0, column=0, padx=20, pady=10)

        self.cpu_label = ctk.CTkLabel(self.metrics_frame, text="CPU: 0%")
        self.cpu_label.grid(row=0, column=1, padx=20, pady=10)

        self.tps_label = ctk.CTkLabel(self.metrics_frame, text="TPS: 0")
        self.tps_label.grid(row=0, column=2, padx=20, pady=10)

        # Progress Bars
        self.progress_ceo = ctk.CTkProgressBar(self.metrics_frame)
        self.progress_ceo.grid(row=1, column=0, columnspan=3, sticky="ew", padx=20, pady=5)
        self.progress_ceo.set(0)
        ctk.CTkLabel(self.metrics_frame, text="CEO Logic Load").grid(row=2, column=0, columnspan=3)

    def start_ecosystem(self):
        if not self.update_running:
            self.update_running = True
            self.ecosystem.start_cycle()
            self.sidebar_status.configure(text="Status: Running")
            self.update_loop()

    def toggle_pause(self):
        self.ecosystem.pause_cycle()
        status = "Paused" if self.ecosystem.is_paused else "Running"
        self.sidebar_status.configure(text=f"Status: {status}")

    def update_loop(self):
        if not self.update_running:
            return

        # Update Metrics from Ecosystem
        status = self.ecosystem.get_status()

        # Simulate metric updates
        self.gpu_label.configure(text=f"GPU: {12 - (status.get('errors', 0) % 3)}/12 GB")
        self.cpu_label.configure(text=f"CPU: {30 + (status.get('agents_active', 0) * 10)}%")
        self.tps_label.configure(text=f"TPS: {status.get('tasks_completed', 0)}")

        # Update File Tree / Logs
        # Get the last few lines of logs from the dashboard
        logs = self.ecosystem.dashboard.logs[-5:]
        log_text = "\n".join(logs)
        self.file_tree.delete("1.0", "end")
        self.file_tree.insert("end", f"Mode: {self.mode_var.get()}\n\n" + log_text)

        # Schedule next update
        self.after(1000, self.update_loop)

if __name__ == "__main__":
    app = DavidAIGUI()
    app.mainloop()

