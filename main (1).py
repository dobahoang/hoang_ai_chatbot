from flask import Flask
from flask import request, jsonify

from app import run_conversation

app = Flask(__name__)


@app.route('/get_services', methods=['POST'])
def get_services():
    data = request.get_json()
    print(data)
    user_query = data['content']
    response = run_conversation(user_query)
    print(response)

    return jsonify({'message': response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
