import logging
import traceback
import random
from flask import Flask, jsonify

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

@app.route('/trigger-error')
def trigger_error():
    try:
        faulty_random_logic()
    except Exception as e:
        # Capture full stack trace
        stack_trace = traceback.format_exc()

        # Log the error and the stack trace
        logger.error("Full stack trace:\n%s", stack_trace)

        response = {
            "error": "Something went wrong",
            "code": 500,
            "message": str(e),
            "trace": stack_trace.splitlines()[-1]
        }
        return jsonify(response), 500

def faulty_random_logic():
    numbers = [random.randint(1, 100) for _ in range(5)]
    logger.info(f"Generated numbers: {numbers}")
    # Try to access an index that doesn't exist
    return numbers[10]  # This will raise IndexError

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    logger.info(f"Accessed path: /{path}")
    return f"You accessed path: /{path}\n", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
