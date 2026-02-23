# main.py

from Menu import Tampilkan_menu
from InputPesanan import ambil_pesanan
from pembayaran import pembayaran

print("===== SISTEM KASIR RESTORAN AYAM GEPREK =====")
menu = Tampilkan_menu()

i = 0

for item in menu.values():
    i += 1
    print(f"{i}. {item[0]} - Rp {item[1]}")
    
pembayaran(ambil_pesanan(menu))