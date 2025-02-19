from flask import Flask, render_template, jsonify
import time
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Simulated sensor data
latest_data = {"timestamp": time.time(), "sensor_id": "sensor_1", "value": 20, "is_anomaly": False}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
@app.route('/data')
def get_sensor_data():
    global latest_data
    latest_data["timestamp"] = time.time()
    latest_data["value"] = round(random.uniform(10, 50), 2)  # Simulate new value
    latest_data["is_anomaly"] = latest_data["value"] > 45 or latest_data["value"] < 15  # Mark anomalies

    if latest_data["is_anomaly"]:
        send_email_alert(latest_data["sensor_id"], latest_data["value"])

    return jsonify(latest_data)


def send_email_alert(sensor_id, value):
    sender_email = "mavuduruprabhathdeep@gmail.com"
    sender_password = "taqv lese pmui ximl"
    receiver_email = "pdmp648@gmail.com"

    subject = "🚨 Anomaly Detected in Sensor Data!"
    body = f"Anomaly detected!\nSensor: {sensor_id}\nValue: {value}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("📧 Alert email sent successfully!")
    except Exception as e:
        print("❌ Error sending email:", e)


if __name__ == '__main__':
    app.run(debug=True)
