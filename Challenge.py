from blockchainAPI import blockchainAPI
from activePostsManager import activePostsManager

start_message = 'Welcome to Challenge Media!\n' \
                'Here you can make a challenge to yourself or bet on your friends challenges!\n'

menu_message =  'What do you want to do?\n' \
                'Type:\n' \
                '1: to view a post.\n' \
                '2: to create a new post.\n' \
                '3: to place a bet on a post.\n' \
                '4: to vote on a post.\n' \
                '5: to add a validity media on your post.'


class Interface:
    def __init__(self, activePostsManager, blockchainAPI):
        self.__activePostsManager = activePostsManager
        self.__blockchainAPI = blockchainAPI

        self.__commands = {
            "addPost": self.add_post
        }
    
    # TODO: Ler comandos do usuário e chamar as funções corretas
    def run(self):
        "Starts CLI"
        while True:
            print(menu_message)
            command = input("")
            if command not in self.__commands:
                print('Invalid command. Try aguain.')
            else:
                self.__commands[command]()

    def add_post(self, post):
        blockchainAPI.addPost(post)
        activePostsManager.addPost(post)


commands = {'1': self.add_post, }
def receive_comand():
    while True:
        print(menu_message)
        command = input()

        if command not in commands:
            print('Invalid command. Try aguain.')
        else:
            if command == '1':
                pass
            elif command == '2':
                pass

def add_post(self):
    pass








