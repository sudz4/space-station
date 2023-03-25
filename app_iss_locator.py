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

# function to shutdown the server
def shutdown_server():
    os._exit(0)

# starts a timer with the specified delay (in seconds) and then calls the shutdown_server() function to stop the server
def stop_app_after_delay(delay):
    threading.Timer(delay, shutdown_server).start()

# sets the REMOTE_ADDR to 0.0.0.0 for all incoming requests
@app.before_request
def before_request():
    request.environ['REMOTE_ADDR'] = '0.0.0.0'   

# handles the incoming SMS message(s)
@app.route('/sms', methods=['POST'])
def handle_sms():
    message_body = request.form.get('Body', '').strip().lower() # sends the string to lowercase by default, just so we are working with the same string for sure
    # if message_body == 'iss': # has to be explicitly a form of iss (ISS, Iss, etc.) -> more rigid if the user feels fancy
    if 'iss' in message_body: # basically like if the message body contains the string 'iss'
        # send a GET request to get the current location of the ISS
        iss_response = requests.get("http://api.open-notify.org/iss-now.json")
        iss_data = iss_response.json()
        if iss_data["message"] == "success":
            # return the lat and long of the ISS
            return Response(f"The ISS is currently at latitude {iss_data['iss_position']['latitude']} and longitude {iss_data['iss_position']['longitude']}", content_type="text/plain")
        else:
            return Response("Error retrieving ISS location.", content_type="text/plain")
    else:
        return Response("Invalid command. Send 'iss' to get the current location of the International Space Station.", content_type="text/plain")

# starts the application and then stops it after 60mins
if __name__ == '__main__':
    # stop the app after 60 minutes (3600 seconds)
    stop_app_after_delay(3600)

    # run the Flask application
    app.run(debug=False)

"""  
1-To run this program you have to install Flask and ngrok on your local machine.
2-Write your Flask application code and run it on your local machine using Flask's built-in development server.
3-Start ngrok and create a secure tunnel to your local Flask server by running the following command in your terminal:
4-ngrok http <flask_port>
5-Replace <flask_port> with the port number that your Flask server is listening on (usually 5000 by default).
6-Ngrok will generate a public URL that you can use to access your local Flask server from anywhere on the internet. You can find the URL in the ngrok terminal output or in the ngrok web interface.
7-Use the ngrok-generated URL to access your Flask application from any device with internet access.

Also, IMPORTANT!
Remember that your ngrok session is temporary and the generated URL will change every time you restart ngrok. 
You'll need to update the webhook URL in the Twilio console each time you restart ngrok.

"""

"""  
*Flask*
Flask is a Python web framework that allows developers to build web applications quickly and easily. 
One of the challenges in developing a web application is making it accessible over the internet so that others can use it.

***This is where ngrok comes in.***

*ngrok*
Ngrok is a tool that allows developers to expose a local web server to the internet. 
It creates a secure tunnel between the local server and a public URL, 
making it possible for anyone on the internet to access the local web server.

"""

