import pytest
from easyvalid_data_validator.customexceptions.array import InvalidArgumentType

from easyquery_query_builder.queries.read_query_with_joins import ReadQueryWithJoins
from easyquery_query_builder.queries.read_query_with_joins_builder import ReadQueryWithJoinsBuilder


class TestReadQueryWithJoinsBuilder:
    # ----------------------------------------------------------------------
    # Valid - invalid - valid
    # ----------------------------------------------------------------------
    def test_valid_join_statement(self) -> None:
        assert ReadQueryWithJoinsBuilder().add_joins_statement([["teams", "t1", "t1.id = players.team_id"]]).query.__dict__ == {
            'select_': '',
            'from_': '',
            'group_by_': '',
            'having_': '',
            'where_': '',
            'order_by_': '',
            'joins_': [["teams", "t1", "t1.id = players.team_id"]]
        }

    @pytest.mark.parametrize("joins_statement", [
        (1,), ((),), ([],), ({},)
    ])
    def test_join_statement_with_invalid_argument(self, joins_statement) -> None:
        with pytest.raises(InvalidArgumentType) as e:
            assert ReadQueryWithJoinsBuilder().add_joins_statement(joins_statement)
        assert e.value.args[0] == 'Invalid elements argument type'

    def test_read_query_with_join_build(self) -> None:
        result_query = ReadQueryWithJoinsBuilder()\
            .add_select_statement("*")\
            .add_from_statement('players')\
            .add_joins_statement([["teams", "t1", "t1.id = players.team_id"]]).build()
        assert isinstance(result_query, ReadQueryWithJoins)
        assert result_query.parse() == 'select * from players join teams as t1 on t1.id = players.team_id'
