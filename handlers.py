from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("hi")


@router.message(Command("check"))
async def cmd_check(message: Message):
    await message.answer("check")
