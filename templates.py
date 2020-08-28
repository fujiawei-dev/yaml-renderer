# 头部信息
header_tmpl = '''\
swagger: "2.0"
info:
  description: "{{description}}"
  version: "{{version}}"
  title: "{{title}}"

host: "{{host}}"
basePath: "{{basePath}}"
tags:
{%- for tag, description in tags.items() %}
  - name: "{{tag}}"
    description: "{{description}}"
{%- endfor %}

schemes:
  - "http"
  - "https"
'''

# 头部字典模板
__header = {
    "description": "一个简化 Swagger 文档编写的模板渲染器",
    "version": "1.0.0",
    "title": "YAML Randerer",
    "host": "127.0.0.1:8080",
    "basePath": "/rander/yaml",
    "tags": {
        "definitions": "数据结构",
    }
}


# 请求路径
path_tmpl = '''
{%- if path %}
  /{{path}}:
{%- endif %}
    {{method}}:
      tags:
        - "{{tag}}"
      summary: "{{summary}}"
      consumes:
        - "application/json"
      produces:
        - "application/json"
        {%- if method=="post" or  method=="put"%}
      parameters:
        - in: "body"
          name: "{{name}}"
          description: "{{description}}"
          required: {{required}}
          schema:
            $ref: "{{ref}}"
        {%- elif params and method=="get" or method=="delete" %}
      parameters:
        {%- for key, val in params.items() %}
        - name: "{{key}}"
          in: "query"
          type: "{{val.type}}"
          description: "{{val.description}}"
          required: {{val.required}}
        {%- endfor %}
        {%- endif %}
      responses:
        "200":
          description: "操作成功"
        {%- if response %}
          schema:
            $ref: "{{response}}"
        {%- endif -%}
'''

# 请求路径模板

__get = {
    "path": "info",
    "method": "get",
    "tag": "definitions",
    "summary": "查询数据结构定义",
    # 查询参数
    "params": {
        "id": {
            # "type": "boolean",
            # "type": "string",
            "type": "integer",
            "description": "对象标识符",
            "required": "true",
            # "required": "false",
        }
    },
    # 响应数据字典
    "response": {
        "status_code": 200,
        "error_msg": "错误信息",
    }
}

__post = {
    "method": "post",
    "tag": "definitions",
    "summary": "提交数据结构定义",
    "name": "对象标识符",
    "description": "一个新的数据结构",
    "required": "true",
    # "required": "false",
    # 请求数据字典
    "ref": {
        "id": 1,
        "bool": True,
        "content": "数据结构",
    },
    # 响应数据字典
    "response": {
        "status_code": 200,
        "error_msg": "错误信息",
    }
}

# 数据结构
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
