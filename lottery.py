import os
import random
import time
import base58
import datetime
from dotenv import load_dotenv
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.keypair import Keypair
from spl.token.instructions import transfer_checked, get_associated_token_address
from solana.publickey import PublicKey

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
TOKEN_MINT = PublicKey(os.getenv("TOKEN_MINT"))
REWARD_AMOUNT = int(os.getenv("REWARD_AMOUNT"))
PRIVATE_KEY = os.getenv("REWARD_PRIVATE_KEY")

client = Client(RPC_URL)
reward_wallet = Keypair.from_secret_key(base58.b58decode(PRIVATE_KEY))

buyers = []  # <- tutaj powinno się ładować z bazy lub pliku

def select_winner():
    if not buyers:
        print("Brak kupujących.")
        return None
    return random.choice(buyers)

def send_reward(winner):
    ata = get_associated_token_address(reward_wallet.public_key, TOKEN_MINT)
    recipient_ata = get_associated_token_address(PublicKey(winner), TOKEN_MINT)

    txn = Transaction()
    txn.add(
        transfer_checked(
            source=ata,
            dest=recipient_ata,
            owner=reward_wallet.public_key,
            amount=REWARD_AMOUNT,
            decimals=9,
            mint=TOKEN_MINT
        )
    )

    response = client.send_transaction(txn, reward_wallet)
    print(f"🎉 Nagroda wysłana do {winner}: {response}")

if __name__ == "__main__":
    now = datetime.datetime.utcnow()
    if now.hour == 21:
        winner = select_winner()
        if winner:
            send_reward(winner)
# Placeholder – daily draw logic and on-chain reward sending
