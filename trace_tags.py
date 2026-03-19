import re
import sys

# Ensure stdout uses utf-8
sys.stdout.reconfigure(encoding='utf-8')

file_path = r'c:\Users\asus\CascadeProjects\ChurchIligan\templates\core\manage_booking_detail.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    line_num = i + 1
    if '{%' in line and ('if' in line or 'elif' in line or 'else' in line or 'endif' in line):
        # Escape any problematic characters for simple printing
        safe_line = line.strip().replace('₱', 'PHP')
        print(f"{line_num:3}: {safe_line}")
