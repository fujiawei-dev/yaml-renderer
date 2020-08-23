import random
import string
from functools import partial

from jinja2 import Template

from templates import definition_tmpl, header_tmpl, path_tmpl


def render_template(obj: dict, tmpl: str):
    '''Render templates from string.'''
    return Template(tmpl).render(**obj)


render_header = partial(render_template, tmpl=header_tmpl)
render_path = partial(render_template, tmpl=path_tmpl)
render_definition = partial(render_template, tmpl=definition_tmpl)


class RanderYAML(object):

    header = ""
    paths = ["\n\npaths:"]
    definitions = ["\n\ndefinitions:"]
    marks = set()

    def render_header(self, obj: dict):
        self.header = render_header(obj)

    def render_path(self, obj: dict):
        for key in ("ref", "response"):
            val = obj.get(key, False)
            if val and isinstance(val, dict):
                rs = self.random_string(8)
                self.render_definition(obj[key], rs)
                obj[key] = "#/definitions/" + rs
        self.paths.append(render_path(obj))

    def render_definition(self, obj: dict, obj_n: str):
        tags = dict()
        for key, val in obj.items():
            if isinstance(val, bool):
                tags[key] = {"type": "boolean", "example": "true"}
            elif isinstance(val, str):
                tags[key] = {"type": "string", "example": '"%s"' % val}
            elif isinstance(val, int):
                tags[key] = {"type": "integer", "example": val}
            elif isinstance(val, dict):
                ref = self.random_string(8)
                tags[key] = {"type": "object", "ref": "#/definitions/" + ref}
                self.render_definition(val, ref)
            elif isinstance(val, list):
                if isinstance(val[0], bool):
                    tags[key] = {"type": "array",
                                 "sub": "boolean", "example": "true"}
                elif isinstance(val[0], str):
                    tags[key] = {"type": "array",
                                 "sub": "string", "example": '"%s"' % val[0]}
                elif isinstance(val[0], int):
                    tags[key] = {"type": "array",
                                 "sub": "integer", "example": val[0]}
                elif isinstance(val[0], dict):
                    ref = self.random_string(8)
                    tags[key] = {"type": "array",
                                 "ref": "#/definitions/" + ref}
                    self.render_definition(val[0], ref)
        self.definitions.append(render_definition(
            {"object": obj_n, "tags": tags}))

    def generate(self, path):
        c = self.header+"\n\n".join(self.paths) + "\n".join(self.definitions)
        print(c.replace('\n\n\n', '\n\n'),
              file=open(path, 'w', encoding='utf-8'))

    @classmethod
    def random_string(cls, n: int) -> str:
        mark = ''.join(random.sample(string.ascii_letters, n))
        while mark in cls.marks:
            mark = ''.join(random.sample(string.ascii_letters, n))
        cls.marks.add(mark)
        return mark


if __name__ == "__main__":
    from templates import __header, __get, __post
    y = RanderYAML()
    y.render_header(__header)
    y.render_path(__get)
    y.render_path(__post)
    y.generate("swagger.yaml")
