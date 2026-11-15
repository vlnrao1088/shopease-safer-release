
from app import app


def test_health_is_up():
    response = app.test_client().get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'UP'


def test_health_down_when_switch_is_on(monkeypatch):
    monkeypatch.setenv('BREAK_HEALTH', 'true')
    response = app.test_client().get('/health')
    assert response.status_code == 503


def test_order_found():
    response = app.test_client().get('/orders/1001')
    assert response.status_code == 200
    assert response.get_json()['item'] == 'Headphones'


def test_order_not_found():
    response = app.test_client().get('/orders/9999')
    assert response.status_code == 404