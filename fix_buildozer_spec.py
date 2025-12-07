import re
import os

SPEC_FILE = "buildozer.spec"

if not os.path.isfile(SPEC_FILE):
    print(f"Файл {SPEC_FILE} не найден в текущей директории!")
    exit(1)

with open(SPEC_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    # Исправляем True/False на строчные
    line = re.sub(r"=\s*True\b", "= true", line, flags=re.IGNORECASE)
    line = re.sub(r"=\s*False\b", "= false", line, flags=re.IGNORECASE)
    
    # Убираем лишние пробелы вокруг чисел (android.api, android.minapi, version код и т.д.)
    line = re.sub(r"=\s*(\d+)\s*$", r"= \1", line)
    
    new_lines.append(line)

with open(SPEC_FILE, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"Файл {SPEC_FILE} успешно проверен и исправлен!")
