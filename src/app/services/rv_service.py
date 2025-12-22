class RvServiceException(Exception):
    pass

class RvService:
    def __init__(self, rv_dao, brand_dao, rv_type_dao):
        self.rv_dao = rv_dao
        self.brand_dao = brand_dao
        self.rv_type_dao = rv_type_dao

    def create_new_rv(self, spz, manufacture_date, price_for_day, brand_id, type_id):

        if not self.brand_dao.select_brand_by_id(brand_id):
            raise RvServiceException(f"Brand with ID {brand_id} does not exist")

        if not self.rv_type_dao.select_type_by_id(type_id):
            raise RvServiceException(f"RV Type with ID {type_id} does not exist")

        if price_for_day <= 0:
            raise RvServiceException("Price per day must be positive")

        self.rv_dao.create_rv(spz, manufacture_date, price_for_day, brand_id, type_id)

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

        if price_for_day is not None and price_for_day <= 0:
            raise RvServiceException("Price per day must be positive")

        self.rv_dao.update_rv(rv_id, spz, manufacture_date, price_for_day, id_brand, id_type)

    def delete_rv(self, rv_id):

        self.rv_dao.delete_rv(rv_id)

    def check_rv_availability(self, rv_id, date_from, date_to):

        return self.rv_dao.check_availability(rv_id, date_from, date_to)

