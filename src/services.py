import csv
from io import StringIO
from database import DBConn
from datetime import datetime

class Validator:

    def __clean(self, input_string):
        return ''.join(filter(str.isdigit, input_string))

    def validate_cpf(self, cpf_str):
        cpf = self.__clean(cpf_str)
        if len(cpf) != 11:
            return False
        return True

    def validate_cnpj(self, cnpj_str):
        cnpj = self.__clean(cnpj_str)
        if len(cnpj) != 14:
            return False
        return True

    def validate_doc(self, cpf_cnpj):
        return self.validate_cpf(cpf_cnpj) or self.validate_cnpj(cpf_cnpj)


class MainService:
    def __init__(self):
        uri = "mongodb://localhost:27017/"
        db_name = "neoway"
        collection_name = "clients"
        unique_index = "cpf_cnpj"

        self.checker = Validator()
        self.db_conn = DBConn(uri=uri,
                              db_name=db_name,
                              collection_name=collection_name,
                              unique_index=unique_index
                             )
        
        self.init_time = datetime.now()
        self.usage_data = {
            'insert_single': 0,
            'insert_many': 0,
            'find_doc': 0,
            'status': 0
        }


    def insert_single(self, data):
        self.usage_data["insert_single"] += 1

        cpf_cnpj = data["cpf_cnpj"]
        message = {"success": False, "message": "Invalid cpf or cnpj."}

        if self.checker.validate_doc(cpf_cnpj):
            data["blocklist"] = False
            message = self.db_conn.insert_single(data)

        return message


    def format_document(self, doc):
        return {'cpf_cnpj': doc['DOCUMENTO'], 'name': doc['NOME/RAZAO_SOCIAL'], "blocklist": False}


    def insert_many(self, data_str):
        self.usage_data["insert_many"] += 1

        message = {"success": False, "message": "Unable to add the document."}

        csv_file = StringIO(data_str)
        csv_reader = csv.DictReader(csv_file)

        data = [self.format_document(row) for row in csv_reader if self.checker.validate_doc(row["DOCUMENTO"])]

        message = self.db_conn.insert_many(data)

        return message


    def find_doc(self,cpf_cnpj,name):
        self.usage_data["find_doc"] += 1

        result = {"success": False, "message": "Invalid input data."}

        if cpf_cnpj and self.checker.validate_doc(cpf_cnpj):
            result = self.db_conn.search_by_doc(cpf_cnpj)
            return result

        if name:
            result = self.db_conn.search_by_name(name)
            return result
        
        return result


    def get_status(self):
        self.usage_data["status"] += 1
        message = {"success": True, "message": "Data successfuly acquired."}

        usage = dict(self.usage_data)
        usage["total"] = sum(self.usage_data.values())

        timenow = datetime.now()
        usage["uptime"] = str(timenow-self.init_time)
        usage["timestamp"] = timenow.isoformat()

        message["data"] = usage

        return message

if __name__ == "__main__":
    service = MainService()

    t1 = {"cpf_cnpj": "075.210.019-07", "name": "Alqua Ayala"}
    print(service.insert_single(t1))
    t2 = {"cpf_cnpj": "30.607.887/0001-41321", "name": "Alphadale Curtis"}
    print(service.insert_single(t2))