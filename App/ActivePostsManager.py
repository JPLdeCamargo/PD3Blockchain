from App.BlockchainAPI import BlockchainAPI
import App.config as config

class ActivePostsManager:
    def __init__(self, blockchainAPI: BlockchainAPI):
        self.__published_posts = []
        self.__betted_posts = []
        self.__blockchainAPI = blockchainAPI

    def addPublishedPost(self, postID, end_date):
        self.__published_posts.append((postID, end_date))

    def addBettedPost(self, postID, end_date):
        self.__betted_posts.append((postID, end_date))

    def enableVotes(self):
        for post in self.__published_posts:
            self.__blockchainAPI.enableVotes(post[0], config.private_key)

    def terminatePosts(self):
        for post in self.__betted_posts:
            self.__blockchainAPI.terminatePost(post[0], config.private_key)
