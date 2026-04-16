# Tasks
- [x] Task 1: 创建核心应用类: 定义 `SolveSpaceCore` 类以封装核心业务逻辑。
  - [x] SubTask 1.1: 将文档状态（`sys`, `SK`, `undo`, `redo`, `clipboard`）从 `SolveSpaceUI` 迁移至 `SolveSpaceCore`。
  - [x] SubTask 1.2: 将文件 I/O 和模型导出方法迁移至 `SolveSpaceCore`。
  - [x] SubTask 1.3: 将配置参数（单位、网格间距等）迁移至 `SolveSpaceCore`。
- [x] Task 2: 重构全局访问: 移除业务逻辑文件中对全局变量 `SS` 和 `SK` 的依赖。
  - [x] SubTask 2.1: 在约束求解和几何生成函数中传入 `SolveSpaceCore` 引用。
  - [x] SubTask 2.2: 重构绘图相关函数，使其接受上下文/核心对象，而非使用全局 `SS`。
- [x] Task 3: 与现有界面集成及回归测试: 使用现有的 UI 框架重新集成 `SolveSpaceCore`，确保功能无损。
  - [x] SubTask 3.1: 编写一个 UI 与 Core 之间的胶水层（Adapter），保证原有事件（鼠标点击、菜单调用）能平滑路由到核心对象。
  - [x] SubTask 3.2: 更新各平台 UI（如 `guiqt.cpp`, `guigtk.cpp`, `guihtml.cpp`）持有 `SolveSpaceCore` 的实例，并验证能否成功编译。
  - [x] SubTask 3.3: 进行全面功能回归测试，检查渲染、草图编辑、约束求解、文件加载保存、Undo/Redo 是否与原版表现一致。
- [x] Task 4: 修复集成问题与代码审查: 对改造中发现的状态不同步、崩溃或渲染失效等问题进行专门的 Code Review 和修复。
  - [x] SubTask 4.1: 修复界面拖拽参数更新不及时、或者撤销操作导致的界面脏读（Dirty Read）问题。
  - [x] SubTask 4.2: 审核渲染层对核心模型数据的只读访问是否完全符合线程与状态安全。
- [x] Task 5: 将核心层抽离为独立的 CMake Target: 在 `CMakeLists.txt` 中创建一个静态或动态库 Target `solvespace_core`，该目标仅编译业务逻辑，无任何 UI 依赖。

# Task Dependencies
- [Task 2] depends on [Task 1]
- [Task 3] depends on [Task 2]
- [Task 4] depends on [Task 3]
- [Task 5] depends on [Task 4]
