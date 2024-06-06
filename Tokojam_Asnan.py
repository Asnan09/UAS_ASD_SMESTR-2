from prettytable import PrettyTable
import pwinput
import os
import datetime
GREEN = "\033[92m"


def jam_toko():
    waktu_saat_ini = datetime.datetime.now().time()
    waktu_buka = datetime.time(6, 0)
    waktu_tutup = datetime.time(18, 0)
    return waktu_buka <= waktu_saat_ini <= waktu_tutup

def tambah_jam(daftar_jam):
    try:
        nama = input("Masukkan nama jam: ")
        jenis = input("Masukkan jenis jam: ")
        jumlah = int(input("Masukkan jumlah jam: "))
        harga = float(input("Masukkan harga jam: Rp "))
        jam_baru = {'Nama': nama, 'Jenis': jenis, 'Harga': harga, 'Stok': jumlah}
        daftar_jam.append(jam_baru)
        print(f"Barang {nama} ({jumlah} {jenis}) dengan harga Rp {harga:,} telah ditambahkan ke stok.")
    except (ValueError, EOFError, AttributeError):
        print("Input tidak valid. Harap masukkan data yang benar.")
    except KeyboardInterrupt:
        print("\ndibatalkan.")

def tampilkan_daftar_jam(daftar_jam):
    try:
        table = PrettyTable()
        table.field_names = ["No", "Nama", "Jenis", "Harga", "Stok"]
        for i, jam in enumerate(daftar_jam, start=1):
            table.add_row([i, jam['Nama'], jam['Jenis'], f"Rp {jam['Harga']:,}", jam['Stok']])
        print(table)
    except (EOFError, AttributeError):
        print("Terjadi kesalahan saat menampilkan daftar jam.")
    except KeyboardInterrupt:
        print("\ndibatalkan.")

def beli_barang(daftar_jam, pembeli, daftar_belanja):
    try:
        total_harga = 0
        for item in daftar_belanja:
            nama, jumlah = item['Nama'], item['Jumlah']
            for jam in daftar_jam:
                if jam['Nama'].lower() == nama.lower():
                    if jam['Stok'] >= jumlah:
                        total_harga += jam['Harga'] * jumlah
                    else:
                        print(f"Stok {jam['Nama']} tidak mencukupi.")
                        return
        print(f"Total harga sebelum diskon: Rp {total_harga:,}")

        if total_harga >= 350000:
            total_harga_diskon = total_harga * 0.75
            print(f"Total harga setelah diskon 25%: Rp {total_harga_diskon:,}")
        elif total_harga >= 100000:
            total_harga_diskon = total_harga * 0.9
            print(f"Total harga setelah diskon 10%: Rp {total_harga_diskon:,}")
        else:
            total_harga_diskon = total_harga
            print(f"Total harga: Rp {total_harga_diskon:,}")

        if pembeli['E-Pay'] >= total_harga_diskon:
            pembeli['E-Pay'] -= total_harga_diskon
            print(f"Pembelian berhasil. Saldo E-Pay {pembeli['Nama']}: Rp {pembeli['E-Pay']:,}")
            for item in daftar_belanja:
                nama, jumlah = item['Nama'], item['Jumlah']
                for jam in daftar_jam:
                    if jam['Nama'].lower() == nama.lower():
                        jam['Stok'] -= jumlah
        else:
            print("Saldo E-Pay tidak mencukupi.")
    except (ValueError, EOFError, AttributeError):
        print("Terjadi kesalahan saat proses pembelian.")
    except KeyboardInterrupt:
        print("\npembelian dibatalkan.")

def top_up_epay(pembeli, jumlah):
    try:
        if pembeli['Saldo'] >= jumlah:
            pembeli['E-Pay'] += jumlah
            pembeli['Saldo'] -= jumlah
            print(f"Top-up E-Pay berhasil. Saldo E-Pay {pembeli['Nama']}: Rp {pembeli['E-Pay']:,}")
            print(f"Saldo {pembeli['Nama']}: Rp {pembeli['Saldo']:,}")
        else:
            print("Saldo tidak mencukupi untuk melakukan top-up E-Pay.")
    except (ValueError, EOFError, AttributeError):
        print("Terjadi kesalahan saat top-up E-Pay.")
    except KeyboardInterrupt:
        print("\ntop-up dibatalkan.")

