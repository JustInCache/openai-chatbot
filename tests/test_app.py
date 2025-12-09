import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def app():
    """Create application for testing."""
    from main import app
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


class TestIndexRoute:
    """Tests for the index route."""
    
    def test_index_returns_200(self, client):
        """Test that index page returns 200 status code."""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_index_returns_html(self, client):
        """Test that index page returns HTML content."""
        response = client.get('/')
        assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data


class TestChatRoute:
    """Tests for the chat route."""
    
    def test_chat_requires_post(self, client):
        """Test that chat endpoint only accepts POST requests."""
        response = client.get('/chat')
        assert response.status_code == 405
    
    def test_chat_requires_message(self, client):
        """Test that chat endpoint requires a message."""
        response = client.post('/chat', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data


class TestClearRoute:
    """Tests for the clear route."""
    
    def test_clear_returns_200(self, client):
        """Test that clear endpoint returns 200 status code."""
        response = client.post('/clear')
        assert response.status_code == 200
    
    def test_clear_returns_status(self, client):
        """Test that clear endpoint returns cleared status."""
        response = client.post('/clear')
        data = response.get_json()
        assert data['status'] == 'cleared'


class TestStaticFiles:
    """Tests for static file serving."""
    
    def test_index_contains_chat_container(self, client):
        """Test that index page contains chat container element."""
        response = client.get('/')
        assert b'chatContainer' in response.data
    
    def test_index_contains_message_input(self, client):
        """Test that index page contains message input element."""
        response = client.get('/')
        assert b'messageInput' in response.data

