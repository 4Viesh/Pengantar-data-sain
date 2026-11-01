import pandas as pd

print("=== MEMPROSES DATASET POS 2024-2025 ===")

# 1. Membaca File Dataset
try:
    df = pd.read_csv('paket_a_transaksi_pos_2024_2025.csv')
    print("✓ Dataset berhasil dimuat.")
except FileNotFoundError:
    print("X File 'paket_a_transaksi_pos_2024_2025.csv' tidak ditemukan di folder ini!")
    exit()

# 2. Penanganan Missing Value
df['kode_kasir'] = df['kode_kasir'].fillna('UNKNOWN')

# 3. Membersihkan Format Harga Satuan (Menangani koma desimal & titik ribuan)
def bersihkan_harga(val):
    val_str = str(val).strip()
    if ',' in val_str:
        val_str = val_str.split(',')[0].replace('.', '')
    else:
        val_str = val_str.replace('.', '')
    return float(val_str)

df['harga_satuan_clean'] = df['harga_satuan'].apply(bersihkan_harga)

# 4. Parsing Tanggal & Ekstrak Tahun
df['tanggal_clean'] = pd.to_datetime(df['tanggal'], format='mixed', dayfirst=True)
df['tahun'] = df['tanggal_clean'].dt.year

# 5. Filtering Status Transaksi (Hanya status SELESAI)
df_selesai = df[df['status'] == 'SELESAI'].copy()

# 6. Menghitung Pendapatan Bersih (Memperhitungkan Diskon Persen)
df_selesai['pendapatan_kotor'] = df_selesai['jumlah'] * df_selesai['harga_satuan_clean']
df_selesai['pendapatan_bersih'] = df_selesai['pendapatan_kotor'] * (1 - (df_selesai['diskon_persen'] / 100.0))

# 7. Menghitung Jumlah Pendapatan per Tahun (2024 & 2025)
ringkasan = df_selesai.groupby('tahun')['pendapatan_bersih'].sum().reset_index()

# Format tampilan Rupiah
ringkasan['total_pendapatan'] = ringkasan['pendapatan_bersih'].apply(lambda x: f"Rp {x:,.2f}")

print("\n==========================================")
print("       HASIL REKAP PENDAPATAN PER TAHUN   ")
print("==========================================")
print(ringkasan[['tahun', 'total_pendapatan']].to_string(index=False))
print("==========================================\n")