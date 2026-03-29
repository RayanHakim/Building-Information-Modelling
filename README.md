🏗️ BIM Structural Simulator & Earthquake Analyzer

BIM Structural Simulator adalah aplikasi berbasis Python yang menggabungkan logika teknik sipil, perhitungan struktur otomatis (mengacu pada pendekatan sederhana standar SNI), serta visualisasi 3D interaktif.

Aplikasi ini memungkinkan pengguna untuk merancang dimensi bangunan dan menguji ketahanannya terhadap simulasi gempa secara real-time.

🌟 Fitur Utama
🔹 Automatic Structural Calculation

Menghitung dimensi:

Kolom
Balok
Tebal plat lantai

secara otomatis berdasarkan luas bangunan dan jumlah lantai.

🔹 Safety Validation

Melakukan validasi beban struktur (berat beton) terhadap kapasitas kolom menggunakan pendekatan standar SNI sederhana.

🔹 Bill of Quantity (BQ) Estimator

Menyediakan estimasi kebutuhan material:

Total titik kolom
Total balok
🔹 Seismic Simulation

Simulasi gempa interaktif dengan:

Skala Richter (1.0 – 9.0)
Efek defleksi realistis
Lantai atas bergoyang lebih besar (sesuai prinsip fisika struktur)
🔹 Interactive 3D View

Visualisasi 3D menggunakan VPython:

Rotasi kamera
Zoom in / zoom out
Tampilan struktur bangunan secara real-time
🛠️ Persyaratan Sistem & Library

Aplikasi ini dikembangkan menggunakan:

Python 3.13

Install dependency utama:

pip install vpython

⚠️ Note:
Aplikasi menggunakan multiprocessing dan threading agar GUI tetap responsif saat rendering 3D berjalan.

🚀 Cara Penggunaan
1. Clone Repository
git clone https://github.com/username-kamu/bim-structural-simulator.git
2. Masuk ke Folder Project
cd bim-structural-simulator
3. Jalankan Aplikasi
python bim_simulator.py
4. Cara Menggunakan Aplikasi
Masukkan parameter:
Panjang bangunan
Lebar bangunan
Jumlah lantai
Skala Richter
Klik Hitung & Validasi
→ untuk melihat laporan teknis struktur
Klik Buka Visualisasi 3D
→ untuk melihat model bangunan dan simulasi gempa
📐 Logika Perhitungan (Civil Engineering Logic)

Proyek ini menggunakan beberapa pendekatan teknik sipil:

🔸 Dimensi Balok

Menggunakan rasio:

1
12
×
bentang maksimum
12
1
	​

×bentang maksimum
🔸 Dimensi Kolom

Ditentukan berdasarkan:

Beban akumulatif tiap lantai
Faktor pengali zona gempa
🔸 Gaya Gempa (Simulasi Visual)

Menggunakan fungsi sinusoidal:

𝐴
⋅
sin
⁡
(
𝜔
𝑡
)
A⋅sin(ωt)

Keterangan:

𝐴
A (amplitudo) ∝ tinggi struktur (
𝑦
y)
Semakin tinggi lantai → semakin besar simpangan
🎯 Tujuan Proyek
Menggabungkan konsep BIM sederhana + simulasi fisika
Membantu pembelajaran teknik sipil secara visual & interaktif
Menjadi prototype tools analisis struktur berbasis Python
