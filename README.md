Base Wallet Manager Premium v3.7 (Termux Edition)
Script Python berbasis CLI yang dioptimalkan untuk mengelola banyak wallet di jaringan Base Mainnet. Fitur utama meliputi pembuatan wallet massal, monitoring saldo real-time, dan pengiriman USDC otomatis (satuan atau massal).

🚀 Fitur Utama
Pembuatan Wallet Massal: Generate wallet baru lengkap dengan mnemonic, alamat, dan private key yang tersimpan otomatis dalam format JSON.

Monitor Saldo Otomatis: Memeriksa saldo ETH dan USDC secara real-time untuk seluruh daftar wallet.

Auto-Export Wallet Berisi: Secara otomatis menyaring wallet yang memiliki saldo USDC > 0 dan menyimpannya ke file address.txt dan private.txt dalam format teks murni baris demi baris.

Multisend / Sweep USDC: Fitur pengiriman massal dari semua wallet yang memiliki saldo ke satu alamat penampung yang ditentukan.

Integrasi Telegram: Notifikasi instan ke bot Telegram setiap kali ada pengiriman USDC yang berhasil atau saat meminta data wallet spesifik.

Anti-Rate Limit: Dilengkapi dengan mekanisme auto-retry jika terkena limit RPC (Error 429).

🛠️ Persiapan & Instalasi (Termux)
Pastikan Anda telah menginstal Python dan library yang dibutuhkan di Termux Anda:

Bash

pkg update && pkg upgrade
pkg install python
pip install web3 requests eth-account
📋 Cara Penggunaan
Jalankan script utama:

Bash

python full.py
Menu [1]: Gunakan untuk membuat wallet baru jika belum memiliki file daftar_wallet_eth.json.

Menu [2]: Jalankan untuk memantau saldo. Wallet yang memiliki saldo USDC akan otomatis diekspor ke:

address.txt: Daftar alamat wallet (murni teks).

private.txt: Daftar private key (murni teks).

Menu [4]: Pilih opsi Full Wallet jika ingin melakukan sweep (mengirim semua saldo USDC dari banyak wallet ke 1 alamat tujuan).

⚙️ Konfigurasi
Buka file full.py dan sesuaikan variabel berikut di bagian atas script:

TOKEN_BOT: API Token bot Telegram Anda.

CHAT_ID_USER: ID chat Telegram Anda untuk menerima laporan.

BASE_RPC: URL RPC jaringan Base (Default: Mainnet).

⚠️ Catatan Keamanan
Jangan pernah membagikan file daftar_wallet_eth.json, private.txt, atau private.json kepada siapa pun karena berisi akses penuh ke aset Anda.

Pastikan wallet memiliki saldo ETH (Base) yang cukup untuk biaya gas sebelum melakukan pengiriman USDC.
