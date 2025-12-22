class BrandServiceException(Exception):
    pass

class BrandService:
    def __init__(self, brand_dao, rv_dao):
        self.brand_dao = brand_dao
        self.rv_dao = rv_dao

    def create_brand(self, name):

        if not name or not name.strip():
            raise BrandServiceException("Brand name cannot be empty")

        brands = self.brand_dao.all_brands()
        for brand in brands:
            if brand[0].lower() == name.lower():
                raise BrandServiceException(f"Brand '{name}' already exists")

        self.brand_dao.create_brand(name.strip())

    def get_all_brands(self):

        return self.brand_dao.all_brands()

    def get_all_brands_with_ids(self):

        return self.brand_dao.get_brands_with_ids()

    def get_brand_by_id(self, brand_id):

        return self.brand_dao.select_brand_by_id(brand_id)

    def update_brand(self, brand_id, name):

        if not name or not name.strip():
            raise BrandServiceException("Brand name cannot be empty")

        self.brand_dao.update_brand(brand_id, name.strip())

    def delete_brand(self, brand_id):

        if self.rv_dao.count_rvs_by_brand(brand_id) > 0:
            raise BrandServiceException("Cannot delete brand - it is used by RVs")

        self.brand_dao.delete_brand(brand_id)