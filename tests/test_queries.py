import logging

import pytest
from easyvalid_data_validator.customexceptions.array import InvalidArgumentType
from easyvalid_data_validator.customexceptions.common import ValidationError

from easyquery_query_builder.queries import ReadQueryBuilder, Query, ReadQuery, ReadQueryWithJoinBuilder, \
    ReadQueryWithJoins


class TestReadQuery:
    # ----------------------------------------------------------------------
    # Clear cases
    # ----------------------------------------------------------------------

    def test_read_query_with_default_values(self, default_read_query) -> None:
        with pytest.raises(ValueError) as e:
            default_read_query.parse()
        assert e.value.args[0] == "Query requirement is to have select and from statements"
        assert e.type == ValueError
        assert default_read_query.__dict__ == {'from_': '', 'group_by_': '', 'having_': '', 'select_': '', 'where_': '',
                                               'order_by_': ''}

    def test_read_query_only_with_select(self, only_valid_select_read_query) -> None:
        with pytest.raises(ValueError) as e:
            only_valid_select_read_query.parse()
        assert e.value.args[0] == "Query requirement is to have select and from statements"
        assert e.type == ValueError

    def test_read_query_with_select_and_from(self, only_valid_select_and_from) -> None:
        result = only_valid_select_and_from.parse()
        assert result == "select * from teams"
        assert type(result) == str

    def test_read_query_with_valid_select_from_where(self, only_valid_select_from_where) -> None:
        result = only_valid_select_from_where.parse()
        assert type(result) == str
        assert result == "select * from teams where id > 0"

    def test_read_query_with_valid_select_from_where_group_by(self, only_valid_select_from_where_group_by) -> None:
        result = only_valid_select_from_where_group_by.parse()
        assert type(result) == str
        assert result == "select * from teams where id > 0 group by age"

    def test_read_query_with_valid_select_from_where_group_by_having(self,
                                                                     only_valid_select_from_where_group_by_having) -> None:
        result = only_valid_select_from_where_group_by_having.parse()
        assert type(result) == str
        assert result == "select * from teams where id > 0 group by age having age > 30"

    def test_read_query_with_valid_select_from_order_by(self, only_valid_select_and_from_order_by) -> None:
        result = only_valid_select_and_from_order_by.parse()
        assert type(result) == str
        assert result == "select * from teams order by id desc" \
               or result == "select * from teams order by id, name"

    # ----------------------------------------------------------------------
    # Cases with invalid structure
    # ----------------------------------------------------------------------

    def test_read_query_with_valid_select_but_without_from_and_with_other_statements(
            self, valid_select_but_invalid_structure) -> None:
        with pytest.raises(ValueError) as e:
            valid_select_but_invalid_structure.parse()
        assert e.value.args[0] == "Query requirement is to have select and from statements"
        assert e.type == ValueError

    def test_read_query_with_valid_from_but_without_select_and_with_other_statements(
            self, valid_from_but_invalid_structure):
        with pytest.raises(ValueError) as e:
            valid_from_but_invalid_structure.parse()
        assert e.value.args[0] == "Query requirement is to have select and from statements"
        assert e.type == ValueError

    def test_read_query_without_select_and_from_but_without_select_and_with_other_statements(
            self, without_select_and_from_but_with_other_statements):
        with pytest.raises(ValueError) as e:
            without_select_and_from_but_with_other_statements.parse()
        assert e.value.args[0] == "Query requirement is to have select and from statements"
        assert e.type == ValueError

    def test_read_query_with_valid_select_from_but_having_without_group_by(
            self, valid_select_from_but_having_without_group_by) -> None:
        with pytest.raises(ValueError) as e:
            valid_select_from_but_having_without_group_by.parse()
        assert e.value.args[0] == "You cannot use having block without declaring group by block"
        assert e.type == ValueError

    # ----------------------------------------------------------------------
    # Cases with invalid types provided as arguments
    # ----------------------------------------------------------------------

    def test_read_query_with_invalid_select_argument(self, invalid_select_argument) -> None:
        with pytest.raises(Exception) as e:
            invalid_select_argument.parse()
        assert e.type == ValidationError
        assert e.value.args[0] == {'select_': ["Invalid type - isn't same type like compare type"]}

    def test_read_query_with_invalid_from_argument(self, invalid_from_argument) -> None:
        with pytest.raises(Exception) as e:
            invalid_from_argument.parse()
        assert e.type == ValidationError
        assert e.value.args[0] == {'from_': ["Invalid type - isn't same type like compare type"]}

    def test_read_query_with_invalid_where_argument(self, invalid_where_argument) -> None:
        with pytest.raises(Exception) as e:
            invalid_where_argument.parse()
        assert e.type == ValidationError
        assert e.value.args[0] == {'where_': ["Invalid type - isn't same type like compare type"]}

    def test_read_query_with_invalid_group_by_argument(self, invalid_group_by_argument) -> None:
        with pytest.raises(Exception) as e:
            invalid_group_by_argument.parse()
        assert e.type == ValidationError
        assert e.value.args[0] == {'group_by_': ["Invalid type - isn't same type like compare type"]}

    def test_read_query_with_invalid_having_argument(self, invalid_having_argument) -> None:
        with pytest.raises(Exception) as e:
            invalid_having_argument.parse()
        assert e.type == ValidationError
        assert e.value.args[0] == {'having_': ["Invalid type - isn't same type like compare type"]}

    def test_read_query_with_invalid_order_by_argument(self, invalid_order_by_argument) -> None:
        with pytest.raises(Exception) as e:
            invalid_order_by_argument.parse()
        assert e.type == ValidationError
        assert e.value.args[0] == {'order_by_': ["Invalid type - isn't same type like compare type"]}


