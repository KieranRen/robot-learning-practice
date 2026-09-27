# M2 MuJoCo 实验 - Review Model

[English](README.md) | [中文](README_zh.md)

---

## 概览

这个实验将目前学习过的 MuJoCo 基础内容整合到一个简单的仿真场景中。

实验目标是复习并串联以下知识：

- 仿真环境配置
- 视觉设置
- Asset 资源
- Material 材质
- Worldbody
- Body
- Geom
- Site
- 相对坐标
- Free Joint
- 重力
- 质量
- 摩擦
- 基础碰撞行为

实验文件为：

```text
review_model.xml
```

---

## 实验结构

这个场景包括：

- 一个地面平面
- 自定义棋盘格纹理
- 地面材质
- 一个圆柱形 support body
- 一个嵌套的 motor body
- 一个 site 标记点
- 一个自由下落的小球
- 一个固定 box
- 一个固定 capsule
- 重力
- 摩擦
- 多种 geom 类型

简化后的层级结构为：

```text
worldbody
├── floor
├── support
│   └── motor
│       └── motor_top site
├── falling_ball
├── box
└── capsule
```

---

## 1. 仿真参数

实验使用：

```xml
<option timestep="0.002"
        gravity="0 0 -9.81"
        integrator="implicitfast"/>
```

表示：

```text
timestep = 0.002 s
gravity = (0, 0, -9.81)
integrator = implicitfast
```

因此仿真会以较小的时间步长运行，同时重力沿 z 轴负方向作用。

---

## 2. 视觉设置

场景中还加入了基础视觉设置，例如：

```xml
<visual>
    <global realtime="1"/>
    <quality shadowsize="4096"/>
    <headlight diffuse="1 1 1"
               specular="0.5 0.5 0.5"
               active="1"/>
</visual>
```

这些设置主要控制：

- 实时播放
- 阴影质量
- 光照
- Viewer 中的显示效果

---

## 3. Asset 资源

实验在 `<asset>` 中定义了可重复使用的资源。

其中包括：

- Skybox 天空背景
- Checker 地面纹理
- Floor 地面材质

例如：

```xml
<texture name="floor_tex"
         type="2d"
         builtin="checker"
         rgb1="0.2 0.2 0.2"
         rgb2="0.8 0.8 0.8"
         width="512"
         height="512"/>
```

之后地面材质使用这个纹理：

```xml
<material name="floor_mat"
          texture="floor_tex"
          texrepeat="5 5"
          reflectance="0.2"/>
```

这里复习了：

```text
texture
↓
material
↓
geom
```

这一关系。

---

## 4. Ground Plane 地面

场景中包含一个地面平面：

```xml
<geom name="floor"
      type="plane"
      size="5 5 0.1"
      material="floor_mat"
      friction="1 0.005 0.0001"/>
```

这个 geom：

- 使用 `plane` 几何体
- 使用自定义 `floor_mat`
- 设置了接触摩擦
- 作为整个场景的地面

---

## 5. Support Body

主要支撑刚体定义为：

```xml
<body name="support"
      pos="0 0 1">
```

这表示 support body 的局部坐标系原点位于世界坐标：

```text
(0, 0, 1)
```

在这个 body 上附着了一个 cylinder geom。

例如：

```xml
<geom type="cylinder"
      size="0.15 0.5"
      mass="2"
      rgba="0.2 0.2 0.8 1"/>
```

这里复习了：

```text
body
→ 刚体 + 局部坐标系

geom
→ 附着在 body 上的实际几何形状
```

---

## 6. 嵌套的 Motor Body

在 support body 内部又嵌套了一个 motor body：

```xml
<body name="motor"
      pos="0 0 0.6">
```

因为 `motor` 写在 `support` 内部，所以它的位置是相对于 support 的局部坐标系定义的。

因此：

```text
support z = 1.0
motor 相对 z = 0.6
```

如果没有旋转：

```text
motor 世界坐标 z = 1.6
```

这就是父子 body 层级关系的一个简单例子。

---

