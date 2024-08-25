import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from twilio.rest import Client
import pywhatkit as pwk
import time
import logging
import requests
import base64
from gtts import gTTS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Define your Twilio account credentials
account_sid = ""
auth_token = ""
client = Client(account_sid, auth_token)

# Define the sender phone number
sender_no = ""
twiml_url = "http://demo.twilio.com/docs/voice.xml"

@app.route('/')
def index():
    return app.send_static_file('pythonprojects.html')

from flask import Flask, request, jsonify
import logging
import time
from twilio.rest import Client

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Your Twilio credentials
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

@app.route('/send_whatsapp_message', methods=['POST'])
def send_whatsapp_message():
    data = request.json
    phone_num = data.get('phone')
    message = data.get('message')
    
    try:      
        logging.info(f"Sending message to {phone_num}")

        # Send the message using Twilio
        response_message = client.messages.create(
            body=message,
            from_='whatsapp:+',  # Your Twilio WhatsApp-enabled number
            to=f'whatsapp:{phone_num}'
        )
        
        logging.info(f"Response from Twilio: {response_message.sid}")

        # Simulate processing time
        time.sleep(3)
        
        # Return a success response
        return jsonify({"status": "success", "message": "Message sent successfully!"})

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, request, render_template
from twilio.rest import Client

app = Flask(__name__)

# Twilio credentials (replace with your own)
account_sid = ''
auth_token = ''
twilio_number = '+'

client = Client(account_sid, auth_token)

@app.route('/')
def index():
    return render_template('pythonprojects.html')  # Assuming your HTML is named 'index.html'

@app.route('/send-message', methods=['POST'])
def send_message():
    phone_number = request.form['phone']
    message_body = request.form['message']

    message = client.messages.create(
        body=message_body,
        from_=twilio_number,
        to=phone_number
    )

    return f'Message sent to {phone_number}'

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/make_twilio_call', methods=['POST'])
def make_twilio_call():
    data = request.json
    to_phone_number = data.get('phone_num')
    
    try:
        # Make the call
        call = client.calls.create(
            from_=sender_no,
            to=to_phone_number,
            url=twiml_url
        )
        
        # Print the call SID
        logging.info(f"Call initiated with SID: {call.sid}")
        return jsonify({"status": "success", "message": "Call initiated successfully!", "call_sid": call.sid})
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.json
    sender_email = "pawansoni2k3@gmail.com"
    receiver_email = data.get('receiver_email')
    password = ""
    subject = data.get('subject')
    body = data.get('body')

    # Setup the MIME
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    try:
        # Use Gmail's SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, password)  # Login to the email account
        text = message.as_string()  # Convert the message to a string
        server.sendmail(sender_email, receiver_email, text)  # Send the email
        logging.info(f"Email sent to {receiver_email}")
        return jsonify({"status": "success", "message": "Email sent successfully!"})
    except Exception as e:
        logging.error(f"Failed to send email. Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        server.quit()  # Close the connection

@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({"status": "error", "message": "Text is required"}), 400
    
    try:
        # Create a speech object
        speech = gTTS(text=text, lang='en', slow=False)
        file_path = "text.mp3"
        
        # Save the speech to an MP3 file
        speech.save(file_path)
        
        # Return the file as a response
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logging.error(f"Failed to generate speech. Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

@app.route('/send_photo', methods=['POST'])
def send_photo():
    phone_num = request.form.get('phone_num')
    image_data = request.form.get('image')

    # Decode the image data
    image_data = image_data.split(",")[1]
    image_data = base64.b64decode(image_data)

    # Save the image to a temporary file
    image_path = "temp_photo.png"
    with open(image_path, "wb") as f:
        f.write(image_data)

    # Send the image via WhatsApp using Twilio
    try:
        message = client.messages.create(
            body='Here is your photo!',
            from_='whatsapp:' + TWILIO_PHONE_NUMBER,
            to='whatsapp:' + phone_num,
            media_url=[f"http://your_server_address/{image_path}"]
        )
        return jsonify({'message': 'Photo sent successfully!'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500

    finally:
        # Clean up the image file
        if os.path.exists(image_path):
            os.remove(image_path)

if __name__ == '__main__':
    app.run(debug=True)