import asyncio
import aio_pika
from services.surveys import SurveysService
from typing import Callable, Awaitable
from settings import settings


async def run_consumer(queue_name: str, exchange_name: str, topic: str, process_message: Callable[[str], Awaitable]):
    rabbitmq_connection = await aio_pika.connect_robust(
        settings.rabbit.connection_string
    )

    async with rabbitmq_connection:
        channel = await rabbitmq_connection.channel()
        queue = await channel.declare_queue(queue_name)
        exchange = await channel.declare_exchange(exchange_name, aio_pika.ExchangeType.TOPIC)
        await queue.bind(exchange, routing_key=topic)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print('message process start')
                    await process_message(message.body.decode())
                    print('message process end')