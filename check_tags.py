import re

filepath = r'c:\Users\asus\CascadeProjects\ChurchIligan\templates\core\my_appointments.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Find ALL django tags with their positions
all_tags = []
for m in re.finditer(r'\{%[-\s]*(.*?)[-\s]*%\}', content, re.DOTALL):
    tag_content = m.group(1).strip()
    tag_name = tag_content.split()[0] if tag_content.split() else ''
    # Calculate line number
    line_num = content[:m.start()].count('\n') + 1
    all_tags.append((line_num, tag_name, tag_content[:60]))

# Now check balance
stack = []
for line_num, tag_name, tag_preview in all_tags:
    if tag_name in ('if', 'for', 'block', 'with', 'ifchanged'):
        stack.append((tag_name, line_num, tag_preview))
    elif tag_name in ('endif', 'endfor', 'endblock', 'endwith', 'endifchanged'):
        base = tag_name[3:]  # remove 'end'
        if stack:
            if stack[-1][0] == base:
                stack.pop()
            else:
                print("MISMATCH at line %d: Found {%% %s %%} but expected {%% end%s %%} (opened at line %d: %s)" % (line_num, tag_name, stack[-1][0], stack[-1][1], stack[-1][2]))
                # Try to find matching in stack
                found = False
                for idx in range(len(stack)-1, -1, -1):
                    if stack[idx][0] == base:
                        # Pop everything above
                        unclosed = stack[idx+1:]
                        for u in unclosed:
                            print("  -> UNCLOSED: {%% %s %%} at line %d: %s" % (u[0], u[1], u[2]))
                        stack = stack[:idx]
                        found = True
                        break
                if not found:
                    print("  -> No matching open tag found in stack!")
        else:
            print("EXTRA CLOSE at line %d: {%% %s %%} but stack is empty!" % (line_num, tag_name))

if stack:
    print("\nUnclosed tags at end:")
    for s in stack:
        print("  {%% %s %%} at line %d: %s" % (s[0], s[1], s[2]))
else:
    print("All tags balanced!")