def hapus_barang(daftar_jam, nama_jam_hapus):
    try:
        for jam in daftar_jam:
            if jam['Nama'].lower() == nama_jam_hapus.lower():
                daftar_jam.remove(jam)
                print(f"Jam {nama_jam_hapus} telah dihapus dari stok.")
                return
        print(f"Jam {nama_jam_hapus} tidak ditemukan di stok.")
    except (EOFError, AttributeError):
        print("Terjadi kesalahan saat menghapus barang.")
    except KeyboardInterrupt:
        print("\npenghapusan dibatalkan.")

def menu_admin(daftar_jam):
    while True:
        try:
            print("|================================|")
            print("|         Menu Admin             |")
            print("|================================|")
            print("| 1. Tambahkan Jam ke Stok       |")
            print("| 2. Hapus Barang dari Stok      |")
            print("| 3. Lihat Daftar Jam            |")
            print("| 4. Keluar                      |")
            print("|================================|")

            pilihan = int(input("Masukkan nomor pilihan: "))
            os.system('cls')

            if pilihan == 1:
                tambah_jam(daftar_jam)
            elif pilihan == 2:
                nama_jam_hapus = input("Masukkan nama jam yang ingin dihapus: ")
                hapus_barang(daftar_jam, nama_jam_hapus)
            elif pilihan == 3:
                tampilkan_daftar_jam(daftar_jam)
            elif pilihan == 4:
                print("Keluar dari menu admin.")
                os.system('cls')
                break
            else:
                print("Pilihan tidak valid. Silakan masukkan nomor yang benar.")
        except (ValueError, EOFError):
            print("Input tidak valid. Silakan coba lagi.")
        except KeyboardInterrupt:
            print("\nSilakan coba lagi.")

def cetak_struk(pembeli, daftar_belanja, daftar_jam):
    try:
        # Mengambil tanggal dan waktu saat ini
        sekarang = datetime.datetime.now()
        tanggal = sekarang.strftime("%Y-%m-%d")
        waktu = sekarang.strftime("%H:%M:%S")

        print("========== Struk Pembelian ==========")
        print(f"Nama Pembeli: {pembeli['Nama']}")
        print(f"Tanggal     : {tanggal}")
        print(f"Jam         : {waktu}")
        print("=====================================")
        print("Daftar Barang:")
        total_harga = 0

        table = PrettyTable()
        table.field_names = ["No", "Nama Barang", "Jumlah", "Harga Satuan", "Subtotal"]

        for i, item in enumerate(daftar_belanja, start=1):
            nama, jumlah = item['Nama'], item['Jumlah']
            for jam in daftar_jam:
                if jam['Nama'].lower() == nama.lower():
                    subtotal = jam['Harga'] * jumlah
                    table.add_row([i, jam['Nama'], jumlah, f"Rp {jam['Harga']:,}", f"Rp {subtotal:,}"])
                    total_harga += subtotal

        print(table)
        print("-------------------------------------")
        print(f"Total Harga sebelum diskon: Rp {total_harga:,}")

        if total_harga >= 350000:
            diskon = total_harga * 0.25
            print(f"Diskon 25%: Rp {diskon:,}")
        elif total_harga >= 100000:
            diskon = total_harga * 0.1
            print(f"Diskon 10%: Rp {diskon:,}")
        else:
            diskon = 0
            print("Tidak ada diskon")

        total_harga_diskon = total_harga - diskon
        print(f"Total harga setelah diskon: Rp {total_harga_diskon:,}")

        pajak = total_harga_diskon * 0.1
        print(f"Pajak 10%: Rp {pajak:,}")

        total_bayar = total_harga_diskon + pajak
        print(f"Total Bayar: Rp {total_bayar:,}")

        print(f"Saldo E-Pay {pembeli['Nama']}: Rp {pembeli['E-Pay']:,}")
    except (ValueError, EOFError, AttributeError):
        print("Terjadi kesalahan saat mencetak struk pembelian.")
    except KeyboardInterrupt:
        print("\npencetakan struk dibatalkan.")

