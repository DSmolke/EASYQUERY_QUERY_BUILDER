import logging
import pytest

from easyquery_query_builder.queries import ReadQuery, ReadQueryWithJoins

logging.basicConfig(level=logging.INFO)

# ----------------------------------------------------------------------
# READ_QUERY
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# Valid objects
# ----------------------------------------------------------------------
@pytest.fixture
def default_read_query():
    return ReadQuery()

@pytest.fixture(params=["*", "column", "column_name", "column, column_n"])
def only_valid_select_read_query(request):
    """ Read queries with valid select statements """
    logging.info(request.param)
    return ReadQuery(select_=request.param)

@pytest.fixture
def only_valid_select_and_from():
    """ ReadQuery -> 'select * from teams' """
    return ReadQuery(select_="*", from_="teams")

@pytest.fixture
def only_valid_select_from_where():
    """ ReadQuery -> 'select * from teams where id > 0' """
    return ReadQuery(select_="*", from_="teams", where_="id > 0")


@pytest.fixture
def only_valid_select_from_where_group_by():
    """ ReadQuery -> 'select * from teams where id > 0 group by age' """
    return ReadQuery(select_="*", from_="teams", where_="id > 0", group_by_="age")

@pytest.fixture
def only_valid_select_from_where_group_by_having():
    """ ReadQuery -> 'select * from teams where id > 0 group by age having age > 30' """
    return ReadQuery(select_="*", from_="teams", where_="id > 0", group_by_="age", having_="age > 30")

@pytest.fixture(params=['id desc', 'id, name'])
def only_valid_select_and_from_order_by(request):
    """
        ReadQuery -> 'select * from teams order by id desc'
        ReadQuery -> 'select * from teams order by id, name'
    """
    return ReadQuery(select_="*", from_="teams", order_by_=request.param)

# ----------------------------------------------------------------------
# Cases with invalid structure
# ----------------------------------------------------------------------
@pytest.fixture(params=[
    {"select_": "*", "where_": "id > 0"},
    {"select_": "*", "group_by_": "age"},
    {"select_": "*", "having_": "age > 18"},
    {"select_": "*", "order_by_": "id"}
])
def valid_select_but_invalid_structure(request):
    """ Read queries with all invalid combinations for from statement """
    return ReadQuery(**request.param)


@pytest.fixture(params=[
    {"from_": "teams", "where_": "id > 0"},
    {"from_": "teams", "group_by_": "age"},
    {"from_": "teams", "having_": "age > 18"},
    {"from_": "teams", "order_by_": "id"}
])
def valid_from_but_invalid_structure(request):
    """ Read queries with all invalid combinations for from statement"""
    return ReadQuery(**request.param)


@pytest.fixture
def without_select_and_from_but_with_other_statements():
    """ ReadQuery -> 'where id > 0 group by age having age > 18 order by id' """
    return ReadQuery(where_="id > 0", group_by_="age", having_="age > 18", order_by_="id")

@pytest.fixture
def valid_select_from_but_having_without_group_by():
    """ ReadQuery -> 'select * from teams having age > 100' """
    return ReadQuery(select_="*", from_="teams", having_="age > 100")

# ----------------------------------------------------------------------
# Cases with invalid types provided as arguments
# ----------------------------------------------------------------------

@pytest.fixture(params=[1, (1, 1), []])
def invalid_select_argument(request):
    return ReadQuery(select_=request.param, from_='teams')

@pytest.fixture(params=[1, (1, 1), []])
def invalid_from_argument(request):
    return ReadQuery(select_="*", from_=request.param)

@pytest.fixture(params=[1, (1, 1), []])
def invalid_where_argument(request):
    return ReadQuery(select_="*", from_='teams', where_=request.param)

@pytest.fixture(params=[1, (1, 1), []])
def invalid_group_by_argument(request):
    return ReadQuery(select_="*", from_='teams', group_by_=request.param)

@pytest.fixture(params=[1, (1, 1), []])
def invalid_having_argument(request):
    return ReadQuery(select_="*", from_='teams', group_by_='id', having_=request.param)

@pytest.fixture(params=[1, (1, 1), []])
def invalid_order_by_argument(request):
    return ReadQuery(select_='*', from_='teams', order_by_=request.param)
# ----------------------------------------------------------------------
# / READ_QUERY
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# READ_QUERY_WITH_JOIN
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# Valid cases
# ----------------------------------------------------------------------
@pytest.fixture
def valid_select_from_and_join_data():
    return ReadQueryWithJoins(select_="*", from_="teams", joins_=[["cars", "c", "teams.id = c.id"]])

@pytest.fixture
def valid_select_from_and_multiple_join_data():
    return ReadQueryWithJoins(select_="*", from_="teams", joins_=[["cars", "c", "teams.id = c.id"], ["players", "p", "teams.id = p.id"]])

# ----------------------------------------------------------------------
# Cases with invalid types provided as arguments
# ----------------------------------------------------------------------
@pytest.fixture(params=[
    (('teams', 't', 'desc'),), [('teams', 't', 'desc')]
])
def valid_select_from_and_invalid_join_argument(request):
    return ReadQueryWithJoins(select_="*", from_="cars", joins_=request.param)
# ----------------------------------------------------------------------
# / READ_QUERY_WITH_JOIN
# ----------------------------------------------------------------------
