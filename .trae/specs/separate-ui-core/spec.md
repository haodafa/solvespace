# 界面和核心业务逻辑分离设计说明

## Why
目前 SolveSpace 的界面逻辑（渲染、窗口管理、事件处理）与核心业务逻辑（草图绘制、约束求解、文件读写、几何生成、模型导出）紧密耦合在 `SolveSpaceUI` 类和全局访问实例（如 `SS`、`SK`）中。这种耦合使得业务逻辑无法被轻易地重用、测试，或嵌入到其他独立程序中。

## What Changes
- **BREAKING**: 将所有非界面的业务逻辑从 `SolveSpaceUI` 中抽离，构建一个新的 `CoreApplication`（或 `SolveSpaceCore`）类。
- 将文件 I/O（保存/加载/导入/导出）、撤销/重做栈（Undo/Redo）、约束求解（`System`）、草图状态（`Sketch`）及网格生成逻辑移动到核心层。
- 解耦绘图相关代码（如 `draw.cpp`, `drawentity.cpp`, `drawconstraint.cpp`），使它们接受 `CoreApplication` 实例作为上下文，而不是依赖全局的 `SS`。
- 定义清晰的 C++ API 接口，允许在没有任何窗口系统（Qt、GTK、macOS、HTML 等）的环境下独立实例化和使用核心逻辑。
- 更新现有的各平台 GUI 代码（如 `guiqt.cpp`, `guigtk.cpp` 等），使其仅作为 `CoreApplication` 的外壳。

## Impact
- Affected specs: 无
- Affected code: `src/solvespace.h`, `src/solvespace.cpp`, `src/gui.h`, `src/draw*.cpp`, `src/platform/gui*.cpp`，以及所有访问全局 `SS` 和 `SK` 的核心文件。

## ADDED Requirements
### Requirement: 可嵌入的核心 API
系统必须提供一个解耦的 `CoreApplication` 类，可以在不初始化任何 UI 或窗口系统的情况下实例化。

#### Scenario: Success case
- **WHEN** 第三方程序实例化 `CoreApplication` 并加载一个 `.slvs` 文件
- **THEN** 它可以成功解析文件、生成网格，并导出为 STL 等格式，全程没有任何 UI 依赖或错误。

## MODIFIED Requirements
### Requirement: 界面独立性
各平台 GUI（Qt、GTK、HTML、macOS）必须且仅通过 `CoreApplication` 接口与核心逻辑进行交互，不再共享单一庞大的 `SolveSpaceUI` 状态。
