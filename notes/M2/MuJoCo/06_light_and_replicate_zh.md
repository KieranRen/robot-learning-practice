# MuJoCo Light 与 Replicate

[English](06_light_and_replicate.md) | [中文](06_light_and_replicate_zh.md)

---

## 概览

本笔记整理的是 Albusgive MuJoCo 学习来源中两个 MJCF 功能：

- `light`
- `replicate`

这两个功能作用完全不同：

```text
light
→ 控制场景如何被照亮和渲染

replicate
→ 自动复制重复的 MJCF 结构
```

其中：

```text
light
→ 主要影响可视化

replicate
→ 主要提高重复建模效率
```

---

# Part I - Light

## 1. `light` 是干什么的

MuJoCo 中的 `light` 用来控制 Viewer 中的光照效果。

它可以定义：

- 灯的位置
- 灯的方向
- 环境光
- 漫反射
- 镜面反射
- 阴影
- 距离衰减
- 聚光灯范围
- 跟踪行为

需要注意：

```text
light
```

主要影响的是显示效果。

它不会直接改变：

```text
mass
gravity
joint motion
actuator control
collision behavior
```

---

## 2. 基本 Light 示例

一个简单的 light 可以写成：

```xml
<light
    directional="true"
    pos="0 0 5"
    dir="0 0 -1"
    ambient="1 1 1"
    diffuse="1 1 1"
    specular="1 1 1"/>
```

可以理解为：

```text
light position
→ 在场景上方

light direction
→ 向下照

ambient / diffuse / specular
→ 控制不同类型的光照效果
```

---

## 3. `pos`

参数：

```xml
pos="x y z"
```

表示 light 的位置。

例如：

```xml
pos="0 0 5"
```

表示：

```text
灯位于 world origin 上方 5 个单位
```

对于非 directional light，这个位置非常重要。

---

## 4. `dir`

参数：

```xml
dir="x y z"
```

表示光线方向。

例如：

```xml
dir="0 0 -1"
```

表示：

```text
光朝负 z 方向照
```

也就是从上往下。

---

## 5. `directional`

如果：

```xml
directional="true"
```

表示使用 directional light。

它可以近似理解为太阳光：

```text
光线近似平行
```

这种情况下：

```text
direction
```

比灯的位置更加重要。

如果：

```xml
directional="false"
```

则更像一个局部光源，此时：

```text
pos
```

会明显影响照明效果。

---

## 6. `ambient`

`ambient` 表示环境光。

例如：

```xml
ambient="0.2 0.2 0.2"
```

表示：

> 即使物体表面没有直接面对灯，也会拥有一定基础亮度。

可以简单记成：

```text
ambient
→ 场景基础亮度
```

---

## 7. `diffuse`

`diffuse` 表示漫反射光。

这是物体表面正常被照亮时最主要的一部分。

可以理解为：

```text
表面越正对光源
↓
diffuse illumination 越明显
```

所以：

```text
diffuse
→ 普通受光亮度
```

---

## 8. `specular`

`specular` 表示镜面反射高光。

它会让物体表面出现：

```text
亮点
高光
反光
```

具体效果会和：

- 表面方向
- 灯光方向
- camera 方向
- material

有关。

可以简单记：

```text
specular
→ 高光 / 反光
```

---

## 9. Ambient / Diffuse / Specular 对比

最简单的记法：

```text
ambient
→ 基础亮度

diffuse
→ 正常受光亮度

specular
→ 表面高光
```

这三项主要影响显示效果，不直接影响动力学。

---

## 10. `castshadow`

参数：

```xml
castshadow="true"
```

表示这个 light 可以产生阴影。

如果：

```xml
castshadow="false"
```

那么：

```text
物体仍然可以被照亮
但是不会因为这个灯产生阴影
```

关闭阴影有时可以降低渲染开销。

---

## 11. `active`

参数：

```xml
active="true"
```

表示 light 当前启用。

如果：

```xml
active="false"
```

那么 light 虽然被定义了，但不会实际工作。

