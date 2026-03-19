import re

files = [
    r'c:\Users\asus\CascadeProjects\ChurchIligan\templates\core\manage_booking_detail.html',
    r'c:\Users\asus\CascadeProjects\ChurchIligan\templates\core\my_appointments.html'
]

def sanitize(path):
    with open(path, 'rb') as f:
        content = f.read()

    # Decoding with replacement to ignore bad bytes
    text = content.decode('utf-8', errors='replace')
    
    # Normalize unicode spaces to ASCII space
    text = text.replace('\u00A0', ' ')
    
    # Replace all forms of curly braces with ASCII
    # Ensure {{ and }} are pure ASCII.
    # Note: This is aggressive but safe for Django templates usually.
    # We must be careful not to break other usages of braces if any (e.g. JS objects)
    # But usually JS objects don't have {{ }} without spaces unless using frameworks.
    
    # Find all pattern that looks like a Django variable tag
    # We'll re-write them to ensure standard spacing.
    
    def repl(m):
        # m.group(1) is internal content
        inner = m.group(1).strip()
        return '{' + '{ ' + inner + ' }' + '}'

    # Regex for {{ prop }}
    # We look for {{, any chars, }}
    # But we want to avoid matching across lines if it was the issue, though we fixed that.
    # Improve regex to capture potential bad chars
    text = re.sub(r'\{\{\s*(.*?)\s*\}\}', repl, text, flags=re.DOTALL)
    
    # Also fix {% tag %}
    def repl_tag(m):
        inner = m.group(1).strip()
        return '{% ' + inner + ' %}'
        
    text = re.sub(r'\{%\s*(.*?)\s*%\}', repl_tag, text, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print(f"Sanitized {path}")

for f in files:
    try:
        sanitize(f)
    except Exception as e:
        print(f"Error processing {f}: {e}")
