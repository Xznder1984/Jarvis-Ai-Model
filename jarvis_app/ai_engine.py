from __future__ import annotations

from dataclasses import dataclass

import requests


@dataclass
class AISettings:
    provider: str = "local"
    model: str = "jarvis-local-v1"
    endpoint: str = "https://api.openai.com/v1/chat/completions"


class JarvisAI:
    def __init__(self, settings: AISettings) -> None:
        self.settings = settings

    def chat(self, prompt: str, api_key: str | None = None) -> str:
        if self.settings.provider == "local" or not api_key:
            return self._local_response(prompt)

        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.settings.model,
            "messages": [
                {"role": "system", "content": "You are Jarvis, a concise and helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        }

        try:
            response = requests.post(self.settings.endpoint, headers=headers, json=payload, timeout=25)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as exc:
            return f"Cloud provider unavailable. Falling back to local AI. Details: {exc}\n\n{self._local_response(prompt)}"

    def _local_response(self, prompt: str) -> str:
        lower = prompt.lower()
        if "status" in lower:
            return "All systems look stable. Sensors standby, AI core online."
        if "camera" in lower:
            return "Camera can be enabled from the Devices panel if you grant permission."
        if "projector" in lower:
            return "Projector mode activates when an external display is detected and allowed."
        return f"Local Jarvis response: I heard '{prompt}'. Ask me for status, camera, or projector support."
