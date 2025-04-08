import aiohttp
import tempfile
import subprocess
import speech_recognition as sr


def ogg_to_flac(ogg_file_path, flac_file_path):
    subprocess.run(['ffmpeg', '-i', ogg_file_path, '-acodec', 'flac', flac_file_path])


async def transcribe(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status != 200:
                return "Ошибка загрузки"

            with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
                tmp.write(await r.read())
                tmp.flush()

                flac_path = tmp.name + ".flac"
                ogg_to_flac(tmp.name, flac_path)

                recognizer = sr.Recognizer()

                with sr.AudioFile(flac_path) as src:
                    voice = recognizer.record(src)

                try:
                    text = recognizer.recognize_google(voice, language="ko-KR")
                    return text
                except:
                    return "Не удалось распознать речь"
