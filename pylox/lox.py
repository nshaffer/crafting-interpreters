#!/usr/bin/env python
import sys
import scanner
import parser
import token_types
from ast_printer import AstPrinter


HAD_ERROR = False


def main(args):
    if len(args) > 1:
        print("Usage: pylox [script]")
        sys.exit(64)
    elif len(args) == 1:
        run_file(args[0])
    else:
        run_prompt()
    return


def run_file(path):
    text = open(path, 'r').read()
    run(text)

    if HAD_ERROR:
        sys.exit(65)
    return


def run_prompt():
    global HAD_ERROR
    while True:
        run(input("> "))
        HAD_ERROR = False # Don't want errors to kill the session
    return


def run(source):
    s = scanner.Scanner(source)
    tokens = s.scan_tokens()
    
    p = parser.Parser(tokens)
    expression = p.parse()

    if HAD_ERROR:
        return
    
    print(AstPrinter().print(expression))
    return


# def error(line, message):
#     report(line, "", message)
#     return


def report(line, where, message):
    global HAD_ERROR
    sys.stderr.write("[line {0}] Error {1}: {2}\n".format(line, where, message))
    HAD_ERROR = True
    return


def error(token, message):
    if token.token_type == token_types.EOF:
        report(token.line, " at end", message)
    else:
        report(token.line, " at '{}'".format(token.lexeme), message)
    return


if __name__ == "__main__":
    main(sys.argv[1:])
    
