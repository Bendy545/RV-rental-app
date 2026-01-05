from src.db.dao.brand import BrandDAOException, BrandNotFoundError as DAOBrandNotFoundError, BrandDatabaseError as DAOBrandDatabaseError

class BrandServiceException(Exception):
    pass

class BrandValidationError(BrandServiceException):
    pass

class BrandNotFoundError(BrandServiceException):
    pass

class BrandDatabaseError(BrandServiceException):
    pass

class BrandService:
    def __init__(self, brand_dao, rv_dao):
        self.brand_dao = brand_dao
        self.rv_dao = rv_dao

    def create_brand(self, name):
        try:

            if not name or not name.strip():
                raise BrandValidationError("Brand name cannot be empty")

            self.brand_dao.create_brand(name.strip())
        except BrandValidationError:
            raise
        except DAOBrandDatabaseError as e:
            raise BrandDatabaseError(str(e)) from e
        except BrandDAOException as e:
            raise BrandServiceException(f"Unexpected DAO error: {str(e)}")

    def get_all_brands(self):
        try:
            return self.brand_dao.all_brands()
        except BrandDAOException as e:
            raise BrandServiceException(f"Failed to fetch brands: {str(e)}")

    def get_all_brands_with_ids(self):
        try:
            return self.brand_dao.select_brands_with_ids()
        except BrandDAOException as e:
            raise BrandServiceException(f"Failed to fetch brands with IDs: {str(e)}")

    def get_brand_by_id(self, brand_id):
        try:
            brand = self.brand_dao.select_brand_by_id(brand_id)
            if not brand:
                raise BrandNotFoundError(f"Brand with ID {brand_id} not found")
            return brand
        except BrandDAOException as e:
            raise BrandServiceException(f"Error fetching brand: {str(e)}")

    def update_brand(self, brand_id, name):
        try:
            if not name or not name.strip():
                raise BrandValidationError("Brand name cannot be empty")

            self.brand_dao.update_brand(brand_id, name.strip())

        except BrandValidationError:
            raise
        except DAOBrandNotFoundError as e:
            raise BrandNotFoundError(str(e)) from e
        except DAOBrandDatabaseError as e:
            raise BrandDatabaseError(str(e)) from e
        except BrandDAOException as e:
            raise BrandServiceException(f"Unexpected DAO error: {str(e)}")

    def delete_brand(self, brand_id):
        try:
            if self.rv_dao.count_rvs_by_brand(brand_id) > 0:
                raise BrandDatabaseError("Cannot delete brand - it is used by RVs")

            self.brand_dao.delete_brand(brand_id)

        except BrandValidationError:
            raise
        except DAOBrandNotFoundError as e:
            raise BrandNotFoundError(str(e)) from e
        except DAOBrandDatabaseError as e:
            raise BrandDatabaseError(str(e)) from e
        except BrandDAOException as e:
            raise BrandServiceException(f"Unexpected DAO error: {str(e)}")