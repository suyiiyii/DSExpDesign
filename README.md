# 全国交通咨询模拟

## 问题描述

出于不同目的的旅客对交通工具有不同的要求。例如，因公出差的旅客希望在旅途中的时间尽可能短，出门旅游的游客则期望旅费尽可能省，而老年旅客则要求中转次数最少。编
制一个全国城市间的交通咨询程序，为旅客提供两种或三种最优决策的交通咨询。

## 基本要求

1. 提供对城市信息进行编辑（如：添加或删除）的功能。
2. 城市之间有两种交通工具：火车和飞机。提供对列车时刻表和飞机航班进行编辑（增设或删除）的功能。
3. 提供两种最优决策：最快到达或最省钱到达。全程只考虑一种交通工具。
4. 旅途中耗费的总时间应该包括中转站的等候时间。
5. 咨询以用户和计算机的对话方式进行。由用户输入起始站、终点站、最优决策原则和交通工具，输出信息为：最快需要多长时间才能到达或者最少需要多少旅费才能到达，并详细说明依次于何时乘坐哪一趟列车或哪一次班机到何地。

## 测试数据

参考全国交通图，自行设计列车时刻表和飞机航班。

## 实现提示

1. 对全国城市交通图和列车时刻表及飞机航班表的编辑，应该提供文件形式输入和键盘输入两种方式。飞机航班表的信息应包括：起始站的出发时间、终点站的到达时间和票价；列车时刻表则需根据交通图给出各个路段的详细信息，例如：对从北京到上海的火车，需给出北京至天津、天津至徐州及徐州至上海各段的出发时间、到达时间及票价等信息。

2. 以邻接表作交通图的存储结构，表示边的结点内除含有邻接点的信息外，还应包括交通工具、路程中消耗的时间和花费以及出发和到达的时间等多项属性。

## 选做内容

增加旅途中转次数最少的最优决策。

## TODO

- [x] 交通图的存储结构
- [x] 交通图的编辑
- [x] 交通图的显示
- [x] 查询结果的展示
- [x] 最快到达
- [x] 最省钱到达
- [x] 最少中转次数到达
- [x] 最快到达算法优化