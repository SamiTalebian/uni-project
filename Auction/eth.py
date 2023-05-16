from django.conf import settings
from web3 import Web3


web3 = Web3(Web3.HTTPProvider(settings.ETHEREUM_NODE_URL))
