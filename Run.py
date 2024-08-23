import asyncio
from app.handlers import form_router

from create_bot import dp, bot

dp.include_router(form_router)


async def main():
    # Start event dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
