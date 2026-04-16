# Tasks
- [ ] Task 1: 创建核心应用类: 定义 `SolveSpaceCore` 类以封装核心业务逻辑。
  - [ ] SubTask 1.1: 将文档状态（`sys`, `SK`, `undo`, `redo`, `clipboard`）从 `SolveSpaceUI` 迁移至 `SolveSpaceCore`。
  - [ ] SubTask 1.2: 将文件 I/O 和模型导出方法迁移至 `SolveSpaceCore`。
  - [ ] SubTask 1.3: 将配置参数（单位、网格间距等）迁移至 `SolveSpaceCore`。
- [ ] Task 2: 重构全局访问: 移除业务逻辑文件中对全局变量 `SS` 和 `SK` 的依赖。
  - [ ] SubTask 2.1: 在约束求解和几何生成函数中传入 `SolveSpaceCore` 引用。
  - [ ] SubTask 2.2: 重构绘图相关函数，使其接受上下文/核心对象，而非使用全局 `SS`。
- [ ] Task 3: 更新各平台 GUI: 调整各平台特定的 UI 代码以适配新的 `SolveSpaceCore` API。
  - [ ] SubTask 3.1: 更新 `guiqt.cpp` 以持有 `SolveSpaceCore` 实例。
  - [ ] SubTask 3.2: 同样更新 `guigtk.cpp`, `guimac.mm` 及 `guihtml.cpp`。
  - [ ] SubTask 3.3: 确保事件处理程序（鼠标、键盘）正确映射至核心 API 调用。
- [ ] Task 4: 将核心层抽离为独立的 CMake Target: 在 `CMakeLists.txt` 中创建一个静态或动态库 Target `solvespace_core`，该目标仅编译业务逻辑，无任何 UI 依赖。

# Task Dependencies
- [Task 2] depends on [Task 1]
- [Task 3] depends on [Task 2]
- [Task 4] depends on [Task 1] and [Task 2]
