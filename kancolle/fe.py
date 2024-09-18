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
from typing import List, Dict, Union
from kancolle.models import *

class FleetExpressionComponent:
    def __init__(self, ship_types: List[str], min_count: int, max_count: Union[int, float], positions: List[int], level_condition: int = 0, negated: bool = False):
        self.ship_types = ship_types
        self.min_count = min_count
        self.max_count = max_count if max_count != '*' else float('inf')
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
            if '*' in expr and 'ANY' not in ship_types:
                ship_types.append('ANY')
        else:
            ship_types = ['ANY']

        # Parse quantity
        quantity_match = re.search(r'\{(\d+)(?:,(\d+|\*|))?\}', expr)
        if quantity_match:
            min_count = int(quantity_match.group(1))
            max_count = quantity_match.group(2)
            if max_count is None:
                max_count = min_count  # This handles the {num} case
            elif max_count == '' or max_count == '*':
                max_count = float('inf')  # This handles the {num,} case
            else:
                max_count = int(max_count)
        else:
            min_count = max_count = 1

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
            return self._to_chinese_simplified()
        elif self.lang == 'zh_Hant':
            return self._to_chinese_traditional()
        elif self.lang == 'ja':
            return self._to_japanese()
        else:
            return self._to_english()

    def _to_chinese_simplified(self) -> str:
        result = []
        has_any = any('ANY' in comp.ship_types for comp in self.components)

        for component in self.components:
            if 'ANY' in component.ship_types and len(component.ship_types) == 1:
                continue

            ship_types = '/'.join(self._convert_ship_type(st) for st in component.ship_types if st != 'ANY')

            if component.min_count == component.max_count:
                count = f"{component.min_count}"
            elif component.min_count == 0 and component.max_count < float('inf'):
                count = f"至多{component.max_count}"
            elif component.min_count > 0 and component.max_count == float('inf'):
                count = f"至少{component.min_count}"
            else:
                count = f"{component.min_count}~{component.max_count}"

            position = "旗舰" if 0 in component.positions else ""

            level = f"(等级>{component.level_condition})" if component.level_condition > 0 else ""

            negated = "不能带" if component.negated else "需要"

            result.append(f"{negated}{count}个{ship_types}{position}{level}")

        if not has_any:
            result.append("不能带其它舰种")

        return '，'.join(result)

    def _to_chinese_traditional(self) -> str:
        result = []
        has_any = any('ANY' in comp.ship_types for comp in self.components)

        for component in self.components:
            if 'ANY' in component.ship_types and len(component.ship_types) == 1:
                continue

            ship_types = '/'.join(self._convert_ship_type(st) for st in component.ship_types if st != 'ANY')

            if component.min_count == component.max_count:
                count = f"{component.min_count}"
            elif component.min_count == 0 and component.max_count < float('inf'):
                count = f"至多{component.max_count}"
            elif component.min_count > 0 and component.max_count == float('inf'):
                count = f"至少{component.min_count}"
            else:
                count = f"{component.min_count}~{component.max_count}"

            position = "旗艦" if 0 in component.positions else ""

            level = f"(等級>{component.level_condition})" if component.level_condition > 0 else ""

            negated = "不能帶" if component.negated else "需要"

            result.append(f"{negated}{count}個{ship_types}{position}{level}")

        if not has_any:
            result.append("不能帶其它艦種")

        return '，'.join(result)

    def _to_japanese(self) -> str:
        result = []
        has_any = any('ANY' in comp.ship_types for comp in self.components)

        for component in self.components:
            if 'ANY' in component.ship_types and len(component.ship_types) == 1:
                continue

            ship_types = '/'.join(self._convert_ship_type(st) for st in component.ship_types if st != 'ANY')

            if component.min_count == component.max_count:
                count = f"{component.min_count}"
            elif component.min_count == 0 and component.max_count < float('inf'):
                count = f"最大{component.max_count}"
            elif component.min_count > 0 and component.max_count == float('inf'):
                count = f"少なくとも{component.min_count}"
            else:
                count = f"{component.min_count}~{component.max_count}"

            position = "旗艦" if 0 in component.positions else ""

            level = f"(レベル>{component.level_condition})" if component.level_condition > 0 else ""

            negated = "不可" if component.negated else "必要"

            result.append(f"{ship_types}{count}隻{negated}{position}{level}")

        if not has_any:
            result.append("他の艦種は不可")

        return '、'.join(result)

    def _to_english(self) -> str:
        result = []
        has_any = any('ANY' in comp.ship_types for comp in self.components)

        for component in self.components:
            if 'ANY' in component.ship_types and len(component.ship_types) == 1:
                continue

            ship_types = ' or '.join(self._convert_ship_type(st) for st in component.ship_types if st != 'ANY')

            if component.min_count == component.max_count:
                count = f"exactly {component.min_count}"
            elif component.min_count == 0 and component.max_count < float('inf'):
                count = f"up to {component.max_count}"
            elif component.min_count > 0 and component.max_count == float('inf'):
                count = f"at least {component.min_count}"
            else:
                count = f"{component.min_count} to {component.max_count}"

            position = " as flagship" if 0 in component.positions else ""

            level = f" (level > {component.level_condition})" if component.level_condition > 0 else ""

            negated = "Cannot have" if component.negated else "Require"

            result.append(f"{negated} {count} {ship_types}{position}{level}")

        if not has_any:
            result.append("No other ship types allowed")

        return ', '.join(result)

    def _convert_ship_type(self, ship_type: str) -> str:
        # This method should be implemented to convert ship types to their proper names
        # based on the language. For now, we'll just return the ship type as is.
        return ship_type

def resolve(expr: str, lang: str = 'zh_Hans') -> str:
    fe = FleetExpression(expr, lang)
    return fe.resolve()
