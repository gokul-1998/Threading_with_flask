from flask import Flask, jsonify
from flask_restful import Api, Resource
import threading
import queue
import os
import time
import uuid

app = Flask(__name__)
api = Api(app)

# Global placeholder for resources
class GlobalResources:
    call = type('call', (), {})()  # Namespace-like object for call-related resources
    tts = None

lib = GlobalResources()

# Function to create a unique folder for each call
def create_unique_folder():
    unique_name = str(uuid.uuid4())
    path = os.path.join(os.getcwd(), unique_name)
    os.makedirs(path, exist_ok=True)
    return unique_name, path

# Mock TTS and Audio Processor classes
class PiperTTS:
    pass

class LiveAudioProcessor:
    pass

# Example Resource that initializes and runs in a thread
class MyResource(Resource):
    def __init__(self):
        global lib
        # Create a random folder for the call
        lib.call.dir = type('dir', (), {})()  # Simulating nested attributes
        lib.call.dir.name, lib.call.dir.path = create_unique_folder()

        # Initialize resources
        lib.call.live_audio_processor_instance = LiveAudioProcessor()
        if not lib.tts:
            lib.tts = PiperTTS()
        
        self.error_queue = queue.Queue()  # Queue to capture errors from threads

        # Start the main processing in a separate thread
        main_thread = threading.Thread(target=self.main, daemon=True)
        main_thread.start()

    def main(self):
        try:
            time.sleep(2)  # Simulate processing time
            raise ValueError("An error occurred in the background processing.")
        except Exception as e:
            self.error_queue.put(e)  # Capture any errors in the error queue

    def get(self):
        # Check for any errors in the error queue
        if not self.error_queue.empty():
            error = self.error_queue.get()
            return jsonify({"error": str(error)}), 500
        
        return jsonify({"message": "Initialization and processing started"})


# Adding resource to the API
api.add_resource(MyResource, '/process')

if __name__ == '__main__':
    app.run(debug=True)
