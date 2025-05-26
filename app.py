from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/trigger-error')
def trigger_error():
    response = {
        "error": "Something went wrong",
        "code": 400,
        "message": "This is a simulated error response"
    }
    return jsonify(response), 400  # HTTP 400 Bad Request

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return f"You accessed path: /{path}\n", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
