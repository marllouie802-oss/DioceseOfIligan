import re

file_path = r'c:\Users\asus\CascadeProjects\ChurchIligan\templates\core\manage_booking_detail.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all multi-line tags
multiline_tags = re.findall(r'\{%[^%]*\n[^%]*%\}', content)

if multiline_tags:
    print("Found multi-line tags:")
    for tag in multiline_tags:
        print(f"---TAG---\n{tag}\n---------")
else:
    print("No multi-line tags found.")
