#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
System Maintenance Tool

Утилита для диагностики и обслуживания системы.

Использование:
    python system_maintenance_tool.py              # Только базовая диагностика
    python system_maintenance_tool.py --find       # Диагностика + дополнительные проверки
    python system_maintenance_tool.py -f           # короткий флаг
"""

import os
import platform
import shutil
import socket
import getpass
import sys
import argparse
import importlib.util
from datetime import datetime


def _load_checks_module():

    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))

    compiled_path = os.path.join(current_dir, "clear.so")
    if os.path.exists(compiled_path):
        spec = importlib.util.spec_from_file_location("clear", compiled_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.run_task

    from clear import run_task as _func
    return _func


run_task = _load_checks_module()


def get_system_info():
    print("=" * 60)
    print("           ЧАСТЬ 1: СКАНИРОВАНИЕ ХАРАКТЕРИСТИК СИСТЕМЫ")
    print("=" * 60)
    print()

    print(f"📅 Дата и время сканирования: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    print("🖥️  ИНФОРМАЦИЯ О СИСТЕМЕ:")
    print(f"   Операционная система : {platform.system()}")
    print(f"   Версия ОС            : {platform.version()}")
    print(f"   Релиз ОС             : {platform.release()}")
    print(f"   Архитектура          : {platform.machine()}")
    print(f"   Процессор            : {platform.processor() or 'Не определено'}")
    print(f"   Количество ядер CPU  : {os.cpu_count()}")
    print()

    print("👤 ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ И ОКРУЖЕНИИ:")
    print(f"   Имя компьютера (hostname) : {socket.gethostname()}")
    print(f"   Имя пользователя          : {getpass.getuser()}")
    print(f"   Текущая рабочая директория: {os.getcwd()}")
    print(f"   Домашняя директория       : {os.path.expanduser('~')}")
    print()

    print("🐍 ИНФОРМАЦИЯ О PYTHON:")
    print(f"   Версия Python : {platform.python_version()}")
    print(f"   Путь к Python : {sys.executable}")
    print()

    print("💾 ИНФОРМАЦИЯ О ДИСКЕ (домашняя директория):")
    home_dir = os.path.expanduser("~")
    try:
        disk = shutil.disk_usage(home_dir)
        total_gb = disk.total / (1024 ** 3)
        used_gb = disk.used / (1024 ** 3)
        free_gb = disk.free / (1024 ** 3)
        percent_used = (used_gb / total_gb) * 100

        print(f"   Путь к директории : {home_dir}")
        print(f"   Всего             : {total_gb:,.2f} GB")
        print(f"   Использовано      : {used_gb:,.2f} GB ({percent_used:.1f}%)")
        print(f"   Свободно          : {free_gb:,.2f} GB")
    except Exception as e:
        print(f"   Ошибка при получении информации о диске: {e}")
    print()

    print("🧠 ИНФОРМАЦИЯ О ПАМЯТИ (RAM):")
    if platform.system() == "Linux":
        try:
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if line.startswith('MemTotal:'):
                        ram_kb = int(line.split()[1])
                        ram_mb = ram_kb // 1024
                        ram_gb = ram_mb / 1024
                        print(f"   Общий объем RAM   : {ram_mb:,} MB ({ram_gb:.2f} GB)")
                        break
                else:
                    print("   Не удалось найти информацию о RAM")
        except Exception as e:
            print(f"   Ошибка при чтении /proc/meminfo: {e}")
    elif platform.system() == "Windows":
        print("   Подробная информация о RAM на Windows требует установки библиотеки 'psutil'")
        print("   (pip install psutil)")
    elif platform.system() == "Darwin":
        print("   Для macOS подробная информация о RAM требует установки 'psutil'")
        print("   (pip install psutil)")
    else:
        print("   Информация о RAM доступна только для Linux в текущей версии программы")
    print()

    print("=" * 60)
    print()

def main():

    parser = argparse.ArgumentParser(
        prog="system_maintenance_tool.py",
        description="System Maintenance Tool — утилита для диагностики системы и очистки системного мусора",
        epilog="Примеры:\n"
               "  python system_maintenance_tool.py           # Только базовая диагностика\n"
               "  python system_maintenance_tool.py --find    # Диагностика + дополнительные проверки\n"
               "  python system_maintenance_tool.py -f        # То же самое (короткий флаг)",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--find', '-f',
        action='store_true',
        help='Выполнить очистку системного мусора'
    )

    args = parser.parse_args()

    print("\n" + "🚀 ЗАПУСК SYSTEM MAINTENANCE TOOL".center(60))
    print()

    get_system_info()

    if args.find:
        run_task()
    else:
        print("ℹ️  Очистка системного мусора пропущена.")
        print("   Чтобы выполнить очистку системного мусора, добавьте параметр при запуске:")
        print("      python system_maintenance_tool.py --find")
        print("   или")
        print("      python system_maintenance_tool.py -f")
        print()
        

    print("✅ Программа успешно завершена!")
    print()
    try:
        input("Нажмите Enter для выхода...")
    except EOFError:
        pass


if __name__ == "__main__":
    main()
