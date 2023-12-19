"""Ship Type Model."""


class ShipType(object):
    """Ship Type.

    from data shiptype.json

    """

    def __init__(self, type_id, name, chinese_name, english_name):
        """Initialize the instance variables.

        Args:
            type_id (int): The type id
            name (str): The name
            chinese_name (str): The Chinese name
            english_name (str): The English name
        """
        self.id = type_id  # The type id
        self.name = name  # The name
        self.chinese_name = chinese_name  # The Chinese name
        if english_name == "Fast BB":
            english_name = "FBB"
        if english_name == "CLp":
            english_name = "CT"
        self.english_name = english_name  # The English name


def load_ship_type(json) -> ShipType:
    """Load ship type.

    Args:
        json (dict): json

    Returns:
        ShipType:

    """
    return ShipType(
        type_id=json.get("id"),
        name=json.get("name"),
        chinese_name=json.get("chinese_name"),
        english_name=json.get("english_name"),
    )


def load_ship_type_list(json_list) -> list[ShipType]:
    """Load ship type list.

    Args:
        json_list (list[dict]): json list

    Returns:
        list[ShipType]:

    """
    return [load_ship_type(json) for json in json_list]
