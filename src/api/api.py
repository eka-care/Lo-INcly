
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from src.linker.engine import Engine

app = Flask(__name__)
cors = CORS(app)


cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:5555"}})

linking_engine = Engine()

@app.route("/")
@cross_origin()
def root():
    return app.send_static_file("index.html")


@app.route("/get_prediction", methods=["POST"])
@cross_origin()
def get_prediction():
    """
    This GET call is used for POC ui used for tuning the system. For deployed version there's the POST call
    Returns
    -------

    """
    prediction = {}

    if request.method == "POST":
        test_name = request.form["test_name"]
        unit = request.form.get("unit", None)
        specimen = request.form.get("specimen", None)
        method = request.form.get("method", None)
        

        candidates = linking_engine.resolve(test_name, unit=unit, specimen=specimen, method=method)
        for cand in candidates:
            cand["loinc_url"] = f"https://loinc.org/{cand['loinc']}/"
            for key, val in cand.items():
                if str(val) == "nan":
                    cand[key] = ""

        prediction["candidates"] = candidates

    print(prediction)
    return jsonify({"status": "success", "prediction": prediction})


app.run(host="0.0.0.0", port="8089")

