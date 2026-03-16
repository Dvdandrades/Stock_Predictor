import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from stock_predictor.dependencies.database import get_db
from stock_predictor.database.session import Base
from main import app


engine = create_engine("sqlite:///:memory:", echo=True)
Base.metadata.create_all(engine)
mock_session = sessionmaker(bind=engine)


def mock_get_db():
    db = mock_session()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def mock_client():
    app.dependency_overrides[get_db] = mock_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
