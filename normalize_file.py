import os

file_path = r'c:\Users\asus\CascadeProjects\ChurchIligan\templates\core\manage_booking_detail.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace non-breaking spaces (U+00A0) with standard spaces
content = content.replace('\u00a0', ' ')

# Normalize line endings
content = content.replace('\r\n', '\n').replace('\r', '\n')

with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("File normalized.")
