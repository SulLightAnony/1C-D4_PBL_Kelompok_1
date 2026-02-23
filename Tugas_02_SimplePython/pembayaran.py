def pembayaran(pesanan) :
    total = 0 
    konfirmasi = False #konfirmasi agar proses pembayaran berulang saat pembayaran kurang

    for item in pesanan :
        total += item[2]

    print("\nTotal pembelian : Rp ", total)
    while konfirmasi == False : 
        uang_bayar = int(input("input pembayaran : "))

        if uang_bayar < total :
            print("Pembayaran anda kurang!")
        elif uang_bayar == total :
            konfirmasi = True
            kembalian = 0;
            print("Pembayaran anda sebesar Rp ", uang_bayar, " berhasil!")
            print("Kembalian : Rp ", kembalian)
        else :
            konfirmasi = True
            kembalian = uang_bayar - total
            print("Pembayaran anda sebesar ", uang_bayar, " berhasil!")
            print("Kembalian : Rp ", kembalian)
    
 #pembuatan struk
    from datetime import datetime

    print("=" * 40)
    print("        AYAM GEPREK BERKAH")
    print("=" * 40)

    # Tanggal
    tanggal = datetime.now().strftime("%d-%m-%Y")
    print(f"Tanggal : {tanggal}")
    print("Kasir   : Asep")

    print("-" * 40)
    print(f"{'Menu':<22}{'Qty':>6}{'Subtotal':>12}")
    print("-" * 40)

    # data belanja
    for nama, qty, subtotal in pesanan:
        print(f"{nama:<22}{qty:>6}{subtotal:>12}")

    print("-" * 40)
    print(f"{'Total':<28}{total:>12}")
    print(f"{'Bayar':<28}{uang_bayar:>12}")
    print(f"{'Kembalian':<28}{kembalian:>12}")

    print("-" * 40)
    print("      Terima Kasih :)")
    print("    Selamat Menikmati!")
    print("=" * 40)
    