from typing import Self

from easyvalid_data_validator.constraints import Constraint
from easyvalid_data_validator.validator import validate_json_data

from easyquery_query_builder.queries.query import Query
from easyquery_query_builder.queries.read_query import ReadQuery


class ReadQueryBuilder:
    """ Builder used to create new ReadQueries 'from scratch' or modify existing ones to desired form """
    def __init__(self, query: Query | None = None):
        if query is None:
            self.query = ReadQuery()
        else:
            self.query = query

    def add_select_statement(self, new_select: str) -> Self:
        """ Ads new select statement provided by user. Basic validation of argument is performed"""
        data = {"new_select": new_select}
        constraints = {"new_select": {Constraint.IS_TYPE: str}}
        validate_json_data(data, constraints)
        self.query.select_ = new_select
        return self

    def add_from_statement(self, new_from: str) -> Self:
        """ Ads new from statement provided by user. Basic validation of argument is performed"""
        data = {"new_from": new_from}
        constraints = {"new_from": {Constraint.IS_TYPE: str}}
        validate_json_data(data, constraints)
        self.query.from_ = new_from
        return self

    def add_where_statement(self, new_where: str) -> Self:
        """ Ads new where statement provided by user. Basic validation of argument is performed"""
        data = {"new_where": new_where}
        constraints = {"new_where": {Constraint.IS_TYPE: str}}
        validate_json_data(data, constraints)
        self.query.where_ = new_where
        return self

    def add_group_by_statement(self, new_group_by: str) -> Self:
        """ Ads new group by statement provided by user. Basic validation of argument is performed"""
        data = {"new_group_by": new_group_by}
        constraints = {"new_group_by": {Constraint.IS_TYPE: str}}
        validate_json_data(data, constraints)
        self.query.group_by_ = new_group_by
        return self

    def add_having_statement(self, new_having: str) -> Self:
        """ Ads new having statement provided by user. Basic validation of argument is performed"""
        data = {"new_having": new_having}
        constraints = {"new_having": {Constraint.IS_TYPE: str}}
        validate_json_data(data, constraints)
        self.query.having_ = new_having
        return self

    def add_order_by_statement(self, new_order_by: str) -> Self:
        """ Ads new order by statement provided by user. Basic validation of argument is performed"""
        data = {"new_order_by": new_order_by}
        constraints = {"new_order_by": {Constraint.IS_TYPE: str}}
        validate_json_data(data, constraints)
        self.query.order_by_ = new_order_by
        return self

    def build(self) -> ReadQuery:
        """ Builds query based on all operations that were made """
        return self.query
