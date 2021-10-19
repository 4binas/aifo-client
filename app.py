import os
from service.chatbot import Chatbot
from view.chat_gui import ChatGUI

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./key.json"

chatbot = Chatbot("aifo-project-jpdg", "abcde", "en-US", "SBBob")

app = ChatGUI(chatbot)
app.run()
