"""Shared pytest fixtures for all tests."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app


@pytest.fixture(scope="function")
def client() -> TestClient:
    """
    FastAPI test client fixture.

    Provides a test client for making HTTP requests to the API.

    Returns:
        FastAPI TestClient instance
    """
    return TestClient(app)


@pytest.fixture(scope="function")
def db_session() -> Session:
    """
    Database session fixture for testing (placeholder).

    TODO: Implement test database connection with:
    - In-memory SQLite or separate test PostgreSQL database
    - Transaction rollback after each test
    - Proper cleanup

    Returns:
        SQLAlchemy Session instance
    """
    # TODO: Implement test database setup
    # Example implementation:
    # engine = create_engine("sqlite:///:memory:")
    # Base.metadata.create_all(bind=engine)
    # TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # session = TestSessionLocal()
    # try:
    #     yield session
    # finally:
    #     session.close()
    #     Base.metadata.drop_all(bind=engine)
    pass


@pytest.fixture(scope="function")
def override_get_db(db_session: Session) -> None:
    """
    Override get_db dependency for testing (placeholder).

    TODO: Implement dependency override to use test database:

    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()
    """
    pass