---

## 12. 聚光灯参数

局部光源还可以做成类似 spotlight 的效果。

常见参数：

```text
cutoff
exponent
```

### `cutoff`

`cutoff` 控制光锥角度。

可以理解为：

```text
cutoff 小
→ 光束更窄

cutoff 大
→ 光束更宽
```

---

### `exponent`

`exponent` 控制光束中心有多集中。

一般：

```text
exponent 越大
→ 中心越集中
→ 边缘衰减越明显
```

所以：

```text
cutoff
→ 管“有多宽”

exponent
→ 管“中心有多集中”
```

---

## 13. `attenuation`

局部光源会随着距离增加而变暗。

MuJoCo 可以通过：

```xml
attenuation="a b c"
```

控制这种衰减。

可以粗略理解成：

```text
light intensity
≈
1 / (a + b·d + c·d²)
```

其中：

```text
d
→ 灯和物体之间的距离
```

当前阶段不需要背公式。

只需要记：

```text
attenuation
→ 控制光随距离增加而减弱的速度
```

---

## 14. Light Modes

Light 可以设置不同 mode，例如：

```text
fixed
track
trackcom
targetbody
targetbodycom
```

这些模式主要决定：

> 灯和模型中 body 的关系。

---

## 15. `fixed`

如果：

```text
mode="fixed"
```

表示 light 固定在自己的父坐标系中。

它不会主动跟踪其他 body。

---

## 16. `track`

`track` 可以让 light 跟随某个 body 移动。

可以理解为：

```text
body 移动
↓
light 一起移动
```

例如可以把灯装在机器人上。

---

## 17. `trackcom`

`trackcom` 表示：

```text
跟踪 body 的 center of mass
```

也就是质心。

适合让 light 跟随某个物体整体移动。

---

## 18. `targetbody`

Light 可以始终指向一个特定 body。

例如：

```xml
<light
    mode="targetbody"
    target="arm0"
    .../>
```

表示：

```text
这个 light
→ 始终朝向 arm0
```

这对于机器人可视化很有用。

---

## 19. `targetbodycom`

这个模式和 `targetbody` 类似。

区别可以简单理解为：

```text
targetbody
→ 指向 body

targetbodycom
→ 指向 body 的质心
```

---

## 20. Light 总结

最重要的参数：

```text
pos
→ 灯在哪里

dir
→ 灯朝哪里

directional
→ 平行光还是局部光源

ambient
→ 基础亮度

diffuse
→ 普通受光效果

specular
→ 高光

castshadow
→ 是否产生阴影

mode / target
→ 是否跟踪或瞄准 body

cutoff / exponent
→ 聚光灯形状

attenuation
→ 距离衰减
```

最重要的一句话：

```text
light
→ 管显示
→ 不直接管机器人动力学
```

---

# Part II - Replicate

## 21. `replicate` 是干什么的

`replicate` 用来自动复制一段 MJCF 结构。

它很像 CAD 软件中的：

```text
Linear Pattern
Circular Pattern
Array
```

如果需要创建很多相同或相似对象，就不需要手动写几十遍 XML。

只需要：

```xml
<replicate>
```

就可以批量生成。

---

## 22. 基本 Replicate 示例

例如：

```xml
<replicate count="4" offset="0 0.5 0">
    <geom type="box" size="0.1 0.1 0.1"/>
</replicate>
```

表示：

```text
生成 4 个 box
```

并且每一个相对于前一个：

```text
y 方向增加 0.5
```

所以大约是：

```text
copy 0
→ y = 0

copy 1
→ y = 0.5

copy 2
→ y = 1.0

copy 3
→ y = 1.5
```

---

## 23. `count`

参数：

```xml
count="4"
```

表示最终生成：

```text
4 份
```

不是：

```text
原始 1 个
+
额外复制 4 个
=
5 个
```

而是：

```text
最终总数就是 4
```

---

## 24. `offset`

参数：

```xml
offset="x y z"
```

