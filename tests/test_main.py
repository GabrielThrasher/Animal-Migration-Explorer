import builtins
import sys
from unittest.mock import patch
import os

import app.main as main
import pytest
from unittest.mock import patch
from app.cli import CLI  # Make sure this path matches your project

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
