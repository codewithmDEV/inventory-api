import pytest
from unittest.mock import patch, Mock
import requests
import external_api


@patch("external_api.requests.get")
def test_fetch_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": 1,
        "product": {"product_name": "Nutella", "brands": "Ferrero"}
    }
    mock_get.return_value = mock_response

    result = external_api.fetch_by_barcode("3017620422003")
    assert result["product_name"] == "Nutella"


@patch("external_api.requests.get")
def test_fetch_not_found(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": 0}
    mock_get.return_value = mock_response

    result = external_api.fetch_by_barcode("0000000000000")
    assert result is None


@patch("external_api.requests.get")
def test_fetch_network_error(mock_get):
    mock_get.side_effect = requests.RequestException("Network down")

    result = external_api.fetch_by_barcode("3017620422003")
    assert result is None