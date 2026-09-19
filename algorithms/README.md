# Algorithms

这里维护尽量与具体机器人模型和仿真器解耦的算法实现。`v0.2.0` 提供 [geometry/](geometry/README.md) 的旋转、刚体变换、逆变换与点坐标换算，用于 M1 的最小数值实践。`v0.1.0` 不包含该实现。

仿真模型、场景和可复用运行组件由 `simulation/` 维护；项目实验设置与整理结果随 `projects/` 保存。本库不建设直接执行真机的接口，完整职责见 [目录总览](../docs/repository_structure.md)。

计划主题包括下面几类。

- `geometry/` 已建设最小旋转与变换工具，更广的数值工具按实际问题补充
- `kinematics/` FK、IK、Jacobian 与微分运动学
- `trajectory/` 时间参数化与轨迹生成
- `controllers/` 关节、笛卡尔、阻抗、导纳与力控制
- `planning/` 运动与操作规划
- `perception/` 观测处理、状态与姿态估计接口
- `learning/` 数据集、策略、训练与评价接口

创建主题目录时需要同时加入 README、最小可运行实现和测试，避免用空目录表示进度。核心算法应保留公式、变量、坐标系与代码之间的对应关系。
