import re

file_path = r'c:\Users\asus\CascadeProjects\ChurchIligan\templates\core\manage_booking_detail.html'

def inspect_file(path):
    with open(path, 'rb') as f:
        content = f.read()
    
    # Check for non-ascii
    try:
        text = content.decode('utf-8')
    except UnicodeDecodeError:
        print(f"File {path} is not valid UTF-8")
        return

    # Find lines with {{ 
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if '{{' in line:
            # Print repr to see hidden chars
            print(f"Line {i+1}: {ascii(line)}")

print("Inspecting manage_booking_detail.html...")
inspect_file(file_path)

print("\nInspecting my_appointments.html...")
inspect_file(r'c:\Users\asus\CascadeProjects\ChurchIligan\templates\core\my_appointments.html')
