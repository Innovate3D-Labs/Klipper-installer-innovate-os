import os
import subprocess
import asyncio
from typing import Dict, Optional, List
from pathlib import Path

class KlipperInstaller:
    def __init__(self, base_dir: str = None):
        # Basis-Verzeichnis dynamisch ermitteln
        if base_dir is None:
            if os.getuid() == 0:  # Root-Benutzer
                base_dir = "/root"
            else:
                base_dir = str(Path.home())

        # Verzeichnisse konfigurieren
        self.base_dir = base_dir
        self.config_dir = os.path.join(self.base_dir, "printer_data/config")
        self.klipper_dir = os.path.join(self.base_dir, "klipper")
        self.firmware_dir = os.path.join(self.klipper_dir, "out")
        
        # Erstelle notwendige Verzeichnisse
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "printer_data/logs"), exist_ok=True)

    async def install_klipper(self) -> Dict[str, str]:
        """Installiert Klipper und seine Abhängigkeiten"""
        try:
            # Klipper Repository klonen
            if not os.path.exists(self.klipper_dir):
                await self._run_command(f"git clone https://github.com/Klipper3d/klipper.git {self.klipper_dir}")

            # Python-Umgebung erstellen
            venv_dir = os.path.join(self.base_dir, "klippy-env")
            if not os.path.exists(venv_dir):
                await self._run_command(f"python3 -m venv {venv_dir}")

            # Abhängigkeiten installieren
            install_script = os.path.join(self.klipper_dir, "scripts/install-debian.sh")
            await self._run_command(f"bash {install_script}")

            return {"status": "success", "message": "Klipper wurde erfolgreich installiert"}
        except Exception as e:
            return {"status": "error", "message": f"Fehler bei der Klipper-Installation: {str(e)}"}

    async def compile_firmware(self, mcu_type: str = None, processor: str = None) -> Dict[str, str]:
        """Kompiliert die Klipper-Firmware für den spezifizierten MCU"""
        try:
            # MCU-Typ basierend auf USB-ID bestimmen
            if mcu_type is None:
                # CH340 (1A86:7523) -> Meist Arduino Mega/RAMPS
                mcu_type = "atmega2560"
                processor = "AVR"

            # Konfigurationsdatei erstellen
            config = f"""CONFIG_LOW_LEVEL_OPTIONS=y
CONFIG_MACH_{processor.upper()}=y
CONFIG_{mcu_type.upper()}=y
"""
            config_path = os.path.join(self.klipper_dir, ".config")
            with open(config_path, "w") as f:
                f.write(config)

            # Firmware kompilieren
            await self._run_command("make clean", cwd=self.klipper_dir)
            await self._run_command("make", cwd=self.klipper_dir)

            if not os.path.exists(os.path.join(self.firmware_dir, "klipper.elf.hex")):
                raise Exception("Firmware-Kompilierung fehlgeschlagen")

            return {"status": "success", "message": "Firmware wurde erfolgreich kompiliert"}
        except Exception as e:
            return {"status": "error", "message": f"Fehler bei der Firmware-Kompilierung: {str(e)}"}

    async def flash_firmware(self, port: str, mcu_type: str = None) -> Dict[str, str]:
        """Flasht die kompilierte Firmware auf den MCU"""
        try:
            if mcu_type is None:
                mcu_type = "atmega2560"  # Standard für CH340

            # Stelle sicher, dass der Port existiert
            if not os.path.exists(port):
                raise Exception(f"Port {port} nicht gefunden")

            # Stelle sicher, dass die Firmware existiert
            firmware_path = os.path.join(self.firmware_dir, "klipper.elf.hex")
            if not os.path.exists(firmware_path):
                raise Exception("Firmware-Datei nicht gefunden")

            # Flash-Befehl basierend auf MCU-Typ
            flash_cmd = ""
            if mcu_type == "atmega2560":
                await self._run_command("apt-get install -y avrdude")
                flash_cmd = f"avrdude -p atmega2560 -c wiring -P {port} -U flash:w:{firmware_path}:i -D"
            else:
                raise Exception(f"Nicht unterstützter MCU-Typ: {mcu_type}")

            await self._run_command(flash_cmd)
            return {"status": "success", "message": "Firmware wurde erfolgreich geflasht"}
        except Exception as e:
            return {"status": "error", "message": f"Fehler beim Flashen der Firmware: {str(e)}"}

    async def setup_klipper_service(self) -> Dict[str, str]:
        """Richtet den Klipper-Service ein"""
        try:
            venv_dir = os.path.join(self.base_dir, "klippy-env")
            service_file = f"""[Unit]
Description=Klipper 3D Printer Firmware
After=network.target

[Service]
Type=simple
User={os.environ.get('SUDO_USER', os.getlogin())}
RemainAfterExit=yes
ExecStart={venv_dir}/bin/python {self.klipper_dir}/klippy/klippy.py {self.config_dir}/printer.cfg -l {self.base_dir}/printer_data/logs/klippy.log
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
            # Service-Datei erstellen
            service_path = "/etc/systemd/system/klipper.service"
            with open(service_path, "w") as f:
                f.write(service_file)

            # Service aktivieren und starten
            await self._run_command("systemctl daemon-reload")
            await self._run_command("systemctl enable klipper")
            await self._run_command("systemctl start klipper")

            return {"status": "success", "message": "Klipper-Service wurde erfolgreich eingerichtet"}
        except Exception as e:
            return {"status": "error", "message": f"Fehler beim Einrichten des Klipper-Service: {str(e)}"}

    async def create_printer_config(self, config_data: Dict[str, str]) -> Dict[str, str]:
        """Erstellt die Klipper-Konfigurationsdatei für den Drucker"""
        try:
            config_template = f"""[mcu]
