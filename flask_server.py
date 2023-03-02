from flask import Flask, request, Response
import configparser
from tg_bot import TG_Bot
import pandas as pd

# read config
config = configparser.ConfigParser()
config.read('config.ini')
token = config["telegram"]["token"]
channel_chat_id = config["telegram"]["channel_chat_id"]

# init instance
app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_msg():
    try:
        raw_msg = request.get_json()
    except:
        return "error"
    with open("log.txt", "a") as f:
        f.write(str(raw_msg))  
        f.write("\n")
    try:
        msg = raw_msg["message"]
    # pass reply msgs
    except KeyError:
        return "reply"
    
    # check msg received time
    if msg["date"] > bot.init_time:
        #date, chat_id, text
        msg_dir = bot.parse_massage(msg)
        
        if msg_dir["text"] == "/start":
            bot.send_message(msg_dir["chat_id"], "歡迎使用，目前只支援英文轉中文服務")
            
        else:
            msg_dir['translated_text'] = bot.translate(msg_dir["text"])
            bot.send_message(msg_dir["chat_id"], msg_dir['translated_text'])
            with open("log", "a") as f:
                log_msg = f"{msg_dir['date']}||{msg_dir['chat_id']}||{msg_dir['text']}||{msg_dir['translated_text']}\n"
                f.write(log_msg)   
                bot.send_message(channel_chat_id, log_msg)
        return Response('ok', status=200)
    else:
        return "old"
     
if __name__ == '__main__':
    bot = TG_Bot()
    app.run(port=5002)