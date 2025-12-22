class RvTypeServiceException(Exception):
    pass

class RvTypeService:
    def __init__(self, rv_type_dao, rv_dao):
        self.rv_type_dao = rv_type_dao
        self.rv_dao = rv_dao

    def create_rv_type(self, name, description):

        if not name or not name.strip():
            raise RvTypeServiceException("RV type name cannot be empty")

        if not description or not description.strip():
            raise RvTypeServiceException("Description cannot be empty")

        types = self.rv_type_dao.all_types()
        for rv_type in types:
            if rv_type[0].lower() == name.lower():
                raise RvTypeServiceException(f"RV type '{name}' already exists")

        self.rv_type_dao.create_type(name.strip(), description.strip())

    def get_all_types(self):

        return self.rv_type_dao.all_types()

    def get_all_types_with_ids(self):

        return self.rv_type_dao.get_types_with_ids()

    def get_type_by_id(self, type_id):

        return self.rv_type_dao.select_type_by_id(type_id)

    def update_rv_type(self, type_id, name=None, description=None):

        if name is not None and (not name or not name.strip()):
            raise RvTypeServiceException("RV type name cannot be empty")

        if description is not None and (not description or not description.strip()):
            raise RvTypeServiceException("Description cannot be empty")

        self.rv_type_dao.update_type(type_id, name, description)

    def delete_rv_type(self, type_id):

        if self.rv_dao.count_rvs_by_type(type_id) > 0:
            raise RvTypeServiceException("Cannot delete RV type - it is used by RVs")

        self.rv_type_dao.delete_type(type_id)
