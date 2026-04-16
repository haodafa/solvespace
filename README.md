# SolveSpace - 解耦版架构设计与集成指南

本项目是对开源参数化 3D CAD 软件 **SolveSpace** 的架构重构版本。主要目的是将**核心业务逻辑**（Core）与**图形用户界面**（UI）在物理文件层面上进行完全分离，使您可以将参数化几何引擎、约束求解器、网格生成及文件 I/O 直接作为**动态/静态链接库**嵌入到您自己的程序中。

---

## 🏗 架构设计与调用关系

重构后的系统采用了严格的“UI 消费 Core”的层级架构，以下是整体的架构图，帮助您理解各个组件之间的关系和数据流向：

```mermaid
graph TD
    subgraph "Your Application (第三方程序)"
        App[自定义客户端 / 服务端]
    end

    subgraph "SolveSpace UI (src/ui)"
        UI_Entry[solvespace.cpp (主入口)]
        UI_Platform[Platform (Qt/GTK/Win32/Mac)]
        UI_Render[Renderer (OpenGL/Cairo)]
        UI_Event[Events (鼠标/键盘交互)]
        
        UI_Entry --> UI_Platform
        UI_Platform --> UI_Event
        UI_Render -->|读取渲染数据| Core_Doc
    end

    subgraph "SolveSpace Core Library (src/core)"
        Core_App[SolveSpaceCore (核心上下文)]
        
        subgraph "核心业务逻辑 (Business Logic)"
            Core_Doc[Sketch (模型状态/草图/选择集)]
            Core_Solver[System (几何约束求解器)]
            Core_Mesh[BSP/Mesh/Triangulate (几何网格生成)]
            Core_Undo[UndoRedo (历史记录管理)]
            Core_IO[File I/O (加载/保存/导出)]
        end
        
        Core_App --> Core_Doc
        Core_App --> Core_Solver
        Core_App --> Core_Mesh
        Core_App --> Core_Undo
        Core_App --> Core_IO
        
        Core_Event[UpdateParamAndSolve (解算触发)] --> Core_Solver
    end

    subgraph "Solver C API (src/slvs)"
        Slvs[slvs.h (低级约束求解器接口)]
    end

    %% 依赖关系
    App == 链接并调用 ==> Core_App
    UI_Event == 调用 ==> Core_Event
    Core_Solver -.-> Slvs
    
    classDef core fill:#d4edda,stroke:#28a745,stroke-width:2px;
    classDef ui fill:#cce5ff,stroke:#0056b3,stroke-width:2px;
    classDef thirdparty fill:#fff3cd,stroke:#856404,stroke-width:2px;
    
    class Core_App,Core_Doc,Core_Solver,Core_Mesh,Core_Undo,Core_IO,Core_Event core;
    class UI_Entry,UI_Platform,UI_Render,UI_Event ui;
    class App thirdparty;
```

### 架构组件说明

1. **SolveSpace Core Library (`src/core`)**
   - 这是项目的“心脏”，已被完全独立出来，去除了所有的 `extern SolveSpaceUI` 全局依赖，对外统一提供 `SolveSpaceCore` 类。
   - **线程与状态安全**：内置 `stateMutex` 锁保护，防止在后台求解或 Undo/Redo 时由于界面渲染导致的内存越界或脏读。
   - **跨平台导出**：所有需要暴露给外部的类都添加了 `SOLVESPACE_CORE_API` 宏（Windows 下为 `__declspec(dllexport)`），直接生成动态库。

2. **SolveSpace UI (`src/ui`)**
   - 现有的应用程序界面，它目前仅仅是 `SolveSpaceCore` 的一个消费者。
   - 包含特定于平台的窗口代码（Win32、macOS、GTK）以及渲染层（OpenGL、Cairo）。渲染层只对核心层中的模型进行“只读访问”。

3. **低级 Solver 库 (`src/slvs`)**
   - 最底层的代数约束求解器，供 `SolveSpaceCore` 中的 `System` 调用。

---

## 🚀 目录结构精简说明

为了保持项目清爽并专注核心业务，无用的模块已被剔除或归档：

- `src/core/`：核心业务逻辑（约束、几何、网格、文件导出）。
- `src/ui/`：现有的界面程序代码。
- `src/slvs/`：底层解算器库。
- `extlib/`：必需的第三方库（如 mimalloc, eigen, libdxfrw 等）。
- `vs-project/`：为您手动生成的可直接用于 Visual Studio 编译的工程文件配置（内含 `.sln` 和 `.vcxproj`）。
- `scripts/`：存放开发、重构和自动生成的辅助脚本。

---

## 🛠 编译指南 (Visual Studio / Windows)

为了让您能够非常容易地在 Windows 下开发和集成，本代码库对 VS 编译做了深度支持（预编译头、导出宏处理）。

### 方法一：使用内置的纯净版 VS 项目（推荐）
如果您只想直接编译核心库（不依赖 CMake 环境）：
1. 打开 `vs-project/SolveSpace.sln`。
2. 该解决方案中包含了 `solvespace_core` 动态库项目，已经为您配置好了 `SOLVESPACE_CORE_EXPORTS` 宏及所需的所有预处理头文件与附加包含目录。
3. 选择 **Debug** 或 **Release**（x64），点击 **生成解决方案** 即可生成 `solvespace_core.dll` 和 `solvespace_core.lib`。

### 方法二：使用 CMake 生成完整解决方案（包含界面）
如果您希望同时编译出带有界面的 `solvespace.exe` 以便对比和测试：
1. 打开命令提示符（CMD / PowerShell）。
2. 进入项目根目录。
3. 运行 CMake 命令生成 VS 工程：
   ```cmd
   cmake -B build-vs -S . -G "Visual Studio 17 2022" -A x64
   ```
4. 进入 `build-vs` 目录，打开生成的 `solvespace.sln`。
5. 编译 `solvespace_core` 目标（生成库），或者编译 `solvespace` 目标（生成可执行程序）。

## 💡 如何在您的程序中嵌入？
1. 在您的项目中链接生成的 `solvespace_core.lib`。
2. 将 `src/core` 及 `extlib` 的包含路径（Include Directories）加入到您的项目中。
3. `#include "solvespace_core.h"`，实例化 `SolveSpaceCore` 类。
4. 您现在可以直接调用核心类的方法，比如：
   ```cpp
   SolveSpaceCore coreApp;
   // 加载模型
   coreApp.LoadFromFile("test_model.slvs");
   // 修改参数并重新解算
   // ...
   // 导出为 STL 或执行网格处理
   coreApp.ExportMeshTo("output.stl");
   ```
