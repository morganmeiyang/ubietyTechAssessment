import pytest

from assessment import db, create_app

@pytest.fixture()
def app():
    app = create_app("sqlite://")
    with app.app_context():
        db.create_all()
    
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

