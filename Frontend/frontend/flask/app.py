from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# In-memory storage for demonstration purposes
data_store = [0,0]


@app.route('/')
def hello_world():  # Display the stored data
    return jsonify(data_store)


@app.route('/api/endpoint', methods=['POST'])
def receive_data():
    data = request.json
    data_store.append(data)  # Store the incoming data
    return jsonify({"status": "success", "data_received": data}), 200


if __name__ == '__main__':
    app.run(debug=True)
