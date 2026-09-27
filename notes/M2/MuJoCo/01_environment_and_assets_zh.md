[English](01_environment_and_assets.md) | [中文](01_environment_and_assets_zh.md)

---

# 01 - 环境配置与资源

## 概览

本笔记记录 M2 阶段学习到的 MuJoCo 基础环境配置与资源相关内容。

本节内容包括：

- MuJoCo 根结构
- 编译器设置
- 仿真参数
- 视觉设置
- Asset 资源
- Texture 纹理
- Material 材质
- Mesh 网格模型
- Height Field 高度场
- Skybox 天空盒

---

## 1. MuJoCo 根结构

一个 MuJoCo XML / MJCF 模型通常都会写在下面这个根标签中：

```xml
<mujoco model="model_name">

    ...

</mujoco>
```

`<mujoco>` 是整个 MuJoCo 模型最外层的根元素。

例如：

```xml
<mujoco model="My Model">

</mujoco>
```

其中：

```text
model="My Model"
```

用于给整个模型设置一个便于识别的名称。

可以简单理解为：

```text
<mujoco>
→ 整个 MuJoCo 仿真模型的最外层容器
```

---

## 2. Compiler 编译器设置

`<compiler>` 用来控制 MuJoCo 如何解释模型中的某些参数。

例如：

```xml
<compiler angle="degree" autolimits="true"/>
```

目前学习到的主要参数包括：

### `angle`

```xml
angle="degree"
```

表示 XML 中的角度按照“度”来解释。

例如：

```text
90
```

表示：

```text
90°
```

如果写成：

```xml
angle="radian"
```

则角度按照弧度解释。

例如：

```text
1.57
```

大约表示：

```text
90°
```

---

### `autolimits`

```xml
autolimits="true"
```

表示 MuJoCo 可以根据模型中已经设置的范围参数，自动推断某些限制配置。

例如以后定义关节：

```xml
<joint range="-90 90"/>
```

MuJoCo 可以根据这个范围自动处理相应的关节限制设置。

目前只需要理解：

```text
autolimits
→ 帮助 MuJoCo 自动处理部分运动范围限制
```

---

## 3. Simulation Options 仿真参数

`<option>` 用于控制整个仿真的全局物理参数。

例如：

```xml
<option timestep="0.002"
        gravity="0 0 -9.81"
        integrator="implicitfast"/>
```

---

### `timestep`

```xml
timestep="0.002"
```

表示每进行一个 simulation step，仿真时间前进：

```text
0.002 s
```

因此：

```text
500 steps = 1 second
```

因为：

```text
500 × 0.002 = 1
```

可以把 `timestep` 理解成：

```text
仿真每一步向前推进多少时间
```

通常来说：

```text
timestep 越小
→ 仿真时间分辨率越高
→ 计算量越大

timestep 越大
→ 计算速度可能更快
→ 但仿真精度和稳定性可能降低
```

---

### `gravity`

```xml
gravity="0 0 -9.81"
```

表示重力向量：

```text
x = 0
y = 0
z = -9.81
```

因此重力沿 z 轴负方向作用。

可以写成：

```text
g = (0, 0, -9.81)
```

如果写：

```xml
gravity="0 0 0"
```

则表示：

```text
无重力环境
```

---

### `integrator`

`integrator` 决定 MuJoCo 如何通过数值方法，从当前时刻计算到下一个仿真时刻。

常见积分器包括：

- `Euler`
- `RK4`
- `implicit`
- `implicitfast`

例如：

```xml
integrator="implicitfast"
```

目前最重要的理解是：

```text
integrator
→ 决定运动状态如何随时间一步步更新
```

可以粗略理解为：

```text
当前状态
↓
数值积分
↓
下一时刻状态
```

---

### `solver`

`solver` 主要用于处理各种物理约束，例如：

- 接触
- 摩擦
- 关节约束
- 碰撞响应

常见 solver 类型包括：

- `PGS`
- `CG`
- `Newton`

可以这样区分：

```text
integrator
→ 决定系统的运动如何随时间推进

solver
→ 决定接触、摩擦、关节等约束如何求解
```

---

### `iterations`

例如：

```xml
iterations="100"
```

表示 solver 最多允许迭代 100 次。

求解器在处理接触、摩擦等约束时，通常需要不断迭代逼近结果。

可以理解为：

```text
第 1 次
→ 得到初步结果

第 2 次
→ 修正结果

第 3 次
→ 继续修正

...

最多 100 次
```

通常：

```text
iterations 增加
→ 可能提高求解精度或稳定性
→ 但也会增加计算量
```

---

### `tolerance`

例如：

```xml
tolerance="1e-8"
```

这个参数定义 solver 的停止误差阈值。

如果结果已经足够精确，那么 solver 可以在达到最大迭代次数之前提前停止。

所以：

```text
iterations
→ 最多允许计算多少次

tolerance
→ 精确到什么程度以后可以停止
```

---

## 4. Visual Settings 视觉设置

`<visual>` 用于控制 MuJoCo Viewer 中的视觉显示效果。

例如：

```xml
<visual>

    <global realtime="1"/>

    <quality shadowsize="4096"/>

    <headlight diffuse="1 1 1"
               specular="0.5 0.5 0.5"
               active="1"/>

</visual>
```

---

### `global`

例如：

```xml
<global realtime="1"/>
```

用于控制 Viewer 的全局显示参数。

其中：

```text
realtime="1"
```

可以理解为：

```text
Viewer 尽量让仿真时间和现实时间保持接近 1:1
```

