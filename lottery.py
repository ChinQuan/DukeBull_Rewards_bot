import os, json, random, datetime, base58
from solana.rpc.api import Client
from solana.keypair import Keypair
from spl.token.instructions import transfer_checked, get_associated_token_address
from solana.transaction import Transaction
from solana.publickey import PublicKey

RPC_URL = os.getenv("RPC_URL")
TOKEN_MINT = PublicKey(os.getenv("TOKEN_MINT"))
DECIMALS = 9
REWARD = int(os.getenv("REWARD_AMOUNT"))
PRIVATE = os.getenv("REWARD_PRIVATE_KEY")

LIST_FILE = "buyers.json"
buyers = json.load(open(LIST_FILE))
if not buyers:
    print("Brak kupujących dziś.")
    raise SystemExit

winner = PublicKey(random.choice(buyers))
print("🏆  Winner:", winner)

client = Client(RPC_URL)
sender = Keypair.from_secret_key(base58.b58decode(PRIVATE))
src_ata  = get_associated_token_address(sender.public_key, TOKEN_MINT)
dst_ata  = get_associated_token_address(winner, TOKEN_MINT)

tx = Transaction()
tx.add(
    transfer_checked(
        source = src_ata,
        dest   = dst_ata,
        owner  = sender.public_key,
        amount = REWARD,
        decimals = DECIMALS,
        mint   = TOKEN_MINT,
    )
)

sig = client.send_transaction(tx, sender)
print("✅  Sent reward, sig:", sig["result"])
# (opcjonalnie) wyczyść listę na kolejny dzień
open(LIST_FILE,"w").write("[]")
