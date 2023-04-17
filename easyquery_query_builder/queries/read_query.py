from easyvalid_data_validator.validator import validate_json_data
from easyvalid_data_validator.constraints import Constraint

class ReadQuery:
    def __init__(self, select_="", from_="", where_="", group_by_="", having_="", order_by_=""):
        """ Empty query is created if no values are provided.(designed for builder)"""
        self.select_ = select_
        self.from_ = from_
        self.where_ = where_
        self.group_by_ = group_by_
        self.having_ = having_
        self.order_by_ = order_by_

    def parse(self) -> str:
        """ Creates sql query expression using fields provided in instance """

        # validation of all fields - checks only types
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

        # validation that force all fields to be properly structured - minimum of select and from statements, having only with group by
        s, f, w, g, h = self.select_, self.from_, self.where_, self.group_by_, self.having_

        if (s == "" and f == "") or (s != "" and f == "") or (s == "" and f != ""):
            raise ValueError("Query requirement is to have select and from statements")
        if h != "" and g == "":
            raise ValueError("You cannot use having block without declaring group by block")

        # creation of sql query
        statement = f"{f'select {self.select_}' if self.select_ else ''}" \
                    f"{f' from {self.from_}' if self.from_ else ''}" \
                    f"{f' where {self.where_}' if self.where_ else ''}" \
                    f"{f' group by {self.group_by_}' if self.group_by_ else ''}" \
                    f"{f' having {self.having_}' if self.having_ else ''}" \
                    f"{f' order by {self.order_by_}' if self.order_by_ else ''}"
        return statement
