
from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def valid_session():
    return {
        "Administrative": 1,
        "Administrative_Duration": 20.0,
        "Informational": 0,
        "Informational_Duration": 0.0,
        "ProductRelated": 5,
        "ProductRelated_Duration": 100.0,
        "BounceRates": 0.02,
        "ExitRates": 0.04,
        "PageValues": 0.0,
        "SpecialDay": 0.0,
        "Month": "May",
        "OperatingSystems": 2,
        "Browser": 2,
        "Region": 1,
        "TrafficType": 2,
        "VisitorType": "Returning_Visitor",
        "Weekend": False,
    }


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to the ShopSense API"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["model_loaded"] is True


def test_prediction_response():
    response = client.post("/predict", json=valid_session())

    assert response.status_code == 200

    result = response.json()
    assert 0 <= result["purchase_probability"] <= 1
    assert result["predicted_purchase"] in [0, 1]
    assert result["decision_threshold"] == 0.37


def test_missing_feature_is_rejected():
    session = valid_session()
    del session["PageValues"]

    response = client.post("/predict", json=session)

    assert response.status_code == 422


def test_invalid_bounce_rate_is_rejected():
    session = valid_session()
    session["BounceRates"] = 1.5

    response = client.post("/predict", json=session)

    assert response.status_code == 422
