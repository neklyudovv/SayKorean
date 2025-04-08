from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class Pronounce(StatesGroup):
    waiting_for_voice = State()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("hi")


@router.message(Command("check"))
async def cmd_check(message: Message, state: FSMContext):
    args = message.text.strip().split(maxsplit=1)

    if len(args) < 2:
        await message.answer("no word")
        return

    word = args[1].strip()
    await state.update_data(expected_word=word)
    await state.set_state(Pronounce.waiting_for_voice)
    await message.answer(f"checking {word}")


@router.message(Pronounce.waiting_for_voice, F.voice)
async def handle_voice(message: Message, state: FSMContext):
    data = await state.get_data()
    expected_word = data.get("expected_word")

    voice = message.voice
    recognized_text = "todo"

    if recognized_text.lower().strip() == expected_word.lower().strip():
        await message.answer("Произношение совпадает!")
    else:
        await message.answer(f"Не совпало. Ты сказал: {recognized_text}, ожидалось: {expected_word}")

    await state.clear()
