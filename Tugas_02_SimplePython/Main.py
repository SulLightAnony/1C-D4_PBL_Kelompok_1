# main.py

from menu import menu
from input_pesanan import ambil_pesanan
from pembayaran import proses_pembayaran

print("===== SISTEM KASIR RESTORAN AYAM GEPREK =====")
menu = menu()

i = 0

for item in menu.values():
    i += 1
    print(f"{i}. {item[0]} - Rp {item[1]}")
    
proses_pembayaran(ambil_pesanan(menu))