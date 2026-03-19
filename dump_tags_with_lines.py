import re
file_path = r'c:\Users\asus\CascadeProjects\ChurchIligan\templates\core\manage_booking_detail.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
    matches = re.finditer(r'\{%[ ]*(if|endif|elif|else|for|endfor|with|endwith|block|endblock)[^%]*%\}', content)

for m in matches:
    line_num = content[:m.start()].count('\n') + 1
    print(f"{line_num:3}: {m.group(0).strip()}")
