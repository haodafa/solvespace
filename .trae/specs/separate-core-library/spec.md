# Separate Core Library Spec

## Why
当前虽然通过 CMake 的 `add_library` 将核心业务代码分为了一个静态目标 `solvespace_core`，但代码文件仍然混杂在 `src/` 同一目录下，没有实现物理隔离。此外，目前的实现没有提供明确的导出宏（Export Macros），如果作为动态链接库（DLL）在 Visual Studio 中编译时会遇到符号无法导出的问题。用户希望代码在物理结构上完全分开，并作为标准的库进行调用，且完美支持 VS 编译。

## What Changes
- **BREAKING**: 将所有核心业务逻辑的源文件和头文件移动到新的目录 `src/core/` 下。
- **BREAKING**: 将所有 UI 相关的源文件和头文件移动到新的目录 `src/ui/` 下。
- 在 `src/core/` 中建立独立的 `CMakeLists.txt`，用于编译核心库，并添加宏以支持生成动态链接库（Shared Library）。
- 在 `src/core/` 的头文件（如 `solvespace_core.h`）中添加跨平台的导出宏 `SOLVESPACE_CORE_API`（处理 `__declspec(dllexport)` 和 `__declspec(dllimport)`），以支持 Visual Studio 编译动态库。
- 在 `src/core/` 和 `src/ui/` 中分别设置和引入**预编译头（Precompiled Headers）**，如 `stdafx.h` 或使用 CMake 3.16+ 的 `target_precompile_headers` 以加速 Visual Studio 下的编译速度。
- 在 `src/ui/` 中建立独立的 `CMakeLists.txt`，用于编译界面可执行程序，并链接到 `core` 库。
- 修改项目根目录及 `src/` 目录的 `CMakeLists.txt` 以支持新的目录结构。

## Impact
- Affected specs: 无
- Affected code: `src/` 目录下的所有文件结构将被重组，相关的 `CMakeLists.txt` 将被重写，核心类的类定义将添加导出宏。

## ADDED Requirements
### Requirement: 物理隔离与动态库支持
系统必须在文件系统层面上将核心代码与 UI 代码分开，并支持在 Visual Studio 下作为独立的动态库/静态库进行编译。

#### Scenario: Success case
- **WHEN** 开发者使用 Visual Studio 生成项目文件并编译时
- **THEN** 核心代码会被编译为独立的 `solvespace_core.dll` 和 `solvespace_core.lib`（或相应的静态库），且 UI 程序成功链接并运行。
