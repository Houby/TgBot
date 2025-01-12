import os

import dotenv

dotenv.load_dotenv('.env')

bot_token = os.environ['bot_token']
dev_bot_token = os.environ['dev_bot_token']
admin_id = os.environ['admin_id']

api_key = os.environ['api_key']
secret_key = os.environ['secret_key']
