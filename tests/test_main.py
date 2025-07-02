import builtins
import sys
from unittest.mock import patch
import os

import app.main as main
import pytest
from unittest.mock import patch
from app.main import CLI  # Make sure this path matches your project

# Test 1: Welcome page should call habitat_page() on 's'
def test_welcome_page_calls_habitat_page(monkeypatch):
    cli = CLI()
    monkeypatch.setattr('builtins.input', lambda _: 's')

    with patch.object(cli, 'habitat_page') as mock_habitat_page:
        cli.welcome_page()
        mock_habitat_page.assert_called_once()


# Test 2: Habitat page sets habitat and calls animal_page()
def test_habitat_page_sets_habitat(monkeypatch):
    cli = CLI()
    monkeypatch.setattr('builtins.input', lambda _: '1')  # "Wetlands"

    with patch.object(cli, 'animal_page') as mock_animal_page:
        cli.habitat_page()
        assert cli.habitat == 'Wetlands'
        mock_animal_page.assert_called_once()


# Test 3: Animal page sets animal and calls article_page()
def test_animal_page_sets_animal(monkeypatch):
    cli = CLI()
    cli.habitat = 'Wetlands'
    monkeypatch.setattr('builtins.input', lambda _: '1')  # "Cranes"

    with patch.object(cli, 'article_page') as mock_article_page:
        cli.animal_page()
        assert cli.animal == 'Cranes'
        mock_article_page.assert_called_once()

from unittest.mock import patch, MagicMock

def test_article_page_map_option(monkeypatch):
    cli = CLI()
    cli.animal = 'Cranes'
    cli.habitat = 'Wetlands'

    # Mock database call
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [("http://example.com", "Sample Summary")]
    mock_conn.cursor.return_value = mock_cursor

    monkeypatch.setattr('builtins.input', lambda _: 'm')  # simulate 'm' for map

    with patch('sqlite3.connect', return_value=mock_conn), \
         patch('app.map_generation.generate_map') as mock_generate_map:
        
        mock_generate_map.return_value = "path/to/generated_map.png"
        cli.article_page()
        mock_generate_map.assert_called_once_with(
            'Cranes',
            '../database/coordinates.db',
            save_dir='map_generation/saved_maps/'
        )

def test_chatbot_page_saves_convo(monkeypatch, tmp_path):
    cli = CLI()
    cli.animal = 'Cranes'
    cli.habitat = 'Wetlands'
    cli.chatbot_convo = "YOU ASKED:\nWhere do cranes go?\nCHATBOT ANSWERED:\nThey migrate south."

    # Simulate user typing 's' to save the convo
    monkeypatch.setattr('builtins.input', lambda _: 's')

    with patch('builtins.open', create=True) as mock_open:
        cli.chatbot_page()
        mock_open.assert_called_once()
        file_handle = mock_open()
        file_handle.write.assert_called_once_with(cli.chatbot_convo.strip())
