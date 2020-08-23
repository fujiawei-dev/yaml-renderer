# 简化 Swagger 文档编写的模板渲染器

> Swagger 接口文档写起来实在太繁琐了，这个程序就是尽可能简化接口文档的书写。

对 YAML 语法不太熟的话，写一份 Swagger 文档相当耗费时间，即使十分熟悉，接口数超过一定量或者请求响应的数据结构复杂，文档势必特别长，总之心累。

既然 Swagger 标准的接口文档写起来这么麻烦，理论上早该有人写一个更方便的工具取代它或者辅助生成它，然而我始终找不到这样的工具，无奈只好自己动手写了这个渲染程序。

简化的核心在于 JSON 数据结构的自动解析。

以这样一个 JSON 为例：

```json
{
    "integer": 1,
    "boolean": true,
    "string": "dGhpcyBpcyBhIGV4YW1wbGU=",
    "array": [1,2,3,5],
    "json": {
        "id": 100,
        "companies":["apple", "google", "mircosoft"]
    }
}
```

这可以是请求数据或者响应数据，一般情况，列表是不存在多态的。定义这样一个结构大概就占了 40 多行，我一开始的想法就是根据 JSON 数据自动生成的 YAML 定义。

因为标准 JSON 与 Python 的字典结构几乎是相同的，所以用 Python 处理起来得天独厚。

首先编写 YAML 定义结构的 Jinja2 模板：

```py
definition_tmpl = '''
  {{object}}:
    type: "object"
    required:
    {%- for val in tags.keys() %}
      - "{{val}}"
    {%- endfor %}
    properties:
    {%- for key, val in tags.items() %}
      {{key}}:
        {%- if val.type=="array" %}
        type: "array"
        items:
        {%- if val.sub %}
          type: "{{val.sub}}"
          example: {{val.example}}
        {%- else %}
          $ref: "{{val.ref}}"
        {%- endif -%}
        {%- elif val.type=="object" %}
          $ref: "{{val.ref}}"
        {%- else %}
          type: "{{val.type}}"
          example: {{val.example}}
        {%- endif -%}
    {% endfor %}
'''
```

然后解析 JSON 数据，生成需渲染的字段：

```python
def render_definition(obj, obj_n):
  for key, val in obj.items():
      elif isinstance(val, str):
          tags[key] = {"type": "string", "example": '"%s"' % val}
      elif isinstance(val, int):
          tags[key] = {"type": "integer", "example": val}
      elif isinstance(val, dict):
          tags[key] = {"type": "object", "ref": "#/definitions/" + random_string(8)}
  return render({"object": obj_n, "tags": tags}))
```

这里是实现代码的部分，基本思想就是这样。而 YAML 文档的其他部分相对就简单了，大部分情况一个模板就可以兼容了。

最后一份渲染出来 800 多行的文档大约只需写 400 行，其中的 JSON 是复制即可的，编写起来方便不少了。

当然还有一个问题，相同的数据结构在不同的请求/响应中，渲染时会以不同的名称重复定义，不过基本没有影响，不管了。

## 用法示例

```python
from render import RanderYAML
from templates import __header, __get, __post

y = RanderYAML()
# 头部信息渲染
y.render_header(__header)
# 请求路径渲染
y.render_path(__get)
y.render_path(__post)
# 生成文件
y.generate("swagger.yaml")
```

今后再编写接口文档应该容易不少。
