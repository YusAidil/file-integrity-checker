"""
=============================================================
  FILE INTEGRITY CHECKER - MD5 & SHA-256
  Mata Kuliah: Keamanan Informasi
=============================================================
"""

import hashlib
import os
import json
import time
from datetime import datetime

# ─────────────────────────────────────────────
#  FUNGSI HASHING
# ─────────────────────────────────────────────

def compute_md5(filepath: str) -> str:
    """Menghitung hash MD5 dari sebuah file."""
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def compute_sha256(filepath: str) -> str:
    """Menghitung hash SHA-256 dari sebuah file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def get_file_info(filepath: str) -> dict:
    """Mengambil informasi lengkap dari file beserta nilai hash-nya."""
    stat = os.stat(filepath)
    return {
        "filename"    : os.path.basename(filepath),
        "filepath"    : os.path.abspath(filepath),
        "size_bytes"  : stat.st_size,
        "md5"         : compute_md5(filepath),
        "sha256"      : compute_sha256(filepath),
        "checked_at"  : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

# ─────────────────────────────────────────────
#  FUNGSI PERBANDINGAN
# ─────────────────────────────────────────────

def compare_files(info_original: dict, info_modified: dict) -> dict:
    """Membandingkan dua snapshot file dan melaporkan perubahan."""
    md5_changed    = info_original["md5"]    != info_modified["md5"]
    sha256_changed = info_original["sha256"] != info_modified["sha256"]
    size_changed   = info_original["size_bytes"] != info_modified["size_bytes"]

    return {
        "file_integrity_compromised" : md5_changed or sha256_changed,
        "md5_changed"                : md5_changed,
        "sha256_changed"             : sha256_changed,
        "size_changed"               : size_changed,
        "original_md5"               : info_original["md5"],
        "modified_md5"               : info_modified["md5"],
        "original_sha256"            : info_original["sha256"],
        "modified_sha256"            : info_modified["sha256"],
        "original_size"              : info_original["size_bytes"],
        "modified_size"              : info_modified["size_bytes"],
    }

# ─────────────────────────────────────────────
#  FUNGSI CETAK LOG
# ─────────────────────────────────────────────

SEP  = "=" * 65
SEP2 = "-" * 65

def print_file_info(label: str, info: dict):
    print(f"\n{'─'*65}")
    print(f"  📄  {label}")
    print(f"{'─'*65}")
    print(f"  Nama File   : {info['filename']}")
    print(f"  Ukuran      : {info['size_bytes']} bytes")
    print(f"  MD5         : {info['md5']}")
    print(f"  SHA-256     : {info['sha256']}")
    print(f"  Diperiksa   : {info['checked_at']}")

def print_comparison(result: dict):
    print(f"\n{SEP}")
    print("  🔍  HASIL PERBANDINGAN INTEGRITAS FILE")
    print(SEP)

    # MD5
    md5_status = "❌ BERUBAH" if result["md5_changed"] else "✅ SAMA"
    print(f"\n  MD5  [{md5_status}]")
    print(f"    Asli     : {result['original_md5']}")
    print(f"    Diubah   : {result['modified_md5']}")

    # SHA-256
    sha_status = "❌ BERUBAH" if result["sha256_changed"] else "✅ SAMA"
    print(f"\n  SHA-256  [{sha_status}]")
    print(f"    Asli     : {result['original_sha256']}")
    print(f"    Diubah   : {result['modified_sha256']}")

    # Ukuran
    size_status = "❌ BERUBAH" if result["size_changed"] else "✅ SAMA"
    print(f"\n  UKURAN FILE  [{size_status}]")
    print(f"    Asli     : {result['original_size']} bytes")
    print(f"    Diubah   : {result['modified_size']} bytes")

    # Verdict
    print(f"\n{SEP}")
    if result["file_integrity_compromised"]:
        print("  🚨  VERDICT : FILE TELAH DIMODIFIKASI — INTEGRITAS GAGAL!")
    else:
        print("  ✅  VERDICT : File aman, tidak ada perubahan terdeteksi.")
    print(SEP)

# ─────────────────────────────────────────────
#  DEMO / SIMULASI PENGUJIAN
# ─────────────────────────────────────────────

def run_simulation():
    print(f"\n{SEP}")
    print("  FILE INTEGRITY CHECKER — MD5 & SHA-256")
    print("  Tugas Keamanan Informasi")
    print(SEP)

    # ── Buat file asli ──────────────────────────────────────────
    original_path = "/home/claude/hash_project/dokumen_asli.txt"
    modified_path = "/home/claude/hash_project/dokumen_dimodifikasi.txt"

    original_content = (
        "Ini adalah dokumen rahasia perusahaan PT. Nusantara Jaya.\n"
        "Tanggal: 2024-06-01\n"
        "Isi kontrak: Pihak A setuju membayar Rp 500.000.000 kepada Pihak B\n"
        "sebagai kompensasi proyek pembangunan Gedung Serbaguna di Makassar.\n"
        "Kontrak berlaku selama 24 bulan terhitung sejak penandatanganan.\n"
        "Ditandatangani oleh: Direktur Utama & Wakil Direktur.\n"
    )

    modified_content = (
        "Ini adalah dokumen rahasia perusahaan PT. Nusantara Jaya.\n"
        "Tanggal: 2024-06-01\n"
        "Isi kontrak: Pihak A setuju membayar Rp 750.000.000 kepada Pihak B\n"   # <-- diubah!
        "sebagai kompensasi proyek pembangunan Gedung Serbaguna di Makassar.\n"
        "Kontrak berlaku selama 24 bulan terhitung sejak penandatanganan.\n"
        "Ditandatangani oleh: Direktur Utama & Wakil Direktur.\n"
    )

    with open(original_path, "w", encoding="utf-8") as f:
        f.write(original_content)

    with open(modified_path, "w", encoding="utf-8") as f:
        f.write(modified_content)

    # ── Hitung hash ─────────────────────────────────────────────
    print("\n[LANGKAH 1] Menghitung hash file ASLI...")
    info_original = get_file_info(original_path)
    print_file_info("FILE ASLI", info_original)

    print("\n[LANGKAH 2] Menghitung hash file YANG DIMODIFIKASI...")
    info_modified = get_file_info(modified_path)
    print_file_info("FILE DIMODIFIKASI", info_modified)

    # ── Perbandingan ────────────────────────────────────────────
    print("\n[LANGKAH 3] Membandingkan integritas kedua file...")
    result = compare_files(info_original, info_modified)
    print_comparison(result)

    # ── Test file tidak berubah ─────────────────────────────────
    print(f"\n\n{SEP}")
    print("  PENGUJIAN TAMBAHAN: File Asli vs Salinannya (Tidak Diubah)")
    print(SEP)

    copy_path = "/home/claude/hash_project/dokumen_salinan.txt"
    with open(copy_path, "w", encoding="utf-8") as f:
        f.write(original_content)

    info_copy = get_file_info(copy_path)
    result_same = compare_files(info_original, info_copy)
    print_file_info("SALINAN FILE (tidak diubah)", info_copy)
    print_comparison(result_same)

    # ── Simpan log JSON ─────────────────────────────────────────
    log = {
        "test_run"      : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "original"      : info_original,
        "modified"      : info_modified,
        "copy_identical": info_copy,
        "result_original_vs_modified" : result,
        "result_original_vs_copy"     : result_same,
    }
    log_path = "/home/claude/hash_project/integrity_log.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

    print(f"\n  📝  Log disimpan ke: {log_path}\n")
    return log

if __name__ == "__main__":
    run_simulation()
