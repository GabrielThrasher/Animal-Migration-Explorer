import builtins
import sys
from unittest.mock import patch
import os

import app.main as main

def test_start_page_valid_s(capsys):
   
    with patch('builtins.input', return_value='s'), \
         patch('app.main.choose_habitat') as mock_choose:
        
        main.start_page()

        
        captured = capsys.readouterr()
        assert "Welcome to Animal Migration Explorer!" in captured.out
        assert "Valid commands" in captured.out

        
        mock_choose.assert_called_once()

def test_choose_habitat_valid_input(capsys):
    with patch('builtins.input', return_value='wetlands'), \
         patch('app.main.choose_animal') as mock_choose_animal:
        
        main.choose_habitat()
        
        captured = capsys.readouterr()
        assert "Wetlands" in captured.out  # prompt should contain habitat name
        mock_choose_animal.assert_called_once_with("Wetlands")
def test_choose_animal_calls_get_article_info(capsys):
    habitat = "Wetlands"
    animal = main.get_animal_selection()[habitat][0].lower()  # first animal lowercase
    
    with patch('builtins.input', side_effect=[animal]), \
         patch('app.main.get_article_info') as mock_get_info, \
         patch('app.main.start_page'), \
         patch('app.main.choose_habitat'):
        main.choose_animal(habitat)

        captured = capsys.readouterr()
        assert habitat in captured.out
        mock_get_info.assert_called_once_with(main.get_animal_selection()[habitat][0], habitat)

def test_choose_animal_back_calls_choose_habitat():
    habitat = "Wetlands"

    with patch('builtins.input', side_effect=['b']), \
         patch('app.main.choose_habitat') as mock_choose_habitat, \
         patch('app.main.start_page'), \
         patch('app.main.get_article_info'):
        main.choose_animal(habitat)
        mock_choose_habitat.assert_called_once()

def test_choose_animal_start_calls_start_page():
    habitat = "Wetlands"

    with patch('builtins.input', side_effect=['s']), \
         patch('app.main.start_page') as mock_start_page, \
         patch('app.main.choose_habitat'), \
         patch('app.main.get_article_info'):
        main.choose_animal(habitat)
        mock_start_page.assert_called_once()

def test_get_article_info_back_calls_choose_animal(capsys):
    animal = "Cranes"
    habitat = "Wetlands"

    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [("url1", "summary1"), ("url2", "summary2")]
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    with patch('sqlite3.connect', return_value=mock_conn), \
         patch('builtins.input', side_effect=['b']), \
         patch('app.main.choose_animal') as mock_choose_animal, \
         patch('app.main.start_page'), \
         patch('app.main.chatbot'):
        main.get_article_info(animal, habitat)

        captured = capsys.readouterr()
        assert "url1" in captured.out and "summary1" in captured.out
        assert "url2" in captured.out and "summary2" in captured.out

        mock_choose_animal.assert_called_once_with(habitat)
