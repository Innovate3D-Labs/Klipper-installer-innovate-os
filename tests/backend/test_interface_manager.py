import pytest
from src.backend.services.interface_manager import InterfaceManager
from src.backend.core.exceptions import InterfaceNotFoundError

def test_get_available_interfaces():
    """Test ob verfügbare Interfaces korrekt zurückgegeben werden"""
    manager = InterfaceManager()
    interfaces = manager.get_available_interfaces()
    
    assert isinstance(interfaces, list)
    assert all(isinstance(interface, dict) for interface in interfaces)
    assert all("name" in interface for interface in interfaces)
    assert all("status" in interface for interface in interfaces)

def test_switch_interface_success(mocker):
    """Test erfolgreicher Interface-Wechsel"""
    manager = InterfaceManager()
    mock_subprocess = mocker.patch("subprocess.run")
    mock_subprocess.return_value.returncode = 0
    
    result = manager.switch_interface("fluidd")
    
    assert result["success"] is True
    assert result["message"] == "Interface successfully switched to fluidd"
    mock_subprocess.assert_called_once()

def test_switch_interface_failure(mocker):
    """Test fehlgeschlagener Interface-Wechsel"""
    manager = InterfaceManager()
    mock_subprocess = mocker.patch("subprocess.run")
    mock_subprocess.return_value.returncode = 1
    mock_subprocess.return_value.stderr = b"Error switching interface"
    
    with pytest.raises(InterfaceNotFoundError):
        manager.switch_interface("invalid_interface")

def test_get_current_interface(mocker):
    """Test Abfrage des aktuellen Interfaces"""
    manager = InterfaceManager()
    mock_subprocess = mocker.patch("subprocess.run")
    mock_subprocess.return_value.stdout = b"fluidd"
    
    current_interface = manager.get_current_interface()
    
    assert current_interface == "fluidd"
    mock_subprocess.assert_called_once()