class TestReadQueryWithJoins:
    # ----------------------------------------------------------------------
    # Valid cases
    # ----------------------------------------------------------------------
    def test_read_query_with_joins_with_single_valid_data(self, valid_select_from_and_join_data) -> None:
        result = valid_select_from_and_join_data.parse()
        assert type(result) == str
        assert result == "select * from teams join cars as c on teams.id = c.id"

    def test_read_query_with_joins_with_multiple_valid_data(self, valid_select_from_and_multiple_join_data) -> None:
        result = valid_select_from_and_multiple_join_data.parse()
        assert type(result) == str
        assert result == "select * from teams join cars as c on teams.id = c.id join players as p on teams.id = p.id"

    # ----------------------------------------------------------------------
    # Cases with invalid types provided as arguments
    # ----------------------------------------------------------------------
    def test_read_query_with_joins_with_invalid_arguments_types(self, valid_select_from_and_invalid_join_argument) -> None:
        with pytest.raises(Exception) as e:
            valid_select_from_and_invalid_join_argument.parse()
        assert e.type == ValidationError or InvalidArgumentType
        assert e.value.args[0] == 'Invalid array - some or all members have unexpected type' or 'Invalid elements argument type'

class TestReadQueryBuilder:
    def test_builder_initialisation_without_query(self) -> None:
        assert ReadQueryBuilder().query.__dict__ == {
            'from_': '',
            'group_by_': '',
            'having_': '',
            'select_': '',
            'where_': '',
            'order_by_': ''
        }

    def test_builder_initialisation_with_query(self, only_valid_select_and_from) -> None:
        query = only_valid_select_and_from
        logging.info(query)
        assert ReadQueryBuilder(query=query).query.__dict__ == {
            'select_': '*',
            'from_': 'teams',
            'group_by_': '',
            'having_': '',
            'where_': '',
            'order_by_': ''
        }

    def test_adding_valid_select_statement(self) -> None:
        assert ReadQueryBuilder().add_select_statement("*").query.__dict__ == {
            'select_': '*',
            'from_': '',
            'group_by_': '',
            'having_': '',
            'where_': '',
            'order_by_': ''
        }

    @pytest.mark.parametrize("select_statement", [
        (1, ), ((), ), ([], ), ({}, )
    ])
    def test_adding_invalid_select_statement(self, select_statement) -> None:
        with pytest.raises(ValidationError) as e:
            assert ReadQueryBuilder().add_select_statement(select_statement)
        assert e.value.args[0] == {'new_select': ["Invalid type - isn't same type like compare type"]}

    def test_adding_valid_from_statement(self) -> None:
        assert ReadQueryBuilder().add_from_statement("cars").query.__dict__ == {
            'select_': '',
            'from_': 'cars',
            'group_by_': '',
            'having_': '',
            'where_': '',
            'order_by_': ''
        }

    @pytest.mark.parametrize("from_statement", [
        (1, ), ((), ), ([], ), ({}, )
    ])
    def test_adding_invalid_from_statement(self, from_statement) -> None:
        with pytest.raises(ValidationError) as e:
            assert ReadQueryBuilder().add_from_statement(from_statement)
        assert e.value.args[0] == {'new_from': ["Invalid type - isn't same type like compare type"]}

    def test_adding_valid_gr_statement(self) -> None:
        assert ReadQueryBuilder().add_select_statement("*").query.__dict__ == {
            'select_': '*',
            'from_': '',
            'group_by_': '',
            'having_': '',
            'where_': '',
            'order_by_': ''
        }

    def test_adding_valid_group_by_statement(self) -> None:
        assert ReadQueryBuilder().add_group_by_statement("id").query.__dict__ == {
            'select_': '',
            'from_': '',
            'group_by_': 'id',
            'having_': '',
            'where_': '',
            'order_by_': ''
        }

    @pytest.mark.parametrize("group_by_statement", [
        (1, ), ((), ), ([], ), ({}, )
    ])
    def test_adding_invalid_group_by_statement(self, group_by_statement) -> None:
        with pytest.raises(ValidationError) as e:
            assert ReadQueryBuilder().add_group_by_statement(group_by_statement)
        assert e.value.args[0] == {'new_group_by': ["Invalid type - isn't same type like compare type"]}

    def test_adding_valid_where_statement(self) -> None:
        assert ReadQueryBuilder().add_where_statement("id > 1").query.__dict__ == {
            'select_': '',
            'from_': '',
            'group_by_': '',
            'having_': '',
            'where_': 'id > 1',
            'order_by_': ''
        }

    @pytest.mark.parametrize("where_statement", [
        (1, ), ((), ), ([], ), ({}, )
    ])
    def test_adding_invalid_where_statement(self, where_statement) -> None:
        with pytest.raises(ValidationError) as e:
            assert ReadQueryBuilder().add_where_statement(where_statement)
        assert e.value.args[0] == {'new_where': ["Invalid type - isn't same type like compare type"]}

    @pytest.mark.parametrize("having_statement", [
        (1, ), ((), ), ([], ), ({}, )
    ])
    def test_adding_invalid_having_statement(self, having_statement) -> None:
        with pytest.raises(ValidationError) as e:
            assert ReadQueryBuilder().add_having_statement(having_statement)
        assert e.value.args[0] == {'new_having': ["Invalid type - isn't same type like compare type"]}

    def test_adding_valid_having_statement(self) -> None:
        assert ReadQueryBuilder().add_having_statement("id > 1").query.__dict__ == {
            'select_': '',
            'from_': '',
            'group_by_': '',
            'having_': 'id > 1',
            'where_': '',
            'order_by_': ''
        }

    def test_adding_valid_order_by_statement(self) -> None:
        assert ReadQueryBuilder().add_order_by_statement("id").query.__dict__ == {
            'select_': '',
            'from_': '',
            'group_by_': '',
            'having_': '',
            'where_': '',
            'order_by_': 'id'
        }

    @pytest.mark.parametrize("order_by_statement", [
        (1, ), ((), ), ([], ), ({}, )
    ])
    def test_adding_invalid_order_by_statement(self, order_by_statement) -> None:
        with pytest.raises(ValidationError) as e:
            assert ReadQueryBuilder().add_order_by_statement(order_by_statement)
        assert e.value.args[0] == {'new_order_by': ["Invalid type - isn't same type like compare type"]}

    def test_read_query_build(self) -> None:
        result_query = ReadQueryBuilder().add_select_statement("*").add_from_statement("cars").build()
        assert isinstance(result_query, ReadQuery)
        assert result_query.parse() == "select * from cars"

