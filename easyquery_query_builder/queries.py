from abc import ABC, abstractmethod
from typing import Self
from easyvalid_data_validator.validator import validate_json_data
from easyvalid_data_validator.constraints import Constraint

import logging

logging.basicConfig(level=logging.INFO)

class Query(ABC):
    @abstractmethod
    def parse(self) -> str:
        pass


class ReadQuery:
    def __init__(self, select_="", from_="", where_="", group_by_="", having_="", order_by_=""):
        self.select_ = select_
        self.from_ = from_
        self.where_ = where_
        self.group_by_ = group_by_
        self.having_ = having_
        self.order_by_ = order_by_

    def parse(self) -> str:
        query_data = self.__dict__
        constraints = {
            "select_": {Constraint.IS_TYPE: str},
            "from_": {Constraint.IS_TYPE: str},
            "where_": {Constraint.IS_TYPE: str},
            "group_by_": {Constraint.IS_TYPE: str},
            "having_": {Constraint.IS_TYPE: str},
            "order_by_": {Constraint.IS_TYPE: str}
        }
        validate_json_data(query_data, constraints)

        s, f, w, g, h = self.select_, self.from_, self.where_, self.group_by_, self.having_
        if (s == "" and f == "") or (s != "" and f == "") or (s == "" and f != ""):
            raise ValueError("Query requirement is to have select and from statements")

        if h != "" and g == "":
            raise ValueError("You cannot use having block without declaring group by block")
        statement = f"{f'select {self.select_}' if self.select_ else ''}" \
                    f"{f' from {self.from_}' if self.from_ else ''}" \
                    f"{f' where {self.where_}' if self.where_ else ''}" \
                    f"{f' group by {self.group_by_}' if self.group_by_ else ''}" \
                    f"{f' having {self.having_}' if self.having_ else ''}" \
                    f"{f' order by {self.order_by_}' if self.order_by_ else ''}"
        return statement


class ReadQueryWithJoins(ReadQuery):
    def __init__(self, select_="", from_="", where_="", group_by_="", having_="", order_by_="", _joins=""):
        super().__init__(select_, from_, where_, group_by_, having_, order_by_)
        self._joins: list[list[str] | str] = _joins

    def parse(self) -> str:
        query_data = self.__dict__
        constraints = {
            "select_": {Constraint.IS_TYPE: str},
            "from_": {Constraint.IS_TYPE: str},
            "where_": {Constraint.IS_TYPE: str},
            "group_by_": {Constraint.IS_TYPE: str},
            "having_": {Constraint.IS_TYPE: str},
            "order_by_": {Constraint.IS_TYPE: str},
            "_joins": {Constraint.IS_TYPE: list, Constraint.ARRAY_MEMBERS_TYPE: list}
        }
        validate_json_data(query_data, constraints)

        s, f, w, g, h = self.select_, self.from_, self.where_, self.group_by_, self.having_
        if (s == "" and f == "") or (s != "" and f == "") or (s == "" and f != ""):
            raise ValueError("Query requirement is to have select and from statements")

        if h != "" and g == "":
            raise ValueError("You cannot use having block without declaring group by block")

        joins_exp = " ".join([f"join {table} as {alias} on {conditions}" for table, alias, conditions in self._joins])
        print(joins_exp)
        statement = f"{f'select {self.select_}' if self.select_ else ''}" \
                    f"{f' from {self.from_}' if self.from_ else ''}" \
                    f" {joins_exp}" \
                    f"{f' where {self.where_}' if self.where_ else ''}" \
                    f"{f' group by {self.group_by_}' if self.group_by_ else ''}" \
                    f"{f' having {self.having_}' if self.having_ else ''}" \
                    f"{f' order by' if self.order_by_ else ''}"
        return statement


class ReadQueryBuilder:
    def __init__(self, query: Query | None = None):
        if query is None:
            self.query = ReadQuery()
        else:
            self.query = query

    def add_select_statement(self, new_select: str) -> Self:
        data = {"new_select": new_select}
        constraints = {"new_select": {Constraint.IS_TYPE: str}}
        validate_json_data(data, constraints)
        self.query.select_ = new_select
        return self

    def add_from_statement(self, new_from: str) -> Self:
        data = {"new_from": new_from}
        constraints = {"new_from": {Constraint.IS_TYPE: str}}
        validate_json_data(data, constraints)
        self.query.from_ = f"{new_from}"
        return self

    def add_where_statement(self, new_where: str) -> Self:
        data = {"new_where": new_where}
        constraints = {"new_where": {Constraint.IS_TYPE: str}}
        validate_json_data(data, constraints)
        self.query.where_ = f"{new_where}"
        return self

    def add_group_by_statement(self, new_group_by: str) -> Self:
        data = {"new_group_by": new_group_by}
        constraints = {"new_group_by": {Constraint.IS_TYPE: str}}
        validate_json_data(data, constraints)
        self.query.group_by_ = f"{new_group_by}"
        return self

    def add_having_statement(self, new_having: str) -> Self:
        data = {"new_having": new_having}
        constraints = {"new_having": {Constraint.IS_TYPE: str}}
        validate_json_data(data, constraints)
        self.query.having_ = f"{new_having}"
        return self

    def add_order_by_statement(self, new_order_by: str) -> Self:
        data = {"new_order_by": new_order_by}
        constraints = {"new_order_by": {Constraint.IS_TYPE: str}}
        validate_json_data(data, constraints)
        self.query.order_by_ = f"{new_order_by}"
        return self

    def build(self) -> ReadQuery:
        return self.query

class ReadQueryWithJoinBuilder(ReadQueryBuilder):
    def __init__(self, query: Query | None = None):
        if query is None:
            self.query = ReadQueryWithJoins()
        else:
            self.query = query

    def add_joins_statement(self, new_joins: str) -> Self:
        data = {"new_joins": new_joins}
        constraints = {"new_joins": {Constraint.IS_TYPE: list, Constraint.ARRAY_MEMBERS_TYPE: list}}
        validate_json_data(data, constraints)
        self.query._joins = new_joins
        return self
