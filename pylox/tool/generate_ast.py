#!/usr/bin/env python
import sys


def main(args):
    if len(args) != 1:
        sys.stderr.write("Usage: generate_ast <path>\n")
        sys.exit(1)

    path = args[0]
    schemas = ["Binary   : left, operator, right",
               "Grouping : expression",
               "Literal  : value",
               "Unary    : operator, right"]
    define_ast(path, "Expr", schemas)
    return


def define_ast(path, base_name, schemas):
    with open(path, 'w') as f:
        f.write("class {0}(object):\n".format(base_name))
        define_visitor(f, base_name, schemas)
        f.write("    def accept(self, visitor):\n")
        f.write("        raise RuntimeError('Method not implemented.')\n")
        f.write("\n\n")
        for schema in schemas:
            class_name, field_names = [_.strip() for _ in schema.split(':')]
            define_type(f, base_name, class_name, field_names)
    return


def define_visitor(f, base_name, schemas):
    for schema in schemas:
        class_name = schema.split(':')[0].strip()
        f.write("    def visit_{0}(self, {1}):\n".format(class_name.lower(), base_name.lower()))
        f.write("        raise RuntimeError('Method not implemented.')\n")
        f.write("\n")
    return


def define_type(f, base_name, class_name, field_names):
    f.write("class {0}({1}):\n".format(class_name, base_name))
    f.write("    def __init__(self, {0}):\n".format(field_names))
    fields = [_.strip() for _ in field_names.split(',')]
    for field in fields:
        f.write("        self.{0} = {0}\n".format(field))
    f.write("\n")
    f.write("    def accept(self, visitor):\n")
    f.write("        return visitor.visit_{0}(self)\n".format(class_name.lower()))
    f.write("\n\n")
    return
            

if __name__ == "__main__":
    main(sys.argv[1:])
