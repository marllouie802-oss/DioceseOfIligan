import re

file_path = r'c:\Users\asus\CascadeProjects\ChurchIligan\templates\core\manage_booking_detail.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all occurrences of "{%"
all_starts = [m.start() for m in re.finditer(r'\{%', content)]

for start in all_starts:
    # Find the matching "%}"
    end = content.find('%}', start)
    if end == -1:
        print(f"Unclosed tag at position {start}")
        continue
    
    tag_content = content[start+2:end].strip()
    if tag_content.startswith('if') or tag_content.startswith('elif') or tag_content.startswith('else') or tag_content.startswith('endif'):
        # Check for standard spacing
        if not re.match(r'^(if|elif|else|endif)(\s+|$)', tag_content):
            print(f"Non-standard tag content: '{{% {tag_content} %}}' at position {start}")

print("Validation complete.")
