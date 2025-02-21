from setuptools import setup, find_packages

setup(
    name="klipper-installer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "aiofiles",
        "python-multipart",
        "pydantic",
        "pyserial"
    ],
)
