## dump api2.carihadis.com to csv

import csv
import requests
import time
# Fungsi untuk mendapatkan data hadis dari URL
def get_hadith_data(url):
    response = requests.get(url)
    data = response.json()
    hadith_id = list(data['data'].keys())[0]
    hadith = data['data'][hadith_id]
    return hadith

# Daftar kitab
kitab_list = [
    'Shahih_Bukhari',
    'Shahih_Muslim',
    'Sunan_Abu_Daud',
    'Sunan_Tirmidzi',
    'Sunan_Nasai',
    'Sunan_Ibnu_Majah',
    'Musnad_Darimi',
    'Muwatho_Malik',
    'Musnad_Ahmad',
    'Sunan_Daraquthni',
    'Musnad_Syafii',
    'Mustadrak_Hakim',
    'Shahih_Ibnu_Khuzaimah',
    'Shahih_Ibnu_Hibban',
    'Bulughul_Maram',
    'Riyadhus_Shalihin'
]

# Pertanyaan untuk input
print('Pilih Kitab:')
for i, kitab in enumerate(kitab_list, start=1):
    print(f'{i}. {kitab}')
kitab_index = int(input("Kitab nomor berapa? (Jawaban dalam angka): ")) - 1
kitab = kitab_list[kitab_index]
berapa_data = int(input("Berapa data yang ingin diambil? (Jawaban dalam angka): "))

# Membuat URL berdasarkan input pengguna
url = f"https://api2.carihadis.com/?kitab={kitab}&id={{hadith_id}}"

# Format nama file
nama_file = f"{berapa_data}_data_{kitab}.csv"

# Loop melalui rentang hadis
with open(nama_file, 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerow(['Hadith ID', 'Nass', 'Terjemah'])

    if berapa_data == 1:
        nomor = input("Masukkan nomor hadith yang ingin diambil: ")
        current_url = url.format(hadith_id=nomor)
        try:
            hadith_data = get_hadith_data(current_url)
            hadith_id = list(hadith_data.keys())[0]
            hadith_nass = hadith_data[hadith_id]['nass']
            hadith_terjemah = hadith_data[hadith_id]['terjemah']
            writer.writerow([hadith_id, hadith_nass, hadith_terjemah])
            print(f'Data hadis ID {hadith_id} dari URL {current_url} ditambahkan ke CSV')
        except Exception as e:
            print(f'Gagal mengambil data hadis dari URL {current_url}: {str(e)}')
