from fastapi import APIRouter
from schema import Message
from config import loop, KAFKA_BOOTSTRAP_SERVERS, KAFKA_CONSUMER_GROUP, KAFKA_TOPIC
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from kafka import KafkaConsumer, KafkaProducer
import json

route = APIRouter()

# Create a Kafka producer
producer = KafkaProducer(
    # Replace with your Kafka server address if different
    bootstrap_servers=['loaclhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


@route.post('/create_message')
async def send(message: Message):
    # producer = AIOKafkaProducer(
    #     loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    # await producer.start()

    # await producer.stop()
    # producer = KafkaProducer(
    #     # Replace with your Kafka server address if different
    #     bootstrap_servers=['loaclhost:9092'],
    #     value_serializer=lambda v: json.dumps(v).encode('utf-8')
    # )

    try:
        # print(f'Sendding message with value: {message}')
        # producer.send('test-01', value={'message': message.message})
        # producer.flush()
        return {"message": "Message sent to Kafka", "data": message.message}

        # value_json = json.dumps(message.__dict__).encode('utf-8')
        # await producer.send_and_wait(topic=KAFKA_TOPIC, value=value_json)
    finally:
        pass
        # producer.close()


async def consume():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC, loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    # consumer = AIOKafkaConsumer(
    #     KAFKA_TOPIC, loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id=KAFKA_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            print(f'Consumer msg: {msg}')
    finally:
        await consumer.stop()
