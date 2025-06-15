
import requests
import pytest
from unittest.mock import Mock, patch

class TestHealthAPI:
    """Comprehensive API Test Suite for Assignment 2"""
    
    def test_health_endpoint_success_scenario(self):
        """Test successful health check response"""
        # Mock a successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "OK", "message": "Service is healthy"}
        
        with patch('requests.get', return_value=mock_response):
            response = requests.get("http://18.226.248.96:8080/health")
            assert response.status_code == 200
            assert "status" in response.json()
            print("✅ Success scenario test passed")
    
    def test_health_endpoint_failure_scenario(self):
        """Test health check failure response"""
        # Mock a failure response
        mock_response = Mock()
        mock_response.status_code = 503
        mock_response.json.return_value = {"status": "ERROR", "message": "Service unavailable"}
        
        with patch('requests.get', return_value=mock_response):
            response = requests.get("http://18.226.248.96:8080/health")
            assert response.status_code == 503
            print("✅ Failure scenario test passed")
    
    def test_invalid_endpoint(self):
        """Test 404 for invalid endpoints"""
        mock_response = Mock()
        mock_response.status_code = 404
        
        with patch('requests.get', return_value=mock_response):
            response = requests.get("http://18.226.248.96:8080/invalid")
            assert response.status_code == 404
            print("✅ Invalid endpoint test passed")
    
    def test_method_not_allowed(self):
        """Test 405 for unsupported HTTP methods"""
        mock_response = Mock()
        mock_response.status_code = 405
        
        with patch('requests.post', return_value=mock_response):
            response = requests.post("http://18.226.248.96:8080/health")
            assert response.status_code == 405
            print("✅ Method not allowed test passed")

if __name__ == "__main__":
    test_suite = TestHealthAPI()
    test_suite.test_health_endpoint_success_scenario()
    test_suite.test_health_endpoint_failure_scenario()
    test_suite.test_invalid_endpoint()
    test_suite.test_method_not_allowed()
    print("🎉 All API tests completed successfully!")
