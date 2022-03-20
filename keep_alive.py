from flask import Flask
from threading import Thread
# keeps the bot server alive by sending a request every 5 seconds to prevent the server from falling asleep
app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()