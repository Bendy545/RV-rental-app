from src.db.dao.rv import RvDAOException, RvNotFoundError as DAONotFound, RvDatabaseError as DAODatabase

class RvServiceException(Exception):
    pass
class RvValidationError(RvServiceException):
    pass
class RvNotFoundError(RvServiceException):
    pass
class RvDatabaseError(RvServiceException):
    pass

class RvService:
    def __init__(self, rv_dao, brand_dao, rv_type_dao):
        self.rv_dao = rv_dao
        self.brand_dao = brand_dao
        self.rv_type_dao = rv_type_dao

    def _validate_rv_data(self, spz, price, brand_id, type_id):
        if not spz or len(spz.strip()) < 5:
            raise RvValidationError("Invalid SPZ format")
        if price <= 0:
            raise RvValidationError("Price must be positive")
        if not self.brand_dao.select_brand_by_id(brand_id):
            raise RvValidationError("Selected brand does not exist")
        if not self.rv_type_dao.select_type_by_id(type_id):
            raise RvValidationError("Selected type does not exist")

    def create_new_rv(self, spz, manufacture_date, price_for_day, brand_id, type_id):
        try:
            self._validate_rv_data(spz, price_for_day, brand_id, type_id)
            self.rv_dao.create_rv(spz.strip().upper(), manufacture_date, price_for_day, brand_id, type_id)
        except DAODatabase as e:
            raise RvDatabaseError(str(e))
        except RvDAOException as e:
            raise RvServiceException(str(e))

    def get_all_rvs_formatted(self):

        rvs = self.rv_dao.all_rvs()

        formatted = []
        for rv in rvs:
            formatted.append({
                'id': rv[0],
                'spz': rv[1],
                'manufacture_date': rv[2],
                'price_per_day': float(rv[3]),
                'brand': rv[4],
                'type': rv[5]
            })

        return formatted

    def get_rv_by_id(self, rv_id):

        return self.rv_dao.select_rv_by_id(rv_id)

    def update_rv(self, rv_id, spz=None, manufacture_date=None, price_for_day=None, id_brand=None, id_type=None):
        try:

            if price_for_day is not None and price_for_day <= 0:
                raise RvValidationError("Price per day must be positive")

            self.rv_dao.update_rv(rv_id, spz, manufacture_date, price_for_day, id_brand, id_type)
        except DAONotFound:
            raise RvNotFoundError(f"RV {rv_id} not found")
        except DAODatabase as e:
            raise RvDatabaseError(str(e))

    def delete_rv(self, rv_id):
        try:
            self.rv_dao.delete_rv(rv_id)
        except DAONotFound:
            raise RvNotFoundError("RV not found")
        except DAODatabase as e:
            raise RvDatabaseError(str(e))

    def check_rv_availability(self, rv_id, date_from, date_to):

        return self.rv_dao.check_availability(rv_id, date_from, date_to)

