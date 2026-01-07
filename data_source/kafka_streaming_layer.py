# Kafka for Streaming
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
import json
from configuration import KAFKA_TOPICS

class KafkaStreamingLayer:
    """Kafka Producers and Topics Management"""

    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self.setup_kafka()

    def setup_kafka(self):
        """Initialize Kafka producer and create topics"""
        try:
            # Create Kafka Producer
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None
            )

            # Create topics if they don't exist
            admin_client = KafkaAdminClient(bootstrap_servers=self.bootstrap_servers)

            topics = [
                NewTopic(name=KAFKA_TOPICS['news'], num_partitions=3, replication_factor=1),
                NewTopic(name=KAFKA_TOPICS['tweets'], num_partitions=3, replication_factor=1),
                NewTopic(name=KAFKA_TOPICS['stocks'], num_partitions=3, replication_factor=1)
            ]

            try:
                admin_client.create_topics(new_topics=topics, validate_only=False)
                print("Kafka topics created")
            except:
                print("Kafka topics already exist")

            admin_client.close()
            print("Kafka producer initialized")

        except Exception as e:
            print(f"Kafka not available (using simulation mode): {e}")
            self.producer = None

    def produce_to_kafka(self, topic, key, value):
        """Send data to Kafka topic"""
        if self.producer:
            try:
                future = self.producer.send(topic, key=key, value=value)
                future.get(timeout=10)
                return True
            except Exception as e:
                print(f"Kafka produce error: {e}")
                return False
        else:
            # Simulation mode - just return the data
            print(f"[SIMULATED] Produced to {topic}: {key}")
            return True

    def close(self):
        """Close Kafka producer"""
        if self.producer:
            self.producer.close()