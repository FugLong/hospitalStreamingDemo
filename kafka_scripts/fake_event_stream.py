from confluent_kafka import Producer
import json
import time
import random
from threading import Thread, Event

conf = {
    'bootstrap.servers': 'kafka:29092'
}

producer = Producer(conf)

# Configuration
VERBOSE_LOGGING = False  # Set to True to enable verbose logging

# Counters for event logging
real_time_event_count = 0
medium_event_count = 0

# Event to signal when to log
log_event = Event()

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")

# Real-Time Monitoring Data Generator
def generate_real_time_data(device_id, patient_id):
    global real_time_event_count
    while True:
        data = {
            'event_type': 'monitoring',
            'device_id': device_id,
            'patient_id': patient_id,
            'ecg': random.uniform(60, 100),  # Simulated heart rate
            'spo2': random.uniform(95, 100),  # Simulated oxygen saturation
            'respiratory_rate': random.uniform(12, 20),  # Simulated respiratory rate
            'timestamp': int(time.time())
        }
        producer.produce('hospital_events', key=str(patient_id), value=json.dumps(data), callback=delivery_report)
        producer.poll(1)
        real_time_event_count += 1
        if VERBOSE_LOGGING:
            print(f"Real-time event: {data}")
        time.sleep(0.5)  # Faster, real-time data generation

# Medium-Frequency Clinical Events Generator
def generate_clinical_events():
    global medium_event_count
    while True:
        data = {
            'event_type': random.choice(['admission', 'discharge', 'transfer']),
            'patient_id': random.randint(1, 100),
            'timestamp': int(time.time())
        }
        producer.produce('hospital_events', key=str(data['patient_id']), value=json.dumps(data), callback=delivery_report)
        producer.poll(1)
        medium_event_count += 1
        if VERBOSE_LOGGING:
            print(f"Medium-speed event: {data}")
        time.sleep(random.uniform(5, 20))  # Faster medium frequency, irregular intervals

# Logger Thread to log event counts every 10 seconds
def log_event_counts():
    global real_time_event_count, medium_event_count
    while not log_event.is_set():
        time.sleep(10)
        if not VERBOSE_LOGGING:
            print(f"Real-time events produced: {real_time_event_count}, Medium-speed events produced: {medium_event_count}")
            # Reset counters after logging
            real_time_event_count = 0
            medium_event_count = 0

if __name__ == "__main__":
    print("Initializing event generator...")
    
    try:
        # Start real-time monitoring data generation for more devices and patients
        for i in range(1, 11):  # Simulate 10 devices monitoring 10 different patients
            patient_id = i
            device_id = f'device_{i}'
            Thread(target=generate_real_time_data, args=(device_id, patient_id)).start()

        # Start medium-frequency clinical events generation
        Thread(target=generate_clinical_events).start()

        # Start the logger thread if verbose logging is not enabled
        if not VERBOSE_LOGGING:
            logger_thread = Thread(target=log_event_counts)
            logger_thread.start()

        # Keep the main thread alive to allow other threads to run
        while True:
            time.sleep(1)

    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        print("Event generator terminated.")
        log_event.set()  # Signal logger thread to stop
        if not VERBOSE_LOGGING:
            logger_thread.join()  # Ensure logger thread finishes before exiting
        producer.flush()
