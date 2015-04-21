## analyze_game_data.py
分析游戏信息生成pkg_info和label_info表

### 处理包名相同的应用

* 先获取到包名相同的信息
* 生成pkg_info和label_info

### 处理包名不相同的应用

* 以游戏名的顺序排序
* 处理游戏名类似度非常高的游戏,作为同一类别
* 生成pkg_info和label_info


## game_types.py

以豌豆荚的游戏类型为基准，将其他渠道游戏类型进行对应
