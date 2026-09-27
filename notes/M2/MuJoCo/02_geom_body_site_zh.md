# 02 - Geom、Body 与 Site

[English](02_geom_body_site.md) | [中文](02_geom_body_site_zh.md)

---

## 概览

本笔记记录 MuJoCo 中与几何体、刚体、父子层级、接触属性和 Site 标记点相关的基础概念。

本节内容包括：

- `geom`
- 几何体类型
- `size`
- `pos`
- `rgba`
- `material`
- `mass`
- `density`
- `friction`
- `condim`
- `contype`
- `conaffinity`
- `fromto`
- `body`
- Body 父子层级
- 相对坐标
- `site`

---

## 1. Geom

`<geom>` 用于定义 MuJoCo 中的几何物体。

一个 geom 可以描述：

- 形状
- 尺寸
- 位置
- 朝向
- 颜色
- 材质
- 质量相关属性
- 碰撞属性
- 摩擦属性

一个简单示例：

```xml
<geom type="sphere"
      size="0.2"
      rgba="1 0 0 1"/>
```

这表示一个半径为 `0.2 m` 的红色球体。

可以简单理解为：

```text
geom
→ 物体的实际几何形状
```

---

## 2. 常见几何体类型

MuJoCo 中常见的 geom 类型包括：

- `plane`
- `sphere`
- `box`
- `cylinder`
- `capsule`
- `mesh`

例如：

```xml
<geom type="box"
      size="0.3 0.2 0.1"/>
```

---

## 3. Size

`size` 的含义取决于 geom 的类型。

### Sphere

```xml
<geom type="sphere"
      size="0.2"/>
```

对于 sphere：

```text
size = 半径
```

因此：

```text
半径 = 0.2 m
直径 = 0.4 m
```

---

### Box

```xml
<geom type="box"
      size="0.3 0.2 0.1"/>
```

对于 box，三个数值都是半尺寸。

所以完整尺寸为：

```text
x = 0.6 m
y = 0.4 m
z = 0.2 m
```

也就是说：

```text
box size
→ x 方向半长
→ y 方向半长
→ z 方向半长
```

---

### Cylinder

```xml
<geom type="cylinder"
      size="0.1 0.5"/>
```

对于 cylinder：

```text
第一个值
→ 半径

第二个值
→ 半长度
```

因此：

```text
半径 = 0.1 m
完整圆柱长度 = 1.0 m
```

---

### Capsule

```xml
<geom type="capsule"
      size="0.15 0.4"/>
```

对于 capsule：

```text
第一个值
→ 半径

第二个值
→ 中间圆柱部分的半长度
```

因此中间圆柱部分完整长度为：

```text
0.8 m
```

另外两端的半球还会增加总长度。

---

## 4. Position

`pos` 用于定义元素的位置。

例如：

```xml
<geom type="sphere"
      pos="1 0 2"
      size="0.2"/>
```

表示：

```text
x = 1
y = 0
z = 2
```

如果一个 geom 直接写在 `worldbody` 中，那么它的位置相对于世界坐标系。

如果 geom 写在某个 `body` 中，那么它的位置相对于该 body 的局部坐标系。

---

## 5. RGBA

`rgba` 用于控制颜色和透明度。

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

也就是完全不透明的红色。

另一个例子：

```xml
rgba="0 1 0 0.5"
```

表示半透明绿色。

---

## 6. Material

geom 可以使用在 `<asset>` 中提前定义好的材质。

例如：

```xml
<geom type="plane"
      material="floor_mat"/>
```

这个材质可能之前定义为：

```xml
<material name="floor_mat"
          texture="floor_tex"/>
```

它们之间的关系是：

```text
texture
↓
material
↓
geom
```

---

## 7. Mass 与 Density

MuJoCo 可以通过 `mass` 或 `density` 定义 geom 的质量属性。

### Mass

例如：

```xml
<geom type="sphere"
      size="0.2"
      mass="1"/>
```

表示直接设置：

```text
质量 = 1 kg
```

---

### Density

例如：

```xml
<geom type="sphere"
      size="0.2"
      density="1000"/>
```

MuJoCo 会根据几何体体积和 density 自动计算质量。

所以：

```text
mass
→ 直接规定总质量

density
→ 根据体积计算质量
```

通常情况下，选择其中一种方式即可，不建议同时设置。

---

## 8. Friction

`friction` 用于控制接触摩擦。

例如：

```xml
friction="0.8 0.005 0.0001"
```

三个值分别对应：

```text
第一个值
→ 滑动摩擦

第二个值
→ 扭转摩擦

第三个值
→ 滚动摩擦
```

目前最重要的是第一个值。

滑动摩擦较大时，通常意味着：

```text
抓地力更强
→ 更不容易滑动
```

滑动摩擦较小时，通常意味着：

```text
抓地力更弱
→ 更容易滑动
```

---

## 9. Contact Dimension

`condim` 用于控制接触约束的维度。

可以先简化理解为：

```text
condim = 1
→ 只考虑法向接触
→ 不考虑摩擦

condim = 3
→ 法向接触 + 滑动摩擦

condim = 4
→ 再增加扭转摩擦

condim = 6
→ 再增加滚动摩擦
```

它决定 MuJoCo 在物体接触时需要考虑哪些类型的接触力。

---

## 10. Collision Filtering

MuJoCo 使用：

```text
contype
conaffinity
```

控制哪些 geom 之间允许发生碰撞。

它们可以理解为碰撞过滤器。

可以这样区分：

```text
condim
→ 接触发生后如何计算

contype / conaffinity
→ 两个 geom 是否允许发生接触
```

这在机器人建模中很有用。

例如：

