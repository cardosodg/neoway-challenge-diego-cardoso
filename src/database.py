from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, BulkWriteError

class DBConn:
    def __init__(self, uri, db_name, collection_name ,unique_index):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        try:
            self.collection.create_index([(unique_index, 1)], unique=True)
            print("Success in creating unique index named {}".format(unique_index))
        except Exception as e:
            print("Failed in creating unique index: {e}")


    def insert_single(self, document):
        """Add a single document in a collection"""
        try:
            result = self.collection.insert_one(document)
            print("Document added with ID: {}".format(result.inserted_id))
            return {
                "success": True,
                "message": "Document added successfully"
            }

        except DuplicateKeyError:
            print("Document already in database, will be ignored.")
            return {
                "success": True,
                "message": "Document already in database."
            }
        
        except Exception as e:
            print("Error saving document: {}".format(e))
            return {
                "success": False,
                "message": "{}".format(e)
            }


    def insert_many(self, document_list):
        """Add multiple documents in the collection"""
        try:
            result = self.collection.insert_many(document_list, ordered=False)
            print("{} documents added in database.".format(len(result.inserted_ids)))
            return {
                "success": True,
                "message": "Document added successfully"
            }

        except BulkWriteError as e:
            duplicate_count = sum(1 for error in e.details.get("writeErrors", []) if error["code"] == 11000)
            return {
                "success": True,
                "message": "Documents added in database. {} duplicates were ignored.".format(duplicate_count)
            }
        except Exception as e:
            print("Error saving documents: {}".format(e))
            return {
                "success": False,
                "message": "{}".format(e)
            }


    def search_by_doc(self, client_cpf_cnpj):
        """Find a single document searching by CPF or CNPJ"""
        try:
            result = self.collection.find_one({"cpf_cnpj": client_cpf_cnpj}, {"_id": 0})
            if result:
                print("Document found: {}".format(result))
                return {
                    "success": True,
                    "message": "Document found.",
                    "data": result
                }
            else:
                print("No document found for {}".format(client_cpf_cnpj))
                return {
                    "success": False,
                    "message": "No document found with the provided data."
                }

        except Exception as e:
            print("Error retrieving document: {}".format(e))
            return {
                "success": False,
                "message": "{}".format(e)
            }


    def search_by_name(self, client_name):
        """Find all documents with a given name and sort alphabetically"""
        try:
            query = {"name": {"$regex": client_name, "$options": "i"}}
            results = self.collection.find(query, {"_id": 0}).sort("name", 1)
            documents = list(results)
            if documents:
                print("Found {} documents.".format(len(documents)))
                return {
                    "success": True,
                    "message": "Documents found.",
                    "data": documents
                }
            else:
                print("No documents found with name = {}".format(client_name))
                return {
                    "success": False,
                    "message": "No documents found with the provided name."
                }

        except Exception as e:
            print("Error retrieving documents: {}".format(e))
            return {
                "success": False,
                "message": "{}".format(e)
            }


if __name__ == "__main__":
    uri = "mongodb://localhost:27017/"
    db_name = "meu_banco"
    collection_name = "usuarios"
    unique_index = 'email'

    # Instanciar a classe (índice será criado automaticamente)
    client = DBConn(uri, db_name, collection_name, unique_index)

    # Inserir um documento
    documento = {"nome": "João", "email": "joao@example.com", "idade": 30}
    client.insert_single(documento)