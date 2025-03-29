# Crypto OSINT Toolkit: Etherscan + Breadcrumbs
# ----------------------------------------------
# Created for open-source OSINT analysts and investigators
# No installation needed for Colab; free and accessible to all.

import requests
import webbrowser
import time

ETHERSCAN_API_KEY = "your_etherscan_api_key"  # Replace with your real API key

# -----------------------------
# Etherscan API Functions
# -----------------------------
def get_eth_transactions(address, limit=10):
    url = (
        f"https://api.etherscan.io/api?module=account&action=txlist"
        f"&address={address}&sort=desc&apikey={ETHERSCAN_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()
    if data['status'] == '1':
        return data['result'][:limit]
    else:
        print("Error fetching transactions:", data['message'])
        return []

def get_token_transfers(address, limit=10):
    url = (
        f"https://api.etherscan.io/api?module=account&action=tokentx"
        f"&address={address}&sort=desc&apikey={ETHERSCAN_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()
    if data['status'] == '1':
        return data['result'][:limit]
    else:
        print("Error fetching token transfers:", data['message'])
        return []

# -----------------------------
# Breadcrumbs Launch Function
# -----------------------------
def open_breadcrumbs_graph(address):
    url = f"https://breadcrumbs.app/graph?q={address}"
    webbrowser.open(url)
    print(f"Opened Breadcrumbs graph for {address}")

# -----------------------------
# Analysis Runner
# -----------------------------
def analyze_wallet(address):
    print(f"\n🔎 Analyzing Ethereum wallet: {address}\n")

    print("[1] Last 10 Transactions:")
    txs = get_eth_transactions(address)
    for tx in txs:
        eth_value = int(tx['value']) / 1e18
        print(f" - From {tx['from']} → To {tx['to']} | {eth_value:.4f} ETH | Hash: {tx['hash'][:10]}...")

    print("\n[2] Last 10 Token Transfers:")
    tokens = get_token_transfers(address)
    for token in tokens:
        print(f" - {token['tokenSymbol']}: {int(token['value']) / 10**int(token['tokenDecimal'])} from {token['from']} to {token['to']}")

    print("\n[3] Launching Breadcrumbs visual trace...")
    time.sleep(2)
    open_breadcrumbs_graph(address)

# -----------------------------
# Example Run
# -----------------------------
if __name__ == "__main__":
    print("""
    ==============================================
      🚀 CRYPTO OSINT TOOLKIT by OSINT Watchdog 
      Free & Open Source | Powered by Etherscan + Breadcrumbs
    ==============================================
    """)
    wallet_address = input("Enter Ethereum wallet address to investigate: ").strip()
    analyze_wallet(wallet_address)
