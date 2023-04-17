import pytest
from easyvalid_data_validator.customexceptions.common import ValidationError
from easyquery_query_builder.queries.read_query import ReadQuery
from easyquery_query_builder.queries.read_query_builder import ReadQueryBuilder


class TestReadQueryBuilder:
    # ----------------------------------------------------------------------
    # Valid cases, then valid case - invalid case ....   by statements
    # ----------------------------------------------------------------------
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
        assert ReadQueryBuilder(query=query).query.__dict__ == {
            'select_': '*',
            'from_': 'teams',
            'group_by_': '',
            'having_': '',
            'where_': '',
            'order_by_': ''
        }

    # ----------------------------------------------------------------------
    # by statements
    # ----------------------------------------------------------------------

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
