
# easyquery-query-builder

Main purpose of package is to provide user with ability to create sql queries using QueryBuilders which are implemented in Builder Project Pattern.

## Installation

Using pip:
```bash
  pip install easyquery-query-builder
```
Using poetry:
```bash
  poetry add easyquery-query-builder
```


    
## Tests and coverage

All functionalities are fully tested.

You are able to run tests on your own by using cloning repository and using it's virtual environment.

### 1. Clone repository and enter it's main directory
```bash
  git clone https://github.com/DSmolke/EASYQUERY_QUERY_BUILDER.git
  cd EASYQUERY_QUERY_BUILDER
```
### 2. Set up and enter virtual environment using poetry

* if you don't have poetry, first install it:
```bash
  pip install poetry
```
* install environment and enter shell:
```bash
  poetry update
  poetry shell
```
(poetry update is used due to some issue that I faced with newest Python version)

### 3. Run tests using pytest
```bash
  poetry run pytest -vv
```

### 4. Access coverage report

If you haven't done step 1, start from here:
```bash
  git clone https://github.com/DSmolke/EASYQUERY_QUERY_BUILDER.git
  cd EASYQUERY_QUERY_BUILDER
```
Then use this command to change branch
```bash
  git checkout with_coverage_files
```

You should be able to see htmlcov directory. Enter it and open index.html file to see full coverage report.






## Basic usage
Let's say we need to prepare query where we ask database for all records from drivers table, joined with licenses table on license id:
```
from easyquery_query_builder.queries import ReadQueryWithJoinBuilder, ReadQueryWithJoins

query: ReadQueryWithJoins = ReadQueryWithJoinBuilder() \
    .add_select_statement('*') \
    .add_from_statement('drivers') \
    .add_joins_statement([['licenses', 'l', 'l.id = drivers.license_id']])\
    .build()
```
Once we built our query it's ready to be used:
```
print(query.parse())
```
with result of:
```
select * from drivers join licenses as l on l.id = drivers.license_id
```

## Objects

At this stage of development one abstract class and two 
inheriting classes are implemented:

### Query
Contains one abstract method .parse() which force to take no arguments and return string value.
It will be used for final step in query creation.

```
class Query(ABC):
    
    @abstractmethod
    def parse(self) -> str:
        pass
```

### ReadQuery
It's purpose is to create and manage sql query that will be returned using parse method.

#### Can be initialised without arguments or with one or more of them:
```
class ReadQuery:
    def __init__(self, select_="", from_="", where_="", group_by_="", having_="", order_by_=""):
        """ Empty query is created if no values are provided.(designed for builder)"""
        self.select_ = select_
        self.from_ = from_
        self.where_ = where_
        self.group_by_ = group_by_
        self.having_ = having_
        self.order_by_ = order_by_
```
As you can see, all statements like select, from etc. have sufix of '_'. It helps with modern IDE like PyCharm to hide sql syntax which can be targeted and indicate fake errors occurring in the code.

#### Parse method after simple arguments validation and query logic validation creates sql query expression:

```
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
```

### ReadQueryWithJoins
Class that inheriting ReadQuery, there are two minor differences between them:

#### Initialisation:
```
class ReadQueryWithJoins(ReadQuery):
    """ Subclass of ReadQuery which implements joins """
    def __init__(self, select_="", from_="", where_="", group_by_="", having_="", order_by_="", joins_=""):
        super().__init__(select_, from_, where_, group_by_, having_, order_by_)
        self.joins_: list[list[str] | str] = joins_
```
filed joins_ added

#### Parse method
```
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
```
```
"joins_": {Constraint.IS_TYPE: list, Constraint.ARRAY_MEMBERS_TYPE: list}
```
Added to constraints and validated, as well as jons_exp now is a part of sql statement.

## Builders

Their role is to create new or manage existing queries

### ReadQueryBuilder

#### Initialisation:
```
class ReadQueryBuilder:
    """ Builder used to create new ReadQueries 'from scratch' or modify existing ones to desired form """
    def __init__(self, query: Query | None = None):
        if query is None:
            self.query = ReadQuery()
        else:
            self.query = query
```
At this stage, new ReadQuery is made if no query is provided as an argument.

