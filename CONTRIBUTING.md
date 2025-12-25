

## Project structure

This project follows a ports and adapter approach to ensure decoupling. The main layer is ```entities``` where the entities and its rules are defined. 
All validation related to the entity must be implemented in this layer.
The ```services``` layer manage the entities and the state of the application. 
For example, if we want to create a ```Workspace```, the service will fetch the current user, check their permission, mark them as the workspace owner and save it.
This layer doesn't know anything about the technologies, for example, it doesn't know what is the database technology.
The services declare their dependencies on ```ports``` and assume it will be implemented outside. 
For example, the ```WorkspaceService``` depends on ```WorkspaceRepository``` that will store the workspace data. 
In the port ```WorkspaceRepository``` is defined the functions that this service needs.

The ```adapters``` layer is where the external dependencies are implemented. 
There, the database for ```Workspace``` is defined as SQL and the SQLAlchemy is used to talk to the database.

All the flow starts in the ```application``` layer. In this case, the application is an API that has its controllers defined in ```application/api/controllers/```.

### Generic definitions

There are some generic definitions that makes easier to implement new CRUDs. ```GenericService``` is an abstract class 
that implements CRUD functions. All entities that will be persisted should implement a service extending this ```GenericService```.
```GenericRepository``` is the abstract class with the CRUD functions that all repositories must implement. A service that implements ```GenericService``` needs a repository that implements ```GenericRepository```.

```GenericEntity``` is the abstract class that has some common attributes and functions for the entities. 

```GenericEntityRepository``` is the abstract repository for entities that extends ```GenericEntity```.

```GenericMapper``` is the class used to convert DTOs/entities. It is a class that will be extended for the entity mapper. For example, for entity ```User```, we need an implementation like this:

```
class UserMapper(GenericMapper[User]):
```

```GenericMapper``` uses the ```User``` type to know what it will instantiate as entity.

In the ```adapters``` layer, the ```SQLRepository``` implements the CRUD functions defined in the ```GenericRepository```. All SQL repositories must extend this repository.

There are 2 implementations of generic APIs that have some CRUD functions. ```GenericController``` is the controller with common functions to all entities, POST, PUT, DELETE, and GET by id. 
And ```GenericEntityController``` has functions related to ```GenericEntity```, like find all by workspace.

For each layer, there is a generic test class to be used. For service, it is ```GenericServiceTest```. If the entity extends ```GenericEntity```, the test should implement ```GenericEntityServiceTest```. 
For the repository layer, ```GenericRepositoryTest``` already implements some CRUD tests with database. And for ```GenericEntity```, it must use ```GenericEntityRepositoryTest```.
For the application layer, the generic API test is ```GenericControllerTest``` and for entities that extends ```GenericEntity```, it must extend ```GenericEntityController```.
It is very important to use these generic tests because it already ensures that the endpoints are authenticated and handle well errors.

### Tests approach

To make easier implement new tests, we consider some important things:
- our tests start with 3 items persisted for each entity. The first 2 active and a third one deleted
- the entities will have the same created_at and updated_at dates
- the entities will have the same created_by and updated_by.
- we have FIRST_DEFAULT_ID that will be used for the first object for each entity, and the SECOND_DEFAULT_ID that will be used for the second object for each entity

Each mock should have at least 2 functions:
- get_default_entity: will return the first persisted object. This one must be equal to the object defined in the load db script
- get_valid_entity: a function that returns a random entity

For integration tests, these files are used to prepare the scenarios:
- [init_database.sql](resources/db/init_database.sql): Create the database schema
- [init_database_load.sql](resources/db/init_database_load.sql): Insert the tests scenarios

### How to implement a new CRUD?
These are the steps you should follow to implement a new CRUD:

1. Create the entity in [entities](src/entities) package. Make this new class extends ```GenericEntity```. Implement the function ```_get_invalid_fields``` that check invalid fields and return as list. If this list is not empty, it will raise an exception assuming the object is invalid.
2. Create the entity repository definition in [ports](src/services/ports). It will be an abstract class with all the required functions to access data. This repository will extend ```GenericEntityRepository```.
3. Implement the entity service in [services](src/services). It should extend ```GenericEntityService```.
4. Prepare the test requirement. First we need to implement the mock functions. Implement a new mock utils in [mocks](tests/mocks). Implement the function to get a valid entity and the default entity.
5. Now implement the unit tests for this new service in [services](tests/unit_tests/services). It should extends ```GenericEntityServiceTest```
6. Implement the database model using SQLAlchemy in [models](src/adapters/sql/models). It needs to extend ```GenericEntityDB``` and ```Base``` that requires the entity type.
7. To implement the repository we are going to extends the generic repository and the ```SQLRepository``` that already provides some data access functions.
8. Add the new table to the file [init_database.sql](resources/db/init_database.sql).
9. Add the test scenario to the file [init_database_load.sql](resources/db/init_database_load.sql)
10. Implement the adapters tests in [sql](tests/integration_tests/adapters/sql). It should extend ```BaseSQLAlchemyTest``` and ```GenericEntityRepositoryTest```.
11. Add the service instance to the dependency injector in [dependency_injector.py](src/application/api/dependency_injector.py).
12. Create the DTO/entity mapper in [mappers](src/application/api/mappers). It should extend ```GenericMapper```.
13. Create the entity controller in [controllers](src/application/api/controllers). It should extend ```GenericEntityController```. This class constructor should receive ```app_injector: Injector``` as parameter. When defining the parent class, you need to put the entity service and entity mapper. Something like this: ```class TaskTypeController(GenericEntityController[TaskTypeService, TaskTypeMapper])```
14. Implement the API tests in [controllers](tests/integration_tests/application/api/controllers). It should extend ```BaseAPITest``` and ```GenericEntityControllerTests```.

### Technologies

- SQLAlchemy for database access. We are using Postgres as database
- Flask as the API lib
- injector is the dependency injector
