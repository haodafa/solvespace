import re

with open('src/CMakeLists.txt', 'r') as f:
    content = f.read()

# All files in solvespace-core currently
all_files = ['solvespace_core.cpp', 'polygon.h', 'sketch.h', 'ui.h', 'render/render.h', 'srf/surface.h', 'bsp.cpp', 'clipboard.cpp', 'confscreen.cpp', 'constraint.cpp', 'describescreen.cpp', 'draw.cpp', 'drawconstraint.cpp', 'drawentity.cpp', 'export.cpp', 'exportstep.cpp', 'exportvector.cpp', 'file.cpp', 'generate.cpp', 'graphicswin.cpp', 'group.cpp', 'groupmesh.cpp', 'importdxf.cpp', 'importidf.cpp', 'importmesh.cpp', 'mesh.cpp', 'modify.cpp', 'mouse.cpp', 'polyline.cpp', 'polygon.cpp', 'resource.cpp', 'request.cpp', 'style.cpp', 'textscreens.cpp', 'textwin.cpp', 'toolbar.cpp', 'ttf.cpp', 'undoredo.cpp', 'view.cpp', 'platform/platform.cpp', 'platform/gui.cpp', 'render/render.cpp', 'render/render2d.cpp', 'srf/boolean.cpp', 'srf/curve.cpp', 'srf/merge.cpp', 'srf/ratpoly.cpp', 'srf/raycast.cpp', 'srf/shell.cpp', 'srf/surface.cpp', 'srf/surfinter.cpp', 'srf/triangulate.cpp']

ui_files = ['ui.h', 'render/render.h', 'confscreen.cpp', 'describescreen.cpp', 
            'draw.cpp', 'drawconstraint.cpp', 'drawentity.cpp', 'graphicswin.cpp', 
            'mouse.cpp', 'textscreens.cpp', 'textwin.cpp', 'toolbar.cpp', 'view.cpp', 
            'platform/gui.cpp', 'render/render.cpp', 'render/render2d.cpp']

core_files = [f for f in all_files if f not in ui_files]

# Replace solvespace-core with solvespace_core
content = re.sub(r'add_library\(solvespace-core STATIC.*?\)', 
                 'add_library(solvespace_core STATIC\n        ' + '\n        '.join(core_files) + ')', 
                 content, flags=re.DOTALL)

content = content.replace('target_include_directories(solvespace-core', 'target_include_directories(solvespace_core')
content = content.replace('target_link_libraries(solvespace-core', 'target_link_libraries(solvespace_core')
content = content.replace('get_target_property(solvespace_core_SOURCES solvespace-core SOURCES)', 'get_target_property(solvespace_core_SOURCES solvespace_core SOURCES)')

# Add ui_files to solvespace_core_gl_SOURCES
ui_files_str = '\n        '.join(ui_files)
content = re.sub(r'set\(solvespace_core_gl_SOURCES\n\s*solvespace\.cpp\)', 
                 f'set(solvespace_core_gl_SOURCES\n        solvespace.cpp\n        {ui_files_str})', 
                 content)

# Link solvespace to solvespace_core
content = content.replace('solvespace-core', 'solvespace_core')

with open('src/CMakeLists.txt', 'w') as f:
    f.write(content)

