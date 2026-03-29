from flask import Flask, request, jsonify
from error_query_vector_db import search_query

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():

    user_question = request.json["message"]

    response = search_query(user_question)

    return jsonify({"response": response})


app.run(debug=True)