表示每一份相对于前一份的平移增量。

例如：

```xml
offset="0 0.5 0"
```

表示：

```text
x
→ 不变

y
→ 每次 +0.5

z
→ 不变
```

因此会形成一个直线阵列。

---

## 25. 沿 z 方向复制

例如：

```xml
<replicate count="5" offset="0 0 0.1">
```

可以生成：

```text
z = 0
z = 0.1
z = 0.2
z = 0.3
z = 0.4
```

也就是说：

```text
offset
```

可以沿任意方向使用。

---

## 26. `euler`

`euler` 表示每次复制后的旋转增量。

例如：

```xml
<replicate
    count="50"
    euler="0 0 0.1254">
```

如果当前模型使用：

```xml
<compiler angle="radian"/>
```

那么：

```text
每复制一个
→ 绕 z 轴再旋转 0.1254 rad
```

---

## 27. Circular Replication

如果一个对象先放在旋转中心之外：

```xml
<site
    pos="0.1 0 0"
    .../>
```

然后：

```xml
<replicate
    count="50"
    euler="0 0 0.1254">
```

那么这些 site 可以形成一个圆。

原因是：

```text
site 先离中心有一个半径
↓
每次复制都继续绕中心旋转
↓
位置沿圆周变化
```

其中：

```text
2π / 50
≈
0.12566 rad
```

所以：

```text
0.1254 rad
```

非常接近：

```text
一圈 / 50
```

---

## 28. 为什么原始位置不能在中心

如果原 site 是：

```xml
pos="0 0 0"
```

那么即使：

```text
euler 不断变化
```

它的位置也不会变化。

因为：

> 一个点如果就在旋转中心，那么绕中心旋转后仍然在中心。

所以形成圆周阵列需要：

```text
先有非零半径
+
不断旋转
```

---

## 29. `offset` 和 `euler` 可以同时使用

例如：

```xml
<replicate
    count="4"
    offset="0 0.5 0"
    euler="0 0 0.2">
```

可以理解成：

```text
copy 0
→ 原位置
→ 原姿态

copy 1
→ y +0.5
→ rotation +0.2

copy 2
→ y +1.0
→ rotation +0.4

copy 3
→ y +1.5
→ rotation +0.6
```

也就是说：

```text
平移
+
旋转
```

都可以逐份累计。

---

## 30. `sep`

`sep` 用来控制 MuJoCo 自动生成名字时的分隔符。

例如：

```xml
<replicate
    count="4"
    sep="-">
```

如果原始对象叫：

```xml
<site name="rf"/>
```

复制后名字可能类似：

```text
rf-0
rf-1
rf-2
rf-3
```

所以：

```text
sep
→ 只影响自动生成的名称
```

它不会改变：

```text
位置
形状
物理行为
```

---

## 31. 为什么必须自动生成唯一名称

MJCF 中很多元素会通过 name 被其他元素引用，例如：

```text
body
joint
geom
site
```

如果复制很多份后名字完全一样，就无法区分。

所以 replicate 会自动给复制出来的元素增加后缀。

这样每一个对象都有唯一名称。

---

## 32. Nested Replicate

`replicate` 里面还可以继续放另一个 `replicate`。

例如：

```xml
<replicate
    count="2"
    offset="0 1 0"
    euler="90 0 0">

    <replicate
        count="2"
        sep="-"
        offset="1 0 0"
        euler="0 90 0">

        <geom name="Alice" size=".1"/>

    </replicate>
</replicate>
```

内层：

```text
复制 2 次
```

外层再把整个内层结果：

```text
复制 2 次
```

所以最后：

```text
2 × 2
=
4 个 geom
```

---

## 33. Nested Replicate 可以理解成嵌套循环

它和编程中的 nested loop 很像。

可以理解为：

```text
一层 replicate
→ 一维阵列

两层 replicate
→ 二维阵列

三层 replicate
→ 三维阵列
```

这对于以下场景很方便：

- 网格
- 障碍物阵列
- 传感器阵列
- 重复结构

