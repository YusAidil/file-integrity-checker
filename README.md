# 🛡️ File Integrity Checker

Aplikasi pengecekan integritas file menggunakan algoritma hash kriptografi **MD5** dan **SHA-256**.

> Tugas Mata Kuliah: Keamanan Informasi

---

## 📋 Deskripsi

Program ini dibuat untuk memverifikasi keaslian dan integritas file dengan cara menghitung nilai hash (MD5 dan SHA-256) dari sebuah file, kemudian membandingkannya untuk mendeteksi apakah file telah mengalami modifikasi.

---

## 📁 Struktur File

```
file-integrity-checker/
├── file_integrity_checker.py   # Source code utama (Python)
├── FileIntegrityChecker.html   # Aplikasi web interaktif (bonus)
├── integrity_log.json          # Log hasil pengujian
├── laporan_analisis.md         # Laporan analisis lengkap
└── README.md                   # Dokumentasi ini
```

---

## 🚀 Cara Menjalankan

### Program Python
```bash
python file_integrity_checker.py
```

### Aplikasi Web
Buka file `FileIntegrityChecker.html` langsung di browser (Chrome/Firefox/Edge).  
Tidak perlu install apapun — semua proses terjadi di browser.

---

## ⚙️ Fitur Program

| Fitur | Status |
|-------|--------|
| Hitung hash MD5 | ✅ |
| Hitung hash SHA-256 | ✅ |
| Deteksi perubahan file | ✅ |
| Simpan log JSON | ✅ |
| Antarmuka web (drag & drop) | ✅ |

---

## 🧪 Hasil Pengujian

### Skenario A — File Dimodifikasi
- File asli vs file yang diubah satu angka (Rp 500jt → Rp 750jt)
- Ukuran file **tetap sama** (332 bytes)
- Hasil: **MD5 dan SHA-256 keduanya berubah total** → Integritas GAGAL ✅

### Skenario B — File Identik
- File asli vs salinan identik
- Hasil: **Semua hash identik** → Integritas Terjaga ✅

---

## 🔐 Analisis Singkat

| | MD5 | SHA-256 |
|---|---|---|
| Output | 128-bit | 256-bit |
| Collision ditemukan | ✅ Ya (2004) | ❌ Belum ada |
| Rekomendasi keamanan | ❌ Tidak | ✅ Ya |
| Dipakai TLS/Bitcoin | ❌ | ✅ |

**MD5** sudah tidak aman untuk tujuan keamanan sejak 2004 (collision attack terbukti).  
**SHA-256** adalah standar NIST yang direkomendasikan untuk verifikasi integritas.

---

## 📚 Teknologi

- Python 3 (library standar: `hashlib`, `os`, `json`)
- HTML5 + CSS3 + Vanilla JavaScript
- Web Crypto API (SHA-256 browser-native)
