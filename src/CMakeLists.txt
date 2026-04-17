include(GNUInstallDirs)

# configuration

set(HAVE_SPACEWARE ${SPACEWARE_FOUND})

if(NOT WIN32 OR APPLE)
    if(GTKMM_gtkmm-3.0_VERSION VERSION_LESS "3.24.0")
        set(HAVE_GTK_FILECHOOSERNATIVE 0)
    else()
        set(HAVE_GTK_FILECHOOSERNATIVE 1)
    endif()
endif()

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/config.h.in
               ${CMAKE_CURRENT_BINARY_DIR}/config.h)

if(USE_QT_GUI)
    set(CMAKE_AUTOMOC ON)
    find_package(Qt6 COMPONENTS Core Gui OpenGLWidgets Widgets REQUIRED)
    # find_package(Qt5 COMPONENTS Core Gui Widgets REQUIRED)
    qt_add_resources(RESOURCE_FILES ../res/qt-resources.qrc)
endif()

# solvespace dependencies
add_library(slvs_deps INTERFACE)
target_include_directories(slvs_deps SYSTEM INTERFACE
    ${OPENGL_INCLUDE_DIR}
    ${ZLIB_INCLUDE_DIR}
    ${PNG_PNG_INCLUDE_DIR}
    ${FREETYPE_INCLUDE_DIRS}
    ${MIMALLOC_INCLUDE_DIR}
    ${EIGEN3_INCLUDE_DIRS})
target_link_libraries(slvs_deps INTERFACE
    dxfrw
    ${ZLIB_LIBRARY}
    ${PNG_LIBRARY}
    ${FREETYPE_LIBRARY}
    mimalloc-static)

if(NOT USE_QT_GUI OR ENABLE_CLI)
    target_include_directories(slvs_deps SYSTEM INTERFACE ${CAIRO_INCLUDE_DIRS})
    target_link_libraries(slvs_deps INTERFACE ${CAIRO_LIBRARIES})
endif()

if(Backtrace_FOUND)
    target_include_directories(slvs_deps SYSTEM INTERFACE
        ${Backtrace_INCLUDE_DIRS})
    target_link_libraries(slvs_deps INTERFACE
        ${Backtrace_LIBRARY})
endif()

if(SPACEWARE_FOUND)
    target_include_directories(slvs_deps SYSTEM INTERFACE
        ${SPACEWARE_INCLUDE_DIR})
    target_link_libraries(slvs_deps INTERFACE
        ${SPACEWARE_LIBRARIES})
endif()

if(ENABLE_OPENMP)
    target_link_libraries(slvs_deps INTERFACE slvs_openmp)
endif()

target_compile_options(slvs_deps
    INTERFACE ${COVERAGE_FLAGS})

# platform utilities
if(APPLE)
    target_link_libraries(slvs_deps INTERFACE
        ${APPKIT_LIBRARY})
endif()

# Needed for CI
file(WRITE ${CMAKE_BINARY_DIR}/version.env "\
VERSION_MAJOR=${PROJECT_VERSION_MAJOR}\n\
VERSION_MINOR=${PROJECT_VERSION_MINOR}\n\
VERSION_PATCH=0\n\
VERSION_GIT_HASH=${solvespace_GIT_HASH}\n\
")

add_subdirectory(core)
add_subdirectory(ui)
add_subdirectory(slvs)
