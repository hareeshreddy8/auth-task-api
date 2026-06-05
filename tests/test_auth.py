from fastapi.testclient import TestClient
from api import auth_app

client = TestClient(auth_app)

def test_signup():
    request = client.post("/signup",
                          params={
                              "username" : "harees",
                              "password" : "abc12344"
                          }
                          )
    print(request.json())
    assert request.status_code == 201


