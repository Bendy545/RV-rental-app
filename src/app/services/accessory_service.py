class AccessoryServiceException(Exception):
    pass

class AccessoryService:
    def __init__(self, accessory_dao):
        self.accessory_dao = accessory_dao

    def create_accessory(self, name, description, price_for_day):

        if not name or not name.strip():
            raise AccessoryServiceException("Accessory name cannot be empty")

        if price_for_day <= 0:
            raise AccessoryServiceException("Price per day must be positive")

        self.accessory_dao.create_accessory(name.strip(), description.strip(), price_for_day)

    def get_all_accessories(self):

        return self.accessory_dao.all_accessories()

    def get_all_accessories_with_ids(self):

        return self.accessory_dao.all_accessories_with_ids()

    def get_accessory_by_id(self, accessory_id):

        return self.accessory_dao.select_accessory_by_id(accessory_id)

    def update_accessory(self, accessory_id, name=None, description=None, price_for_day=None):

        if price_for_day is not None and price_for_day <= 0:
            raise AccessoryServiceException("Price per day must be positive")

        self.accessory_dao.update_accessory(accessory_id, name, description, price_for_day)

    def delete_accessory(self, accessory_id):

        self.accessory_dao.delete_accessory(accessory_id)

