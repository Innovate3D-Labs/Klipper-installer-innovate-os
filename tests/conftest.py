import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.backend.core.database import Base
from src.backend.main import app
from src.backend.core.config import get_settings

@pytest.fixture
def test_db():
    """Creates a test database"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_settings] = override_get_db
    
    return engine

@pytest.fixture
def test_client(test_db):
    """Creates a test client"""
    with TestClient(app) as client:
        yield client

@pytest.fixture
def mock_klipper_installer(mocker):
    """Mockt den KlipperInstaller für Tests"""
    return mocker.patch("src.backend.services.klipper_installer.KlipperInstaller")