例如现实中过 1 秒，仿真也尽量运行约 1 秒的仿真时间。

---

### `quality`

例如：

```xml
<quality shadowsize="4096"/>
```

用于控制画面渲染质量。

可能包括：

- 阴影质量
- 渲染细节
- 抗锯齿相关设置

通常：

```text
画质越高
→ 对计算性能要求越高
```

---

### `headlight`

例如：

```xml
<headlight diffuse="1 1 1"
           specular="0.5 0.5 0.5"
           active="1"/>
```

`headlight` 可以理解为一个跟随观察相机的光源。

重要参数包括：

```text
diffuse
→ 漫反射光颜色
```

```text
specular
→ 镜面反射高光
```

```text
active
→ 是否开启 headlight
```

例如：

```xml
active="1"
```

表示开启。

```xml
active="0"
```

表示关闭。

---

### RGBA

MuJoCo 中经常使用 RGBA 定义颜色。

```text
R = Red     = 红色
G = Green   = 绿色
B = Blue    = 蓝色
A = Alpha   = 透明度
```

例如：

```xml
rgba="1 0 0 1"
```

表示：

```text
R = 1
G = 0
B = 0
A = 1
```

也就是：

```text
完全不透明的红色
```

---

## 5. Asset 资源

`<asset>` 用于定义模型中可以重复使用的资源。

一个很重要的理解是：

> `asset` 不是“外部资源库”。

更准确地说：

```text
asset
→ 模型内部的资源定义区 / 素材准备区
```

这些资源既可以：

```text
从外部文件加载
```

也可以：

```text
由 MuJoCo 根据参数直接生成
```

所以可以这样理解：

```text
asset
→ 提前准备资源

worldbody / geom
→ 真正使用这些资源
```

---

## 6. Texture 纹理

`texture` 用于定义图片或表面纹理图案。

---

### 内置生成纹理

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

这里：

```text
builtin="checker"
```

表示让 MuJoCo 直接生成棋盘格纹理。

不需要任何外部图片文件。

其中：

```text
rgb1
rgb2
```

用于定义棋盘格的两种颜色。

---

### 外部纹理

例如：

```xml
<texture name="card_texture"
         type="2d"
         file="card.png"/>
```

表示从外部文件：

```text
card.png
```

中加载纹理。

因此 Texture 有两种常见来源：

```text
builtin
→ MuJoCo 自己生成

file
→ 从外部文件加载
```

---

## 7. Material 材质

`material` 用于控制物体表面的显示效果。

例如：

```xml
<material name="floor_mat"
          texture="floor_tex"
          texrepeat="5 5"
          reflectance="0.2"/>
```

这里创建了一个名为：

```text
floor_mat
```

的材质。

它使用之前定义的：

```text
floor_tex
```

纹理。

它们之间可以这样理解：

```text
texture
↓
material
↓
geom
```

也就是：

```text
纹理
↓
材质
↓
真正应用到几何体
```

例如：

```xml
<geom type="plane"
      material="floor_mat"/>
```

表示：

```text
这个 plane 使用 floor_mat 材质
```

---

## 8. Mesh 网格模型

`mesh` 是一种三维几何模型资源。

它通常可以从外部 3D 模型文件中加载。

例如：

```xml
<mesh name="forearm"
      file="forearm.stl"/>
```

这表示：

```text
加载 forearm.stl
并给这个 mesh 起名叫 forearm
```

之后可以通过：

```xml
<geom type="mesh"
      mesh="forearm"/>
```

真正使用这个模型。

因此流程可以理解成：

```text
STL / OBJ 文件
↓
asset 中定义 mesh
↓
geom 使用 mesh
```

这对于导入 CAD 软件生成的机器人零件非常重要。

例如：

```text
SolidWorks 建模
↓
导出 STL
↓
MuJoCo asset 加载
↓
geom 使用
```

---

## 9. Height Field 高度场

`hfield` 可以用于表示不平整地形。

例如：

```xml
<hfield name="terrain"
        file="terrain.png"
        size="10 10 1 1"/>
```

Height Field 可以用于：

- 崎岖地形
- 斜坡
- 户外机器人仿真
- 足式机器人测试
- 移动机器人越野测试

可以简单理解成：

```text
通过高度信息构建地形
```

---

## 10. Skybox 天空盒

`skybox` 用于创建包围整个仿真场景的背景环境。

例如使用外部图片：

```xml
<texture type="skybox"
         file="desert.png"/>
```

也可以让 MuJoCo 自己生成渐变天空：

```xml
<texture name="sky"
         type="skybox"
         builtin="gradient"
         rgb1="0.4 0.6 0.9"
         rgb2="0.9 0.9 0.9"
         width="512"
         height="512"/>
```

这样不需要任何外部图片，也可以生成天空背景。

---

## 核心理解

本节学习到的主要结构是：

```text
<mujoco>
    <compiler/>
    <option/>
    <visual/>
    <asset/>
</mujoco>
```

可以这样记忆：

```text
compiler
→ MuJoCo 如何解释模型

option
→ 物理仿真如何运行

visual
→ 仿真画面如何显示

asset
→ 提前准备后续需要使用的资源
```

其中一个非常重要的关系是：

```text
asset
→ 准备资源

worldbody
→ 建立仿真世界

body
→ 建立刚体

geom
→ 定义刚体或世界中的几何形状
```

---

## 来源

本学习部分基于以下上游仓库：

https://github.com/Albusgive/mujoco_learning.git

原始仓库及教学材料归对应作者所有。

本文件内容为我在学习过程中的个人整理、总结与理解，并不是对上游仓库内容的直接复制。