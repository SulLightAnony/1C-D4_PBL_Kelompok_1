def pembayaran(pesanan) :
    total = 0 
    konfirmasi = False #konfirmasi agar proses pembayaran berulang saat pembayaran kurang

    for item in pesanan :
        total += item[2]

    while konfirmasi == False : 
        pembayaran = input("input pembayaran : ")
        grandtotal = 150000

        if int(pembayaran) < total :
            print("Pembayaran anda kurang!")
        elif int(pembayaran) == total :
            konfirmasi = True
            kembalian = 0;
            print("Pembayaran anda sebesar ", int(pembayaran), " berhasil!")
            print("Kembalian : Rp ", kembalian)
        else :
            konfirmasi = True
            kembalian = int(pembayaran) - total
            print("Kembalian : Rp ", kembalian)

