from confluent_kafka import Consumer, KafkaError

# Configuration for the Kafka Consumer
conf = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker
    'group.id': 'mygroup',  # Consumer group ID
    'auto.offset.reset': 'earliest'  # Start reading at the earliest offset
}

# Create the Kafka Consumer
consumer = Consumer(conf)

# Subscribe to the topic
consumer.subscribe(['hospital_events'])

# Function to handle the consumption of messages
try:
    while True:
        msg = consumer.poll(1.0)  # Poll for messages

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                continue
            else:
                print(msg.error())
                break

        print(f"Received message: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    pass
finally:
    consumer.close()  # Close the consumer
