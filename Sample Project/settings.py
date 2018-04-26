""" 
It contains the configuration variables
"""
import os
from dotenv import load_dotenv
load_dotenv()

app_name = os.getenv('APP_NAME')
host = os.getenv('HOST')
port = os.getenv('PORT')
