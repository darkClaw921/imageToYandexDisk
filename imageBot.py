from loguru import logger
from dotenv import load_dotenv
from art import text2art
from aiogram.types.message import ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from PIL import Image

import yadisk

import os 

load_dotenv()
token = os.environ.get('TOKEN')
vkToken = os.environ.get('VK_TOKEN')
tgToken = os.environ.get('TG_TOKEN')
ADMIN_ID = 105431859



bot = Bot(token=str(tgToken)) 
dp = Dispatcher(bot,storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@logger.catch
def build_image(images):
    watermark = Image.open('image.png')
    img = Image.open(f'{images}.png') 
    img = img.resize((1200,1800))
    img.paste(watermark, (0, 0),  watermark)
    img.save(f"{images}.png")
    

@logger.catch
def upload_image_to_disk(nameImage:str):
    y = yadisk.YaDisk(token=token)
    try: 
        y.upload(f'{nameImage}.png', f"/test/{nameImage}.png") # Загружает первый файл
    except yadisk.exceptions.PathExistsError:
        y.remove(f"/test/{nameImage}.png", permanently=True)
        y.upload(f'{nameImage}.png', f"/test/{nameImage}.png") # Загружает первый файл

   #y.upload("file2.txt", "/test/file2.txt") # Загружает второй файл

@logger.catch
def main():
    #upload_image_to_disk('ts')
    #while True:
    #    event = vk.get_event()
    #    user_id = event.user_id
    #    message = event.message.lower()
    #    print(message)
    pass

@dp.message_handler(content_types=['photo'])
@logger.catch
async def handle_docs_photo(message):
    name = message.from_user.id
    await message.photo[-1].download(f'{name}.png')
    build_image(name)
    upload_image_to_disk(f'{name}')
    photo = open(f'{name}.png', 'rb')
    await bot.send_photo(message.chat.id, photo)#f'{name}.png')
    photo.close()

@dp.message_handler(state='firstMsg') 
async def first_state(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)
    await state.finish()
    message = msg.text
    user_id = msg.from_user.id
    #pprint(msg)


@dp.message_handler(content_types=ContentType.ANY)
@logger.catch
async def echo_message(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)
    
    try:
        message = msg.text.lower()
        user_id = msg.from_user.id
    except:
        message = 'хз'

    await bot.send_message(msg.from_user.id, 'Пришлите ваше фото')
    await state.set_state('firstMsg')




if __name__ == '__main__':
    art = text2art('imager', 'rand')
    print(art)
    #main()
    executor.start_polling(dp)

