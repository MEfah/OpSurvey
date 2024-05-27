import asyncio
import aio_pika
import aio_pika.abc
import json
from settings import settings


async def publish_message(exchange_name: str, topic: str, message: dict | str):
    # Explicit type annotation
    connection: aio_pika.RobustConnection = await aio_pika.connect_robust(
        settings.rabbit.connection_string
    )

    channel: aio_pika.abc.AbstractChannel = await connection.channel()
    exchange: aio_pika.abc.AbstractExchange = await channel.declare_exchange(exchange_name, aio_pika.ExchangeType.TOPIC)
    data = ''
    if isinstance(message, dict):
        data = json.dumps(message)
    else:
        data = message

    await exchange.publish(
        aio_pika.Message(
            body=data.encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        ),
        routing_key=topic
    )

    await connection.close()