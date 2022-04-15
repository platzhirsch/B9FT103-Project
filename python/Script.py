import os
from dotenv import load_dotenv
from pathlib import Path

#IMPORT PRIVATE KEY AND RPC PROVIDER 
dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)

#LOAD VARIABLES 
private_key = os.getenv('PRIVATE_KEY')
rpc_provider = os.getenv('RPC_PROVIDER')