def registrasi_pembeli(daftar_pembeli):
    try:
        nama = input("Masukkan nama Anda: ")
        pin = pwinput.pwinput("Masukkan PIN Anda: ", mask='*')
        umur = int(input("Masukkan umur Anda: "))
        gender = input("Masukkan gender Anda (l/p): ").lower()
        saldo = 2000000
        e_pay = 500000 

        pembeli_baru = {'Nama': nama, 'PIN': pin, 'Umur': umur, 'Gender': gender, 'Saldo': saldo, 'E-Pay': e_pay}
        daftar_pembeli.append(pembeli_baru)
        print("Selamat Registrasi Anda berhasil.")
        return pembeli_baru
    except (ValueError, EOFError, AttributeError):
        print("Input tidak valid. Harap masukkan data yang benar.")
    except KeyboardInterrupt:
        print("\nRegistrasi dibatalkan.")
        return None

def menu_pembeli(daftar_jam, daftar_pembeli):
    while True:
        try:
            pembeli_nama = input("Masukkan nama Anda: ")
            pembeli_pin = pwinput.pwinput("Masukkan PIN Anda: ", mask='*')
            os.system('cls')

            pembeli = verifikasi_akun(daftar_pembeli, pembeli_nama, pembeli_pin)

            while pembeli is None:
                print("Nama dan PIN Anda tidak valid. Akun anda tidak terdaftar.")
                while True:
                    registrasi = input("Apakah Anda ingin registrasi? (ya/tidak): ").lower()
                    if registrasi == 'ya' or registrasi == 'tidak':
                        break
                    else:
                        print("Masukkan pilihan yang valid (ya/tidak).")
                if registrasi == 'ya':
                    os.system('cls')
                    pembeli = registrasi_pembeli(daftar_pembeli)
                elif registrasi == 'tidak':
                    os.system('cls')
                    return

            if pembeli is not None:
                pembeli_umur = pembeli['Umur']
                pembeli_gender = pembeli['Gender']
                if  pembeli_umur >= 30 and pembeli_umur <= 70:
                    sapaan = "Bapak" if pembeli_gender == 'l' else "Ibu"
                    jenis_jam = 'Jam Dewasa'
                elif 18 <= pembeli_umur <= 29:
                    sapaan = "Bang" if pembeli_umur == 'l' else "Mba"
                    jenis_jam = 'Jam anak cowok' if pembeli_gender == 'l' else 'Jam anak perempuan'
                elif pembeli_umur >= 10 and pembeli_umur <= 17:
                    sapaan = "Adek"
                    jenis_jam = 'Jam anak-anak'
                else:
                    sapaan = "Anda"
                    jenis_jam = ''

                print(f"Selamat datang, {sapaan} {pembeli['Nama']} di Toko Jam Asnan")
                while True:
                    print("|======================================|")
                    print("|             Menu Pembeli             |")
                    print("|======================================|")
                    print("| 1. Lihat Daftar jam                  |")
                    print("| 2. Beli Jam                          |")
                    print("| 3. Top Up E-Pay                      |")
                    print("| 4. Lihat Saldo dan E-Pay             |")
                    print("| 5. Keluar                            |")
                    print("|======================================|")

                    pilihan = input("Masukkan nomor pilihan: ")
                    os.system('cls')

                    if pilihan == "1":
                        tampilkan_daftar_jam([jam for jam in daftar_jam if jam['Jenis'] == jenis_jam])
                    elif pilihan == "2":
                        tampilkan_daftar_jam([jam for jam in daftar_jam if jam['Jenis'] == jenis_jam])
                        daftar_belanja = []
                        while True:
                            try:
                                nomor_jam = int(input("Masukkan nomor jam yang ingin Anda beli: "))
                                if nomor_jam < 1 or nomor_jam > len(daftar_jam):
                                    print("Masukkan nomor yang valid.")
                                    continue
                                jumlah_jam = int(input("Masukkan jumlah jam yang ingin Anda beli: "))
                                daftar_belanja.append({'Nama': daftar_jam[nomor_jam-1]['Nama'], 'Jumlah': jumlah_jam})
                            except (ValueError, EOFError):
                                print("Masukkan nomor yang valid.")
                            
                            while True:
                                lagi = input("Apakah Anda ingin membeli barang lain? (ya/tidak): ").lower()
                                if lagi == 'ya' or lagi == 'tidak':
                                    break
                                else:
                                    print("Masukkan pilihan yang valid (ya/tidak).")
                        
                            if lagi != 'ya':
                                break
                        deftar_belanja_filtered = []
                        for barang in daftar_jam:
                            for jam in daftar_jam:
                                if barang['Nama'] == jam['Nama'] and jam['Jenis'] == jenis_jam:
                                    deftar_belanja_filtered.append(barang)
                                    break

                        cetak_struk(pembeli, daftar_belanja, daftar_jam)
                        beli_barang(daftar_jam, pembeli, daftar_belanja)
                    elif pilihan == "3":
                        try:
                            jumlah_topup_epay = float(input("Masukkan jumlah top-up E-Pay: "))
                            top_up_epay(pembeli, jumlah_topup_epay)
                        except (ValueError, EOFError):
                            print("Masukkan jumlah top-up yang valid.")
                    elif pilihan == "4":
                        print(f"Saldo {pembeli['Nama']}: Rp {pembeli['Saldo']:,}")
                        print(f"Saldo E-Pay {pembeli['Nama']}: Rp {pembeli['E-Pay']:,}")
                    elif pilihan == "5":
                        print("Keluar dari menu pembeli.")
                        os.system('cls')
                        break
                    else:
                        print("Pilihan tidak valid. Silakan masukkan nomor yang benar.")
                if input("Apakah Anda ingin melakukan transaksi lagi? (ya/tidak): ").lower() != 'ya':
                    os.system('cls')
                    break
            else:
                print("Nama atau PIN tidak valid. Akun anda tidak terdaftar.")
        except (ValueError, EOFError):
            print("Input tidak valid. Silakan coba lagi.")
        except KeyboardInterrupt:
            print("\nSilakan coba lagi.")



