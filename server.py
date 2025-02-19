from flask import Flask, render_template, jsonify
from flask_mail import Mail, Message
import random
import time

app = Flask(__name__)

# Configure email settings
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "mavuduruprabhathdeep@gmail.com"  # Replace with your Gmail
app.config["MAIL_PASSWORD"] = "taqv lese pmui ximl"  # Replace with your App Password
app.config["MAIL_DEFAULT_SENDER"] = "pdmp648@gmail.com"

mail = Mail(app)

# Define anomaly range
MIN_THRESHOLD = 15
MAX_THRESHOLD = 45

def generate_sensor_data():
    """Simulate sensor data and detect anomalies."""
    sensor_id = random.choice(["sensor_1", "sensor_2", "sensor_3"])
    value = round(random.uniform(10, 50), 2)
    timestamp = time.time()

    is_anomaly = value < MIN_THRESHOLD or value > MAX_THRESHOLD

    # Send email alert if anomaly detected
    if is_anomaly:
        send_email_alert(sensor_id, value)

    return {
        "timestamp": timestamp,
        "sensor_id": sensor_id,
        "value": value,
        "is_anomaly": is_anomaly
    }

def send_email_alert(sensor_id, value):
    """Send an email alert when an anomaly is detected."""
    msg = Message(
        "🚨 Anomaly Detected!",
        recipients=["recipient_email@gmail.com"],  # Replace with recipient email
        body=f"⚠️ Anomaly detected! \nSensor: {sensor_id} \nValue: {value}"
    )
    mail.send(msg)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    return jsonify(generate_sensor_data())

if __name__ == "__main__":
    app.run(debug=True)
