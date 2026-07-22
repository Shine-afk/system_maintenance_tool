#!/bin/bash
#
# Скрипт сборки core.so для Ubuntu
# Использует виртуальное окружение
#

set -e

echo "=== Сборка System Maintenance Tool ==="
echo

PYTHON=python3

if ! command -v $PYTHON &> /dev/null; then
    echo "Ошибка: python3 не найден."
    exit 1
fi

VENV_DIR=".build_venv"

echo "Создаём временное виртуальное окружение..."
$PYTHON -m venv "$VENV_DIR"

source "$VENV_DIR/bin/activate"

echo "Устанавливаем Nuitka..."
pip install --upgrade pip setuptools wheel
pip install nuitka

echo
echo "Компилируем core.py → core.so..."
python -m nuitka \
    --module \
    --output-dir=. \
    --remove-output \
    --python-flag=no_docstrings \
    --lto=yes \
    core.py

deactivate

rm -rf "$VENV_DIR"

echo
echo "✅ Сборка успешно завершена!"
echo "Файл core.so создан в текущей директории."
echo
echo "Теперь можно запускать:"
echo "  python3 system_maintenance_tool.py --find"
