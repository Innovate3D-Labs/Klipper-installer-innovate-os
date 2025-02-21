from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict
from ..services.klipper_installer import KlipperInstaller
from ..core.schemas import InstallationResponse
import os

router = APIRouter()
installer = KlipperInstaller()

@router.post("/install/{printer_id}", response_model=InstallationResponse)
async def install_klipper(printer_id: str, background_tasks: BackgroundTasks) -> Dict[str, str]:
    """Startet die Klipper-Installation für einen bestimmten Drucker"""
    try:
        # Prüfe Root-Rechte
        if os.getuid() != 0:
            raise HTTPException(
                status_code=403,
                detail="Die Installation muss mit Root-Rechten ausgeführt werden"
            )

        # Klipper installieren
        result = await installer.install_klipper()
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])

        # Firmware kompilieren (MCU-Typ wird automatisch erkannt)
        result = await installer.compile_firmware()
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])

        # Firmware flashen
        result = await installer.flash_firmware("/dev/ttyUSB0")
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
            "fan_pin": "ar9",
            "temp_pin": "analog1"
        }
        
        result = await installer.create_printer_config(config_data)
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])

        return {"status": "success", "message": "Klipper wurde erfolgreich installiert"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
