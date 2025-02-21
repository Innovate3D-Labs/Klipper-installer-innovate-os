from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict
from ..services.klipper_installer import KlipperInstaller
from ..core.schemas import InstallationResponse

router = APIRouter()
installer = KlipperInstaller()

@router.post("/install/{printer_id}", response_model=InstallationResponse)
async def install_klipper(printer_id: str, background_tasks: BackgroundTasks) -> Dict[str, str]:
    """Startet die Klipper-Installation für einen bestimmten Drucker"""
    try:
        # Klipper installieren
        result = await installer.install_klipper()
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])

        # MCU-Typ basierend auf Hardware-ID bestimmen
        # TODO: Implementiere MCU-Erkennung basierend auf VID:PID
        mcu_type = "atmega2560"  # Standard für viele 3D-Drucker
        processor = "AVR"

        # Firmware kompilieren
        result = await installer.compile_firmware(mcu_type, processor)
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])

        # Firmware flashen
        result = await installer.flash_firmware(f"/dev/ttyUSB0", mcu_type)
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])

        # Klipper-Service einrichten
        result = await installer.setup_klipper_service()
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])

        # Drucker-Konfiguration erstellen
        config_data = {
            "serial_port": "/dev/ttyUSB0",
            "kinematics": "cartesian",
            "max_velocity": "300",
            "max_accel": "3000",
            "max_z_velocity": "5",
            "max_z_accel": "100",
            # Standard-Pins für RAMPS 1.4
            "x_step_pin": "ar54",
            "x_dir_pin": "ar55",
            "x_enable_pin": "ar38",
            "x_endstop_pin": "ar3",
            "y_step_pin": "ar60",
            "y_dir_pin": "ar61",
            "y_enable_pin": "ar56",
            "y_endstop_pin": "ar14",
            "z_step_pin": "ar46",
            "z_dir_pin": "ar48",
            "z_enable_pin": "ar62",
            "z_endstop_pin": "ar18",
            "e_step_pin": "ar26",
            "e_dir_pin": "ar28",
            "e_enable_pin": "ar24",
            "heater_pin": "ar10",
            "temp_sensor_pin": "analog13",
            "bed_heater_pin": "ar8",
            "bed_sensor_pin": "analog14",
            "fan_pin": "ar9",
            "display_cs_pin": "ar16",
            "display_sclk_pin": "ar23",
            "display_sid_pin": "ar17"
        }
        result = await installer.create_printer_config(config_data)
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])

        return {
            "status": "success",
            "message": "Klipper wurde erfolgreich installiert und konfiguriert",
            "config_path": result.get("config_path")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
