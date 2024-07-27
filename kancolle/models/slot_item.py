"""Slot Item Model."""


class SlotItem:
    """Slot Item Model."""

    def __init__(self, item_id, name, type_id_list) -> None:
        """Initializes an instance of the class.

        Args:
            item_id (int): The ID of the slot item.
            name (str): The name of the slot item.
            type_id_list (list): The type ID list of the slot item.

        Returns:
            None
        """
        self.id = item_id
        self.name = name
        self.type_id_list = type_id_list


def load_slot_item(json) -> SlotItem:
    """Load slot item.

    Args:
        json (dict): json

    Returns:
        SlotItem:

    """
    return SlotItem(item_id=json.get("id"), name=json.get("name"), type_id_list=json.get("type"))


def load_slot_item_list(json_list) -> list[SlotItem]:
    """Load slot item list.

    Args:
        json_list (list[dict]): json list

    Returns:
        list[SlotItem]:

    """
    return [load_slot_item(json) for json in json_list]
