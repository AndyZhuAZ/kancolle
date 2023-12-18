"""Ship Class."""


class ShipClass(object):
    """Ship Class.

    from data shipclass.json: {"id": 1,"name": "綾波型","chinese_name": "绫波型"}


    """

    def __init__(self, class_id, name, chinese_name):
        """Initializes the instance with the specified class_id, name, and chinese_name. It doesn't return any value.

        Args:
            class_id (int): The ID for the class.
            name (str): The English name for the class.
            chinese_name (str): The Chinese name for the class.
        """
        self.id = class_id
        self.name = name
        self.chinese_name = chinese_name


def load_ship_class(json) -> ShipClass:
    """Load Ship Class from json.

    Args:
        json (dict):

    Returns:
        ShipClass

    """
    return ShipClass(class_id=json.get('id'), name=json.get('name'), chinese_name=json.get('chinese_name'))


def load_ship_class_list(json_list) -> list[ShipClass]:
    """Load Ship Class from json list.

    Args:
        json_list (list[dict]):

    Returns:
        list[ShipClass]

    """
    return [load_ship_class(json) for json in json_list]
