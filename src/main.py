from flask import Flask, request, jsonify
from datetime import datetime
from services import MainService
from datetime import datetime

app = Flask(__name__)

main_service = MainService()

@app.route("/insert", methods=["POST"])
def insert():
    """
    Handle POST requests to the /insert endpoint.

    This function receives data in JSON format from the request body
    and performs a single insertion operation.
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        result = main_service.insert_single(data)

        if result["success"]:
            return jsonify({"message": result["message"]}), 200
        else:
            return jsonify({"error": result.get("message", "Unknown error occurred")}), 400
    
    except Exception as e:
        print("ERROR: {}".format(e))
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route("/load-file", methods=["POST"])
def load_file():
    """
    Handle POST requests to /load-file endpoint.

    This function accepts a CSV file via POST request, reads its content,
    and save all in a single execution.
    """
    d1 = datetime.now()
    try:
        if 'file' not in request.files:
            return {"error": "No file part in the request"}, 400
        file = request.files['file']

        if file.filename == '':
            return {"error": "No file selected"}, 400

        file_content = file.read().decode("utf-8")
        result = main_service.insert_many(file_content)

        d2 = datetime.now()
        print("Time elapsed: {}".format((d2-d1)))
        if result["success"]:
            return jsonify({"message": result["message"]}), 200
        else:
            return jsonify({"error": result.get("message", "Unknown error occurred")}), 400


    except Exception as e:
        print("Error: {}".format(e))
        return {"error": "An unexpected error occurred"}, 500


@app.route("/search", methods=["GET"])
def search():
    """
    Handle GET requests to /search endpoint.

    This function accepts query parameters (cpf_cnpj or name) and search data based on it.
    """
    try:
        cpf_cnpj = request.args.get("cpf_cnpj")
        name = request.args.get("name")
        if not cpf_cnpj and not name:
            return jsonify({"error": "At least one search parameter (cpf_cnpj or name) must be provided"}), 400

        result = main_service.find_doc(cpf_cnpj,name)
        return jsonify(result), 200

    except Exception as e:
        print("Error: {}".format(e))
        return {"error": "An unexpected error occurred"}, 500


@app.route("/status", methods=["GET"])
def status():
    """
    Handle GET requests to /status endpoint.
    
    This function returns the uptime and requests count and current datetime in UTC.
    """
    try:
        result = main_service.get_status()

        return jsonify(result), 200

    except Exception as e:
        print("Error: {}".format(e))
        return {"error": "An unexpected error occurred"}, 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

