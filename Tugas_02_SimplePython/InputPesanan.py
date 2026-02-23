def ambil_pesanan(menu):
    pesanan = []

    while True:
        try:
            pilih = int(input("\nMasukkan ID menu (0 untuk selesai): "))
            
            if pilih == 0:
                break
            
            if pilih in menu:
                jumlah = int(input("Masukkan jumlah: "))
                nama, harga = menu[pilih]
                subtotal = harga * jumlah

                pesanan.append((nama, jumlah, subtotal))
                print(f"{nama} ditambahkan!")
            else:
                print("ID tidak tersedia!")

        except ValueError:
            print("Input harus berupa angka!")

    return pesanan