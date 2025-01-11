import asyncio
import os
from typing import Optional, Callable
from ..core.logging import InstallationLogger, logger

class KlipperInstaller:
    def __init__(self):
        self.installation_logger = InstallationLogger()
        self.installation_process: Optional[asyncio.subprocess.Process] = None
        self.status_callback: Optional[Callable] = None

    async def install_dependencies(self):
        """Installiert alle notwendigen Abhängigkeiten"""
        self.installation_logger.log('INFO', 'Starte Installation der Abhängigkeiten')
        try:
            cmd = "sudo apt-get update && sudo apt-get install -y git python3-pip"
            await self._run_command(cmd)
            self.installation_logger.log('INFO', 'Abhängigkeiten erfolgreich installiert')
        except Exception as e:
            self.installation_logger.log('ERROR', f'Fehler bei der Installation der Abhängigkeiten: {str(e)}')
            raise

    async def clone_klipper(self):
        """Klont das Klipper-Repository"""
        self.installation_logger.log('INFO', 'Klipper-Repository wird geklont')
        try:
            if not os.path.exists("~/klipper"):
                cmd = "git clone https://github.com/Klipper3d/klipper.git ~/klipper"
                await self._run_command(cmd)
                self.installation_logger.log('INFO', 'Klipper-Repository erfolgreich geklont')
            else:
                self.installation_logger.log('INFO', 'Klipper-Repository bereits vorhanden')
        except Exception as e:
            self.installation_logger.log('ERROR', f'Fehler beim Klonen des Repositories: {str(e)}')
            raise

    async def compile_firmware(self, config_path: str):
        """Kompiliert die Firmware mit der angegebenen Konfiguration"""
        self.installation_logger.log('INFO', 'Starte Firmware-Kompilierung')
        try:
            # Kopiere die Konfiguration
            cmd = f"cp {config_path} ~/klipper/.config"
            await self._run_command(cmd)
            self.installation_logger.log('INFO', 'Firmware-Konfiguration kopiert')
            
            # Kompiliere
            cmd = "cd ~/klipper && make"
            await self._run_command(cmd)
            self.installation_logger.log('INFO', 'Firmware erfolgreich kompiliert')
        except Exception as e:
            self.installation_logger.log('ERROR', f'Fehler bei der Firmware-Kompilierung: {str(e)}')
            raise

    async def install_service(self):
        """Installiert und startet den Klipper-Service"""
        self.installation_logger.log('INFO', 'Starte Installation des Klipper-Services')
        try:
            cmds = [
                "cd ~/klipper/scripts",
                "./install-octopi.sh",
                "sudo systemctl enable klipper",
                "sudo systemctl start klipper"
            ]
            for cmd in cmds:
                await self._run_command(cmd)
            self.installation_logger.log('INFO', 'Klipper-Service erfolgreich installiert und gestartet')
        except Exception as e:
            self.installation_logger.log('ERROR', f'Fehler bei der Service-Installation: {str(e)}')
            raise

    async def _run_command(self, cmd: str):
        """Führt einen Shell-Befehl aus und aktualisiert den Status"""
        try:
            self.installation_logger.log('INFO', f'Führe Befehl aus: {cmd}')
            self.installation_process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await self.installation_process.communicate()
            
            if self.installation_process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unbekannter Fehler"
                self.installation_logger.log('ERROR', f'Befehl fehlgeschlagen: {error_msg}')
                raise Exception(error_msg)
            
            output = stdout.decode()
            self.installation_logger.log('INFO', f'Befehl erfolgreich ausgeführt: {output[:200]}...' if len(output) > 200 else output)
                
            if self.status_callback:
                await self.status_callback({
                    'command': cmd,
                    'status': 'completed',
                    'output': output,
                    'logs': self.installation_logger.get_logs()
                })
                
        except Exception as e:
            error_msg = f'Fehler bei der Ausführung von {cmd}: {str(e)}'
            self.installation_logger.log('ERROR', error_msg)
            if self.status_callback:
                await self.status_callback({
                    'command': cmd,
                    'status': 'error',
                    'error': error_msg,
                    'logs': self.installation_logger.get_logs()
                })
            raise

    def set_status_callback(self, callback: Callable):
        """Setzt eine Callback-Funktion für Statusupdates"""
        self.status_callback = callback

    def get_installation_logs(self) -> list[dict]:
        """Gibt alle Installations-Logs zurück"""
        return self.installation_logger.get_logs()
