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

    def import_customers_from_csv(self, file_path):

        imported_count = 0
        errors = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row_num, row in enumerate(reader, start=2):
                    try:
                        self.customer_dao.create_customer(
                            name=row['name'].strip(),
                            surname=row['surname'].strip(),
                            email=row['email'].strip(),
                            tel=row['tel'].strip()
                        )
                        imported_count += 1
                    except KeyError as e:
                        errors.append(f"Row {row_num}: Missing column {e}")
                    except Exception as e:
                        errors.append(f"Row {row_num}: {str(e)}")

        except FileNotFoundError:
            raise ImportServiceException(f"File not found: {file_path}")
        except Exception as e:
            raise ImportServiceException(f"Error reading CSV: {str(e)}")

        return {'imported': imported_count, 'errors': errors}

    def import_brands_from_csv(self, file_path):

        imported_count = 0
        errors = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row_num, row in enumerate(reader, start=2):
                    try:
                        self.brand_dao.create_brand(name=row['name'].strip())
                        imported_count += 1
                    except KeyError as e:
                        errors.append(f"Row {row_num}: Missing column {e}")
                    except Exception as e:
                        errors.append(f"Row {row_num}: {str(e)}")

        except FileNotFoundError:
            raise ImportServiceException(f"File not found: {file_path}")
        except Exception as e:
            raise ImportServiceException(f"Error reading CSV: {str(e)}")

        return {'imported': imported_count, 'errors': errors}

    def import_accessories_from_json(self, file_path):

        imported_count = 0
        errors = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, list):
                raise ValueError("JSON must contain an array")

            for idx, item in enumerate(data):
                try:
                    self.accessory_dao.create_accessory(
                        name=item['name'].strip(),
                        description=item['description'].strip(),
                        price_for_day=Decimal(str(item['price_for_day']))
                    )
                    imported_count += 1
                except KeyError as e:
                    errors.append(f"Item {idx}: Missing key {e}")
                except Exception as e:
                    errors.append(f"Item {idx}: {str(e)}")

        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")

        return {'imported': imported_count, 'errors': errors}

    def import_rv_types_from_json(self, file_path):

        imported_count = 0
        errors = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, list):
                raise ValueError("JSON must contain an array")

            for idx, item in enumerate(data):
                try:
                    self.rv_type_dao.create_type(
                        name=item['name'].strip(),
                        description=item['description'].strip()
                    )
                    imported_count += 1
                except KeyError as e:
                    errors.append(f"Item {idx}: Missing key {e}")
                except Exception as e:
                    errors.append(f"Item {idx}: {str(e)}")

        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")

        return {'imported': imported_count, 'errors': errors}