serial: {config_data.get('serial_port', '/dev/ttyUSB0')}
restart_method: command

[printer]
kinematics: {config_data.get('kinematics', 'cartesian')}
max_velocity: {config_data.get('max_velocity', '300')}
max_accel: {config_data.get('max_accel', '3000')}
max_z_velocity: {config_data.get('max_z_velocity', '5')}
max_z_accel: {config_data.get('max_z_accel', '100')}

[stepper_x]
step_pin: {config_data.get('x_step_pin')}
dir_pin: {config_data.get('x_dir_pin')}
enable_pin: {config_data.get('x_enable_pin')}
microsteps: {config_data.get('x_microsteps', '16')}
rotation_distance: {config_data.get('x_rotation_distance', '40')}
endstop_pin: {config_data.get('x_endstop_pin')}
position_endstop: 0
position_max: {config_data.get('x_position_max', '200')}
homing_speed: 50

[stepper_y]
step_pin: {config_data.get('y_step_pin')}
dir_pin: {config_data.get('y_dir_pin')}
enable_pin: {config_data.get('y_enable_pin')}
microsteps: {config_data.get('y_microsteps', '16')}
rotation_distance: {config_data.get('y_rotation_distance', '40')}
endstop_pin: {config_data.get('y_endstop_pin')}
position_endstop: 0
position_max: {config_data.get('y_position_max', '200')}
homing_speed: 50

[stepper_z]
step_pin: {config_data.get('z_step_pin')}
dir_pin: {config_data.get('z_dir_pin')}
enable_pin: {config_data.get('z_enable_pin')}
microsteps: {config_data.get('z_microsteps', '16')}
rotation_distance: {config_data.get('z_rotation_distance', '8')}
endstop_pin: {config_data.get('z_endstop_pin')}
position_endstop: 0.5
position_max: {config_data.get('z_position_max', '200')}

[extruder]
step_pin: {config_data.get('e_step_pin')}
dir_pin: {config_data.get('e_dir_pin')}
enable_pin: {config_data.get('e_enable_pin')}
microsteps: {config_data.get('e_microsteps', '16')}
rotation_distance: {config_data.get('e_rotation_distance', '33.500')}
nozzle_diameter: {config_data.get('nozzle_diameter', '0.400')}
filament_diameter: {config_data.get('filament_diameter', '1.750')}
heater_pin: {config_data.get('heater_pin')}
sensor_type: {config_data.get('temp_sensor_type', 'EPCOS 100K B57560G104F')}
sensor_pin: {config_data.get('temp_sensor_pin')}
control: pid
pid_Kp: {config_data.get('pid_kp', '22.2')}
pid_Ki: {config_data.get('pid_ki', '1.08')}
pid_Kd: {config_data.get('pid_kd', '114')}
min_temp: 0
max_temp: {config_data.get('max_temp', '250')}

[heater_bed]
heater_pin: {config_data.get('bed_heater_pin')}
sensor_type: {config_data.get('bed_sensor_type', 'EPCOS 100K B57560G104F')}
sensor_pin: {config_data.get('bed_sensor_pin')}
control: pid
pid_Kp: {config_data.get('bed_pid_kp', '54.027')}
pid_Ki: {config_data.get('bed_pid_ki', '0.770')}
pid_Kd: {config_data.get('bed_pid_kd', '948.182')}
min_temp: 0
max_temp: {config_data.get('bed_max_temp', '130')}

[fan]
pin: {config_data.get('fan_pin')}

[display]
lcd_type: {config_data.get('display_type', 'st7920')}
cs_pin: {config_data.get('display_cs_pin')}
sclk_pin: {config_data.get('display_sclk_pin')}
sid_pin: {config_data.get('display_sid_pin')}

[virtual_sdcard]
path: ~/gcode_files

[pause_resume]

[display_status]

[gcode_macro PAUSE]
description: Pause the actual running print
rename_existing: PAUSE_BASE
gcode:
    PAUSE_BASE
    SAVE_GCODE_STATE NAME=PAUSE_state
    PARK_HEAD

[gcode_macro RESUME]
description: Resume the actual running print
rename_existing: RESUME_BASE
gcode:
    RESTORE_GCODE_STATE NAME=PAUSE_state MOVE=1
    RESUME_BASE

[gcode_macro CANCEL_PRINT]
description: Cancel the actual running print
rename_existing: CANCEL_PRINT_BASE
gcode:
    TURN_OFF_HEATERS
    CANCEL_PRINT_BASE
"""
            # Konfigurationsdatei speichern
            config_path = os.path.join(self.config_dir, "printer.cfg")
            with open(config_path, "w") as f:
                f.write(config_template)

            return {
                "status": "success",
                "message": "Drucker-Konfiguration wurde erfolgreich erstellt",
                "config_path": config_path
            }
        except Exception as e:
            return {"status": "error", "message": f"Fehler beim Erstellen der Konfiguration: {str(e)}"}

    async def _run_command(self, cmd: str, cwd: str = None) -> str:
        """Führt einen Shell-Befehl aus und gibt die Ausgabe zurück"""
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            raise Exception(f"Befehl fehlgeschlagen: {stderr.decode()}")
        
        return stdout.decode()
