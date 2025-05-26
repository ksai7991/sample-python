import logging
import traceback
from flask import Flask, jsonify

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/trigger-error')
def trigger_error():
    try:
        # Simulate an error by raising an exception
        raise ValueError("Simulated error for testing stack trace logging")
    except Exception as e:
        # Log the error with stack trace
        logger.error("Error triggered", exc_info=True)

        response = {
            "error": "Something went wrong",
            "code": 400,
            "message": str(e)
        }
        return jsonify(response), 400  # HTTP 400 Bad Request

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    logger.info(f"Accessed path: /{path}")
    return f"You accessed path: /{path}\n", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
