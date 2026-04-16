add_library(slvs-solver INTERFACE)
target_sources(slvs-solver INTERFACE
    dsc.h
    expr.h
    handle.h
    param.h
    ../ui/platform/platform.h
    solvespace.h

    constrainteq.cpp
    entity.cpp
    expr.cpp
    ../ui/platform/platformbase.cpp
    system.cpp
    util.cpp
)
target_include_directories(slvs-solver SYSTEM INTERFACE
    ${MIMALLOC_INCLUDE_DIR}
    ${EIGEN3_INCLUDE_DIRS})
target_include_directories(slvs-solver INTERFACE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/../ui)

add_library(solvespace_core
    solvespace_core.cpp
    polygon.h
    sketch.h
    srf/surface.h
    ../ui/render/render.h
    bsp.cpp
    clipboard.cpp
    constraint.cpp
    export.cpp
    exportstep.cpp
    exportvector.cpp
    file.cpp
    generate.cpp
    group.cpp
    groupmesh.cpp
    importdxf.cpp
    importidf.cpp
    importmesh.cpp
    mesh.cpp
    modify.cpp
    polyline.cpp
    polygon.cpp
    resource.cpp
    request.cpp
    style.cpp
    ttf.cpp
    undoredo.cpp
    ../ui/platform/platform.cpp
    ../ui/render/render.cpp
    ../ui/render/render2d.cpp
    srf/boolean.cpp
    srf/curve.cpp
    srf/merge.cpp
    srf/ratpoly.cpp
    srf/raycast.cpp
    srf/shell.cpp
    srf/surface.cpp
    srf/surfinter.cpp
    srf/triangulate.cpp)

target_compile_definitions(solvespace_core PRIVATE SOLVESPACE_CORE_EXPORTS)
target_precompile_headers(solvespace_core PRIVATE <vector> <string>)

target_include_directories(solvespace_core PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/../ui
    ${CMAKE_CURRENT_BINARY_DIR}/..)
target_link_libraries(solvespace_core PRIVATE slvs-solver)
target_link_libraries(solvespace_core PUBLIC slvs_deps)

# Alias for compatibility with other CMake files that might use it
add_library(SolveSpace::Core ALIAS solvespace_core)
