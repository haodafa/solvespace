if(ENABLE_GUI OR ENABLE_CLI)
    set(every_platform_SOURCES
        platform/guiwin.cpp
        platform/guigtk.cpp
        platform/guimac.mm
        platform/guihtml.cpp)

    set(solvespace_core_gl_SOURCES
        solvespace.cpp
        ui.h
        confscreen.cpp
        describescreen.cpp
        draw.cpp
        drawconstraint.cpp
        drawentity.cpp
        graphicswin.cpp
        mouse.cpp
        textscreens.cpp
        textwin.cpp
        toolbar.cpp
        view.cpp
        platform/gui.cpp
    )

    if(HAVE_GETTEXT)
        get_target_property(solvespace_core_SOURCES solvespace_core SOURCES)
        set(inputs
            ${solvespace_core_SOURCES}
            ${every_platform_SOURCES}
            ${solvespace_core_gl_SOURCES})

        set(templ_po   ${CMAKE_CURRENT_BINARY_DIR}/../../res/messages.po)

        set(output_pot ${CMAKE_CURRENT_SOURCE_DIR}/../../res/messages.pot)
        set(output_po  ${CMAKE_CURRENT_SOURCE_DIR}/../../res/locales/en_US.po)
        file(GLOB locale_pos ${CMAKE_CURRENT_SOURCE_DIR}/../../res/locales/*.po)

        string(REPLACE ${CMAKE_SOURCE_DIR} ${CMAKE_BINARY_DIR}
            gen_output_pot ${output_pot}.gen)
        string(REPLACE ${CMAKE_SOURCE_DIR} ${CMAKE_BINARY_DIR}
            gen_output_po ${output_po}.gen)
        foreach(locale_po ${locale_pos})
            string(REPLACE ${CMAKE_SOURCE_DIR} ${CMAKE_BINARY_DIR}
                gen_locale_po ${locale_po}.gen)
            list(APPEND gen_locale_pos ${gen_locale_po})
        endforeach()

        add_custom_command(
            OUTPUT  ${gen_output_pot}
            COMMAND ${XGETTEXT}
                    --language=C++
                    --keyword --keyword=_ --keyword=N_ --keyword=C_:2,1c --keyword=CN_:2,1c
                    --force-po --width=100 --sort-by-file
                    --package-name=SolveSpace
                    --package-version=${PROJECT_VERSION}
                    "--copyright-holder=the PACKAGE authors"
                    --msgid-bugs-address=phkahler@gmail.com
                    --from-code=utf-8 --output=${gen_output_pot} ${inputs}
            COMMAND ${CMAKE_COMMAND} -E copy_if_different ${gen_output_pot} ${output_pot}
            DEPENDS ${inputs}
            WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
            COMMENT "Extracting translations"
            VERBATIM)

        file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/../../res/locales)

        add_custom_command(
            OUTPUT  ${gen_output_po}
            COMMAND ${MSGINIT}
                    --locale=en_US --no-translator
                    --output=${templ_po} --input=${gen_output_pot}
            COMMAND ${MSGMERGE}
                    --force-po --no-fuzzy-matching
                    --output=${gen_output_po} ${output_po} ${templ_po}
            COMMAND ${CMAKE_COMMAND} -E copy_if_different ${gen_output_po} ${output_po}
            DEPENDS ${gen_output_pot}
            COMMENT "Updating en_US translations"
            VERBATIM)

        foreach(locale_po ${locale_pos})
            string(REPLACE ${CMAKE_SOURCE_DIR} ${CMAKE_BINARY_DIR}
                gen_locale_po ${locale_po}.gen)

            get_filename_component(locale_name ${locale_po} NAME_WE)
            if(locale_name STREQUAL "en_US")
                continue()
            endif()

            add_custom_command(
                OUTPUT  ${gen_locale_po}
                COMMAND ${MSGMERGE}
                        --no-fuzzy-matching
                        --output=${gen_locale_po} ${locale_po} ${gen_output_pot}
                COMMAND ${CMAKE_COMMAND} -E copy_if_different ${gen_locale_po} ${locale_po}
                DEPENDS ${gen_output_pot}
                COMMENT "Updating ${locale_name} translations"
                VERBATIM)
        endforeach()

        add_custom_target(translate_solvespace
            DEPENDS ${gen_output_pot} ${gen_output_po} ${gen_locale_pos})
    endif()
endif()

if(ENABLE_GUI)
    add_executable(solvespace WIN32 MACOSX_BUNDLE
        ${solvespace_core_gl_SOURCES}
        $<TARGET_PROPERTY:resources,EXTRA_SOURCES>)

    if(NOT USE_QT_GUI)
        target_sources(solvespace PRIVATE platform/entrygui.cpp)
    endif()

    add_dependencies(solvespace resources)

    target_link_libraries(solvespace PRIVATE solvespace_core ${OPENGL_LIBRARIES})

    if(OPENGL STREQUAL 3)
        target_sources(solvespace PRIVATE render/gl3shader.cpp render/rendergl3.cpp)
    elseif(OPENGL STREQUAL 1)
        target_sources(solvespace PRIVATE render/rendergl1.cpp)
    else()
        message(FATAL_ERROR "Unsupported OpenGL version ${OPENGL}")
    endif()

    if(WIN32 AND NOT USE_QT_GUI)
        target_sources(solvespace PRIVATE platform/guiwin.cpp)
        target_link_libraries(solvespace PRIVATE comctl32)
    elseif(APPLE)
        target_compile_options(solvespace PRIVATE -fobjc-arc)
        target_compile_definitions(solvespace PRIVATE GL_SILENCE_DEPRECATION)

        target_sources(solvespace PRIVATE platform/guimac.mm)
        set_target_properties(solvespace PROPERTIES
            OUTPUT_NAME SolveSpace
            XCODE_ATTRIBUTE_ENABLE_HARDENED_RUNTIME "YES"
            XCODE_ATTRIBUTE_PRODUCT_BUNDLE_IDENTIFIER "com.solvespace"
            RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
    elseif(EMSCRIPTEN)
        if(NOT EMSCRIPTEN_VERSION OR EMSCRIPTEN_VERSION VERSION_LESS "4.0.8")
            message(FATAL_ERROR "The Emscripten build requires at least version 4.0.8")
        endif()

        target_compile_features(solvespace PRIVATE cxx_std_17)

        set(SHELL "${CMAKE_CURRENT_SOURCE_DIR}/platform/html/emshell.html")
        set(RESP_LINK_FLAGS
            --bind --shell-file "\"${SHELL}\"" --no-heap-copy
            "-s ALLOW_MEMORY_GROWTH=1" "-s WASM=1"
            "-s ASYNCIFY=1" "-s DYNCALLS=1" "-s ASSERTIONS=1"
            "-s TOTAL_STACK=33554432" "-s TOTAL_MEMORY=134217728")

        get_target_property(resource_list resources SOURCES)
        foreach(resource ${resource_list})
            file(RELATIVE_PATH target_path "${CMAKE_SOURCE_DIR}" "${resource}")
            list(APPEND RESP_LINK_FLAGS "--preload-file \"${resource}\"@\"${target_path}\"")
        endforeach()

        if(CMAKE_BUILD_TYPE STREQUAL Debug)
            list(APPEND RESP_LINK_FLAGS --emrun --emit-symbol-map "-s DEMANGLE_SUPPORT=1" "-s SAFE_HEAP=1")
        endif()

        target_sources(solvespace PRIVATE platform/guihtml.cpp)

        set(resp_file_path "${CMAKE_CURRENT_BINARY_DIR}/emscripten_flags.rsp")
        file(GENERATE OUTPUT "${resp_file_path}" CONTENT "$<JOIN:${RESP_LINK_FLAGS},\n>")

        set_target_properties(solvespace PROPERTIES
            SUFFIX ".html"
            LINK_FLAGS "@${resp_file_path}"
            LINK_DEPENDS "${SHELL};${resp_file_path};${resource_list}")

        add_custom_command(TARGET solvespace POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy_if_different ${CMAKE_CURRENT_SOURCE_DIR}/platform/html/solvespaceui.css ${EXECUTABLE_OUTPUT_PATH}/solvespaceui.css)
        add_custom_command(TARGET solvespace POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy_if_different ${CMAKE_CURRENT_SOURCE_DIR}/platform/html/solvespaceui.js ${EXECUTABLE_OUTPUT_PATH}/solvespaceui.js)
        add_custom_command(TARGET solvespace POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy_if_different ${CMAKE_CURRENT_SOURCE_DIR}/platform/html/filemanagerui.js ${EXECUTABLE_OUTPUT_PATH}/filemanagerui.js)
    elseif(USE_QT_GUI)
        set_target_properties(solvespace PROPERTIES OUTPUT_NAME solvespace-qt)
        target_sources(solvespace PRIVATE platform/guiqt.cpp platform/guiqt.h ${RESOURCE_FILES})
        target_include_directories(solvespace SYSTEM PRIVATE ${FONTCONFIG_INCLUDE_DIRS})
        target_link_directories(solvespace PRIVATE ${FONTCONFIG_LIBRARY_DIRS})
        target_link_libraries(solvespace PRIVATE ${FONTCONFIG_LIBRARIES} Qt6::Core Qt6::Gui Qt6::OpenGLWidgets Qt6::Widgets)
    else()
        target_sources(solvespace PRIVATE platform/guigtk.cpp)
        target_include_directories(solvespace SYSTEM PRIVATE ${GTKMM_INCLUDE_DIRS} ${JSONC_INCLUDE_DIRS} ${FONTCONFIG_INCLUDE_DIRS})
        target_link_directories(solvespace PRIVATE ${GTKMM_LIBRARY_DIRS} ${JSONC_LIBRARY_DIRS} ${FONTCONFIG_LIBRARY_DIRS})
        target_link_libraries(solvespace PRIVATE ${GTKMM_LIBRARIES} ${JSONC_LIBRARIES} ${FONTCONFIG_LIBRARIES})
    endif()

    if(WIN32)
        if(MSVC)
            set_target_properties(solvespace PROPERTIES LINK_FLAGS "/MANIFEST:NO /SAFESEH:NO /INCREMENTAL:NO /OPT:REF")
        elseif(CMAKE_CXX_COMPILER_ID STREQUAL "Clang" AND MSVC_VERSION)
            string(REPLACE " -Xlinker /MANIFEST:EMBED" "" CMAKE_CXX_LINK_EXECUTABLE "${CMAKE_CXX_LINK_EXECUTABLE}")
            target_link_options(solvespace PRIVATE "SHELL:-Xlinker /MANIFEST:NO")
        endif()
    endif()
endif()

if(ENABLE_CLI)
    add_library(solvespace-headless STATIC EXCLUDE_FROM_ALL
        ${solvespace_core_gl_SOURCES}
        platform/guinone.cpp
        render/rendercairo.cpp)

    target_compile_definitions(solvespace-headless PRIVATE HEADLESS)
    target_include_directories(solvespace-headless INTERFACE ${CMAKE_CURRENT_SOURCE_DIR} PUBLIC ${EIGEN3_INCLUDE_DIRS})
    target_link_libraries(solvespace-headless PRIVATE solvespace_core)

    add_executable(solvespace-cli platform/entrycli.cpp $<TARGET_PROPERTY:resources,EXTRA_SOURCES>)
    target_link_libraries(solvespace-cli solvespace_core solvespace-headless)
    add_dependencies(solvespace-cli resources)

    if(MSVC)
        set_target_properties(solvespace-cli PROPERTIES LINK_FLAGS "/INCREMENTAL:NO /OPT:REF")
    endif()
endif()

if(NOT (WIN32 OR APPLE OR EMSCRIPTEN))
    if(ENABLE_GUI)
        install(TARGETS solvespace COMPONENT solvespace RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
    endif()
    if(ENABLE_CLI)
        install(TARGETS solvespace-cli COMPONENT solvespace RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
    endif()
endif()

if(APPLE)
    set(LIBOMP_LIB_PATH ${OpenMP_CXX_INCLUDE_DIRS}/../lib/libomp.dylib)
    set(LIBOMP_LINK_PATH "@executable_path/../Resources/libomp.dylib")
    set(LIBOMP_LINK_PATH_UTILS "@executable_path/SolveSpace.app/Contents/Resources/libomp.dylib")
    if(ENABLE_GUI)
        add_custom_command(TARGET solvespace POST_BUILD COMMAND cp -r ${CMAKE_BINARY_DIR}/Resources $<TARGET_BUNDLE_CONTENT_DIR:solvespace>)
        if(ENABLE_OPENMP)
            execute_process(COMMAND install_name_tool -id ${LIBOMP_LINK_PATH} ${LIBOMP_LIB_PATH})
            add_custom_command(TARGET solvespace POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E copy ${LIBOMP_LIB_PATH} $<TARGET_BUNDLE_CONTENT_DIR:solvespace>/Resources/libomp.dylib
                COMMAND install_name_tool -change ${LIBOMP_LINK_PATH} ${LIBOMP_LINK_PATH_UTILS} $<TARGET_FILE:solvespace-debugtool>)
        endif()
    endif()
    if(ENABLE_TESTS AND ENABLE_OPENMP)
        add_custom_command(TARGET solvespace POST_BUILD COMMAND install_name_tool -change ${LIBOMP_LINK_PATH} ${LIBOMP_LINK_PATH_UTILS} $<TARGET_FILE:solvespace-testsuite>)
    endif()
    if(ENABLE_CLI)
        add_custom_command(TARGET solvespace POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:solvespace-cli> $<TARGET_FILE_DIR:solvespace> COMMENT "Bundling executable solvespace-cli" VERBATIM)
    endif()
endif()
