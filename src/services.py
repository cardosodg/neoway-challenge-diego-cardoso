import csv
from io import StringIO
from database import DBConn
from datetime import datetime

class Validator:

    def __clean(self, input_string):
        return ''.join(filter(str.isdigit, input_string))

    def validate_cpf(self, cpf_str):
        cpf = self.__clean(cpf_str)
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        numbers = [int(digit) for digit in cpf]


        sum_first = sum(num * i for num, i in zip(numbers[:9], range(10, 1, -1)))
        first_verifier = 11 - (sum_first % 11)
        first_verifier = first_verifier if first_verifier < 10 else 0
        if first_verifier != numbers[9]:
            return False

        sum_second = sum(num * i for num, i in zip(numbers[:10], range(11, 1, -1)))
        second_verifier = 11 - (sum_second % 11)
        second_verifier = second_verifier if second_verifier < 10 else 0
        if second_verifier != numbers[10]:
            return False

        return True

    def validate_cnpj(self, cnpj_str):
        cnpj = self.__clean(cnpj_str)
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False
        
        weights_first = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        weights_second = [6] + weights_first
        numbers = [int(digit) for digit in cnpj]

        sum_first = sum(num * weight for num, weight in zip(numbers[:12], weights_first))
        first_verifier = 11 - (sum_first % 11)
        first_verifier = first_verifier if first_verifier < 10 else 0
        if first_verifier != numbers[12]:
            return False

        sum_second = sum(num * weight for num, weight in zip(numbers[:13], weights_second))
        second_verifier = 11 - (sum_second % 11)
        second_verifier = second_verifier if second_verifier < 10 else 0
        if second_verifier != numbers[13]:
            return False

        return True

    def validate_doc(self, cpf_cnpj):
        return self.validate_cpf(cpf_cnpj) or self.validate_cnpj(cpf_cnpj)


class MainService:
    def __init__(self):
        uri = "mongodb://mongodb:27017/"
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
    validator = Validator()
    cpfs = ["123.456.789-09", "111.444.777-35", "000.000.000-00", "111.111.111-11"]
    for cpf in cpfs:
        if validator.validate_cpf(cpf):
            print("{}: ok".format(cpf))
        else:
            print("{}: not ok".format(cpf))

    print("\n")
    cnpjs = [
        "11.444.777/0001-61",
        "12.345.678/9012-34",
        "00.000.000/0000-00",
        "11.111.111/1111-11",
        ]
    for cnpj in cnpjs:
        if validator.validate_cnpj(cnpj):
            print("{}: ok".format(cnpj))
        else:
            print("{}: not ok".format(cnpj))