class TestReadQueryWithJoinsBuilder:
    # ----------------------------------------------------------------------
    # Valid cases
    # ----------------------------------------------------------------------
    def test_valid_join_statement(self) -> None:
        assert ReadQueryWithJoinBuilder().add_joins_statement([["teams", "t1", "t1.id = players.team_id"]]).query.__dict__ == {
            'select_': '',
            'from_': '',
            'group_by_': '',
            'having_': '',
            'where_': '',
            'order_by_': '',
            '_joins': [["teams", "t1", "t1.id = players.team_id"]]
        }

    @pytest.mark.parametrize("joins_statement", [
        (1,), ((),), ([],), ({},)
    ])
    def test_join_statement_with_invalid_argument(self, joins_statement) -> None:
        with pytest.raises(InvalidArgumentType) as e:
            assert ReadQueryWithJoinBuilder().add_joins_statement(joins_statement)
        assert e.value.args[0] == 'Invalid elements argument type'

    def test_read_query_with_join_build(self) -> None:
        result_query = ReadQueryWithJoinBuilder()\
            .add_select_statement("*")\
            .add_from_statement('players')\
            .add_joins_statement([["teams", "t1", "t1.id = players.team_id"]]).build()
        assert isinstance(result_query, ReadQueryWithJoins)
        assert result_query.parse() == 'select * from players join teams as t1 on t1.id = players.team_id'




