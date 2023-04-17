from typing import Self

from easyvalid_data_validator.constraints import Constraint
from easyvalid_data_validator.validator import validate_json_data

from easyquery_query_builder.queries.query import Query
from easyquery_query_builder.queries.read_query_builder import ReadQueryBuilder
from easyquery_query_builder.queries.read_query_with_joins import ReadQueryWithJoins


class ReadQueryWithJoinsBuilder(ReadQueryBuilder):
    """
        Builder that is subclass of ReadQueryBuilder used to create new ReadQueriesWithJoin
        'from scratch' or modify existing ones to desired form
    """
    def __init__(self, query: Query | None = None):
        if query is None:
            self.query = ReadQueryWithJoins()
        else:
            self.query = query

    def add_joins_statement(self, new_joins: str) -> Self:
        """ Ads new joins arguments provided by user: [[<table_name>, <table_alias>, <join_condition>], ...]. Basic validation of argument is performed"""
        data = {"new_joins": new_joins}
        constraints = {"new_joins": {Constraint.IS_TYPE: list, Constraint.ARRAY_MEMBERS_TYPE: list}}
        validate_json_data(data, constraints)
        self.query.joins_ = new_joins
        return self

    def build(self) -> ReadQueryWithJoins:
        """ Builds query based on all operations that were made """
        return self.query
