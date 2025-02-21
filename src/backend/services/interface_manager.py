import os
import subprocess
import logging
import asyncio
from typing import Optional

class InterfaceManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_interface: Optional[str] = None
        self._check_current_interface()

    def _check_current_interface(self):
        """Überprüft, welche Weboberfläche aktuell installiert ist"""
        if os.path.exists("/home/pi/fluidd"):
            self.current_interface = "fluidd"
        elif os.path.exists("/home/pi/mainsail"):
            self.current_interface = "mainsail"

    async def install_fluidd(self):
        """Installiert Fluidd"""
        try:
            commands = [
                "sudo apt-get update",
                "sudo apt-get install -y nginx",
                "cd /home/pi",
                "rm -rf fluidd",
                "mkdir fluidd",
                "cd fluidd",
                "wget -q -O fluidd.zip https://github.com/fluidd-core/fluidd/releases/latest/download/fluidd.zip",
                "unzip fluidd.zip",
                "rm fluidd.zip",
                "sudo ln -sf /home/pi/fluidd /var/www/fluidd"
            ]
            
            for cmd in commands:
                process = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                
                if process.returncode != 0:
                    raise Exception(f"Fehler beim Ausführen von {cmd}: {stderr.decode()}")
            
            # Nginx-Konfiguration
            nginx_config = """
server {
    listen 80;
    server_name _;

    root /var/www/fluidd;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /printer {
        proxy_pass http://localhost:7125/printer;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
    }

    location /api {
        proxy_pass http://localhost:7125/api;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
    }

    location /websocket {
        proxy_pass http://localhost:7125/websocket;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 86400;
    }
}
"""
            with open("/etc/nginx/sites-available/fluidd", "w") as f:
                f.write(nginx_config)
            
            os.symlink("/etc/nginx/sites-available/fluidd", "/etc/nginx/sites-enabled/fluidd")
            subprocess.run(["sudo", "nginx", "-s", "reload"])
            
            self.current_interface = "fluidd"
            return True
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Fluidd-Installation: {str(e)}")
            raise

    async def install_mainsail(self):
        """Installiert Mainsail"""
        try:
            commands = [
                "sudo apt-get update",
                "sudo apt-get install -y nginx",
                "cd /home/pi",
                "rm -rf mainsail",
                "mkdir mainsail",
                "cd mainsail",
                "wget -q -O mainsail.zip https://github.com/mainsail-crew/mainsail/releases/latest/download/mainsail.zip",
                "unzip mainsail.zip",
                "rm mainsail.zip",
                "sudo ln -sf /home/pi/mainsail /var/www/mainsail"
            ]
            
            for cmd in commands:
                process = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                
                if process.returncode != 0:
                    raise Exception(f"Fehler beim Ausführen von {cmd}: {stderr.decode()}")
            
            # Nginx-Konfiguration
            nginx_config = """
server {
    listen 80;
    server_name _;

    root /var/www/mainsail;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /printer {
        proxy_pass http://localhost:7125/printer;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
    }

    location /api {
        proxy_pass http://localhost:7125/api;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
    }

    location /websocket {
        proxy_pass http://localhost:7125/websocket;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 86400;
    }
}
"""
            with open("/etc/nginx/sites-available/mainsail", "w") as f:
                f.write(nginx_config)
            
            os.symlink("/etc/nginx/sites-available/mainsail", "/etc/nginx/sites-enabled/mainsail")
            subprocess.run(["sudo", "nginx", "-s", "reload"])
            
            self.current_interface = "mainsail"
            return True
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Mainsail-Installation: {str(e)}")
            raise

    async def switch_interface(self, interface: str):
        """Wechselt zwischen Fluidd und Mainsail"""
        if interface not in ["fluidd", "mainsail"]:
            raise ValueError("Ungültige Weboberfläche")

        if interface == self.current_interface:
            return True

        try:
            # Entferne alte Nginx-Konfiguration
            if os.path.exists("/etc/nginx/sites-enabled/fluidd"):
                os.remove("/etc/nginx/sites-enabled/fluidd")
            if os.path.exists("/etc/nginx/sites-enabled/mainsail"):
                os.remove("/etc/nginx/sites-enabled/mainsail")

            # Installiere neue Oberfläche
            if interface == "fluidd":
                await self.install_fluidd()
            else:
                await self.install_mainsail()

            return True

        except Exception as e:
            self.logger.error(f"Fehler beim Wechsel der Weboberfläche: {str(e)}")
            raise

    def get_current_interface(self) -> Optional[str]:
        """Gibt die aktuell installierte Weboberfläche zurück"""
        return self.current_interface
