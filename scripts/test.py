import re

with open('src/CMakeLists.txt', 'r') as f:
    content = f.read()

# Let's find add_library(solvespace-core STATIC ...)
match = re.search(r'add_library\(solvespace-core STATIC(.*?)^\)', content, re.MULTILINE | re.DOTALL)
if match:
    files = match.group(1).strip().split('\n')
    files = [f.strip() for f in files if f.strip()]
    
    ui_files = []
    core_files = []
    
    for f in files:
        if f in ['ui.h', 'render/render.h', 'confscreen.cpp', 'describescreen.cpp', 
                 'draw.cpp', 'drawconstraint.cpp', 'drawentity.cpp', 'graphicswin.cpp', 
                 'mouse.cpp', 'textscreens.cpp', 'textwin.cpp', 'toolbar.cpp', 'view.cpp', 
                 'platform/gui.cpp', 'render/render.cpp', 'render/render2d.cpp']:
            ui_files.append(f)
        else:
            core_files.append(f)
            
    print("UI FILES:", ui_files)
    print("CORE FILES:", core_files)
