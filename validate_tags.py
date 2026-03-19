import re

file_paths = [
    r'c:\Users\asus\CascadeProjects\ChurchIligan\templates\core\manage_booking_detail.html',
    r'c:\Users\asus\CascadeProjects\ChurchIligan\templates\core\partials\booking_invoice_content.html'
]

def check_tags(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple tag stack
    stack = []
    # Find all {% ... %} including multi-line
    tags = re.findall(r'\{%[ \n\r]*([^%]+?)[ \n\r]*%\}', content, re.DOTALL)
    
    for tag in tags:
        tag_trimmed = tag.strip()
        parts = tag_trimmed.split()
        if not parts: continue
        
        main_tag = parts[0]
        
        # Check if tag itself contains newline which is usually a bad sign in Django templates for the tag name itself
        # Although Django might actually allow it for the expression, it's safer to avoid.
        
        if main_tag == 'if':
            stack.append(('if', tag_trimmed))
        elif main_tag == 'elif' or main_tag == 'else':
            if not stack or stack[-1][0] != 'if':
                print(f"Error: {main_tag} without if in {file_path}")
        elif main_tag == 'endif':
            if not stack or stack[-1][0] != 'if':
                print(f"Error: endif without if in {file_path}")
            else:
                stack.pop()
        elif main_tag == 'for':
            stack.append(('for', tag_trimmed))
        elif main_tag == 'endfor':
            if not stack or stack[-1][0] != 'for':
                print(f"Error: endfor without for in {file_path}")
            else:
                stack.pop()
        elif main_tag == 'block':
            stack.append(('block', tag_trimmed))
        elif main_tag == 'endblock':
            if not stack or stack[-1][0] != 'block':
                print(f"Error: endblock without block in {file_path}")
            else:
                stack.pop()
        elif main_tag == 'with':
            stack.append(('with', tag_trimmed))
        elif main_tag == 'endwith':
            if not stack or stack[-1][0] != 'with':
                print(f"Error: endwith without with in {file_path}")
            else:
                stack.pop()
    
    if stack:
        print(f"Unclosed tags in {file_path}:")
        for type, content in stack:
            print(f"  - {type}: {content}")
    else:
        print(f"All tags appear closed in {file_path}.")

for path in file_paths:
    check_tags(path)
