import datetime
from App.BlockchainAPI import BlockchainAPI
from App.ActivePostsManager import ActivePostsManager
import App.config as config

class Interface:
    def __init__(self, activePostsManager: ActivePostsManager, blockchainAPI: BlockchainAPI):
        self.__activePostsManager = activePostsManager
        self.__blockchainAPI = blockchainAPI

        self.__commands = {
            "1": self.intGetPost,
            "2": self.intAddPost,
            "3": self.intAddBet,
            "4": self.intAddVote,
            "5": self.intAddValidityMedia,
            "6": self.registerUser
        }

    # TODO: Ler comandos do usuário e chamar as funções corretas
    def run(self):
        start_message = 'Welcome to Challenge Media!\n' \
            'Here you can make a challenge to yourself or bet on your friends challenges!\n'

        menu_message = 'What do you want to do?\n' \
            'Type:\n' \
            '1: to view a post.\n' \
            '2: to create a new post.\n' \
            '3: to place a bet on a post.\n' \
            '4: to vote on a post.\n' \
            '5: to add a validity media on your post.\n' \
            '6: to change your information.'

        print(start_message)
        self.registerUser()
        while True:
            print(menu_message)
            command = input("")
            if command not in self.__commands:
                print('Invalid command. Try again.')
            else:
                self.__commands[command]()

    def registerUser(self):
        # local_address = input('Whats your address?')
        local_address = "0xfd7F30473aAA05E4370dC57C936318F11EbCc638"
        # local_private_key = input('Whats yout private key?')
        local_private_key = "0xa1d25ac484d6f294f2edc6614a62b722a2f2223a2bd63e05786876912398e066"
        print('You were registered! Thank you.\n')
        return local_address, local_private_key

    def intGetPost(self):
        post_id = int(input("Declare the post id: \n "))
        post = self.__blockchainAPI.getPost(post_id, config.address, config.private_key)
        print(post)

    def intAddPost(self):
        text = input("What's your chalenge?")
        media_link = input("Insert a midia link:")
        time_in_days = int(
            input("How long does it take to complete the challenge? (in days)"))
        date = datetime.datetime.now() + datetime.timedelta(time_in_days)

        post_id = self.__blockchainAPI.addPost(text, media_link, date, config.address, config.private_key)
        self.__activePostsManager.addPublishedPost(post_id, date)

    def intAddBet(self, post_id):
        post_id = int(input("What's the post id?"))
        side = input("Do you want to bet in favor or against? ('i' or 'a')")
        if side.lower() == 'i':
            in_favor = True
        else:
            in_favor = False
        amount = int(input('How much do you want to bet?'))
        post_id = self.__blockchainAPI.addBet(post_id, amount, in_favor, config.address, config.private_key)

    def intAddVote(self):
        post_id = int(input("declare the post id: \n "))
        is_valid = bool(
            input("is the in favor(True) or against(False) the bet? \n"))
        self.__blockchainAPI.vote(post_id, is_valid, config.address, config.private_key)

    def intAddValidityMedia(self):
        post_id = int(input("declare the post id: \n "))
        validity_text = input("insert validity text: \n")
        validity_link = input("insert the validity link: \n")
        self.__blockchainAPI.addValidityMedia(post_id, validity_text, validity_link, config.address, config.private_key)