---

## 34. Replicate 整个 Body

`replicate` 并不只能复制 geom。

它还可以复制一个完整 body。

例如：

```xml
<replicate count="5" offset="1 0 0">
    <body>
        <joint .../>
        <geom .../>
        <site .../>
    </body>
</replicate>
```

这样就可以生成：

```text
5 个完整机构
```

也就是说：

```text
joint
geom
site
body hierarchy
```

都可以一起被复制。

---

## 35. Replicate Site

`site` 很适合配合 `replicate` 使用。

例如可以用来创建：

```text
sensor locations
measurement points
visual markers
ray directions
```

你刚才看到的圆形 site 示例就是这种用途。

---

## 36. Replicate 后的名字和引用

当带名字的对象被 replicate 后：

```text
MuJoCo 会自动修改名称
```

如果复制结构内部还有其他元素引用这些对象，相关引用也可以一起正确展开。

例如：

```text
site
+
引用这个 site 的 sensor
```

在 replicate 后，可以保持对应关系。

所以 replicate 并不是单纯：

```text
复制几个 geom
```

而是：

> 可以复制完整 MJCF 结构，并同步处理名称与引用。

---

## 37. Replicate 和手动复制 XML 的区别

如果不用 replicate，创建 50 个相似对象可能要：

```text
手动写 50 遍 XML
```

使用 replicate 后只需要：

```text
定义一次结构
+
设置复制数量
+
设置变换增量
```

这样可以提高：

- 可读性
- 可维护性
- 一致性
- 建模效率

---

## 38. 常见 Replicate 模式

### Linear Pattern

```text
count
+
offset
```

例如：

```xml
<replicate count="10" offset="0.2 0 0">
```

---

### Circular Pattern

```text
count
+
euler
+
对象先离旋转中心有一个半径
```

---

### Grid Pattern

```text
nested replicate
+
不同方向的 offset
```

---

### Repeated Mechanism

```text
replicate
+
完整 body hierarchy
```

---

## 39. Replicate 最重要的参数

当前阶段最值得记住：

```text
count
→ 复制多少份

offset
→ 每一份平移多少

euler
→ 每一份旋转多少

sep
→ 自动名称使用什么分隔符
```

这四个参数已经足够理解大部分基础 replicate 示例。

---

## 40. Replicate 核心理解

最核心流程：

```text
先定义一个结构
↓
自动重复生成
↓
每一份增加一定 transform
↓
自动生成唯一名称
```

可以简单记：

```text
只用 offset
→ 直线阵列

euler + radius
→ 圆周阵列

nested replicate
→ 网格 / 多维阵列
```

---

# Light 与 Replicate 对比

## 41. 两者作用完全不同

虽然它们在同一个学习章节中出现，但解决的是完全不同的问题。

```text
light
→ 控制场景怎么看起来

replicate
→ 控制重复模型结构怎么生成
```

进一步说：

```text
light
→ rendering / visualization

replicate
→ model construction
```

它们都不是用来替代：

```text
body
joint
geom
actuator
```

而是辅助这些核心结构。

---

## 42. 当前阶段需要记住什么

对于 `light`：

```text
pos
→ 灯在哪里

dir
→ 灯朝哪里

directional
→ 平行光还是局部光源

ambient
→ 基础亮度

diffuse
→ 普通照明

specular
→ 高光

castshadow
→ 阴影

mode / target
→ 跟踪或瞄准行为
```

对于 `replicate`：

```text
count
→ 复制多少

offset
→ 平移增量

euler
→ 旋转增量

sep
→ 名称分隔符
```

最简单的记忆：

```text
light
→ illuminate
→ 照亮

replicate
→ copy
→ 复制
```

---

## 来源

本笔记基于：

```text
Albusgive/mujoco_learning
```

来源仓库：

https://github.com/Albusgive/mujoco_learning

原始仓库与教学材料归对应作者所有。

本文记录的是我在学习过程中的个人理解、例子分析、代码解读与总结。