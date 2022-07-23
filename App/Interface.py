from blockchainAPI import blockchainAPI
from activePostsManager import activePostsManager

class Interface:
    def __init__(self, activePostsManager, blockchainAPI):
        self.__activePostsManager = activePostsManager
        self.__blockchainAPI = blockchainAPI

        self.__commands = {
            "addPost": self.addPost
        }
    
    # TODO: Ler comandos do usuário e chamar as funções corretas
    def run(self):
        "Starts CLI"
        while True:
            command = input("")
            self.__commands[command]()

    def addPost(self, post):
        blockchainAPI.addPost(post)
        activePostsManager.addPost(post)
