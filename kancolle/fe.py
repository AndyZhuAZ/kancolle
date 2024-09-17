"""KanColle fleet expression.

This module contains functions for resolving fleet expression.
Fleet expression are used to describe the components of a fleet.
For example, a fleet may consist of one BB and two CV, it can be written as BB{1}-CV{2}.
Fleet expression are parsed and resolved into a list of components.
It is similar to the regular expression syntax, but with a few differences.

Syntax Elements:
- |     : OR operator (e.g., BB|CV means BB or CV)
- {}    : Quantity specifier (e.g., {1,2} means 1 to 2, {2} means exactly 2, {2,} means 2 or more)
- []    : Position specifier (e.g., [0] means flagship position)
- *     : Zero or more of the preceding element
- !     : Negation (e.g., !(BB|BBV) means no BB or BBV)
- #     : Specific ship ID
- @     : Ship class ID
- ANY   : Any ship
- level : Ship level condition

sample fleet expressions:
=====================
(BB|BBV|FBB){1,2}[0]-(CV|CVB){0,2}-(DD|DE)*
---------------------
only have BB,BBV,FBB,CV,CVB,DD,DE, and BB,BBV,FBB have 1 or 2 as flagship(first
ship),CV,CVB have 0 or 2, DD,DE have 0 or more.
=====================
#543[0]-#424-#452-#425-ANY*
---------------------
have #543(長波改二) as flagship, include #424(高波,高波改,高波改二), #452(沖波,沖波改,沖波改二), #425(朝霜,朝霜改,朝霜改二)
and the ANY* is not limited other ships.
=====================
@30{4,}|@38{4,}
---------------------
only have @30(陽炎型) and more than 4 ships or have @38(夕雲型) and more than 4 ships
=====================
#646![0]-ANY*
---------------------
have #646(加賀改二護) as flagship, not limited other ships.
=====================
!(BB|BBV|FBB)
---------------------
can not have BB
=====================
ANY[0,level>70]
---------------------
The flag ship need level upper than 70
=====================

>>> from kancolle.fe import resolve
>>> resolve('BB|BBV|FBB{1,2}[0]-CV|CVB{0,2}-DD|DE*', 'zh_Hans')

"""
import re
from typing import List, Dict
from models import *

class FleetExpressionComponent:
    def __init__(self, ship_types: List[str], min_count: int, max_count: int, positions: List[int], level_condition: int = 0, negated: bool = False):
        self.ship_types = ship_types
        self.min_count = min_count
        self.max_count = max_count
        self.positions = positions
        self.level_condition = level_condition
        self.negated = negated

class FleetExpression:
    def __init__(self, expr: str, lang: str = 'zh_Hans'):
        self.expr = expr
        self.lang = lang
        self.components: List[FleetExpressionComponent] = []

    def resolve(self):
        self.expr_list = self.expr.split('-')
        for expr in self.expr_list:
            self.components.append(self.resolve_expr(expr))
        return self.to_string()

    def resolve_expr(self, expr: str) -> FleetExpressionComponent:
        negated = expr.startswith('!')
        if negated:
            expr = expr[1:]

        ship_types = []
        min_count = 1
        max_count = 1
        positions = []
        level_condition = 0

        # Parse ship types
        ship_type_match = re.match(r'([\w|@#]+)(?:\{|\[|$)', expr)
        if ship_type_match:
            ship_types = ship_type_match.group(1).split('|')

        # Parse quantity
        quantity_match = re.search(r'\{(\d+)(?:,(\d+))?\}', expr)
        if quantity_match:
            min_count = int(quantity_match.group(1))
            max_count = int(quantity_match.group(2) or min_count)

        # Parse positions
        position_match = re.search(r'\[([\d,]+)\]', expr)
        if position_match:
            positions = [int(pos) for pos in position_match.group(1).split(',')]

        # Parse level condition
        level_match = re.search(r'level>(\d+)', expr)
        if level_match:
            level_condition = int(level_match.group(1))

        return FleetExpressionComponent(ship_types, min_count, max_count, positions, level_condition, negated)

    def to_string(self) -> str:
        if self.lang == 'zh_Hans':
            return self._to_chinese()
        else:
            return self._to_english()

    def _to_chinese(self) -> str:
        result = []
        for component in self.components:
            ship_types = '或'.join(self._convert_ship_type(st) for st in component.ship_types)
            count = f"{component.min_count}" if component.min_count == component.max_count else f"{component.min_count}到{component.max_count}"
            positions = '任意位置' if not component.positions else f"位置 {', '.join(map(str, component.positions))}"
            level = f" 等级大于{component.level_condition}" if component.level_condition > 0 else ""
            negated = "不能有" if component.negated else "有"
            result.append(f"{negated}{count}艘{ship_types}在{positions}{level}")
        return '，'.join(result)

    def _to_english(self) -> str:
        result = []
        for component in self.components:
            ship_types = ' or '.join(self._convert_ship_type(st) for st in component.ship_types)
            count = f"{component.min_count}" if component.min_count == component.max_count else f"{component.min_count} to {component.max_count}"
            positions = 'any position' if not component.positions else f"position(s) {', '.join(map(str, component.positions))}"
            level = f" with level > {component.level_condition}" if component.level_condition > 0 else ""
            negated = "Cannot have" if component.negated else "Have"
            result.append(f"{negated} {count} {ship_types} in {positions}{level}")
        return ', '.join(result)

    def _convert_ship_type(self, ship_type: str) -> str:
        # This method should be implemented to convert ship types to their proper names
        # based on the language. For now, we'll just return the ship type as is.
        return ship_type

def resolve(expr: str, lang: str = 'zh_Hans') -> str:
    fe = FleetExpression(expr, lang)
    return fe.resolve()

if __name__ == "__main__":
    expr = "BB|BBV|FBB{1,2}[0]-CV|CVB{0,2}-DD|DE*"
    print(resolve(expr, 'zh_Hans'))
    print(resolve(expr, 'en'))
