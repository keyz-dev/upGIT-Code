import os
from loguru import logger

current_dir = os.path.dirname(__file__)
log_file = os.path.join(os.getcwd(), 'logs', 'app.log')

logger.add(log_file, format="{time} {level} {message}", rotation="10 MB", retention="10 days")

PATH_TO_DB = os.path.join(
  current_dir,
  '..', 
  'config',
  "upgit.db"
  )

