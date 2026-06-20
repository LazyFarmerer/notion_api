import os
from dotenv import load_dotenv

load_dotenv()

class Key:
    농부api = os.getenv("농부api")
    읽기전용 = os.getenv("읽기전용")

