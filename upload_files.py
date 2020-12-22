import os
import asyncio
import logging
from aiogram import Bot
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import DB_FILENAME

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

MY_ID = int(os.environ.get("MY_ID", default=0))

if MY_ID == 0:
        raise ValueError("Environment variable \"MY_ID\" \
is not set, with no default")
class MediaIds(Base):
    __tablename__ = 'Media ids'
    id = Column(Integer, primary_key=True)
    file_id = Column(String(255))
    filename = Column(String(255))

logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)

engine = create_engine(f'sqlite:///{DB_FILENAME}')

if not os.path.isfile(f'./{DB_FILENAME}'):
    Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

bot = Bot(token=os.environ.get("TELEGRAM_API_TOKEN"))


BASE_MEDIA_PATH = ''


async def uploadMediaFiles(folder, method, file_attr):
    folder_path = folder
    for filename in os.listdir(folder_path):
        if filename.startswith('.'):
            continue

        logging.info(f'Started processing {filename}')
        with open(os.path.join(folder_path, filename), 'rb') as file:
            msg = await method(MY_ID, file, disable_notification=True)
            if file_attr == 'photo':
                file_id = msg.photo[-1].file_id
            else:
                file_id = getattr(msg, file_attr).file_id
            session = Session()
            newItem = MediaIds(file_id=file_id, filename=filename)
            try:
                session.add(newItem)
                session.commit()
            except Exception as e:
                logging.error(
                    'Couldn\'t upload {}. Error is {}'.format(filename, e))
            else:
                logging.info(
                    f'Successfully uploaded and saved to DB file {filename} with id {file_id}')
            finally:
                session.close()

loop = asyncio.get_event_loop()

tasks = [
    loop.create_task(uploadMediaFiles('media', bot.send_voice, 'voice')),
]

wait_tasks = asyncio.wait(tasks)

loop.run_until_complete(wait_tasks)
loop.close()
Session.remove()