import pytest
from easyvalid_data_validator.customexceptions.array import InvalidArgumentType
from easyvalid_data_validator.customexceptions.common import ValidationError


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