```text
机器人某些 link
→ 需要和地面碰撞

但相邻 link
→ 可能不希望彼此碰撞
```

---

## 11. From-To Definition

`fromto` 可以用于快速定义两个点之间的细长几何体。

例如：

```xml
<geom type="capsule"
      fromto="0 0 0  0 0 1"
      size="0.1"/>
```

这表示创建一个从：

```text
点 A = (0, 0, 0)
```

到：

```text
点 B = (0, 0, 1)
```

的 capsule。

其半径为：

```text
0.1 m
```

这种方式非常适合：

- 机器人连杆
- 手臂
- 腿
- 杆件
- 结构件

使用 `fromto` 可以避免手动计算：

- 中心位置
- 长度
- 朝向

---

## 12. Body

`<body>` 表示一个刚体，同时定义一个局部坐标系。

例如：

```xml
<body name="support"
      pos="0 0 1">

    <geom type="cylinder"
          size="0.15 0.5"/>

</body>
```

可以这样理解：

```text
body
→ 刚体 + 局部坐标系

geom
→ 附着在 body 上的实际几何形状
```

---

## 13. Worldbody

Body 通常创建在：

```xml
<worldbody>
```

内部。

例如：

```xml
<worldbody>

    <body name="support"
          pos="0 0 1">

        <geom type="cylinder"
              size="0.15 0.5"/>

    </body>

</worldbody>
```

`worldbody` 可以理解为整个物理仿真世界的根节点。

所以：

```text
worldbody
→ 仿真世界

body
→ 世界中的刚体

geom
→ 附着在刚体上的实际几何形状
```

---

## 14. Body Hierarchy

Body 可以嵌套在另一个 body 中。

例如：

```xml
<body name="support"
      pos="0 0 1">

    <body name="motor"
          pos="0 0 0.6">

    </body>

</body>
```

结构为：

```text
world
└── support
    └── motor
```

子 body 的位置是相对于父 body 定义的。

在这个例子中：

```text
support 世界坐标 z = 1.0
motor 相对 support 的 z = 0.6
```

如果没有旋转：

```text
motor 世界坐标 z
= 1.0 + 0.6
= 1.6
```

这是 MuJoCo 机器人建模中非常重要的概念。

---

## 15. Relative Coordinates

Body 的层级关系实际上形成了一棵坐标系树。

例如：

```text
world
└── support
    └── motor
        └── camera
```

每个子 body 都有自己的局部坐标系。

它的位置和姿态相对于父 body 定义。

因此可以理解成：

```text
父坐标变换
↓
子坐标变换
↓
下一层子坐标变换
↓
...
```

这个概念和机器人正运动学密切相关。

---

## 16. Geom Inside a Body

一个 body 可以包含一个或多个 geom。

例如：

```xml
<body name="robot_part">

    <geom type="box"
          size="0.2 0.1 0.1"/>

    <geom type="cylinder"
          pos="0 0 0.3"
          size="0.05 0.2"/>

</body>
```

这两个 geom 都属于同一个刚体。

所以：

```text
一个 body
→ 可以包含多个 geom
```

这对于构建复杂形状的刚体很有用。

---

## 17. Site

`<site>` 是附着在 body 上的辅助标记。

例如：

```xml
<site name="motor_top"
      pos="0 0 0.25"
      size="0.05"
      rgba="0 1 0 1"/>
```

Site 可以用于：

- 末端执行器标记
- 传感器位置
- 目标点
- 参考点
- 力作用点

可以这样理解：

```text
site
→ 附着在 body 上的标记点
```

它不是一个新的刚体。

---

## 18. Site 作为 Body 的子元素

考虑：

```xml
<body name="motor">

    <geom type="sphere"
          size="0.18"/>

    <site name="motor_top"
          pos="0 0 0.25"
          size="0.05"/>

</body>
```

结构为：

```text
motor
├── geom
└── site
```

Site 是 body 的子元素。

但是：

```text
site ≠ 子刚体
```

它不会创建一个新的刚体层级。

如果 motor 移动或旋转：

```text
geom 会跟着 motor 一起运动
site 也会跟着 motor 一起运动
```

因为它们都附着在同一个 body 上。

---

## 19. Practical Structure

一个简单的 MuJoCo 模型可能写成：

```xml
<worldbody>

    <geom name="floor"
          type="plane"/>

    <body name="support"
          pos="0 0 1">

        <geom type="cylinder"
              size="0.15 0.5"/>

        <body name="motor"
              pos="0 0 0.6">

            <geom type="sphere"
                  size="0.18"/>

            <site name="motor_top"
                  pos="0 0 0.25"
                  size="0.05"/>

        </body>

    </body>

</worldbody>
```

层级结构为：

```text
worldbody
├── floor
└── support
    ├── support geom
    └── motor
        ├── motor geom
        └── motor_top site
```

---

## 核心理解

这一节最重要的关系是：

```text
worldbody
→ 整个仿真世界

body
→ 刚体 + 局部坐标系

geom
→ 物体的实际几何形状

site
→ 辅助参考标记
```

层级关系可以理解为：

```text
world
↓
父 body
↓
子 body
↓
下一层子 body
```

而：

```text
geom
site
```

通常附着在某个 body 上。

另一个非常重要的区别是：

```text
body
→ 定义刚体层级和坐标系

geom
→ 定义物理几何形状和接触

site
→ 定义参考点或标记
```

---

## 来源

本学习部分基于以下上游仓库：

https://github.com/Albusgive/mujoco_learning.git

原始仓库及教学材料归对应作者所有。

本文件内容为我在学习过程中的个人整理、总结与理解，并不是对上游仓库内容的直接复制。