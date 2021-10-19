from tkinter import *
from PIL import Image, ImageTk
import os
import urllib.request
import webbrowser

BG_RED = "#EB0000"
BG_COLOR = "#FFFFFF"
TEXT_COLOR = "#1F1F1F"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"
global imageArray
imageArray = []

class ChatGUI:
    
    
    def __init__(self, bot):
        self.bot = bot
        self.window = Tk()
        self.window.iconbitmap("sbb_icon.ico")
        self._setup_main_window()

    def run(self):
        self.window.mainloop()
    
    def _setup_main_window(self):
        self.window.title(self.bot.bot_name)
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)

        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        line = Label(self.window, width=450, bg=BG_RED)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        bottom_label = Label(self.window, bg=BG_RED, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        self.msg_entry = Entry(bottom_label, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
        
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_RED,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    def callback(self, url):
      webbrowser.open_new(url)

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "You")
        
    def _insert_message(self, msg, sender):
        if not msg:
            return
        
        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        (res, cards) = self.bot.get_response(msg)
        
        msg2 = f"{self.bot.bot_name}: {res}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        

        if cards:
          for card in cards:
            urllib.request.urlretrieve(
            card.image_uri,
            "image")
            img = Image.open("image")
            imageArray.append(ImageTk.PhotoImage(img))
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, f"{card.title}: ")
            # image_link = Label(self.text_widget, image=imageArray[len(imageArray)-1], cursor="left_ptr")
            # image_link.bind(f"<1>", lambda e: self.callback(card.buttons[0].postback))
            # self.text_widget.window_create("insert", window=image_link)
            hyperlink = Label(self.text_widget, text="(Link)", fg="blue", cursor="hand2")
            hyperlink.bind(f"<1>", lambda e, url = card.buttons[0].postback: self.callback(url))
            self.text_widget.window_create(END, window=hyperlink)
            self.text_widget.insert(END, "\n")
            self.text_widget.image_create(END, image = imageArray[len(imageArray)-1])
            self.text_widget.insert(END, "\n\n")
            self.text_widget.configure(state=DISABLED)
          os.remove("image")
        
        self.text_widget.see(END)