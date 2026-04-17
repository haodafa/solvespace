import re

with open('src/CMakeLists.txt', 'r') as f:
    content = f.read()

# We want to move render.cpp and render2d.cpp from solvespace_core_gl_SOURCES to solvespace_core

content = content.replace('        render/render.cpp\n', '')
content = content.replace('        render/render2d.cpp)\n', ')\n')
content = content.replace('        render/render.h\n', '')

content = content.replace('        srf/surface.h\n', '        srf/surface.h\n        render/render.h\n')
content = content.replace('        srf/boolean.cpp\n', '        render/render.cpp\n        render/render2d.cpp\n        srf/boolean.cpp\n')

with open('src/CMakeLists.txt', 'w') as f:
    f.write(content)
