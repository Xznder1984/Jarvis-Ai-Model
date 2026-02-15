from __future__ import annotations

import threading
import tkinter as tk
from tkinter import messagebox, ttk

from jarvis_app.ai_engine import AISettings, JarvisAI
from jarvis_app.devices import detect_all
from jarvis_app.security import SecureVault


class JarvisApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Jarvis AI")
        self.geometry("960x640")
        self.configure(bg="#0b1020")

        self.settings = AISettings()
        self.ai = JarvisAI(self.settings)
        self.vault = SecureVault(master_password="jarvis-default-passphrase")

        self._build_ui()

    def _build_ui(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")

        container = ttk.Notebook(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        assistant_tab = ttk.Frame(container)
        devices_tab = ttk.Frame(container)
        settings_tab = ttk.Frame(container)

        container.add(assistant_tab, text="Assistant")
        container.add(devices_tab, text="Devices")
        container.add(settings_tab, text="Security & AI")

        self.chat_log = tk.Text(assistant_tab, bg="#101931", fg="#ccf2ff", insertbackground="white")
        self.chat_log.pack(fill="both", expand=True, padx=8, pady=8)

        input_frame = ttk.Frame(assistant_tab)
        input_frame.pack(fill="x", padx=8, pady=8)
        self.prompt_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.prompt_var).pack(side="left", fill="x", expand=True)
        ttk.Button(input_frame, text="Ask Jarvis", command=self._ask).pack(side="left", padx=6)

        self.devices_label = ttk.Label(devices_tab, text="Scan your camera/projector and authorize usage.")
        self.devices_label.pack(anchor="w", padx=8, pady=8)
        ttk.Button(devices_tab, text="Detect Devices", command=self._detect_devices).pack(anchor="w", padx=8)

        self.camera_allowed = tk.BooleanVar(value=False)
        self.proj_allowed = tk.BooleanVar(value=False)
        ttk.Checkbutton(devices_tab, text="Allow Camera", variable=self.camera_allowed).pack(anchor="w", padx=8, pady=3)
        ttk.Checkbutton(devices_tab, text="Allow Projector", variable=self.proj_allowed).pack(anchor="w", padx=8, pady=3)

        ttk.Label(settings_tab, text="Provider").grid(row=0, column=0, sticky="w", padx=8, pady=8)
        self.provider_var = tk.StringVar(value="local")
        ttk.Combobox(settings_tab, textvariable=self.provider_var, values=["local", "openai-compatible"]).grid(row=0, column=1)

        ttk.Label(settings_tab, text="Model").grid(row=1, column=0, sticky="w", padx=8, pady=8)
        self.model_var = tk.StringVar(value="jarvis-local-v1")
        ttk.Entry(settings_tab, textvariable=self.model_var, width=40).grid(row=1, column=1)

        ttk.Label(settings_tab, text="Endpoint").grid(row=2, column=0, sticky="w", padx=8, pady=8)
        self.endpoint_var = tk.StringVar(value="https://api.openai.com/v1/chat/completions")
        ttk.Entry(settings_tab, textvariable=self.endpoint_var, width=40).grid(row=2, column=1)

        ttk.Label(settings_tab, text="API key").grid(row=3, column=0, sticky="w", padx=8, pady=8)
        self.api_key_var = tk.StringVar()
        ttk.Entry(settings_tab, textvariable=self.api_key_var, width=40, show="*").grid(row=3, column=1)

        ttk.Button(settings_tab, text="Save Key Securely", command=self._save_key).grid(row=4, column=1, sticky="e", padx=8, pady=8)

    def _save_key(self) -> None:
        provider = self.provider_var.get().strip()
        key = self.api_key_var.get().strip()
        if not key:
            messagebox.showwarning("Jarvis", "Provide an API key first.")
            return
        self.vault.add_api_key(provider, key)
        messagebox.showinfo("Jarvis", f"Encrypted key saved for {provider}.")

    def _ask(self) -> None:
        prompt = self.prompt_var.get().strip()
        if not prompt:
            return
        self.settings.provider = self.provider_var.get().strip()
        self.settings.model = self.model_var.get().strip()
        self.settings.endpoint = self.endpoint_var.get().strip()
        api_key = self.vault.get_api_key(self.settings.provider)

        self.chat_log.insert("end", f"You: {prompt}\n")
        self.prompt_var.set("")

        def worker() -> None:
            answer = self.ai.chat(prompt, api_key=api_key)
            self.chat_log.insert("end", f"Jarvis: {answer}\n\n")
            self.chat_log.see("end")

        threading.Thread(target=worker, daemon=True).start()

    def _detect_devices(self) -> None:
        status = detect_all()
        cam_use = "Enabled" if self.camera_allowed.get() and status.camera_available else "Disabled"
        proj_use = "Enabled" if self.proj_allowed.get() and status.projector_available else "Disabled"
        self.devices_label.configure(
            text=(
                f"Camera available: {status.camera_available} ({cam_use})\n"
                f"Projector available: {status.projector_available} ({proj_use})\n"
                f"Details: {status.details}"
            )
        )


def run() -> None:
    app = JarvisApp()
    app.mainloop()
