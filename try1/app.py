from flask import Flask, jsonify
import threading
import time

app = Flask(__name__)

# Custom error class for demonstration
class CustomThreadError(Exception):
    pass

# Worker class that will run in a separate thread
class ErrorRaisingThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.error = None  # Store any error that occurs in the thread

    def run(self):
        try:
            time.sleep(2)  # Simulate work for 2 seconds
            raise CustomThreadError("An error occurred in the sub-thread.")
        except Exception as e:
            self.error = e  # Store the error to pass it back to the main thread

@app.route('/')
def hello_world():
    # Instantiate and start the thread
    worker = ErrorRaisingThread()
    worker.start()
    worker.join()  # Wait for the thread to finish

    # Check if an error occurred in the thread
    if worker.error:
        # Return the error message as the response
        return jsonify({"error": str(worker.error)}), 500
    return jsonify({"message": "Thread completed without error"})

if __name__ == '__main__':
    app.run(debug=True)
