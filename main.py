from App.Interface import Interface
from App.BlockchainAPI import BlockchainAPI
from App.ActivePostsManager import ActivePostsManager
import App.config as config
import os

blockchainAPI = BlockchainAPI(os.getenv("CONTRACT_ADDRESS"))
activePostsManager = ActivePostsManager(blockchainAPI)
interface = Interface(activePostsManager, blockchainAPI)

config.address, config.private_key = interface.registerUser()

interface.run()
