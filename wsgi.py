from main import app as application
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

if __name__ == '__main__':
    application.run()
