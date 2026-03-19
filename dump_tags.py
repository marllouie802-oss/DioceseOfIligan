import re
file_path = r'c:\Users\asus\CascadeProjects\ChurchIligan\templates\core\manage_booking_detail.html'
with open(file_path, 'r', encoding='utf-8') as f:
    tags = re.findall(r'\{%[ ]*(if|endif|elif|else|for|endfor|with|endwith|block|endblock)[^%]*%\}', f.read())
print(", ".join(tags))
