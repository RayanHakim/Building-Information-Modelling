import tkinter as tk
from tkinter import ttk, messagebox
import math
import time
import multiprocessing as mp

class CivilEngine:
    def __init__(self, panjang, lebar, lantai, richter):
        self.panjang = panjang
        self.lebar = lebar
        self.lantai = lantai
        self.richter = richter
        self.tinggi_lantai = 3.5 
        
        if self.richter <= 4.0:
            self.zona_gempa = "Ringan"
            self.faktor_gempa = 1.0
        elif self.richter <= 6.5:
            self.zona_gempa = "Sedang"
            self.faktor_gempa = 1.25
        else:
            self.zona_gempa = "Tinggi"
            self.faktor_gempa = 1.5

    def hitung_struktur_aman(self):
        bentang_max = min(self.lebar, 4.0)
        tinggi_balok = math.ceil((bentang_max * 100) / 12) 
        lebar_balok = math.ceil(tinggi_balok * 0.5)
        
        tinggi_total = self.lantai * self.tinggi_lantai
        dimensi_kolom_dasar = math.ceil((tinggi_total * 2.5) + 15)
        
        dimensi_kolom = math.ceil(dimensi_kolom_dasar * self.faktor_gempa)
        
        luas_bangunan = self.panjang * self.lebar
        volume_plat = luas_bangunan * 0.12 
        berat_lantai_kg = volume_plat * 2400
        
        luas_penampang_kolom = dimensi_kolom * dimensi_kolom
        kapasitas_kolom_kg = luas_penampang_kolom * 200
        
        status_aman = "AMAN" if kapasitas_kolom_kg > (berat_lantai_kg / 4) else "TIDAK AMAN"

        # --- ESTIMASI JUMLAH STRUKTUR (BARU) ---
        # Asumsi kolom diletakkan per ~4 meter (termasuk pinggir)
        jumlah_kolom_x = math.ceil(self.panjang / 4) + 1
        jumlah_kolom_z = math.ceil(self.lebar / 4) + 1
        jumlah_kolom_per_lantai = jumlah_kolom_x * jumlah_kolom_z
        total_kolom = jumlah_kolom_per_lantai * self.lantai

        # Asumsi balok menghubungkan setiap kolom (grid)
        balok_x_per_lantai = (jumlah_kolom_x - 1) * jumlah_kolom_z
        balok_z_per_lantai = (jumlah_kolom_z - 1) * jumlah_kolom_x
        total_balok_per_lantai = balok_x_per_lantai + balok_z_per_lantai
        total_balok = total_balok_per_lantai * self.lantai

        return {
            "balok": f"{lebar_balok} x {tinggi_balok} cm",
            "kolom": f"{dimensi_kolom} x {dimensi_kolom} cm",
            "tebal_plat": "12 cm",
            "tinggi_total": f"{tinggi_total} m",
            "estimasi_berat_per_lantai": f"{berat_lantai_kg:,.0f} kg",
            "kapasitas_1_kolom": f"{kapasitas_kolom_kg:,.0f} kg",
            "status": status_aman,
            "zona": self.zona_gempa,
            "jml_kolom": total_kolom,
            "jml_balok": total_balok
        }


