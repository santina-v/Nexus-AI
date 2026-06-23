import pyautogui
import subprocess
import platform

class AutomationEngine:

    def take_screenshot(self):
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        return "Screenshot saved as screenshot.png"

    def open_browser(self):
        system = platform.system()
        if system == "Windows":
            subprocess.Popen(["start", "chrome"], shell=True)
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", "Google Chrome"])
        else:
            subprocess.Popen(["google-chrome"])
        return "Browser opened"

    def type_text(self, text):
        pyautogui.typewrite(text, interval=0.05)
        return f"Typed: {text}"

    def execute_command(self, command):
        command = command.lower()

        if "screenshot" in command:
            return self.take_screenshot()
        elif "browser" in command or "chrome" in command:
            return self.open_browser()
        elif "type" in command:
            text = command.replace("type", "").strip()
            return self.type_text(text)
        else:
            return "Command not recognized"