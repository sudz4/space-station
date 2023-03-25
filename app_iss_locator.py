# libraries
from flask import Flask, request, Response
import requests
import threading
import os

"""   
the Flask class is the main class from the Flask web framework.
Flask represents a web application
provides all the necessary functionality to handle HTTP requests, manage routes, serve static files, and more

"""

"""  
When you run a Python script directly (e.g., python app.py), the __name__ variable is set to '__main__'. 
When you import a module (e.g., import app), the __name__ variable is set to the module's name (in this case, 'app').

In the context of creating a Flask app, passing __name__ as an argument helps Flask determine the root path for the application, 
which is useful when serving static files or templates. 
It also allows Flask to know whether the script is being run directly or imported as a module.
"""
# creates a new instance of the Flask web application
app = Flask(__name__) # represents the name of the current module -> app_iss_locator

def shutdown_server():
    os._exit(0)

def stop_app_after_delay(delay): # starts a timer with the specified delay (in seconds) and then calls the shutdown_server() function to stop the server
    threading.Timer(delay, shutdown_server).start()

@app.before_request
def before_request():
    request.environ['REMOTE_ADDR'] = '0.0.0.0'   

@app.route('/sms', methods=['POST'])
def handle_sms():
    message_body = request.form.get('Body', '').strip().lower()
    if message_body == 'iss':
        iss_response = requests.get("http://api.open-notify.org/iss-now.json")
        iss_data = iss_response.json()
        if iss_data["message"] == "success":
            return Response(f"The ISS is currently at latitude {iss_data['iss_position']['latitude']} and longitude {iss_data['iss_position']['longitude']}", content_type="text/plain")
        else:
            return Response("Error retrieving ISS location.", content_type="text/plain")
    else:
        return Response("Invalid command. Send 'iss' to get the current location of the International Space Station.", content_type="text/plain")

if __name__ == '__main__':
    # Stop the app after 60 minutes (3600 seconds)
    stop_app_after_delay(3600)

    # Run the Flask application
    app.run(debug=False)
