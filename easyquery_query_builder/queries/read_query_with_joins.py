from easyvalid_data_validator.constraints import Constraint
from easyvalid_data_validator.validator import validate_json_data

from easyquery_query_builder.queries.read_query import ReadQuery


class ReadQueryWithJoins(ReadQuery):
    """ Subclass of ReadQuery which implements joins """
    def __init__(self, select_="", from_="", where_="", group_by_="", having_="", order_by_="", joins_=""):
        super().__init__(select_, from_, where_, group_by_, having_, order_by_)
        self.joins_: list[list[str] | str] = joins_

    def parse(self) -> str:
        """ Creates sql query expression can be extended with join statements using fields provided in instance """

        # validation of all fields - checks only types and types of members
        query_data = self.__dict__
        constraints = {
            "select_": {Constraint.IS_TYPE: str},
            "from_": {Constraint.IS_TYPE: str},
            "where_": {Constraint.IS_TYPE: str},
            "group_by_": {Constraint.IS_TYPE: str},
            "having_": {Constraint.IS_TYPE: str},
            "order_by_": {Constraint.IS_TYPE: str},
            "joins_": {Constraint.IS_TYPE: list, Constraint.ARRAY_MEMBERS_TYPE: list}
        }
        validate_json_data(query_data, constraints)

        # validation that force all fields to be properly structured - minimum of select and from statements, having only with group by
        s, f, w, g, h = self.select_, self.from_, self.where_, self.group_by_, self.having_
        if (s == "" and f == "") or (s != "" and f == "") or (s == "" and f != ""):
            raise ValueError("Query requirement is to have select and from statements")

        if h != "" and g == "":
            raise ValueError("You cannot use having block without declaring group by block")

        # concatenation of joins
        joins_exp = " ".join([f"join {table} as {alias} on {conditions}" for table, alias, conditions in self.joins_])

        # creation of sql query
        statement = f"{f'select {self.select_}' if self.select_ else ''}" \
                    f"{f' from {self.from_}' if self.from_ else ''}" \
                    f" {joins_exp}" \
                    f"{f' where {self.where_}' if self.where_ else ''}" \
                    f"{f' group by {self.group_by_}' if self.group_by_ else ''}" \
                    f"{f' having {self.having_}' if self.having_ else ''}" \
                    f"{f' order by' if self.order_by_ else ''}"
        return statement
