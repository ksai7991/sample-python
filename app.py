from flask import Flask, request

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return f"You accessed path: /{path}\n", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
