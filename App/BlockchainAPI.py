from datetime import datetime
import json
from web3 import Web3
import App.config as config


class BlockchainAPI:
    def __init__(self, contractAddress):
        self.__contractAddress = contractAddress
        with open("./App/abi.json", "r") as file:
            self.__abi = json.loads(file.read())

        self.__w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

        self.__contract = self.__w3.eth.contract(
            address=contractAddress, abi=self.__abi)

        self.__chain_id = 1337

    def getTransaction(self, address, wei):
        return {
            "chainId": self.__chain_id,
            "gasPrice": self.__w3.eth.gas_price,
            "from": address,
            "nonce": self.__w3.eth.getTransactionCount(address),
            "value": wei
        }

    def addPost(self, post_text: str, post_media_link: str, date: datetime, address: int, private_key: int):
        contract_function = self.__contract.functions.addPost(post_text, post_media_link, int(date.timestamp()))
        self.runBlockchainFunc(contract_function, address, private_key)

    def addBet(self, postID: int, betted_amount: int, address: int, private_key: int):
        contract_function = self.__contract.functions.addBet(postID)
        self.runBlockchainFunc(contract_function, address, private_key, betted_amount)

    def addValidityMedia(self, postID: int, text: str, link: str, address: int, private_key: int):
        contract_function = self.__contract.functions.addValidityMedia(postID, text, link)
        self.runBlockchainFunc(contract_function, address, private_key)

    def vote(self, postID: int, is_valid: bool, address: int, private_key: int):
        contract_function = self.__contract.functions.vote(postID, is_valid)
        self.runBlockchainFunc(contract_function, address, private_key)

    def enableVotes(self, postID: int, address: int, private_key: int):
        contract_function = self.__contract.functions.enableVotes(postID)
        self.runBlockchainFunc(contract_function, address, private_key)

    def terminatePost(self, postID: int, address: int, private_key: int):
        contract_function = self.__contract.functions.terminatePost(postID)
        self.runBlockchainFunc(contract_function, address, private_key)

    def getPost(self, postID: int, address: int, private_key: int):
        return self.__contract.functions.getPost(postID).call()

    def runBlockchainFunc(self, contract_function, address, private_key: int, wei = 0):
        transaction = contract_function.buildTransaction(self.getTransaction(address, wei))
        signed_txn = self.__w3.eth.account.sign_transaction(transaction, private_key = private_key)
        tx_hash = self.__w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(tx_hash)
        tx_receipt = self.__w3.eth.wait_for_transaction_receipt(tx_hash)
        print(tx_receipt)