## 7. Site 标记点

motor body 上还附着了一个 site：

```xml
<site name="motor_top"
      pos="0 0 0.25"
      size="0.05"
      rgba="0 1 0 1"/>
```

Site 不是一个新的刚体。

它只是附着在 motor 上的辅助标记。

以后可以用于：

- 末端执行器位置
- 传感器位置
- 目标点
- 参考位置
- 力作用点

---

## 8. 自由下落小球

实验中加入了一个可以自由运动的球：

```xml
<body name="falling_ball"
      pos="1 0 2">

    <freejoint/>

    <geom type="sphere"
          size="0.2"
          mass="1"
          friction="0.8 0.005 0.0001"
          rgba="1 0.5 0 1"/>

</body>
```

其中最重要的是：

```xml
<freejoint/>
```

它允许这个 body 在三维空间中自由运动。

因此这个 body 可以受到：

- 重力
- 碰撞
- 接触
- 摩擦

的影响。

如果没有 `freejoint` 或其他 joint，这个 body 会固定在父级上，不会自由下落。

---

## 9. Box 几何体

场景中包含一个 box：

```xml
<geom name="box"
      type="box"
      pos="-1 0 0.25"
      size="0.3 0.3 0.25"
      rgba="0.2 0.8 0.2 1"
      mass="2"/>
```

对于 box：

```text
size = 半尺寸
```

所以：

```text
size = (0.3, 0.3, 0.25)
```

表示完整尺寸为：

```text
0.6 × 0.6 × 0.5 m
```

因为 box 的高度是：

```text
0.5 m
```

所以把它的中心放在：

```text
z = 0.25
```

时，它的底面大约正好位于：

```text
z = 0
```

也就是地面上。

---

## 10. Capsule 几何体

场景中还加入了一个 capsule：

```xml
<geom name="capsule"
      type="capsule"
      pos="0 -1 0.6"
      size="0.15 0.4"
      rgba="0.7 0.3 0.9 1"
      mass="1"/>
```

对于 capsule：

```text
第一个 size
→ 半径

第二个 size
→ 中间圆柱部分的半长度
```

所以：

```text
半径 = 0.15 m
圆柱部分半长度 = 0.4 m
```

这个部分用于复习另一种常见的 MuJoCo geom 类型。

---

## 11. 本实验复习的知识

这个实验将目前学习过的主要 MuJoCo XML 元素结合在了一起：

```text
<mujoco>
<option>
<visual>
<asset>
<texture>
<material>
<worldbody>
<body>
<geom>
<site>
<freejoint>
```

同时复习了：

- `timestep`
- `gravity`
- `integrator`
- `pos`
- `size`
- `rgba`
- `mass`
- `friction`
- 不同 geom 类型
- 父子 body 层级
- 相对坐标关系

---

## 12. 运行实验

首先激活 MuJoCo 环境：

```bash
conda activate mujoco_env
```

进入 XML 文件所在目录：

```bash
cd /d "C:\Users\A\Desktop\Robot Learning\mujoco\model"
```

然后运行：

```bash
python -m mujoco.viewer --mjcf review_model.xml
```

MuJoCo Viewer 应该会加载该场景。

开始仿真后，自由球体会在重力作用下下落，并与地面发生接触。

---

## 核心理解

这个实验将 MuJoCo 的“环境配置”部分和“模型构建”部分连接了起来。

可以这样总结：

```text
option
→ 控制物理仿真参数

visual
→ 控制显示效果

asset
→ 提前准备可重复使用的资源

worldbody
→ 包含整个物理场景

body
→ 定义刚体和局部坐标系

geom
→ 定义实际几何形状

site
→ 定义辅助参考标记

joint / freejoint
→ 定义 body 可以如何运动
```

---

## 来源

本实验基于以下上游仓库中学习到的相关概念：

https://github.com/Albusgive/mujoco_learning.git

原始仓库及教学材料归对应作者所有。

本实验文件和说明文档是我在学习过程中的个人实践、整理与理解，并不是对上游仓库内容的直接复制。