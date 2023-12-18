#!/usr/bin/env python
"""Tests for `kancolle` package."""

import pytest
from click.testing import CliRunner

from kancolle import cli


@pytest.fixture
def ship_data_response():
    """Ship data response."""
    from kancolle.data import KC_DATA_URL

    ship_data_url = KC_DATA_URL + "ship/ship.json"
    import requests  # type: ignore

    return requests.get(ship_data_url).json()


@pytest.fixture
def ship_type_response():
    """Ship type response."""
    from kancolle.data import KC_DATA_URL

    ship_type_url = KC_DATA_URL + "shiptype/all.json"
    import requests  # type: ignore

    return requests.get(ship_type_url).json()


@pytest.fixture
def ship_class_response():
    """Ship class response."""
    from kancolle.data import KC_DATA_URL

    ship_class_url = KC_DATA_URL + "shipclass/all.json"
    import requests  # type: ignore

    return requests.get(ship_class_url).json()


def test_load_ship_data(ship_data_response, ship_class_response, ship_type_response):
    """Test load ship data."""
    from kancolle.models import ship
    from kancolle.models import ship_class
    from kancolle.models import ship_type

    ships = ship.load_ships(ship_data_response)
    ship_classes = ship_class.load_ship_class_list(ship_class_response)
    ship_types = ship_type.load_ship_type_list(ship_type_response)

    assert ships[0].name == '睦月'

    class_name = next((sc.name for sc in ship_classes if sc.id == ships[0].class_id), '')

    assert ships[0].name in class_name

    type_name = next((st.name for st in ship_types if st.id == ships[0].type_id), '')

    assert type_name == "駆逐艦"


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'kancolle' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
