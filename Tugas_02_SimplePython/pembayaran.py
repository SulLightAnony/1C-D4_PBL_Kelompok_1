konfirmasi = False #konfirmasi agar proses pembayaran berulang saat pembayaran kurang

while konfirmasi == False : 
    pembayaran = input("input pembayaran : ")
    grandtotal = 150000

    if int(pembayaran) < grandtotal :
        print("Pembayaran anda kurang!")
    elif int(pembayaran) == grandtotal :
        konfirmasi = True
        kembalian = 0;
        print("Pembayaran anda sebesar ", int(pembayaran), " berhasil!")
        print("Kembalian : Rp ", kembalian)
    else :
        konfirmasi = True
        kembalian = int(pembayaran) - grandtotal
        print("Kembalian : Rp ", kembalian)

#pembuatan struk
from datetime import datetime

print("=================================")
print("        AYAM GEPREK BERKAH")
print("=================================")

# Tanggal
tanggal = datetime.now().strftime("%d-%m-%Y")
print("Tanggal :", tanggal)
print("Kasir   : Asep")

print("---------------------------------")
print("Menu\t\tQty\tSubtotal")
print("---------------------------------")

# data belanja
belanja = [
    ("Ayam Geprek Original", 2, 30000),
    ("Es Teh", 1, 4000),
    ("Nasi Putih", 1, 5000)
]

total = 0
for item in belanja:
    print(f"{item[0]}\t{item[1]}\t{item[2]}")
    total += item[2]

print("---------------------------------")
print("Total\t\t\t", grandtotal)
print("Bayar\t\t\t", int(pembayaran))
print("Kembalian\t\t", kembalian)
print("---------------------------------")
print("     Terima Kasih :)")
print("   Selamat Menikmati!")
print("=================================")