#### Query management:
User can change state of query at any point by using one of method that has same structure as this one:
```
    def add_select_statement(self, new_select: str) -> Self:
        """ Ads new select statement provided by user. Basic validation of argument is performed"""
        data = {"new_select": new_select}
        constraints = {"new_select": {Constraint.IS_TYPE: str}}
        validate_json_data(data, constraints)
        self.query.select_ = new_select
        return self
```
It allows us to chain methods:
```
ReadQueryBuilder().add_select_statement('*').add_from_statement('cars').add_where_statement('production_year > 2020')
```
#### List of valid methods:
- add_select_statement
- add_from_statement
- add_where_statement
- add_group_by_statement
- add_having_statement
- add_order_by_statement

and 

#### build method
Basically returns query that was created or managed by builder:
```
    def build(self) -> ReadQuery:
        """ Builds query based on all operations that were made """
        return self.query
```
### ReadQueryWithJoinsBuilder
#### Initialisation:
Inherits ReadQueryBuilder but operates on ReadQueryWithJoins:
```
    def __init__(self, query: Query | None = None):
        if query is None:
            self.query = ReadQueryWithJoins()
        else:
            self.query = query
```
#### Query management:
It has all the futures of ReadQueryBuilder but adds method for joins:
```
    def add_joins_statement(self, new_joins: str) -> Self:
        """ Ads new joins arguments provided by user. Basic validation of argument is performed"""
        data = {"new_joins": new_joins}
        constraints = {"new_joins": {Constraint.IS_TYPE: list, Constraint.ARRAY_MEMBERS_TYPE: list}}
        validate_json_data(data, constraints)
        self.query.joins_ = new_joins
        return self
```
#### List of valid methods:
- add_select_statement
- add_from_statement
- add_where_statement
- add_group_by_statement
- add_having_statement
- add_order_by_statement
- add_joins_statement

and 

#### build method
Basically returns query that was created or managed by builder:
```
    def build(self) -> ReadQueryWithJoins:
        """ Builds query based on all operations that were made """
        return self.query
```

## Rules and Errors
- When using all add_..._statement methods accept add_joins_statement, user needs to give expression with awareness of sql syntax:
```
ReadQueryBuilder().add_select_statement('id, age')
ReadQueryBuilder().add_select_statement('*')
ReadQueryBuilder().add_select_statement('cars.id, owner.*')
```

- Mandatory statements are select and from, if rule won't be followed it will cause ValueError:
```
query = ReadQueryBuilder().add_select_statement('*').build()
query.parse()
```
```
File "<some path....>", line 47, in parse
    raise ValueError("Query requirement is to have select and from statements")
ValueError: Query requirement is to have select and from statements
```

- Same thing will happen if we'll use having statement without group_by statement

```
query = ReadQueryBuilder()\
    .add_select_statement('*')\
    .add_from_statement('cars')\
    .add_having_statement("value > 300000")\
    .build()
query.parse()
```
```
  File "<some path....>", line 49, in parse
    raise ValueError("You cannot use having block without declaring group by block")
ValueError: You cannot use having block without declaring group by block

```
- When we use ReadQueryWithJoins we need to provide list of lists that contains table name, alias, and condition of join. We can use multiple joins:
```
query = ReadQueryWithJoinsBuilder()\
    .add_select_statement('*')\
    .add_from_statement('cars')\
    .add_joins_statement([['drivers', 'd', 'd.id = cars.driver_id'], ['producers', 'p', 'p.id = cars.prod_id']])\
    .build()
query.parse()
```
Outcome:
```
select * from cars join drivers as d on d.id = cars.driver_id join producers as p on p.id = cars.prod_id
```
- Any attempt of providing argument with wrong type will cause error in add_..._statement as well as in parse method:
```
query = ReadQueryWithJoinsBuilder()\
    .add_select_statement(100)\
    .add_from_statement('cars')
```
```
query = ReadQueryWithJoinsBuilder().add_select_statement(100)
```
```
    File "<some path....>", line 121, in validate_json_data
    raise ValidationError(dict(errors_by_key))
easyvalid_data_validator.customexceptions.common.ValidationError: {'new_select': ["Invalid type - isn't same type like compare type"]}
```
or in parse:
```
sql_expression = ReadQuery(select_=100).parse()
```

```
File File "<some path....>", line 121, in validate_json_data
    raise ValidationError(dict(errors_by_key))
easyvalid_data_validator.customexceptions.common.ValidationError: {'select_': ["Invalid type - isn't same type like compare type"]}
```
## Documentation link

[Github](https://github.com/DSmolke/EASYQUERY_QUERY_BUILDER/tree/master)

