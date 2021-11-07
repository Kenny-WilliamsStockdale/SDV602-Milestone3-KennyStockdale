from db import get_database
import time
import threading

accounts = {
    'localuser': ""
}

dbname = get_database()
# ---User---------------


def add_user(username, password):
    collection_name = dbname["users"]

    user = {"_id": username, "password": password}

    try:
        collection_name.insert_one(user)
    except:
        alert = "Could not add user"
        return alert


def user_exists(username):

    collection_name = dbname["users"]

    user = collection_name.find_one({"_id": username})
    return True if user else False


def check_password(username, password):

    collection_name = dbname["users"]

    user = collection_name.find_one({"_id": username})

    return True if user["password"] == password else False


class chats:

    def __init__(self, title='', chat=''):
        collection_name = dbname["chats"]
        self.title = title
        self.chat = chat
        self.exitflag = 0

        if collection_name.find_one({"title": self.title}) == None:
            collection_name.insert_one({"title": self.title, "chat": []})

        self.chat = self.get_recent_chat(
            collection_name.find_one({"title": self.title})["chat"])

    def get_recent_chat(self, chat_array):
        while len(chat_array) >= 5:
            chat_array.pop(0)
        self.chat = ''
        for message in chat_array:
            self.chat += message
        return self.chat

    def send_message(self, user, message):
        collection_name = dbname["chats"]

        try:
            collection_name.find_one_and_update(
                {"title": self.title},
                {"$push": {"chat": f"{user}:\n{message}\n\n"}}
            )
        except:
            alert_message = "Message failed to send"
            return alert_message

    def retrieve_chat(self, DES_chat):
        delay = 5
        while True:
            if DES_chat.exitflag:
                break
            time.sleep(delay)
            collection_name = dbname["chats"]
            DES_chat.chat = DES_chat.get_recent_chat(
                collection_name.find_one({"title": DES_chat.title})["chat"])

    def thread_start(self, DES_chat):
        class my_thread(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)

            def run(self):
                chats.retrieve_chat(self, DES_chat)

        thread = my_thread()
        thread.start()
        return thread
