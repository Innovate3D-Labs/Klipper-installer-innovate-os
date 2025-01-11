import asyncio
import os
from typing import Optional, Callable
import logging

class KlipperInstaller:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.installation_process: Optional[asyncio.subprocess.Process] = None
        self.status_callback: Optional[Callable] = None

    async def install_dependencies(self):
        """Installiert alle notwendigen Abhängigkeiten"""
        cmd = "sudo apt-get update && sudo apt-get install -y git python3-pip"
        await self._run_command(cmd)

    async def clone_klipper(self):
        """Klont das Klipper-Repository"""
        if not os.path.exists("~/klipper"):
            cmd = "git clone https://github.com/Klipper3d/klipper.git ~/klipper"
            await self._run_command(cmd)

    async def compile_firmware(self, config_path: str):
        """Kompiliert die Firmware mit der angegebenen Konfiguration"""
        # Kopiere die Konfiguration
        cmd = f"cp {config_path} ~/klipper/.config"
        await self._run_command(cmd)
        
        # Kompiliere
        cmd = "cd ~/klipper && make"
        await self._run_command(cmd)

    async def install_service(self):
        """Installiert und startet den Klipper-Service"""
        cmds = [
            "cd ~/klipper/scripts",
            "./install-octopi.sh",
            "sudo systemctl enable klipper",
            "sudo systemctl start klipper"
        ]
        for cmd in cmds:
            await self._run_command(cmd)

    async def _run_command(self, cmd: str):
        """Führt einen Shell-Befehl aus und aktualisiert den Status"""
        try:
            self.installation_process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await self.installation_process.communicate()
            
            if self.installation_process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unbekannter Fehler"
                self.logger.error(f"Fehler beim Ausführen von {cmd}: {error_msg}")
                raise Exception(error_msg)
                
            if self.status_callback:
                await self.status_callback({
                    "command": cmd,
                    "status": "completed",
                    "output": stdout.decode()
                })
                
        except Exception as e:
            self.logger.error(f"Fehler bei der Installation: {str(e)}")
            if self.status_callback:
                await self.status_callback({
                    "command": cmd,
                    "status": "error",
                    "error": str(e)
                })
            raise

    def set_status_callback(self, callback: Callable):
        """Setzt eine Callback-Funktion für Statusupdates"""
        self.status_callback = callback
