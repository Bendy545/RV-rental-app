from src.db.dao.accessory import AccessoryDAOException, AccessoryNotFoundError as DAOAccessoryNotFoundError,  AccessoryDatabaseError as DAOAccessoryDatabaseError

class AccessoryServiceException(Exception):
    pass

class AccessoryValidationError(AccessoryServiceException):
    pass

class AccessoryNotFoundError(AccessoryServiceException):
    pass

class AccessoryDatabaseError(AccessoryServiceException):
    pass

class AccessoryService:
    def __init__(self, accessory_dao):
        self.accessory_dao = accessory_dao

    def create_accessory(self, name, description, price_for_day):

        try:

            if not name or not name.strip():
                raise AccessoryServiceException("Accessory name cannot be empty")

            if price_for_day <= 0:
                raise AccessoryServiceException("Price per day must be positive")

            self.accessory_dao.create_accessory(name.strip(), description.strip(), price_for_day)

        except AccessoryValidationError:
            raise

        except DAOAccessoryNotFoundError as e:
            raise AccessoryNotFoundError(str(e)) from e

        except DAOAccessoryDatabaseError as e:
            raise AccessoryDatabaseError(str(e)) from e

    def get_all_accessories(self):

        try:
            return self.accessory_dao.all_accessories()

        except DAOAccessoryDatabaseError as e:
            raise AccessoryDatabaseError(str(e)) from e

    def get_all_accessories_with_ids(self):

        try:
            return self.accessory_dao.all_accessories_with_ids()
        except DAOAccessoryDatabaseError as e:
            raise AccessoryDatabaseError(str(e)) from e

    def get_accessory_by_id(self, accessory_id):

        try:
            if not isinstance(accessory_id, int) or accessory_id <= 0:
                raise AccessoryValidationError("Accessory ID must be a positive integer")

            return self.accessory_dao.select_accessory_by_id(accessory_id)

        except AccessoryValidationError:
            raise

        except DAOAccessoryNotFoundError:
            raise AccessoryNotFoundError(f"Accessory with ID {accessory_id} not found")
        except DAOAccessoryDatabaseError as e:
            raise AccessoryDatabaseError(f"Database error: {str(e)}")

    def update_accessory(self, accessory_id, name=None, description=None, price_for_day=None):

        try:
            if not isinstance(accessory_id, int) or accessory_id <= 0:
                raise AccessoryValidationError("Accessory ID must be a positive integer")

            if name is not None:
                if not name or not name.strip():
                    raise AccessoryValidationError("Accessory name cannot be empty")

            if description is not None:
                if not description or not description.strip():
                    raise AccessoryValidationError("Description cannot be empty")

            if price_for_day is not None and price_for_day <= 0:
                raise AccessoryServiceException("Price per day must be positive")

            self.accessory_dao.update_accessory(accessory_id, name, description, price_for_day)

        except AccessoryValidationError:
            raise
        except DAOAccessoryNotFoundError:
            raise AccessoryNotFoundError(f"Accessory with ID {accessory_id} not found")
        except DAOAccessoryDatabaseError as e:
            raise AccessoryDatabaseError(f"Failed to update accessory: {str(e)}")
        except AccessoryDAOException as e:
            raise AccessoryServiceException(f"Unexpected DAO error: {str(e)}")

    def delete_accessory(self, accessory_id):

        try:
            if not isinstance(accessory_id, int) or accessory_id <= 0:
                raise AccessoryValidationError("Accessory ID must be a positive integer")

            self.accessory_dao.delete_accessory(accessory_id)

        except AccessoryValidationError:
            raise
        except DAOAccessoryNotFoundError:
            raise AccessoryNotFoundError(f"Accessory with ID {accessory_id} not found")
        except DAOAccessoryDatabaseError as e:
            raise AccessoryDatabaseError(f"Failed to delete accessory: {str(e)}")
        except AccessoryDAOException as e:
            raise AccessoryServiceException(f"Unexpected DAO error: {str(e)}")
