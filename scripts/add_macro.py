import os
import re

header_files = []
for root, dirs, files in os.walk('/workspace/src/core'):
    for f in files:
        if f.endswith('.h'):
            header_files.append(os.path.join(root, f))

# regex to find class/struct definitions, ignoring templates and forward declarations
# pattern looks for:
# ^(class|struct)\s+([A-Za-z0-9_]+)\s*(:|{|final)
pattern = re.compile(r'^(class|struct)\s+([A-Za-z0-9_]+)(?=\s*[:{]|\s+final)', re.MULTILINE)

# wait, we shouldn't add it to template classes easily, let's see if we can exclude them.
# actually, in C++, it's `template<...> class SOLVESPACE_CORE_API Foo {`. This is valid syntax but causes warnings on MSVC. 
# Let's just add it to all class/struct that are defined.

for path in header_files:
    with open(path, 'r') as f:
        content = f.read()
        
    if 'SOLVESPACE_CORE_API' in content:
        continue
        
    new_content = pattern.sub(r'\1 SOLVESPACE_CORE_API \2', content)
    
    if new_content != content:
        # Need to include solvespace_core_api.h
        include_stmt = '#include "solvespace_core_api.h"\n'
        # find where to insert it. After the last #include or after #define ..._H
        lines = new_content.split('\n')
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('#define '):
                insert_idx = i + 1
                break
        
        lines.insert(insert_idx, include_stmt)
        new_content = '\n'.join(lines)
        
        with open(path, 'w') as f:
            f.write(new_content)
