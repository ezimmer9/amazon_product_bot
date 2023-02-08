import os
import sys
import smtplib

mail_server_dict = {
    'gmail': {'server': 'smtp.gmail.com', 'port': 587},
    'localhost': {'server': 'localhost', 'port': 25},
}


class email:
    def __init__(self, receiver):
        self.__sender = 'eliranzim@gmail.com'
        self.receiver = receiver
        self.msg = None
        self.__psw = None
        self.server = None
        self.loged_in = False

    def set_text(self, text):
        self.msg = text

    def login(self, mail_server, psw):
        self.__psw = psw
        server = mail_server_dict[mail_server]
        self.server = smtplib.SMTP(server['server'], server["port"])
        self.server.ehlo()
        self.server.starttls()
        self.server.login(self.__sender, self.__psw)
        self.loged_in = True

    def send(self):
        self.server.sendmail(self.__sender, self.receiver, self.msg)
        self.server.quit()

    def change_sender(self, sender):
        self.__sender = sender


# reciver = 'eliransharon@gmail.com'
# psw = 'uvfeovzrzetgfhxb'
# e = email(reciver, 'this is test mail')
# e.login('gmail', psw)
# e.send()