from fastapi import FastAPI, HTTPException, WebSocket
from confluent_kafka import Producer, Consumer
import asyncio
import uvicorn

app = FastAPI()

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_TOPIC = 'test-01'

# Kafka producer
producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

# Kafka consumer
consumer = Consumer({
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe([KAFKA_TOPIC])


@app.post("/produce/{message}")
async def produce_message(message: str):
    message = 'message ' + message
    producer.produce(KAFKA_TOPIC, message.encode('utf-8'))
    producer.flush()
    return {"message": "Message produced successfully", "body_msg": message}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        message = consumer.poll(timeout=1.0)
        if message is not None:
            # message = 'socket ' + message
            await websocket.send_text(message.value().decode('utf-8'))
        await asyncio.sleep(1)


@app.get("/consume")
async def consume_message():
    message = consumer.poll(timeout=1.0)
    if message is None:
        raise HTTPException(status_code=404, detail="No messages available")
    return {"message": message.value().decode('utf-8')}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
    # uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
