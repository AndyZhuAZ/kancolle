"""Main module."""
from kancolle.data import data
from kancolle.models import ship, ship_class, ship_type, slot_item


def get_ships():
    """Get all ships."""
    return [ship.load_ship(_data) for _data in data.load_ship_data()]


def get_ship_types():
    """Get all ship types."""
    return [ship_type.load_ship_type(_data) for _data in data.load_ship_type_data()]


def get_ship_classes():
    """Get all ship classes."""
    return [ship_class.load_ship_class(_data) for _data in data.load_ship_class_data()]


def get_slot_items():
    """Get all slot items."""
    return [slot_item.load_slot_item(_data) for _data in data.load_slot_item_data()]


class Kancolle:
    """Kancolle class."""

    def __init__(self):
        """Initialize."""
        self.ships = get_ships()
        self.ship_types = get_ship_types()
        self.ship_classes = get_ship_classes()
        self.slot_items = get_slot_items()
