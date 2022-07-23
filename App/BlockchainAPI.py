from datetime import datetime

class BlockchainAPI:
    def __init__(self):
        pass

    def addPost(post_text: str, post_media_link: str, date: datetime, private_key: int):
        pass

    def addBet(postID: int, betted_amount: int, private_key: int):
        pass

    def addValidityMedia(postID: int, text: str, link: str, private_key: int):
        pass

    def vote(postID: int, is_valid: bool, private_key: int):
        pass

    def enableVotes(postID: int, private_key: int):
        pass

    def terminatePost(postID: int, private_key: int):
        pass

    def getPost(postID: int, private_key: int):
        pass
