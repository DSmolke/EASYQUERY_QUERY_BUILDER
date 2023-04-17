import pytest
from easyvalid_data_validator.customexceptions.common import ValidationError


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
