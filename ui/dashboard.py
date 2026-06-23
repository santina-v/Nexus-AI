import customtkinter as ctk
import threading
import psutil
from core.ai import ChatEngine
from core.automation import AutomationEngine
from core.documents import DocumentAnalyzer
from tkinter import filedialog

# Theme setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NexusAIDashboard:
    def __init__(self):
        self.ai = ChatEngine()
        self.auto = AutomationEngine()
        self.doc_analyzer = DocumentAnalyzer()

        self.window = ctk.CTk()
        self.window.title("NEXUS AI — Offline Assistant")
        self.window.geometry("1280x720")
        self.window.configure(fg_color="#0a0a0f")

        self.build_ui()

    def build_ui(self):
        # Title bar
        title = ctk.CTkLabel(
            self.window,
            text="⬡  NEXUS AI — OFFLINE ASSISTANT",
            font=ctk.CTkFont(family="Consolas", size=24, weight="bold"),
            text_color="#00f7ff"
        )
        title.pack(pady=10)

        # System stats bar
        self.stats_label = ctk.CTkLabel(
            self.window,
            text="CPU: 0%  |  RAM: 0%  |  STATUS: ONLINE",
            font=ctk.CTkFont(family="Courier", size=11),
            text_color="#00c8ff"
        )
        self.stats_label.pack()

        # Tab view
        self.tabs = ctk.CTkTabview(
            self.window, 
            fg_color="#0d1117",
            segmented_button_fg_color="#111827",
            segmented_button_selected_color="#00e5ff",
            segmented_button_selected_hover_color="#00bcd4",
            segmented_button_unselected_color="#1f2937",
            text_color="#ffffff"
        )
        self.tabs.pack(fill="both", expand=True, padx=15, pady=10)

        self.tabs.add("💬  CHAT")
        self.tabs.add("🖥  AUTOMATE")
        self.tabs.add("📄  DOCUMENTS")

        self.build_chat_tab()
        self.build_automation_tab()
        self.build_documents_tab()

        # Start stats updater
        self.update_stats()

    # ── CHAT TAB ──────────────────────────────────────────────────────────────

    def build_chat_tab(self):
        tab = self.tabs.tab("💬  CHAT")

        self.chat_display = ctk.CTkTextbox(
            tab,
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color="#020b14",
            text_color="#00e5ff",
            border_width=1,
            border_color="#00e5ff",
            corner_radius=12,
            wrap="word"
        )
        self.chat_display.pack(fill="both", expand=True, pady=(0, 10))
        self.chat_display.insert("end", "NEXUS AI ready. Type your message below.\n\n")
        self.chat_display.configure(state="disabled")

        input_frame = ctk.CTkFrame(tab, fg_color="transparent")
        input_frame.pack(fill="x")

        self.chat_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="Ask anything...",
            font=ctk.CTkFont(family="Courier", size=12),
            fg_color="#07121f",
            border_color="#00f7ff",
            border_width=2,
            text_color="#00f7ff",
            corner_radius=12,
            height=42,
        )
        self.chat_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.chat_input.bind("<Return>", lambda e: self.send_message())

        send_btn = ctk.CTkButton(
            input_frame,
            text="SEND ▶",
            command=self.send_message,
            fg_color="#00e5ff",
            hover_color="#00bcd4",
            text_color="#02131f",
            corner_radius=12,
            height=42,
            font=ctk.CTkFont(
                family="Consolas",
                size=13,
                weight="bold"
            ),
        )
        send_btn.pack(side="right")

    def send_message(self):
        message = self.chat_input.get().strip()
        if not message:
            return

        self.chat_input.delete(0, "end")
        self.append_chat(f"YOU › {message}\n")

        def get_response():
            self.append_chat("NEXUS › thinking...\n")
            reply = self.ai.chat(message)
            self.chat_display.configure(state="normal")
            content = self.chat_display.get("1.0", "end")
            content = content.replace("NEXUS › thinking...\n", "")
            self.chat_display.delete("1.0", "end")
            self.chat_display.insert("end", content)
            self.chat_display.configure(state="disabled")
            self.append_chat(f"NEXUS › {reply}\n\n")

        threading.Thread(target=get_response, daemon=True).start()

    def append_chat(self, text):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", text)
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

    # ── AUTOMATION TAB ────────────────────────────────────────────────────────

    def build_automation_tab(self):
        tab = self.tabs.tab("🖥  AUTOMATE")

        label = ctk.CTkLabel(
            tab,
            text="Click a button to control your desktop",
            font=ctk.CTkFont(family="Courier", size=12),
            text_color="#4a8a99"
        )
        label.pack(pady=10)

        buttons = [
            ("📸  Take Screenshot", "screenshot"),
            ("🌐  Open Browser", "open browser"),
            ("📋  Read Clipboard", "clipboard"),
        ]

        for btn_text, cmd in buttons:
            ctk.CTkButton(
                tab,
                text=btn_text,
                command=lambda c=cmd: self.run_automation(c),
                fg_color="#081520",
                hover_color="#0ea5e9",
                border_width=1,
                border_color="#00e5ff",
                corner_radius=14,
                height=50,
                text_color="#00e5ff",
                font=ctk.CTkFont(
                    family="Consolas",
                    size=14,
                    weight="bold"
                ),
            ).pack(fill="x", padx=40, pady=8)

        self.auto_log = ctk.CTkTextbox(
            tab,
            font=ctk.CTkFont(family="Courier", size=11),
            fg_color="#020c12",
            text_color="#4a8a99",
            height=150
        )
        self.auto_log.pack(fill="x", padx=0, pady=10)
        self.auto_log.insert("end", "Automation log ready...\n")

    def run_automation(self, command):
        result = self.auto.execute_command(command)
        self.auto_log.configure(state="normal")
        self.auto_log.insert("end", f"✓ {result}\n")
        self.auto_log.see("end")

    # ── DOCUMENTS TAB ─────────────────────────────────────────────────────────

    def build_documents_tab(self):
        tab = self.tabs.tab("📄  DOCUMENTS")

        ctk.CTkLabel(
            tab,
            text="Upload a PDF or TXT file to summarize",
            font=ctk.CTkFont(family="Courier", size=12),
            text_color="#4a8a99"
        ).pack(pady=10)

        ctk.CTkButton(
            tab,
            text="⬆  UPLOAD FILE",
            command=self.upload_document,
            fg_color="#00e5ff",
            text_color="#020a0f",
            font=ctk.CTkFont(family="Courier", size=13, weight="bold"),
            height=45
        ).pack(pady=10)

        self.doc_display = ctk.CTkTextbox(
            tab,
            fg_color="#020b14",
            text_color="#00e5ff",
            border_width=1,
            border_color="#00e5ff",
            corner_radius=12,
            font=ctk.CTkFont(
                family="Consolas",
                size=12
            ),
            wrap="word"
        )
        self.doc_display.pack(fill="both", expand=True)
        self.doc_display.insert("end", "Document summary will appear here...\n")

    def upload_document(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf"), ("Text files", "*.txt")]
        )
        if not file_path:
            return

        self.doc_display.delete("1.0", "end")
        self.doc_display.insert("end", "Analyzing document...\n")

        def analyze():
            result = self.doc_analyzer.analyze(file_path)
            self.doc_display.delete("1.0", "end")
            self.doc_display.insert("end", result)

        threading.Thread(target=analyze, daemon=True).start()

    # ── SYSTEM STATS ──────────────────────────────────────────────────────────

    def update_stats(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        self.stats_label.configure(
            text=f"CPU: {cpu}%  |  RAM: {ram}%  |  MODEL: phi3:mini  |  STATUS: ONLINE"
        )
        self.window.after(2000, self.update_stats)

    def run(self):
        self.window.mainloop()