import pytest
from unittest.mock import MagicMock, patch
from web_interface.app import create_app

@pytest.fixture
def mock_nlp_client():
    mock = MagicMock()
    mock.analyze_entities.return_value = MagicMock(
        entities=[MagicMock(name='Brahman', type='OTHER', salience=0.9)]
    )
    return mock

@pytest.fixture
def mock_graph_driver():
    mock_session_run = MagicMock()
    mock_session_run.side_effect = [
        iter([{"id": "Brahman", "group": "OTHER"}]),
        iter([{"source": "Brahman", "target": "reality", "value": 0.9}])
    ]
    mock_session = MagicMock()
    mock_session.run = mock_session_run
    mock_driver = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    return mock_driver

@pytest.fixture
def client(mock_nlp_client, mock_graph_driver):
    app = create_app(nlp_client=mock_nlp_client, graph_driver=mock_graph_driver)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_get(client):
    """Test the index page loads correctly."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Sanskrit NLP" in rv.data

def test_index_post(client, mock_nlp_client, mock_graph_driver):
    """Test posting text to the index page."""
    with patch('sanskrit_nlp.main.KnowledgeGraph.add_entity') as mock_add_entity:
        rv = client.post('/', data={'text': 'Brahman is the ultimate reality.'})

        assert rv.status_code == 302 # Should redirect
        mock_add_entity.assert_called_once()

def test_graph_data(client, mock_graph_driver):
    """Test the graph data endpoint."""
    rv = client.get('/graph_data')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['nodes'][0]['id'] == 'Brahman'
    assert data['links'][0]['source'] == 'Brahman'
