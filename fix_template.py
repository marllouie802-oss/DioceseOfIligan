import os

file_path = r'c:\Users\asus\CascadeProjects\ChurchIligan\templates\core\manage_booking_detail.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the specific split tag
old_content = """<div class="value" style="font-weight: 700; color: #059669;">{% if booking.service.price > 0 %}₱{{
            booking.service.price|floatformat:2 }}{% else %}Free / Donation{% endif %}</div>"""

# Actually, the view_file showed:
# 354:           <div class="value" style="font-weight: 700; color: #059669;">{% if booking.service.price > 0 %}₱{{
# 355:             booking.service.price|floatformat:2 }}{% else %}Free / Donation{% endif %}</div>

import re
pattern = r'<div class="value" style="font-weight: 700; color: #059669;">\{% if booking\.service\.price > 0 %\}₱\{\{[ \n\r]*booking\.service\.price\|floatformat:2 \}\}\{% else %\}Free / Donation\{% endif %\}</div>'
replacement = '<div class="value" style="font-weight: 700; color: #059669;">{% if booking.service.price > 0 %}₱{{ booking.service.price|floatformat:2 }}{% else %}Free / Donation{% endif %}</div>'

new_content = re.sub(pattern, replacement, content)

if new_content != content:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Success: File updated.")
else:
    print("Error: Pattern not found.")
