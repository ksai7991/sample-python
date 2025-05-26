import logging
import traceback
from flask import Flask, jsonify

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

@app.route('/trigger-error')
def trigger_error():
    try:
        simulate_error()
    except Exception as e:
        # Get the full formatted traceback as a string
        stack_trace = traceback.format_exc()

        # Log the full stack trace
        logger.error("Full stack trace:\n%s", stack_trace)

        response = {
            "error": "Something went wrong",
            "code": 400,
            "message": str(e),
            "trace": stack_trace.splitlines()[-1]  # Optionally send only the last line
        }
        return jsonify(response), 400

def simulate_error():
    nested_function()

def nested_function():
    raise ValueError("Simulated error in nested function")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    logger.info(f"Accessed path: /{path}")
    return f"You accessed path: /{path}\n", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
