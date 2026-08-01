# DokPDF

Kelola PDF jadi mudah. Aplikasi web untuk konversi, penggabungan, dan pemrosesan dokumen PDF.

## Fitur

- **Konversi Dokumen**: Konversi Word (docx), Excel (xlsx), PowerPoint (pptx), dan Gambar (jpg, png) ke PDF.
- **Merge PDF**: Gabungkan beberapa file PDF menjadi satu.
- **Split PDF**: Pecah halaman PDF menjadi file terpisah.
- **Antarmuka Modern**: UI bersih dan responsif menggunakan Tailwind CSS.
- **Docker Ready**: Deployment mudah dengan Docker dan Docker Compose.

## Teknologi

- **Backend**: Flask (Python)
- **Frontend**: Vanilla JS, HTML, CSS (Tailwind)
- **Server**: Nginx
- **Processing**: PyPDF2, ReportLab, pdf2image, img2pdf

## Cara Menjalankan

### Menggunakan Docker (Rekomendasi)

Pastikan Docker dan Docker Compose sudah terpasang.

```bash
# Clone repository
git clone https://github.com/gylangsatria/DokPDF.git
cd DokPDF

# Jalankan aplikasi
make up
```

Akses:
- Frontend: `http://localhost:8080`
- API: `http://localhost:5000`

### Lokal (Development)

1. **Install dependensi API**:
   ```bash
   cd api
   pip install -r requirements.txt
   ```

2. **Jalankan Flask**:
   ```bash
   python app.py
   ```

3. **Buka `index.html`** langsung atau lewat server statis.

## Perintah Makefile

- `make build`: Build Docker image.
- `make up`: Jalankan container.
- `make down`: Hentikan container.
- `make logs`: Lihat log container.
- `make clean`: Hapus container dan file sampah.
- `make test`: Cek kesehatan API.

## Struktur Proyek

- `api/`: Kode sumber backend Flask.
- `static/`: File statis frontend (JS, CSS).
- `index.html`: Halaman utama.
- `docker-compose.yml`: Konfigurasi orchestrasi container.
- `nginx.conf`: Konfigurasi reverse proxy.

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).
