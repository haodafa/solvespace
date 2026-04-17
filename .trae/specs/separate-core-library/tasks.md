# Tasks
- [x] Task 1: 创建物理目录结构: 在 `src/` 下创建 `core` 和 `ui` 目录。
- [x] Task 2: 移动核心代码到 `src/core/`: 将所有属于 `solvespace_core` 的源代码和头文件（如 `constraint.cpp`, `mesh.cpp`, `solvespace_core.h`, `srf/` 目录, `render/` 目录等核心部分）移动到 `src/core/` 目录。
- [x] Task 3: 移动 UI 代码到 `src/ui/`: 将所有属于界面相关的源代码和头文件（如 `platform/` 目录, `solvespace.cpp`, `gui*.cpp`, `graphicswin.cpp` 等）移动到 `src/ui/` 目录。
- [x] Task 4: 添加跨平台导出宏与预编译头:
  - [x] SubTask 4.1: 在 `src/core/solvespace_core.h` 及需要导出的类定义前添加 `SOLVESPACE_CORE_API` 宏（`__declspec(dllexport/dllimport)`），支持 VS 动态库编译。
  - [x] SubTask 4.2: 建立预编译头文件（例如 `core_pch.h` 和 `ui_pch.h`）或在 CMake 中利用 `target_precompile_headers` 为两个模块设置预编译头。
- [x] Task 5: 编写各子目录的 `CMakeLists.txt`:
  - [x] SubTask 5.1: 在 `src/core/CMakeLists.txt` 中配置 `solvespace_core` 库（根据配置支持 SHARED/STATIC），并设置 `target_include_directories`。
  - [x] SubTask 5.2: 在 `src/ui/CMakeLists.txt` 中配置主可执行文件 `solvespace` 以及链接 `solvespace_core`。
  - [x] SubTask 5.3: 修改项目原有的 `src/CMakeLists.txt`，通过 `add_subdirectory(core)` 和 `add_subdirectory(ui)` 来组织编译。
- [x] Task 6: 修复头文件引用与编译错误: 更新代码中由于目录移动导致的 `#include` 路径错误，并确保在 Linux 和 Windows(VS) 下都能正常编译。

# Task Dependencies
- [Task 2] depends on [Task 1]
- [Task 3] depends on [Task 1]
- [Task 4] depends on [Task 2]
- [Task 5] depends on [Task 2] and [Task 3]
- [Task 6] depends on [Task 4] and [Task 5]
