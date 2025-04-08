from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from speech_to_text import transcribe

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
        await message.answer("Укажи слово. Пример: /check 안녕")
        return

    word = args[1].strip()
    # нужна проверка корейское ли слово

    await state.update_data(expected_word=word)
    await state.set_state(Pronounce.waiting_for_voice)

    await message.answer(f"Проверка слова: {word}\nЗапиши голосовое сообщение 🎤")


@router.message(Pronounce.waiting_for_voice, F.voice)
async def handle_voice(message: Message, state: FSMContext):
    data = await state.get_data()
    expected_word = data.get("expected_word")

    voice = message.voice
    file = await message.bot.get_file(voice.file_id)
    file_url = f"https://api.telegram.org/file/bot{message.bot.token}/{file.file_path}"

    recognized_text = await transcribe(file_url)

    if recognized_text.lower().strip() == expected_word.lower().strip():
        await message.answer("Произношение совпадает!")
    else:
        await message.answer(f"Не совпало. Ты сказал: {recognized_text}, ожидалось: {expected_word}")

    await state.clear()


@router.message(Pronounce.waiting_for_voice)
async def handle_other(message: Message, state: FSMContext):
    await message.answer("Отправь голосовое до 30 сек")
