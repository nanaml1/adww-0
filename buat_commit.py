import os
import datetime
import json # Tambahkan modul json

def buat_commit_mundur(tahun: int, bulan: int, total_commit: int, jumlah_hari: int):
    """
    Fungsi ini tetap sama, tugasnya menjalankan logika pembuatan commit
    berdasarkan parameter yang diterima.
    """
    try:
        tanggal_mulai = datetime.datetime(tahun, bulan, 1, 10, 0, 0)
    except ValueError as e:
        print(f"Error: Tanggal tidak valid - {e}")
        return

    print(f"Membaca konfigurasi: Membuat {total_commit} commit dalam {jumlah_hari} hari.")
    
    commit_per_hari = total_commit // jumlah_hari
    sisa_commit = total_commit % jumlah_hari

    commit_counter = 0
    for i in range(jumlah_hari):
        tanggal_dasar_hari_ini = tanggal_mulai + datetime.timedelta(days=i)
        jumlah_commit_hari_ini = commit_per_hari + (1 if i < sisa_commit else 0)
        
        print(f"\n--- Hari ke-{i+1} ({tanggal_dasar_hari_ini.strftime('%Y-%m-%d')}): Membuat {jumlah_commit_hari_ini} commit ---")

        for j in range(jumlah_commit_hari_ini):
            commit_counter += 1
            waktu_commit = tanggal_dasar_hari_ini + datetime.timedelta(minutes=j * 15)
            tanggal_str = waktu_commit.strftime('%Y-%m-%d %H:%M:%S')

            with open('data.txt', 'a') as file:
                file.write(f'Commit #{commit_counter} pada {tanggal_str}\n')

            os.system('git add data.txt')

            pesan_commit = f"feat: auto-commit #{commit_counter} on {waktu_commit.date()}"
            command_commit = f'git commit --date="{tanggal_str}" -m "{pesan_commit}"'
            
            os.system(command_commit)
            print(f"  > Commit #{commit_counter} berhasil dibuat pada {tanggal_str}")

    print("\nSemua commit berhasil dibuat. Melakukan push ke remote...")
    os.system('git push')
    print("Selesai!")

# --------------------------------------------------------------------
# --- BAGIAN UTAMA: MEMBACA KONFIGURASI DARI JSON ---
# --------------------------------------------------------------------
if __name__ == "__main__":
    nama_file_config = 'config.json'
    
    try:
        with open(nama_file_config, 'r') as file:
            config = json.load(file)

        # Ambil nilai dari file JSON
        TAHUN_AWAL = config['year']
        BULAN_AWAL = config['month']
        TOTAL_COMMIT = config['total_commits']
        JUMLAH_HARI = config['duration_days']
        
        # Panggil fungsi dengan konfigurasi yang sudah dibaca
        buat_commit_mundur(TAHUN_AWAL, BULAN_AWAL, TOTAL_COMMIT, JUMLAH_HARI)

    except FileNotFoundError:
        print(f"Error: File konfigurasi '{nama_file_config}' tidak ditemukan.")
    except KeyError as e:
        print(f"Error: Kunci (key) '{e}' tidak ditemukan di dalam file {nama_file_config}.")
    except json.JSONDecodeError:
        print(f"Error: Format file {nama_file_config} tidak valid. Pastikan format JSON sudah benar.")