# Author: ZengHao
# CreatTime: 2022/10/12
# FileName: 01
# Description: Simple introduction of the code
import math
import turtle as t

# 初始化位置和turtle
t.title("美国队长盾牌")
t.setup(500, 500, 200, 200)
t.pensize(1)
t.speed(0)
t.hideturtle()
t.penup()
t.goto(0, -165)
t.pendown()
# 循环对于每一个不同圆圈填充相应的颜色
for i in range(4):
    if i % 2 == 0:
        t.color('black', 'red')
    elif i == 1:
        t.color('black', 'white')
    else:
        t.color('black', 'blue')
    t.begin_fill()  # 填充颜色
    t.circle(160 - 35 * i, 360)
    t.end_fill()
    t.penup()
    t.left(90)
    t.forward(35)  # 向内圈移动
    t.right(90)
    t.pendown()

# 绘制五角星，旋转的角度是144度
pi = 3.1415926
length = math.sin(0.4 * pi) * 55 * 2
t.penup()
t.left(90)
t.forward(75)  # 起始位置
t.pendown()
t.right(90)
t.right(72)  # 调整方向
t.color('white', 'white')
t.begin_fill()
# 循环绘制五角星的每条边
for i in range(5):
    t.forward(length)
    t.right(144)
t.end_fill()
t.exitonclick()
