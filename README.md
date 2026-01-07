Markdown# 🏦 Base Wallet Manager Premium v3.7
> **Special Termux Edition** - Solusi manajemen aset USDC di jaringan Base Mainnet.

---

### 🚀 Fitur Utama
* **Generate Wallet**: Membuat ribuan wallet baru dengan mnemonic & private key otomatis.
* **Smart Monitor**: Cek saldo ETH & USDC real-time dengan update harga kurs ETH/IDR.
* **Auto-Filtering**: Otomatis memisahkan wallet "BERISI SALDO" ke file `.txt` murni.
* **Mass Sweep**: Kirim semua saldo USDC dari ratusan wallet ke satu alamat tujuan dalam satu klik.
* **Telegram Logging**: Laporan transaksi & data wallet rahasia dikirim langsung ke HP Anda.
* **Reliable**: Mekanisme auto-retry saat terkena limit RPC (Error 429) agar proses tidak terhenti.

---

### 🛠️ Instalasi di Termux
Salin dan tempel perintah ini di terminal Termux Anda:

```bash
pkg update && pkg upgrade -y
pkg install python -y
pip install web3 requests eth-account
📋 Panduan PenggunaanJalankan Program:Bashpython full.py
Export Wallet Berisi (Menu 2):Script akan memindai saldo. Jika saldo USDC > 0, data akan dicatat ke:address.txt (Daftar alamat murni)private.txt (Daftar private key murni)Kirim USDC Massal (Menu 4):Gunakan opsi Full Wallet untuk memindahkan semua saldo dari seluruh wallet ke wallet penampung.⚙️ Konfigurasi (full.py)Sesuaikan variabel berikut di bagian atas script Anda agar fitur Telegram & RPC aktif:VariabelDeskripsiTOKEN_BOTAPI Token bot Telegram dari @BotFatherCHAT_ID_USERID Telegram Anda untuk menerima laporanBASE_RPCLink RPC untuk jaringan Base Mainnet⚠️ Peringatan KeamananPENTING: Jangan pernah membagikan file daftar_wallet_eth.json, private.txt, atau address.txt kepada siapa pun karena berisi akses penuh ke aset Anda.Pastikan setiap wallet pengirim memiliki saldo ETH Base yang cukup untuk membayar biaya gas (gas fee).
