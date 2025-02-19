import joblib  # For loading the AI model
import time
import random
import smtplib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "mavuduruprabhathdeep@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "taqv lese pmui ximl"  # Replace with your App Password
EMAIL_RECEIVER = "pdmp648@gmail.com"  # Replace with recipient email

def send_email_alert(sensor_id, value):
    """Sends an email alert when an anomaly is detected."""
    subject = f"⚠️ Anomaly Detected in {sensor_id}!"
    body = f"Anomalous sensor reading detected:\n\nSensor: {sensor_id}\nValue: {value}\nTimestamp: {time.ctime()}"
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("📩 Alert Email Sent Successfully!")
    except Exception as e:
        print("❌ Failed to Send Email:", e)

class DuplicateFilter:
    def __init__(self):
        self.last_seen = {}

    def is_duplicate(self, sensor_id, value):
        if sensor_id in self.last_seen and self.last_seen[sensor_id] == value:
            return True
        self.last_seen[sensor_id] = value
        return False

class OutlierDetector:
    def __init__(self, min_threshold=15, max_threshold=45):
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold

    def is_outlier(self, value):
        return value < self.min_threshold or value > self.max_threshold

class MissingValueHandler:
    @staticmethod
    def is_missing(value):
        return value is None or value == ""

def log_valid_data(timestamp, sensor_id, value):
    with open("sensor_data.log", "a") as file:
        file.write(f"{timestamp}, {sensor_id}, {value}\n")

# Load trained AI model
model = joblib.load("anomaly_model.pkl")

data_x = []  # X-axis (time)
data_y = []  # Y-axis (sensor values)
anomaly_points = []  # Store anomaly data

def generate_sensor_data():
    sensors = ['sensor_1', 'sensor_2', 'sensor_3']
    duplicate_filter = DuplicateFilter()
    outlier_detector = OutlierDetector()

    while True:
        sensor_id = random.choice(sensors)
        value = random.choice([round(random.uniform(10, 50), 2), None, ""])
        timestamp = time.time()
        
        if MissingValueHandler.is_missing(value):
            print(f"⚠️ WARNING! Missing value detected: {timestamp}, {sensor_id}, {value}")
            continue

        if duplicate_filter.is_duplicate(sensor_id, value):
            continue
        
        if outlier_detector.is_outlier(value):
            print(f"⚠️ ALERT! Outlier detected: {timestamp}, {sensor_id}, {value}")
            send_email_alert(sensor_id, value)  # Send email alert
            anomaly_points.append((timestamp, value))
        else:
            log_valid_data(timestamp, sensor_id, value)
            data_x.append(timestamp)
            data_y.append(value)
        
        time.sleep(1)

def update_plot(frame):
    plt.clf()
    plt.scatter(data_x, data_y, label="Valid Readings", color='blue')
    if anomaly_points:
        anomaly_x, anomaly_y = zip(*anomaly_points)
        plt.scatter(anomaly_x, anomaly_y, label="Anomalies", color='red', marker='x')
    plt.xlabel("Timestamp")
    plt.ylabel("Sensor Value")
    plt.legend()
    plt.title("Real-Time Sensor Data Stream")

def start_streaming():
    fig = plt.figure()
    ani = animation.FuncAnimation(fig, update_plot, interval=1000)
    plt.show()

if __name__ == "__main__":
    from threading import Thread
    Thread(target=generate_sensor_data, daemon=True).start()
    start_streaming()
