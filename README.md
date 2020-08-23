# 简化 Swagger 文档编写的模板渲染器

> Swagger 接口文档写起来实在太繁琐了，这个程序就是尽可能简化接口文档的书写。

接口文档写起来这么麻烦，理论上早该有人写一个更方便的工具取代它或者辅助生成它，然而我始终找不到这样的工具，无奈只好自己动手写了这个渲染程序。

示例如下：

```python
from render import RanderYAML
from templates import __header, __get, __post

y = RanderYAML()
y.render_header(__header)
y.render_path(__get)
y.render_path(__post)
y.generate("swagger.yaml")
```

简化的核心在于 JSON 数据的自动解析。
