from App.Interface import Interface
from App.blockchainAPI import BlockchainAPI
from App.activePostsManager import ActivePostsManager

activePostsManager = ActivePostsManager()
BlockchainAPI = BlockchainAPI()

interface = Interface(activePostsManager, BlockchainAPI)
interface.run()