import time
import requests
from solana.rpc.api import Client

TOKEN_MINT = "BuLL65dUKeRgZ1TUo3g9F3SAgJmdwq23mcx7erb9QX9D"
RPC_URL = "https://api.mainnet-beta.solana.com"
client = Client(RPC_URL)

# Przechowywane adresy kupujących
buyers = set()

def get_recent_buyers():
    global buyers
    print("🔍 Sprawdzam nowych kupujących...")

    try:
        result = client.get_signatures_for_address(TOKEN_MINT, limit=20)
        for tx in result["result"]:
            sig = tx["signature"]
            tx_info = client.get_transaction(sig, encoding="json")
            meta = tx_info["result"]["meta"]
            if meta and meta.get("postTokenBalances"):
                for entry in meta["postTokenBalances"]:
                    owner = entry.get("owner")
                    if owner and owner not in buyers:
                        buyers.add(owner)
                        print(f"✅ Nowy kupujący: {owner}")
    except Exception as e:
        print(f"⚠️ Błąd: {e}")

if __name__ == "__main__":
    while True:
        get_recent_buyers()
        time.sleep(60)
# Placeholder – logic for watching BuLL token buyers
