from src.db.dao.rv_type import (
    RvTypeDAOException,
    RvTypeNotFoundError as DAONotFound,
    RvTypeDatabaseError as DAODatabase
)

class RvTypeServiceException(Exception):
    pass
class RvTypeValidationError(RvTypeServiceException):
    pass
class RvTypeNotFoundError(RvTypeServiceException):
    pass
class RvTypeDatabaseError(RvTypeServiceException):
    pass

class RvTypeService:
    def __init__(self, rv_type_dao, rv_dao):
        self.rv_type_dao = rv_type_dao
        self.rv_dao = rv_dao

    def create_rv_type(self, name, description):
        try:
            if not name or not name.strip():
                raise RvTypeValidationError("RV type name cannot be empty")

            if not description or not description.strip():
                raise RvTypeValidationError("Description cannot be empty")

            types = self.rv_type_dao.all_types()
            for rv_type in types:
                if rv_type[0].lower() == name.lower():
                    raise RvTypeValidationError(f"RV type '{name}' already exists")

            self.rv_type_dao.create_type(name.strip(), description.strip())

        except DAODatabase as e:
            raise RvTypeDatabaseError(str(e))
        except RvTypeDAOException as e:
            raise RvTypeServiceException(str(e))

    def get_all_types(self):

        return self.rv_type_dao.all_types()

    def get_all_types_with_ids(self):

        return self.rv_type_dao.select_types_with_ids()

    def get_type_by_id(self, type_id):

        return self.rv_type_dao.select_type_by_id(type_id)

    def update_rv_type(self, type_id, name=None, description=None):
        try:

            if name is not None and (not name or not name.strip()):
                raise RvTypeServiceException("RV type name cannot be empty")

            if description is not None and (not description or not description.strip()):
                raise RvTypeServiceException("Description cannot be empty")

            self.rv_type_dao.update_type(type_id, name, description)

        except DAONotFound:
            raise RvTypeNotFoundError(f"Type {type_id} not found")
        except DAODatabase as e:
            raise RvTypeDatabaseError(str(e))

    def delete_rv_type(self, type_id):
        try:

            if self.rv_dao.count_rvs_by_type(type_id) > 0:
                raise RvTypeServiceException("Cannot delete RV type - it is used by RVs")

            self.rv_type_dao.delete_type(type_id)

        except DAONotFound:
            raise RvTypeNotFoundError("RV type not found")
        except DAODatabase as e:
            raise RvTypeDatabaseError(str(e))