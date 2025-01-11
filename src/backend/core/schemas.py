from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class PrinterBase(BaseModel):
    """Basis-Schema für Drucker"""
    name: str = Field(..., description="Name des Druckers")
    manufacturer: str = Field(..., description="Hersteller des Druckers")
    type: str = Field(..., description="Typ des Druckers (z.B. Cartesian, CoreXY)")
    build_volume: Dict[str, int] = Field(..., description="Bauvolumen in mm (x, y, z)")
    features: List[str] = Field(default_list, description="Liste der Funktionen")
    description: Optional[str] = Field(None, description="Beschreibung des Druckers")
    mcu_type: Optional[str] = Field(None, description="Typ des Mikrocontrollers")

class PrinterCreate(PrinterBase):
    """Schema für das Erstellen eines neuen Druckers"""
    id: str = Field(..., description="Eindeutige ID des Druckers")
    config: Optional[str] = Field(None, description="Klipper Konfiguration")
    firmware_config: Optional[str] = Field(None, description="Firmware Konfiguration")

class PrinterUpdate(BaseModel):
    """Schema für das Aktualisieren eines Druckers"""
    name: Optional[str] = None
    manufacturer: Optional[str] = None
    type: Optional[str] = None
    build_volume: Optional[Dict[str, int]] = None
    features: Optional[List[str]] = None
    description: Optional[str] = None
    mcu_type: Optional[str] = None
    config: Optional[str] = None
    firmware_config: Optional[str] = None

class PrinterResponse(PrinterBase):
    """Schema für die Drucker-Antwort"""
    id: str
    config_dir: str
    config: Optional[str] = None
    firmware_config: Optional[str] = None

    class Config:
        orm_mode = True

class PrinterConfig(BaseModel):
    """Schema für die Druckerkonfiguration"""
    content: str = Field(..., description="Inhalt der Konfigurationsdatei")
    filename: str = Field(..., description="Name der Konfigurationsdatei")

class FirmwareConfig(BaseModel):
    """Schema für die Firmware-Konfiguration"""
    content: str = Field(..., description="Inhalt der Firmware-Konfiguration")
    mcu_type: str = Field(..., description="Typ des Mikrocontrollers")
