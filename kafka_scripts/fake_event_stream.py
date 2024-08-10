from confluent_kafka import Producer
import json
import time
import random
from threading import Thread

conf = {
    'bootstrap.servers': 'kafka:29092'
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]: {msg.value().decode('utf-8')}")

# Real-Time Monitoring Data Generator
def generate_real_time_data(device_id, patient_id):
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
        time.sleep(1)  # Fast, real-time data generation

# Medium-Frequency Clinical Events Generator
def generate_clinical_events():
    event_count = 0
    while True:
        data = {
            'event_type': random.choice(['admission', 'discharge', 'transfer']),
            'patient_id': random.randint(1, 100),
            'timestamp': int(time.time())
        }
        producer.produce('hospital_events', key=str(data['patient_id']), value=json.dumps(data), callback=delivery_report)
        producer.poll(1)
        event_count += 1
        if event_count % 50 == 0:  # Log every 50 events
            print(f"{event_count} clinical events produced.")
        time.sleep(random.uniform(10, 60))  # Medium frequency, irregular intervals

if __name__ == "__main__":
    print("Initializing event generator...")
    
    try:
        # Start real-time monitoring data generation for multiple devices and patients
        for i in range(1, 6):  # Simulate 5 devices monitoring 5 different patients
            patient_id = i
            device_id = f'device_{i}'
            Thread(target=generate_real_time_data, args=(device_id, patient_id)).start()

        # Start medium-frequency clinical events generation
        generate_clinical_events()
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        print("Event generator terminated.")
        producer.flush()
