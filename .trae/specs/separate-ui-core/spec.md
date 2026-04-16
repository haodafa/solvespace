# 界面和核心业务逻辑分离设计说明

## Why
目前 SolveSpace 的界面逻辑（渲染、窗口管理、事件处理）与核心业务逻辑（草图绘制、约束求解、文件读写、几何生成、模型导出）紧密耦合在 `SolveSpaceUI` 类和全局访问实例（如 `SS`、`SK`）中。这种耦合使得业务逻辑无法被轻易地重用、测试，或嵌入到其他独立程序中。为了支持未来在第三方程序中的嵌入，我们需要将它们完全分离，同时**在改造完成后，必须先使用现有的界面进行集成，确保所有原有功能准确无误**。

## What Changes
- **BREAKING**: 将所有非界面的业务逻辑从 `SolveSpaceUI` 中抽离，构建一个新的 `CoreApplication`（或 `SolveSpaceCore`）类。
- 将文件 I/O（保存/加载/导入/导出）、撤销/重做栈（Undo/Redo）、约束求解（`System`）、草图状态（`Sketch`）及网格生成逻辑移动到核心层。
- 解耦绘图相关代码（如 `draw.cpp`, `drawentity.cpp`, `drawconstraint.cpp`），使其接受 `CoreApplication` 实例作为只读的上下文数据，切断对全局 `SS` 的依赖。
- 定义清晰的 C++ API 接口，允许在没有任何窗口系统（Qt、GTK、macOS、HTML 等）的环境下独立实例化和使用核心逻辑。
- 更新现有的各平台 GUI 代码（如 `guiqt.cpp`, `guigtk.cpp` 等），作为 `CoreApplication` 的使用者（Consumer）进行重新集成。

## 修改可能导致的问题及详细设计 (Detailed Review and Design)
1. **渲染与核心数据结构的强依赖问题**：
   - **问题**：原有的 OpenGL/Cairo 渲染代码深度依赖于核心的实体、约束、草图参数，且直接通过全局变量访问。
   - **设计/解决**：`CoreApplication` 需要暴露一个“只读的当前模型状态（Model State）”接口。渲染层（GraphicsWindow）通过传递核心实例指针来遍历渲染数据，而不是直接耦合。
2. **交互式操作（拖拽、高亮）的实时性问题**：
   - **问题**：在草图中拖拽节点时，UI 会频繁触发核心求解器（Solver），如果分离不当可能导致通信开销或状态不同步。
   - **设计/解决**：核心层提供 `UpdateParamAndSolve()` 的高效 API。UI 层捕获鼠标事件后，直接调用核心层 API，随后核心层返回“是否需要重绘”的标志位，UI 再根据标志位更新界面。
3. **Undo/Redo（撤销/重做）与 UI 状态同步问题**：
   - **问题**：撤销/重做操作会改变整个草图状态，UI 的属性面板（TextWindow）可能未能及时刷新。
   - **设计/解决**：核心层管理完整的 Undo/Redo 栈。执行撤销操作后，核心层触发状态变更回调（或由 UI 显式调用 Refresh 检查），UI 层接收到信号后全面刷新属性面板和图形窗口。
4. **现有界面的无损集成**：
   - **问题**：改造范围大，可能导致原有 SolveSpace 的某些边缘功能（如快捷键、特定导出选项）失效。
   - **设计/解决**：集成阶段必须保留现有所有的 UI 入口。在 `gui.cpp` 层面建立一个“胶水层（Adapter）”，将原有的全局调用转发给 `CoreApplication` 实例，以最大程度减少对各平台原生窗口代码的修改，确保功能 100% 回归。

## Impact
- Affected specs: 无
- Affected code: `src/solvespace.h`, `src/solvespace.cpp`, `src/gui.h`, `src/draw*.cpp`, `src/platform/gui*.cpp`，以及所有访问全局 `SS` 和 `SK` 的核心文件。

## ADDED Requirements
### Requirement: 可嵌入的核心 API 与无损集成
系统必须提供一个解耦的 `CoreApplication` 类，且当前的 SolveSpace 界面必须能够完全基于该类重新集成并正常工作。

#### Scenario: 现有界面回归测试
- **WHEN** 编译完成并运行现有的 SolveSpace GUI 程序
- **THEN** 程序能够正常启动，草图绘制、约束添加、3D 旋转、撤销重做、文件保存等所有功能表现与改造前完全一致。
