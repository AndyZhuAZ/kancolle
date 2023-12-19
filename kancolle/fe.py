"""KanColle fleet expression.

This module contains functions for resolving fleet expression.
Fleet expression are used to describe the components of a fleet.
For example, a fleet may consist of one BB and two CV, it can be written as BB{1}-CV{2}.
Fleet expression are parsed and resolved into a list of components.
It is similar to the regular expression syntax, but with a few differences.

sample fleet expressions:
=====================
BB|BBV|FBB{1,2}[0]-CV|CVB{0,2}-DD|DE*
---------------------
only have BB,BBV,FBB,CV,CVB,DD,DE, and BB,BBV,FBB have 1 or 2 as flagship(first
ship),CV,CVB have 0 or 2, DD,DE have 0 or more.
=====================
#543[0]-#424-#452-#425-ANY*
---------------------
have #543(長波改二) as flagship, include #424(高波,高波改,高波改二), #452(沖波,沖波改,沖波改二), #425(朝霜,朝霜改,朝霜改二)
and the ANY* is not limited other ships.
=====================
@30{4,}
---------------------
only have @30(陽炎型) and more than 4 ships.
=====================
#646![0]-ANY*
---------------------
have #646(加賀改二護) as flagship, not limited other ships.
=====================

>>> from kancolle.fe import resolve
>>> resolve('BB|BBV|FBB{1,2}[0]-CV|CVB{0,2}-DD|DE*', 'zh_Hans')

"""
import re


class FleetExpression:
    #  fleet expression.

    lang = 'zh_Hans'
    expr_list = []

    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return self.expr

    def resolve(self):
        self.expr_list = self.expr.split('-')

    def resolve_expr(self, expr: str):
        flag = FleetExpressionFlag(False)
        # sample: BB|BBV|FBB{1,2}[0]

        # match and remove part like [num] save the number
        match = re.match(r'(.*)\[(.*)]', expr)
        if match:
            expr = match.group(1)
            index = match.group(2)
            if index.isdigit():
                if index == '0':
                    flag.flagship = True
            else:
                for _ in index.split(','):
                    flag.index.append(_)

        # match and remove part like {num} or {num,num} {num,} {,num} save the numbers
        match = re.match(r'(.*)\{(\d+)(?:,(\d+))?\}', expr)
        if match:
            expr = match.group(1)
            min_num = match.group(2)
            max_num = match.group(3)
            if max_num is None:
                max_num = min_num
            assert type(min_num) is int
            assert type(max_num) is int

        prefix = self.convert_ship(expr)

        return f"have more than {flag.min_num} less than {flag.max_num} {prefix} at {flag.index}"

    def convert_ship(self, expr):
        if self.lang == 'zh_Hans':
            return f"covert expr to words here{expr}"
        else:
            raise Exception("not support")


class FleetExpressionFlag:
    #  fleet expression flag.
    optional_ship = []
    max_num = 0
    min_num = 0
    index = []

    def __init__(self, flagship):
        self.flagship = flagship


def resolve(expr: str, lang: str):
    fe = FleetExpression(expr)
    fe.lang = lang
    return str(fe)
