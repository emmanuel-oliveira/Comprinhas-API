import os
from flask import jsonify
from App import app


@app.route("/status", methods=["GET"])
def status():
    data = {
        "status": True,
        "version": os.getenv("VERSION")
    }
    return jsonify(data), 200