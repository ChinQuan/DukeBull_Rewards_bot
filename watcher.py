# watcher.py (uruchamiany w pętli)
import os, json, time
from solana.rpc.api import Client

RPC_URL   = os.getenv("RPC_URL")
TOKEN_MINT = os.getenv("TOKEN_MINT")
LIST_FILE = "buyers.json"
client = Client(RPC_URL)

buyers = set()
if os.path.exists(LIST_FILE):
    buyers.update(json.load(open(LIST_FILE)))

def save():
    json.dump(sorted(buyers), open(LIST_FILE, "w"))

def scan():
    sigs = client.get_signatures_for_address(TOKEN_MINT, limit=50)["result"]
    for sig in sigs:
        tx = client.get_transaction(sig["signature"], encoding="json")["result"]
        for b in tx["meta"]["postTokenBalances"]:
            owner = b.get("owner")
            if owner and owner not in buyers:
                buyers.add(owner)
                print("🟢  new buyer:", owner)
                save()

if __name__ == "__main__":
    while True:
        scan()
        time.sleep(60)
