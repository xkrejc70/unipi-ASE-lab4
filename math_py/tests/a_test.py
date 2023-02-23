import pytest
from math_py import app

def test_add(client):
    rv = client.get('/add?a=1&b=2')
    print(rv)
    assert rv.status_code == 200
    assert rv.get_json() == {'s': 3}