def verifikasi_akun(daftar_pembeli, nama, pin):
    try:
        for pembeli in daftar_pembeli:
            if pembeli['Nama'].lower() == nama.lower() and pembeli['PIN'] == pin:
                return pembeli
        return None
    except (EOFError, AttributeError):
        print("Terjadi kesalahan saat verifikasi akun.")
    except KeyboardInterrupt:
        print("\nOperasi verifikasi dibatalkan.")

def verifikasi_admin(admin_data, username, password):
    try:
        return admin_data['Username'] == username and admin_data['Password'] == password
    except (EOFError, AttributeError):
        print("Terjadi kesalahan saat verifikasi admin.")
    except KeyboardInterrupt:
        print("\nverifikasi dibatalkan.")

if __name__ == "__main__":
    daftar_jam = [
        {'Nama': 'GMT Master II', 'Jenis': ' Jam Dewasa', 'Harga': 75000, 'Stok': 10},
        {'Nama': 'Lady Datejust', 'Jenis': 'Jam Dewasa', 'Harga': 95000, 'Stok': 10},
        {'Nama': 'Oyster Perpetual', 'Jenis': 'Jam Dewasa', 'Harga': 95000, 'Stok': 10},
        {'Nama': 'Day Date', 'Jenis': 'Jam Dewasa', 'Harga': 65000, 'Stok': 10},
        {'Nama': 'Yacht', 'Jenis': 'Jam Dewasa', 'Harga': 50000, 'Stok': 10},
        {'Nama': 'Air King', 'Jenis': 'Jam Dewasa', 'Harga': 50000, 'Stok': 10},
        {'Nama': 'Aries Gold Urban Eterenal', 'Jenis': 'Jam Dewasa', 'Harga': 98000, 'Stok': 10},
        {'Nama': 'Bonia Diamond', 'Jenis': 'Jam Dewasa', 'Harga': 73000, 'Stok': 10},
        {'Nama': 'Aigner Trieste', 'Jenis': 'Jam Dewasa', 'Harga': 430000, 'Stok': 10},
        {'Nama': 'Alexandre Christie Passion', 'Jenis': 'Jam Dewasa', 'Harga': 87000, 'Stok': 10},
        {'Nama': 'Fossil', 'Jenis': 'Jam Dewasa', 'Harga': 80000, 'Stok': 10},
        {'Nama': 'Fossil', 'Jenis': 'Jam anak cowok', 'Harga': 80000, 'Stok': 10},
        {'Nama': 'Orient', 'Jenis': 'Jam anak cowok', 'Harga': 60000, 'Stok': 10},
        {'Nama': 'Citizen', 'Jenis': 'Jam anak cowok', 'Harga': 75000, 'Stok': 10},
        {'Nama': 'Seiko', 'Jenis': 'Jam anak cowok', 'Harga': 40000, 'Stok': 10},
        {'Nama': ' Alexandre Christie', 'Jenis': 'Jam anak cowok', 'Harga': 87000, 'Stok': 10},
        {'Nama': 'Casio', 'Jenis': 'Jam anak cowok', 'Harga': 44000, 'Stok': 10},
        {'Nama': 'Alba', 'Jenis': 'Jam anak perempuan', 'Harga': 77000, 'Stok': 12},
        {'Nama': 'Daniel wellington', 'Jenis': 'Jam anak perempuan', 'Harga': 68000, 'Stok': 5},
        {'Nama': 'Jonas', 'Jenis': 'Jam anak perempuan', 'Harga': 79000, 'Stok': 8},
        {'Nama': 'Marc jacobs', 'Jenis': 'Jam anak perempuan', 'Harga': 86000, 'Stok': 15},
        {'Nama': 'olivia burton', 'Jenis': 'Jam anak perempuan', 'Harga': 95000, 'Stok': 20},
        {'Nama': 'Marvela', 'Jenis': 'Jam anak-anak', 'Harga': 25000, 'Stok': 10},
        {'Nama': 'Disney Mickey Mouse', 'Jenis': 'Jam anak-anak', 'Harga': 20000, 'Stok': 10},
        {'Nama': 'Teknobi', 'Jenis': 'Jam anak-anak', 'Harga': 20000, 'Stok': 10},
        {'Nama': 'Lasika', 'Jenis': 'Jam anak-anak', 'Harga': 30000, 'Stok': 10},
        {'Nama': 'imoo Watch Phone', 'Jenis': 'Jam anak-anak', 'Harga': 35000, 'Stok': 10},
        
    ]

    admin_data = {
        'Username': 'admin',
        'Password': '123'
    }

    daftar_pembeli = []
    
    if jam_toko():
        while True:
            try:
                print(GREEN +"|==========================================|")
                print(       "|      Selamat datang di toko Jam Asnan    |")
                print(       "|==========================================|")
                print(       "| 1. Admin                                 |")
                print(       "| 2. Registras                             |")   
                print(       "| 3. Pembeli                               |")
                print(       "| 4. Keluar                                |")
                print(       "|==========================================|")

                pilihan = int(input("Pilih Menu: "))
                os.system('cls')

                if pilihan == 1:
                    username = input("Masukkan username: ")
                    password = pwinput.pwinput("Masukkan password: ", mask='*')
                    if verifikasi_admin(admin_data, username, password):
                        print("Login berhasil.")
                        menu_admin(daftar_jam)
                    else:
                        print("Username atau password salah.")
                elif pilihan == 2:
                    registrasi_pembeli(daftar_pembeli)
                elif pilihan == 3:
                    menu_pembeli(daftar_jam, daftar_pembeli)
                elif pilihan == 4:
                    print("Terima kasih telah menggunakan sistem manajemen toko.")
                    break
                else:
                    print("Pilihan tidak valid. Silakan masukkan nomor yang benar.")
            except (ValueError, EOFError):
                print("Input tidak valid. Silakan coba lagi.")
            except KeyboardInterrupt:
                print("\nSilakan coba lagi.")
