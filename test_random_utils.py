import pytest
import requests
from meal_max.utils.random_utils import get_random

@pytest.fixture
def mock_random_org(mocker):
    """Fixture to mock the requests.get call to random.org."""
    mock_response = mocker.Mock()
    # Set up a mock valid response (a valid random number as a string)
    mock_response.text = "0.57"  # Example valid random response
    mocker.patch("requests.get", return_value=mock_response)
    return mock_response

def test_get_random(mock_random_org):
    """Test retrieving a random decimal number from random.org."""
    result = get_random()

    # Assert that the result is the mocked random number
    assert result == 0.57, f"Expected random number 0.57, but got {result}"

    # Ensure that the correct URL was called
    mock_random_org.assert_called_once_with(
        "https://www.random.org/decimal-fractions/?num=1&dec=2&col=1&format=plain&rnd=new", 
        timeout=5
    )

def test_get_random_request_failure(mocker):
    """Simulate a request failure."""
    # Mock a request failure (RequestException)
    mocker.patch("requests.get", side_effect=requests.exceptions.RequestException("Connection error"))

    with pytest.raises(RuntimeError, match="Request to random.org failed: Connection error"):
        get_random()

def test_get_random_timeout(mocker):
    """Simulate a timeout."""
    # Mock a request timeout
    mocker.patch("requests.get", side_effect=requests.exceptions.Timeout)

    with pytest.raises(RuntimeError, match="Request to random.org timed out."):
        get_random()

def test_get_random_invalid_response(mock_random_org):
    """Simulate an invalid response (non-digit)."""
    # Set up an invalid response (non-numeric value)
    mock_random_org.text = "invalid_response"

    with pytest.raises(ValueError, match="Invalid response from random.org: invalid_response"):
        get_random()


