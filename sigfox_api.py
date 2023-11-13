import os

from dotenv import load_dotenv

load_dotenv()
api_account = os.getenv("SIGFOX_API_KEY")
api_password = os.getenv("SIGFOX_API_CREDENTIAL")
