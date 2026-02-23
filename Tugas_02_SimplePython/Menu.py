def Tampilkan_menu():
    menu = {
        1: ("Ayam Geprek Original", 15000),
        2: ("Ayam Geprek Keju", 18000),
        3: ("Ayam Geprek Mozzarella", 20000),
        4: ("Ayam Geprek Level 5", 16000),
        5: ("Ayam Geprek Level 10", 17000),
        6: ("Paket Geprek + Nasi + Es Teh", 20000),
        7: ("Nasi Putih", 5000),
        8: ("Es Teh", 4000),
        9: ("Teh Hangat", 3000),
        10: ("Air Mineral", 3000)
    }
    
    print("\n=== MENU AYAM GEPREK ===")
    for id_menu, item in menu.items():
        print(f"{id_menu}. {item[0]} - Rp{item[1]}")
    
    return menu