import heapq

# ==========================================
# 1. DATA GRAF (PETA JAWA TIMUR)
# Berdasarkan sisi/edge dan jarak aslinya
# ==========================================
graph = {
    'Magetan': {'Ngawi': 32, 'Madiun': 22, 'Ponorogo': 34},
    'Ngawi': {'Magetan': 32, 'Madiun': 30, 'Bojonegoro': 44},
    'Ponorogo': {'Magetan': 34, 'Madiun': 29},
    'Madiun': {'Magetan': 22, 'Ngawi': 30, 'Ponorogo': 29, 'Nganjuk': 48},
    'Bojonegoro': {'Ngawi': 44, 'Nganjuk': 33, 'Lamongan': 42, 'Jombang': 70},
    'Nganjuk': {'Madiun': 48, 'Bojonegoro': 33, 'Jombang': 40},
    'Lamongan': {'Bojonegoro': 42, 'Gresik': 14},
    'Jombang': {'Bojonegoro': 70, 'Nganjuk': 40, 'Surabaya': 72},
    'Gresik': {'Lamongan': 14, 'Surabaya': 12},
    'Surabaya': {'Gresik': 12, 'Jombang': 72, 'Bangkalan': 44, 'Sidoarjo': 25},
    'Bangkalan': {'Surabaya': 44, 'Sampang': 52},
    'Sampang': {'Bangkalan': 52, 'Pamekasan': 31},
    'Pamekasan': {'Sampang': 31, 'Sumenep': 54},
    'Sumenep': {'Pamekasan': 54},
    'Sidoarjo': {'Surabaya': 25, 'Probolinggo': 78},
    'Probolinggo': {'Sidoarjo': 78, 'Situbondo': 99},
    'Situbondo': {'Probolinggo': 99}
}

# ==========================================
# 2. DATA HEURISTIK (h(n))
# Jarak Garis Lurus ke SURABAYA
# ==========================================
heuristik_ke_surabaya = {
    'Magetan': 162, 'Surabaya': 0, 'Ngawi': 130, 'Ponorogo': 128,
    'Madiun': 126, 'Bojonegoro': 60, 'Nganjuk': 70, 'Jombang': 36,
    'Lamongan': 36, 'Gresik': 12, 'Sidoarjo': 22, 'Probolinggo': 70,
    'Situbondo': 146, 'Bangkalan': 140, 'Sampang': 90, 'Pamekasan': 104,
    'Sumenep': 150
}

def get_heuristik(kota, tujuan):
    """
    Mengambil nilai heuristik.
    Jika tujuan bukan Surabaya, heuristik dikembalikan 0 agar program tetap
    bisa berjalan mencari rute untuk semua case secara general.
    """
    if tujuan.capitalize() == 'Surabaya':
        return heuristik_ke_surabaya.get(kota, 0)
    return 0

# ==========================================
# 3. ALGORITMA GREEDY BEST-FIRST SEARCH
# Evaluasi murni berdasarkan h(n) terkecil
# ==========================================
def greedy_bfs(awal, tujuan):
    # Struktur antrean: (nilai_h, nama_kota, histori_rute, total_jarak_sementara)
    queue = [(get_heuristik(awal, tujuan), awal, [awal], 0)]
    dikunjungi = set()

    while queue:
        # Selalu pop node dengan nilai heuristik h(n) terkecil
        h_score, current, path, current_cost = heapq.heappop(queue)

        if current == tujuan:
            return path, current_cost

        if current not in dikunjungi:
            dikunjungi.add(current)
            for neighbor, jarak in graph[current].items():
                if neighbor not in dikunjungi:
                    new_cost = current_cost + jarak
                    h_val = get_heuristik(neighbor, tujuan)
                    heapq.heappush(queue, (h_val, neighbor, path + [neighbor], new_cost))
                    
    return None, 0

# ==========================================
# 4. ALGORITMA A* (A-STAR)
# Evaluasi berdasarkan f(n) = g(n) + h(n)
# ==========================================
def a_star(awal, tujuan):
    # Struktur antrean: (nilai_f, nama_kota, histori_rute, nilai_g)
    g_awal = 0
    f_awal = g_awal + get_heuristik(awal, tujuan)
    queue = [(f_awal, awal, [awal], g_awal)]
    
    # Menyimpan cost g(n) termurah ke setiap node
    g_costs = {awal: 0}

    while queue:
        # Selalu pop node dengan nilai f(n) terkecil
        f_score, current, path, g_score = heapq.heappop(queue)

        if current == tujuan:
            return path, g_score

        for neighbor, jarak in graph[current].items():
            new_g = g_score + jarak
            
            # Update rute jika menemukan jalan yang g(n) nya lebih murah
            if neighbor not in g_costs or new_g < g_costs[neighbor]:
                g_costs[neighbor] = new_g
                new_f = new_g + get_heuristik(neighbor, tujuan)
                heapq.heappush(queue, (new_f, neighbor, path + [neighbor], new_g))
                
    return None, 0

# ==========================================
# 5. ANTARMUKA (USER INTERFACE CLI)
# ==========================================
def main():
    while True:
        print("\n" + "="*50)
        print("  PROGRAM PENCARIAN RUTE PETA JAWA TIMUR  ")
        print("="*50)
        print("Daftar Kota Tersedia:")
        print(", ".join(graph.keys()))
        print("-" * 50)
        
        kota_awal = input("Masukkan Kota Asal\t: ").strip().capitalize()
        kota_tujuan = input("Masukkan Kota Tujuan\t: ").strip().capitalize()
        
        # Validasi Input
        if kota_awal not in graph or kota_tujuan not in graph:
            print("\n[!] ERROR: Kota asal atau tujuan tidak ditemukan di peta.")
            print("Silakan cek kembali ejaan kota Anda.")
            continue
            
        print("\nPilih Algoritma Pencarian:")
        print("1. Greedy Best-First Search")
        print("2. A* (A-Star)")
        choice = input("Masukkan Pilihan (1/2)\t: ").strip()
        
        path, cost = None, 0
        algo_name = ""
        
        if choice == '1':
            path, cost = greedy_bfs(kota_awal, kota_tujuan)
            algo_name = "Greedy Best-First Search"
        elif choice == '2':
            path, cost = a_star(kota_awal, kota_tujuan)
            algo_name = "A* (A-Star)"
        else:
            print("\n[!] ERROR: Pilihan algoritma tidak valid.")
            continue
            
        # Menampilkan Hasil
        if path:
            print("\n" + "*"*50)
            print(f"HASIL PENCARIAN ({algo_name})")
            print("*"*50)
            print(f"Kota Asal    : {kota_awal}")
            print(f"Kota Tujuan  : {kota_tujuan}")
            print(f"Rute Perjalanan: \n{' -> '.join(path)}")
            print(f"Total Cost   : {cost}")
            print("*"*50)
        else:
            print("\n[!] Rute tidak ditemukan.")
            
        # Opsi Lanjut/Keluar
        again = input("\nIngin mencari rute lain? (y/n): ").strip().lower()
        if again != 'y':
            print("Terima kasih telah menggunakan program ini!")
            break

if __name__ == "__main__":
    main()