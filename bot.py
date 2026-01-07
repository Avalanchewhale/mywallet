import json
import time
import os
import requests
from web3 import Web3
from eth_account import Account

# ================= KONFIGURASI =================
TOKEN_BOT = "8216614487:AAE5jxthgqmDl-D6YXlECR0mK_vW-034Tbk"
CHAT_ID_USER = "-1003599517048"
BASE_RPC = "https://mainnet.base.org"
USDC_CONTRACT = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
FILE_JSON = "daftar_wallet_eth.json"

# ANSI Warna Terminal
G = '\033[92m' # Hijau
Y = '\033[93m' # Kuning
R = '\033[91m' # Merah
C = '\033[96m' # Cyan
W = '\033[0m'  # Putih
# ===============================================

w3 = Web3(Web3.HTTPProvider(BASE_RPC))
USDC_ABI = [
    {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"},
    {"constant": False, "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "type": "function"}
]

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def load_wallets():
    if os.path.exists(FILE_JSON):
        try:
            with open(FILE_JSON, "r") as f: return json.load(f)
        except: return []
    return []

def save_txt_results(addresses, privkeys):
    """Menyimpan alamat dan private key murni baris demi baris (Hanya yang ada saldo)"""
    # Menyimpan address.txt sesuai format gambar yang Anda minta
    with open('address.txt', 'w') as f:
        f.write("\n".join(addresses))
    
    # Menyimpan private.txt sesuai format gambar yang Anda minta
    with open('private.txt', 'w') as f:
        f.write("\n".join(privkeys))

def execute_send(sender, dest_addr, amount, contract, silent=False):
    """Fungsi eksekusi transaksi USDC"""
    try:
        amt_wei = int(amount * 10**6)
        gas_est = contract.functions.transfer(dest_addr, amt_wei).estimate_gas({'from': sender['address']})
        gas_price = int(w3.eth.gas_price * 1.1)
        
        tx = contract.functions.transfer(dest_addr, amt_wei).build_transaction({
            'chainId': 8453,
            'gas': gas_est,
            'gasPrice': gas_price,
            'nonce': w3.eth.get_transaction_count(sender['address'])
        })
        
        signed = w3.eth.account.sign_transaction(tx, sender['private_key'])
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        
        if not silent: print(f"{G}✅ Sukses! Hash: {w3.to_hex(tx_hash)}{W}")
        
        # Notifikasi Telegram
        msg = f"💸 *USDC SENT*\nDari: ID #{sender['id']}\nKe: `{dest_addr}`\nJumlah: {amount} USDC\nHash: `{w3.to_hex(tx_hash)}`"
        requests.post(f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage", 
                      json={"chat_id": CHAT_ID_USER, "text": msg, "parse_mode": "Markdown"})
        return True
    except Exception as e:
        if not silent: print(f"{R}❌ Gagal dari ID {sender['id']}: {e}{W}")
        return False

def cek_saldo():
    clear_screen()
    print(f"{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{W}")
    print(f"{C}         MONITOR SALDO & AUTO-EXPORT (V3.7)          {W}")
    print(f"{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{W}")
    contract = w3.eth.contract(address=w3.to_checksum_address(USDC_CONTRACT), abi=USDC_ABI)
    while True:
        try:
            wallets = load_wallets()
            if not wallets: print(f"{R}Daftar wallet kosong!{W}"); break
            addr_berisi, pk_berisi = [], []
            print(f"\n{Y}ID | Alamat          | USDC Bal   | ETH Bal     | Status{W}")
            print("-" * 65)
            for w in wallets:
                addr = w3.to_checksum_address(w['address'])
                success = False
                while not success:
                    try:
                        bal_usdc = contract.functions.balanceOf(addr).call() / 10**6
                        bal_eth = w3.from_wei(w3.eth.get_balance(addr), 'ether')
                        success = True
                    except Exception as e:
                        if "429" in str(e): # Mekanisme Retry
                            print(f"{Y}[!] Limit RPC, Menunggu 5 detik...{W}", end="\r")
                            time.sleep(5)
                        else: break
                if success:
                    if bal_usdc > 0:
                        status = f"{G}ADA ISI{W}"
                        print(f"{w['id']:>2} | {w['address'][:10]}... | {bal_usdc:>10.2f} | {bal_eth:.6f} | {status}")
                        # HANYA YANG ADA SALDO DICATAT KE LIST
                        addr_berisi.append(w['address'])
                        pk_berisi.append(w['private_key'])
                    else:
                        status = f"{R}KOSONG{W}"
                        print(f"{w['id']:>2} | {w['address'][:10]}... | {bal_usdc:>10.2f} | {bal_eth:.6f} | {status}")
                time.sleep(0.3)
            
            # Simpan hasil ke address.txt dan private.txt
            save_txt_results(addr_berisi, pk_berisi)
            print("-" * 65)
            print(f"{G}✅ address.txt & private.txt diupdate ({len(addr_berisi)} wallet berisi){W}")
            print(f"{Y}Tekan Ctrl+C untuk kembali ke menu...{W}")
            time.sleep(60); clear_screen()
        except KeyboardInterrupt: break
        except Exception as e: print(f"{R}Error: {e}{W}"); time.sleep(5)

def kirim_usdc():
    clear_screen()
    print(f"{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{W}")
    print(f"{C}           MENU PENGIRIMAN USDC              {W}")
    print(f"{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{W}")
    wallets = load_wallets()
    if not wallets: return

    print(f" [{G}1{W}] Kirim dari SATU Wallet (Pilih ID)")
    print(f" [{G}2{W}] Kirim dari SEMUA Wallet (Sweep/Full)")
    opsi = input(f"\n{Y}Pilih opsi (1/2): {W}")

    dest_addr = input(f"{Y}Masukkan Alamat Tujuan: {W}")
    try: dest_addr = w3.to_checksum_address(dest_addr)
    except: print(f"{R}Alamat tidak valid!{W}"); return

    contract = w3.eth.contract(address=w3.to_checksum_address(USDC_CONTRACT), abi=USDC_ABI)

    if opsi == "1":
        try:
            id_sender = int(input(f"{Y}Masukkan ID Pengirim: {W}"))
            sender = next((w for w in wallets if w['id'] == id_sender), None)
            if not sender: print(f"{R}ID tidak ditemukan!{W}"); return
            amt = float(input(f"{Y}Jumlah USDC: {W}"))
            execute_send(sender, dest_addr, amt, contract)
        except Exception as e: print(f"{R}Error: {e}{W}")

    elif opsi == "2":
        print(f"\n{C}Memproses pengiriman masal...{W}")
        count = 0
        for w in wallets:
            try:
                bal_raw = contract.functions.balanceOf(w['address']).call()
                if bal_raw > 0: # Hanya kirim jika saldo > 0
                    amt = bal_raw / 10**6
                    print(f"{Y}[ID {w['id']}] Mengirim {amt} USDC...{W}", end=" ")
                    if execute_send(w, dest_addr, amt, contract, silent=True):
                        print(f"{G}SENT!{W}")
                        count += 1
                time.sleep(1)
            except: continue
        print(f"\n{G}Selesai! Berhasil mengirim dari {count} wallet.{W}")
    input("\nTekan Enter...")

def generate_wallet():
    clear_screen()
    Account.enable_unaudited_hdwallet_features()
    wallets_data = load_wallets()
    try:
        jumlah = int(input(f"Mau buat berapa wallet baru?: "))
        start_id = len(wallets_data) + 1
        for i in range(start_id, start_id + jumlah):
            acct, mnem = Account.create_with_mnemonic()
            wallets_data.append({"id": i, "label": f"wallet {i}", "address": acct.address, "private_key": acct.key.hex(), "mnemonic": mnem})
            print(f"\r{G}Membuat wallet #{i}...{W}", end="")
        with open(FILE_JSON, "w") as f: json.dump(wallets_data, f, indent=4)
        print(f"\n{G}✅ Sukses!{W}")
    except Exception as e: print(f"\n{R}Gagal: {e}{W}")
    input("\nTekan Enter...")

def main():
    while True:
        clear_screen()
        print(f"{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{W}")
        print(f"{C}       BASE WALLET MANAGER PREMIUM V3.7      {W}")
        print(f"{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{W}")
        print(f" [{G}1{W}] Tambah Wallet Baru")
        print(f" [{G}2{W}] Monitor Saldo & Auto-Export TXT")
        print(f" [{G}3{W}] Kirim Data Wallet ke Telegram")
        print(f" [{G}4{W}] Kirim USDC (Satuan / Full Wallet)")
        print(f" [{R}0{W}] Keluar")
        p = input(f"\n{Y}Pilih Menu: {W}")
        if p == "1": generate_wallet()
        elif p == "2": cek_saldo()
        elif p == "3":
            clear_screen()
            wallets = load_wallets()
            for w in wallets: print(f"[{w['id']}] {w['address']}")
            try:
                pilih = int(input(f"\n{Y}ID Wallet ke TG: {W}"))
                t = next((w for w in wallets if w['id'] == pilih), None)
                if t:
                    msg = f"🔐 *WALLET DATA*\nID: `{t['id']}`\nAddy: `{t['address']}`\nKey: `{t['private_key']}`"
                    requests.post(f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage", json={"chat_id": CHAT_ID_USER, "text": msg, "parse_mode": "Markdown"})
                    print(f"{G}✅ Terkirim!{W}")
            except: pass
            input("\nTekan Enter...")
        elif p == "4": kirim_usdc()
        elif p == "0": break

if __name__ == "__main__": main()
