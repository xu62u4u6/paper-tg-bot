import requests
import configparser
import time 
import openai

config = configparser.ConfigParser()
config.read('config.ini')

class TG_Bot:
    def __init__(self):
        openai.api_key = config["openai"]["key"]
        self.token = config["telegram"]["token"]
        self.webhook_url = config["telegram"]["webhook-url"]
        self.init_time = time.time()
        # chat_id: [msg]
        self.users_msgs = {}
        
    def send_message(self, chat_id, text):
        url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        payload = {'chat_id': chat_id, 'text': text}
        return requests.post(url,json=payload)
    
    def parse_massage(self, msg):
        msg_dir = {}
        msg_dir["date"] = msg["date"]
        msg_dir["chat_id"]  = msg["chat"]["id"]
        msg_dir["text"] = msg["text"]
        for i in ["username", "first_name", "last_name"]:
            if i in msg.keys():
                msg_dir[i] = msg[i]
            else:
                msg_dir[i] = None
        return msg_dir
    
    def set_webhook(self):
        url = f'https://api.telegram.org/bot{self.token}/setWebhook?url={self.webhook_url}'
        res = requests.post(url)
        return res.status_code, res.text
    
    def translate(self, text, source_lang="us", target_lang="zh-tw"):

        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Translate this from {source_lang} into {target_lang}:\n{text}\n",
        temperature=0.3,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        translated_text = response["choices"][0]["text"].strip()
        return translated_text