def jalankan_simulasi_3d(P, L, N, tinggi_lantai, dim_kolom_m, richter):
    import vpython as vp
    import math

    vp.scene.title = f"BIM Simulator - Visualisasi 3D ({N} Lantai, Richter {richter})"
    vp.scene.width = 900
    vp.scene.height = 600
    vp.scene.background = vp.color.gray(0.15)
    
    vp.scene.camera.pos = vp.vector(P * 1.5, N * 3.0, L * 2.0)
    vp.scene.camera.axis = vp.vector(-P * 1.5, -N * 2.5, -L * 2.0)

    # State untuk tombol interaktif
    run_gempa = False

    def toggle_gempa(b):
        nonlocal run_gempa
        run_gempa = not run_gempa
        b.text = "🛑 Hentikan Gempa" if run_gempa else "💥 Mulai Gempa"

    # Panel kontrol (Tombol putar dihapus)
    vp.scene.append_to_caption('\n🏗️ KONTROL SIMULASI:\n')
    vp.button(text="💥 Mulai Gempa", bind=toggle_gempa, color=vp.color.red)
    vp.scene.append_to_caption('\n\n💡 Tips Manual: Klik Kanan + Geser Mouse untuk memutar. Scroll untuk Zoom In/Out.')

    bangunan_parts = []
    jarak_x = P / max(1, math.ceil(P/4))
    jarak_z = L / max(1, math.ceil(L/4))

    tanah = vp.box(pos=vp.vector(P/2, -0.1, L/2), size=vp.vector(P+8, 0.2, L+8), color=vp.color.green)
    bangunan_parts.append(tanah)

    for lantai in range(N):
        tinggi_sekarang = lantai * tinggi_lantai
        
        x = 0.0
        while x <= P:
            z = 0.0
            while z <= L:
                k = vp.box(pos=vp.vector(x, tinggi_sekarang + (tinggi_lantai/2), z), 
                        size=vp.vector(dim_kolom_m, tinggi_lantai, dim_kolom_m), 
                        color=vp.color.orange)
                k.start_pos = vp.vector(k.pos.x, k.pos.y, k.pos.z) 
                bangunan_parts.append(k)
                z += jarak_z
            x += jarak_x
                
        if lantai > 0:
            plat = vp.box(pos=vp.vector(P/2, tinggi_sekarang, L/2), 
                       size=vp.vector(P, 0.12, L), color=vp.color.gray(0.6), opacity=0.85)
            plat.start_pos = vp.vector(plat.pos.x, plat.pos.y, plat.pos.z)
            bangunan_parts.append(plat)

        if lantai == N-1:
            atap = vp.pyramid(pos=vp.vector(P/2, tinggi_sekarang + tinggi_lantai + 1.5, L/2),
                           size=vp.vector(3, P+1, L+1), axis=vp.vector(0,1,0), color=vp.color.cyan)
            atap.start_pos = vp.vector(atap.pos.x, atap.pos.y, atap.pos.z)
            bangunan_parts.append(atap)

    intensitas_visual = (richter / 10.0) * 0.4
    waktu_berjalan = 0
    dt = 0.05 

    while True:
        vp.rate(30) 
        
        if run_gempa:
            waktu_berjalan += dt
            for part in bangunan_parts:
                if part == tanah: continue 
                sway_x = math.sin(waktu_berjalan * 15) * intensitas_visual * (part.pos.y / tinggi_lantai)
                part.pos.x = part.start_pos.x + sway_x
        else:
            waktu_berjalan = 0
            for part in bangunan_parts:
                if part != tanah and part.pos.x != part.start_pos.x:
                    part.pos.x = part.start_pos.x


class BIMSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BIM Simulator - Perhitungan & Simulasi Struktur")
        self.root.geometry("650x750")
        self.root.configure(bg="#f0f2f5")
        
        self.engine = None
        self.struktur = None

        self._build_gui()

    def _build_gui(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        header_label = tk.Label(self.root, text="BIM Structural Simulator", font=("Segoe UI", 16, "bold"), bg="#f0f2f5", fg="#333")
        header_label.pack(pady=15)

        input_frame = tk.LabelFrame(self.root, text=" Parameter Bangunan & Lingkungan ", font=("Segoe UI", 10, "bold"), bg="#f0f2f5", padx=20, pady=15)
        input_frame.pack(padx=25, pady=5, fill=tk.X)

        labels = ["Panjang Bangunan (meter):", "Lebar Bangunan (meter):", "Jumlah Lantai:", "Skala Gempa (Richter 1.0 - 9.0):"]
        defaults = ["10", "6", "3", "7.0"]
        self.entries = []

        for i, (text, default) in enumerate(zip(labels, defaults)):
            tk.Label(input_frame, text=text, bg="#f0f2f5", font=("Segoe UI", 10)).grid(row=i, column=0, sticky="w", pady=8)
            entry = ttk.Entry(input_frame, width=20, font=("Segoe UI", 10))
            entry.grid(row=i, column=1, pady=8, padx=10)
            entry.insert(0, default)
            self.entries.append(entry)

        self.entry_panjang, self.entry_lebar, self.entry_lantai, self.entry_richter = self.entries

        btn_hitung = tk.Button(input_frame, text="🧮 Hitung & Validasi Struktur", font=("Segoe UI", 10, "bold"), bg="#0d6efd", fg="white", relief="flat", command=self.hitung_data)
        btn_hitung.grid(row=4, column=0, columnspan=2, pady=20, ipady=5, sticky="ew")

        report_frame = tk.LabelFrame(self.root, text=" Laporan Hasil Perhitungan ", font=("Segoe UI", 10, "bold"), bg="#f0f2f5", padx=10, pady=10)
        report_frame.pack(padx=25, pady=10, fill=tk.BOTH, expand=True)

        # Laporan Text Area (diperbesar sedikit untuk menampung info baru)
        self.text_report = tk.Text(report_frame, height=14, state=tk.DISABLED, font=("Consolas", 10), bg="#ffffff", relief="flat")
        self.text_report.pack(fill=tk.BOTH, expand=True)

        self.btn_3d = tk.Button(self.root, text="🎬 Buka Visualisasi 3D & Simulasi", font=("Segoe UI", 12, "bold"), bg="#198754", fg="white", relief="flat", state=tk.DISABLED, command=self.mulai_simulasi_3d)
        self.btn_3d.pack(padx=25, pady=20, fill=tk.X, ipady=8)

    def hitung_data(self):
        try:
            p = float(self.entry_panjang.get())
            l = float(self.entry_lebar.get())
            n = int(self.entry_lantai.get())
            r = float(self.entry_richter.get())

            if p <= 0 or l <= 0 or n <= 0 or r <= 0:
                raise ValueError("Angka harus lebih dari 0.")

            self.engine = CivilEngine(p, l, n, r)
            self.struktur = self.engine.hitung_struktur_aman()

            laporan = f"--- DETAIL STRUKTUR (ZONA GEMPA: {self.struktur['zona'].upper()}) ---\n"
            laporan += f"Dimensi Kolom Utama : {self.struktur['kolom']}\n"
            laporan += f"Dimensi Balok Induk : {self.struktur['balok']}\n"
            laporan += f"Tebal Plat Lantai   : {self.struktur['tebal_plat']}\n"
            laporan += f"Tinggi Total Gedung : {self.struktur['tinggi_total']}\n\n"
            
            # Info Kuantitas Material
            laporan += f"--- ESTIMASI KUANTITAS STRUKTUR ---\n"
            laporan += f"Total Kolom (Tiang) : {self.struktur['jml_kolom']} buah\n"
            laporan += f"Total Balok (Induk) : {self.struktur['jml_balok']} buah\n\n"

            laporan += "--- VALIDASI BEBAN (SNI SEDERHANA) ---\n"
            laporan += f"Estimasi Berat/Lantai: {self.struktur['estimasi_berat_per_lantai']}\n"
            laporan += f"Kapasitas Tahan Kolom: {self.struktur['kapasitas_1_kolom']}\n"
            
            status = self.struktur['status']
            laporan += f"STATUS DESAIN        : {status}\n"

            self.text_report.config(state=tk.NORMAL)
            self.text_report.delete(1.0, tk.END)
            self.text_report.insert(tk.END, laporan)
            self.text_report.config(state=tk.DISABLED)

            self.btn_3d.config(state=tk.NORMAL)

        except ValueError as e:
            messagebox.showerror("Input Error", f"Pastikan semua input berisi angka yang valid!\nDetail: {e}")

    def mulai_simulasi_3d(self):
        dim_kolom_m = int(self.struktur['kolom'].split(' ')[0]) / 100 
        
        p = mp.Process(target=jalankan_simulasi_3d, args=(
            self.engine.panjang, 
            self.engine.lebar, 
            self.engine.lantai, 
            self.engine.tinggi_lantai, 
            dim_kolom_m, 
            self.engine.richter
        ))
        p.start()


if __name__ == "__main__":
    mp.freeze_support()
    root = tk.Tk()
    app = BIMSimulatorApp(root)
    root.mainloop()