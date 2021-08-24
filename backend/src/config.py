import secrets
import os


#secret_key = secrets.token_hex(16)
# example output, secret_key = 000d88cd9d90036ebdd237eb6b0db000

SECRET_KEY = 'DEX/BABA/SMC-N/QSM/'
curren_dir = os.path.abspath(os.path.dirname(__file__))
RESSOURCE_DIR = os.path.join(curren_dir, 'ressources')
