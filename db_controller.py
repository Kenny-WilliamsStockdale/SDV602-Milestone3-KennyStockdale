from db import get_database
import time
import threading
"""database controller. Dictates how the data is accessed and proccessed 
    from the remote database and used through the application.
"""

accounts = {
    'localuser': ""
}

dbname = get_database()

# ------ ANCHOR USER SECTION ------ #


def add_user(username, password):
    """[Adds user to the remote datastore/database via registration]

    Args:
        username ([string]): [Takes users entered username]
        password ([string]): [Takes users entered password]

    Returns:
        [string]: [Alert if could not add user to database do to other checks]
    """
    collection_name = dbname["users"]

    user = {"_id": username, "password": password}

    try:
        collection_name.insert_one(user)
    except:
        alert = "Could not add user"
        return alert


def user_exists(username):
    """[Checks username already exists in the remote datastore]

    Args:
        username ([string]): [username that is stored in remote datastore]

    Returns:
        [string]: [returns username if true else false and no username is returned]
    """
    collection_name = dbname["users"]

    user = collection_name.find_one({"_id": username})
    return True if user else False


def check_password(username, password):

    collection_name = dbname["users"]

    user = collection_name.find_one({"_id": username})

    return True if user["password"] == password else False

# ------ ANCHOR CHAT SECTION ------ #
class chats:
    """[Chats class encompassing the functions and proccesses managed by the chats class]
    """

    def __init__(self, title='', chat=''):
        """[Called each time the class is instantiated]

        Args:
            title (str, optional): [title of the user typed the chat]. Defaults to ''.
            chat (str, optional): [chat from the user typed the chat]. Defaults to ''.
        """
        collection_name = dbname["chats"]
        self.title = title
        self.chat = chat
        self.exitflag = 0

        if collection_name.find_one({"title": self.title}) == None:
            collection_name.insert_one({"title": self.title, "chat": []})

        self.chat = self.get_recent_chat(
            collection_name.find_one({"title": self.title})["chat"])

    def get_recent_chat(self, chat_array):
        """[pulls recent chat from the datastore/database]

        Args:
            chat_array ([list]): [pulls string chat as a list for use]

        Returns:
            [string]: [returns chat to push onto chat window]
        """
        while len(chat_array) >= 5:
            chat_array.pop(0)
        self.chat = ''
        for message in chat_array:
            self.chat += message
        return self.chat

    def send_message(self, user, message):
        """[sends message through chat window into the database to create an entry]

        Args:
            user ([string]): [sends username through with chat]
            message ([list, string]): [sends chat message]

        Returns:
            [alert]: [message failed to send if unsuccessful]
        """
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
        """[retrieves chat from the datastore/ database and updates the window to display any new chat every 5 seconds]
        """
        delay = 5
        while True:
            if DES_chat.exitflag:
                break
            time.sleep(delay)
            collection_name = dbname["chats"]
            DES_chat.chat = DES_chat.get_recent_chat(
                collection_name.find_one({"title": DES_chat.title})["chat"])

    def thread_start(self, DES_chat):
        """[Starts extra thread to have two simultaneous python actions to be executed at once]


        Returns:
           [Start of a new thread within python]
        """
        class my_thread(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)

            def run(self):
                chats.retrieve_chat(self, DES_chat)

        thread = my_thread()
        thread.start()
        return thread
