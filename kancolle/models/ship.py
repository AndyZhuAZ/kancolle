"""Ship model."""


class Ship(object):
    """Ship model.

    from data ship.json

    """

    def __init__(self, ship_id, name, class_id, type_id) -> None:
        """Initializes an instance of the class.

        Args:
            ship_id (int): The ID of the ship.
            name (str): The name of the ship.
            class_id (int): The class ID of the ship.
            type_id (int): The type ID of the ship.

        Returns:
            None
        """
        self.id = ship_id
        self.name = name
        self.class_id = class_id
        self.type_id = type_id


def load_ship(json) -> Ship:
    """Load ship from json.

    Args:
        json (dict): ship json data dict

    Returns:
        Ship: ship

    """
    return Ship(ship_id=json.get('id'), name=json.get('name'), class_id=json.get('ctype'), type_id=json.get('stype'))


def load_ship_list(json_list) -> list[Ship]:
    """Load ships from json list.

    Args:
        json_list (list[dict]): ship json list
    Returns:
        list[Ship]: ships
    """
    return [load_ship(json) for json in json_list]
