import json
import csv
from decimal import Decimal

class ImportServiceException(Exception):
    pass

class ImportService:
    def __init__(self, customer_dao, brand_dao, rv_type_dao, accessory_dao):
        self.customer_dao = customer_dao
        self.brand_dao = brand_dao
        self.rv_type_dao = rv_type_dao
        self.accessory_dao = accessory_dao

    def _validate_structure(self, current_keys, required_keys, entity_name):
        current_set = set(current_keys)
        if current_set != required_keys:
            missing = required_keys - current_set
            extra = current_set - required_keys
            error_msg = f"Ivalid structure for {entity_name}."
            if missing: error_msg += f" Missing: {', '.join(missing)}."
            if extra: error_msg += f" Resides: {', '.join(extra)}."
            raise ImportServiceException(error_msg)

    def import_customers_from_csv(self, file_path):

        imported_count = 0
        errors = []
        required= {'name', 'surname', 'email', 'tel'}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self._validate_structure(reader.fieldnames or [], required, "Customers")
                for row_num, row in enumerate(reader, start=2):
                    try:
                        self.customer_dao.create_customer(
                            name=row['name'].strip(),
                            surname=row['surname'].strip(),
                            email=row['email'].strip(),
                            tel=row['tel'].strip()
                        )
                        imported_count += 1
                    except Exception as e:
                        errors.append(f"Row {row_num}: {str(e)}")

        except Exception as e:
            raise ImportServiceException(f"Error reading CSV: {str(e)}")

        return {'imported': imported_count, 'errors': errors}

    def import_brands_from_csv(self, file_path):

        imported_count = 0
        errors = []
        required = {'name'}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self._validate_structure(reader.fieldnames or [], required, "Brands")

                for row_num, row in enumerate(reader, start=2):
                    try:
                        self.brand_dao.create_brand(name=row['name'].strip())
                        imported_count += 1
                    except Exception as e:
                        errors.append(f"Row {row_num}: {str(e)}")

        except Exception as e:
            raise ImportServiceException(f"Error reading CSV: {str(e)}")

        return {'imported': imported_count, 'errors': errors}

    def import_accessories_from_json(self, file_path):

        imported_count = 0
        errors = []
        required = {'name', 'description', 'price_for_day'}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, list):
                raise ValueError("JSON must contain an array")

            self._validate_structure(data[0].keys(), required, "Accessories")

            for idx, item in enumerate(data):

                try:

                    self.accessory_dao.create_accessory(
                        name=item['name'].strip(),
                        description=item['description'].strip(),
                        price_for_day=Decimal(str(item['price_for_day']))
                    )
                    imported_count += 1
                except Exception as e:
                    errors.append(f"Item {idx}: {str(e)}")

        except Exception as e:
            raise ImportServiceException(f"Error while importing JSON: {str(e)}")

        return {'imported': imported_count, 'errors': errors}

    def import_rv_types_from_json(self, file_path):

        imported_count = 0
        errors = []
        required = {'name', 'description'}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, list):
                raise ValueError("JSON must contain an array")

            self._validate_structure(data[0].keys(), required, "rv_types")

            for idx, item in enumerate(data):

                try:
                    self.rv_type_dao.create_type(
                        name=item['name'].strip(),
                        description=item['description'].strip()
                    )
                    imported_count += 1
                except Exception as e:
                    errors.append(f"Item {idx}: {str(e)}")

        except Exception as e:
            raise ImportServiceException(f"Error while importing JSON: {str(e)}")

        return {'imported': imported_count, 'errors': errors}