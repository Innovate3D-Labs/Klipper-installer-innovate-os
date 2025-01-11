import pytest
import asyncio
from src.backend.services.klipper_installer import KlipperInstaller
from src.backend.core.exceptions import InstallationError

@pytest.mark.asyncio
async def test_install_dependencies_success(mocker):
    """Test erfolgreiche Installation von Abhängigkeiten"""
    installer = KlipperInstaller()
    mock_run = mocker.patch("asyncio.create_subprocess_shell")
    mock_process = mocker.Mock()
    mock_process.communicate = mocker.AsyncMock(return_value=(b"Success", b""))
    mock_process.returncode = 0
    mock_run.return_value = mock_process
    
    await installer.install_dependencies()
    
    mock_run.assert_called_once()
    assert "apt-get" in mock_run.call_args[0][0]

@pytest.mark.asyncio
async def test_install_dependencies_failure(mocker):
    """Test fehlgeschlagene Installation von Abhängigkeiten"""
    installer = KlipperInstaller()
    mock_run = mocker.patch("asyncio.create_subprocess_shell")
    mock_process = mocker.Mock()
    mock_process.communicate = mocker.AsyncMock(return_value=(b"", b"Error"))
    mock_process.returncode = 1
    mock_run.return_value = mock_process
    
    with pytest.raises(InstallationError):
        await installer.install_dependencies()

@pytest.mark.asyncio
async def test_clone_klipper_success(mocker):
    """Test erfolgreiches Klonen des Klipper-Repositories"""
    installer = KlipperInstaller()
    mock_run = mocker.patch("asyncio.create_subprocess_shell")
    mock_process = mocker.Mock()
    mock_process.communicate = mocker.AsyncMock(return_value=(b"Success", b""))
    mock_process.returncode = 0
    mock_run.return_value = mock_process
    
    await installer.clone_klipper()
    
    mock_run.assert_called_once()
    assert "git clone" in mock_run.call_args[0][0]

@pytest.mark.asyncio
async def test_compile_firmware_success(mocker):
    """Test erfolgreiche Firmware-Kompilierung"""
    installer = KlipperInstaller()
    mock_run = mocker.patch("asyncio.create_subprocess_shell")
    mock_process = mocker.Mock()
    mock_process.communicate = mocker.AsyncMock(return_value=(b"Success", b""))
    mock_process.returncode = 0
    mock_run.return_value = mock_process
    
    await installer.compile_firmware("test_config.cfg")
    
    assert mock_run.call_count == 2  # cp und make Befehle
    assert "make" in mock_run.call_args_list[1][0][0]

@pytest.mark.asyncio
async def test_status_callback(mocker):
    """Test Status-Callback während der Installation"""
    installer = KlipperInstaller()
    mock_callback = mocker.AsyncMock()
    installer.set_status_callback(mock_callback)
    
    mock_run = mocker.patch("asyncio.create_subprocess_shell")
    mock_process = mocker.Mock()
    mock_process.communicate = mocker.AsyncMock(return_value=(b"Success", b""))
    mock_process.returncode = 0
    mock_run.return_value = mock_process
    
    await installer.install_dependencies()
    
    mock_callback.assert_called_with({
        "command": mocker.ANY,
        "status": "completed",
        "output": "Success",
        "logs": mocker.ANY
    })
