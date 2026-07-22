"""
clear.py — очистка мусора
"""

import subprocess
import sys
import os

def run_task(system_info=None):
    print("=" * 60)
    print("           ВЫПОЛНЕНИЕ ЗАДАЧИ: ОЧИСТКА МУСОРА")
    print("=" * 60)
    print()

    is_windows = sys.platform.startswith("win")

    if is_windows:
        _clean_windows()
    else:
        _clean_linux()

    print()
    print("[+] Очистка мусора завершена.")
    print("=" * 60)
    print()


def _run(cmd, shell=True):
    try:
        print(f"[>] {cmd}")
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.stdout.strip():
            print(result.stdout.strip())
        if result.stderr.strip():
            if not is_windows_error_ignorable(result.stderr):
                print(f"[!] {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"[!] Ошибка: {e}")
        return False


def is_windows_error_ignorable(text):
    ignorable = ["не удается найти", "cannot find", "файл не найден", "not found"]
    return any(x.lower() in text.lower() for x in ignorable)


def _clean_linux():
    print("[+] Режим: Linux / Ubuntu\n")

    print("--- Удаление временных файлов ---")
    _run(r'find /tmp "$HOME/.cache" -type f \( -name "*.tmp" -o -name "*.temp" -o -name "*.bak" -o -name "*.swp" -o -name "*.log" -o -name "*.pyc" \) -delete 2>/dev/null')

    print("\n--- Очистка корзины ---")
    _run(r'rm -rf "$HOME/.local/share/Trash/files/"* "$HOME/.local/share/Trash/info/"* 2>/dev/null')


def _clean_windows():
    print("[+] Режим: Windows\n")

    print("--- Удаление временных файлов пользователя ---")
    _run(r'del /q /f /s "%TEMP%\*.tmp" 2>nul')
    _run(r'del /q /f /s "%TEMP%\*.log" 2>nul')
    _run(r'del /q /f /s "%TEMP%\*.bak" 2>nul')
    _run(r'del /q /f /s "%TMP%\*.tmp" 2>nul')

    print("\n--- Очистка Prefetch ---")
    _run(r'del /q /f /s "%SystemRoot%\Prefetch\*.pf" 2>nul')

    print("\n--- Поиск и удаление __pycache__ ---")
    _run(r'for /d /r "%USERPROFILE%" %d in (__pycache__) do @if exist "%d" rd /s /q "%d" 2>nul')

    print("\n--- Очистка корзины ---")
    _run(r'rd /s /q %systemdrive%\$Recycle.Bin 2>nul')


if __name__ == "__main__":
    run_task()