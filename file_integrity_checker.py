"""
=============================================================
  FILE INTEGRITY CHECKER - MD5 & SHA-256
=============================================================
"""

import hashlib
import os
import json
from datetime import datetime

# ─────────────────────────────────────────────
#  FUNGSI HASHING
# ─────────────────────────────────────────────

def compute_md5(filepath: str) -> str:
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def compute_sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def get_file_info(filepath: str) -> dict:
    stat = os.stat(filepath)
    return {
        "filename"   : os.path.basename(filepath),
        "filepath"   : os.path.abspath(filepath),
        "size_bytes" : stat.st_size,
        "md5"        : compute_md5(filepath),
        "sha256"     : compute_sha256(filepath),
        "checked_at" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

# ─────────────────────────────────────────────
#  FUNGSI PERBANDINGAN
# ─────────────────────────────────────────────

def compare_files(info_original: dict, info_modified: dict) -> dict:
    md5_changed    = info_original["md5"]        != info_modified["md5"]
    sha256_changed = info_original["sha256"]     != info_modified["sha256"]
    size_changed   = info_original["size_bytes"] != info_modified["size_bytes"]
    return {
        "file_integrity_compromised": md5_changed or sha256_changed,
        "md5_changed"               : md5_changed,
        "sha256_changed"            : sha256_changed,
        "size_changed"              : size_changed,
        "original_md5"              : info_original["md5"],
        "modified_md5"              : info_modified["md5"],
        "original_sha256"           : info_original["sha256"],
        "modified_sha256"           : info_modified["sha256"],
        "original_size"             : info_original["size_bytes"],
        "modified_size"             : info_modified["size_bytes"],
    }

# ─────────────────────────────────────────────
#  FUNGSI CETAK
# ─────────────────────────────────────────────

SEP = "=" * 65

def print_file_info(label, info):
    print(f"\n{'─'*65}")
    print(f"  {label}")
    print(f"{'─'*65}")
    print(f"  Nama File  : {info['filename']}")
    print(f"  Ukuran     : {info['size_bytes']} bytes")
    print(f"  MD5        : {info['md5']}")
    print(f"  SHA-256    : {info['sha256']}")
    print(f"  Diperiksa  : {info['checked_at']}")

def print_comparison(result):
    print(f"\n{SEP}")
    print("  HASIL PERBANDINGAN INTEGRITAS FILE")
    print(SEP)

    md5_status = "BERUBAH" if result["md5_changed"] else "SAMA"
    print(f"\n  MD5  [{md5_status}]")
    print(f"    Asli   : {result['original_md5']}")
    print(f"    Baru   : {result['modified_md5']}")

    sha_status = "BERUBAH" if result["sha256_changed"] else "SAMA"
    print(f"\n  SHA-256  [{sha_status}]")
    print(f"    Asli   : {result['original_sha256']}")
    print(f"    Baru   : {result['modified_sha256']}")

    size_status = "BERUBAH" if result["size_changed"] else "SAMA"
    print(f"\n  UKURAN  [{size_status}]")
    print(f"    Asli   : {result['original_size']} bytes")
    print(f"    Baru   : {result['modified_size']} bytes")

    print(f"\n{SEP}")
    if result["file_integrity_compromised"]:
        print("  VERDICT : FILE TELAH DIMODIFIKASI — INTEGRITAS GAGAL!")
    else:
        print("  VERDICT : File aman, tidak ada perubahan terdeteksi.")
    print(SEP)

# ─────────────────────────────────────────────
#  SIMULASI
# ─────────────────────────────────────────────

def run_simulation():
    # Folder yang sama dengan lokasi file Python ini
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    original_path = os.path.join(BASE_DIR, "kontrak_asli.txt")
    modified_path = os.path.join(BASE_DIR, "kontrak_dimodifikasi.txt")
    copy_path     = os.path.join(BASE_DIR, "kontrak_salinan.txt")

    print(f"\n{SEP}")
    print("  FILE INTEGRITY CHECKER — MD5 & SHA-256")
    print(SEP)

    # Cek apakah file uji tersedia
    if not os.path.exists(original_path):
        print(f"\n  ERROR: File '{original_path}' tidak ditemukan!")
        print("  Pastikan file kontrak_asli.txt ada di folder yang sama.")
        return
    if not os.path.exists(modified_path):
        print(f"\n  ERROR: File '{modified_path}' tidak ditemukan!")
        print("  Pastikan file kontrak_dimodifikasi.txt ada di folder yang sama.")
        return

    # Buat salinan identik otomatis
    with open(original_path, "r", encoding="utf-8") as f:
        isi_asli = f.read()
    with open(copy_path, "w", encoding="utf-8") as f:
        f.write(isi_asli)

    # ── Skenario A: Asli vs Dimodifikasi ──
    print("\n[SKENARIO A] File Asli vs File Dimodifikasi")
    print("[LANGKAH 1] Menghitung hash file ASLI...")
    info_original = get_file_info(original_path)
    print_file_info("FILE ASLI", info_original)

    print("\n[LANGKAH 2] Menghitung hash file DIMODIFIKASI...")
    info_modified = get_file_info(modified_path)
    print_file_info("FILE DIMODIFIKASI", info_modified)

    print("\n[LANGKAH 3] Membandingkan...")
    result_a = compare_files(info_original, info_modified)
    print_comparison(result_a)

    # ── Skenario B: Asli vs Salinan Identik ──
    print(f"\n\n{SEP}")
    print("[SKENARIO B] File Asli vs Salinan Identik")
    print(SEP)
    info_copy = get_file_info(copy_path)
    print_file_info("SALINAN IDENTIK", info_copy)
    result_b = compare_files(info_original, info_copy)
    print_comparison(result_b)

    # ── Simpan log ──
    log = {
        "test_run" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "skenario_A": {
            "original" : info_original,
            "modified" : info_modified,
            "result"   : result_a,
        },
        "skenario_B": {
            "original" : info_original,
            "copy"     : info_copy,
            "result"   : result_b,
        },
    }
    log_path = os.path.join(BASE_DIR, "integrity_log.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

    print(f"\n  Log disimpan ke: {log_path}\n")

if __name__ == "__main__":
    run_simulation()
