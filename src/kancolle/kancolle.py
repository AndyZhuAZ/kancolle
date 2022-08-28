import quest


class KanColle:

    def __str__(self) -> str:
        return super().__str__()

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def quest(_id: str | None, name: str | None) -> quest.Quest:
        if _id:
            return quest.query_id(_id)
        if name:
            pass
