from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class USBPrinterResponse(BaseModel):
    """Schema für erkannte USB-Drucker"""
    id: str = Field(..., description="Eindeutige ID des Druckers (USB-Port)")
    name: str = Field(..., description="Name oder Beschreibung des Druckers")
    port: str = Field(..., description="USB-Port des Druckers")
    description: Optional[str] = Field(None, description="Ausführliche Beschreibung des Druckers")
    manufacturer: Optional[str] = Field(None, description="Hersteller des Druckers")
    hardware_id: Optional[str] = Field(None, description="Hardware-ID des USB-Geräts")
    vid: Optional[int] = Field(None, description="Vendor ID des USB-Geräts")
    pid: Optional[int] = Field(None, description="Product ID des USB-Geräts")
    serial_number: Optional[str] = Field(None, description="Seriennummer des USB-Geräts")
    status: str = Field("connected", description="Status des Druckers")

class PrinterBase(BaseModel):
    """Basis-Schema für Drucker"""
    name: str = Field(..., description="Name des Druckers")
    manufacturer: str = Field(..., description="Hersteller des Druckers")
    type: str = Field(..., description="Typ des Druckers (z.B. Cartesian, CoreXY)")
    build_volume: Dict[str, int] = Field(..., description="Bauvolumen in mm (x, y, z)")
    features: List[str] = Field(default_factory=list, description="Liste der Funktionen")
    description: Optional[str] = Field(None, description="Beschreibung des Druckers")
    mcu_type: Optional[str] = Field(None, description="Typ des Mikrocontrollers")

class PrinterCreate(PrinterBase):
    """Schema für das Erstellen eines neuen Druckers"""
    id: str = Field(..., description="Eindeutige ID des Druckers")
    config: Optional[str] = Field(None, description="Klipper Konfiguration")
    firmware_config: Optional[str] = Field(None, description="Firmware Konfiguration")
    port: Optional[str] = Field(None, description="USB-Port des Druckers")

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
    port: Optional[str] = Field(None, description="USB-Port des Druckers")

class PrinterResponse(PrinterBase):
    """Schema für die Drucker-Antwort"""
    id: str
    config_dir: str
    config: Optional[str] = None
    firmware_config: Optional[str] = None
    port: Optional[str] = Field(None, description="USB-Port des Druckers")
    status: str = Field("unknown", description="Status des Druckers")

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

class InstallationResponse(BaseModel):
    """Modell für die Antwort bei der Installation"""
    status: str = Field(..., description="Status der Installation (success/error)")
    message: str = Field(..., description="Statusmeldung")
    config_path: Optional[str] = Field(None, description="Pfad zur Konfigurationsdatei")

class WebInterfaceResponse(BaseModel):
    """Modell für die Antwort bei Webinterface-Abfragen"""
    current_interface: str = Field(..., description="Aktuell aktives Webinterface")
    available_interfaces: List[str] = Field(..., description="Liste der verfügbaren Webinterfaces")

class WebInterfaceSwitchRequest(BaseModel):
    """Modell für die Anfrage zum Wechseln des Webinterfaces"""
    interface: str = Field(..., description="Name des zu aktivierenden Webinterfaces")
