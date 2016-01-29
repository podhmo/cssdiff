# -*- coding:utf-8 -*-
import sys
import cssutils
from collections import defaultdict
VERBOSE = False


class DiffObject(object):
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        self.merged = full_difference(src, dst)

    def to_string(self):
        buf = []
        for style, diff_line_list in sorted(self.merged.items()):
            buf.append("{style} {{".format(style=style))
            for diff_line in diff_line_list:
                op = diff_line[0]
                if op == "-" or op == "+":
                    buf.append("{op}  {name}: {value};".format(op=op, name=diff_line[1], value=diff_line[2]))
                elif op == "->":
                    buf.append("-  {name}: {value};".format(op=op, name=diff_line[1], value=diff_line[2]))
                    buf.append("+  {name}: {value};".format(op=op, name=diff_line[1], value=diff_line[3]))
            buf.append("}\n")
        return "\n".join(buf)


class Element(object):
    def __init__(self, sheet, structure=None, verbose=True):
        self.sheet = sheet
        self.structure = structure or to_dict(self.sheet, verbose)
        self.verbose = verbose

    def simplify(self):
        return self.__class__(self.sheet, simplify(self.structure), verbose=self.verbose)

    def difference(self, other):
        src = simplify(self.structure)
        dst = simplify(other.structure)
        return DiffObject(src, dst)


def loads(css, verbose=VERBOSE):
    sheet = cssutils.parseString(css, validate=verbose)
    return Element(sheet, verbose=verbose)


def load(rf, verbose=VERBOSE):
    return loads(rf.read(), verbose=verbose)


def load_from_file(filename, verbose=VERBOSE):
    with open(filename) as rf:
        return load(rf)


def describe(sheet):
    for rule in sheet:
        print("S")
        for selector in rule.selectorList:
            print("\t{}".format(selector.selectorText))
        print("R")
        for prop in rule.style:
            print("\t{} {}".format(prop.name, prop.value))
        print("-")


def simplify(structure):
    return {k1: {k2: vs[-1] for k2, vs in sd.items()} for k1, sd in structure.items()}


def full_difference(src, dst):
    merged = defaultdict(list)
    added_or_changed = difference(dst, src, op="+", iterate=lambda x: x.items())
    deleted_or_changed = difference(src, dst, op="-", iterate=lambda x: x.items())

    for k, vs in added_or_changed.items():
        merged[k].extend(vs)

    for k, vs in deleted_or_changed.items():
        for v in vs:
            if v[0] == '-':
                merged[k].append(v)
    return merged


def difference(s1, s2, op="+", iterate=lambda s: sorted(s.items())):
    """s1 - s2"""
    def change(name, x, y):
        return ("->", name, x, y)

    def add(name, v):
        return (op, name, v)

    def addall(rules):
        return [add(name, value) for name, value in iterate(rules)]

    # Dict[style, Dict[name, value]]
    d = defaultdict(list)
    for style, rules in iterate(s1):
        another_rules = s2.get(style)
        if another_rules is None:
            d[style].extend(addall(rules))
            continue
        for name, value in iterate(rules):
            another_value = another_rules.get(name)
            if another_value is None:
                d[style].append(add(name, value))
            elif value != another_value:
                d[style].append(change(name, another_value, value))
    return d


def to_dict(sheet, verbose=True):
    d = defaultdict(lambda: defaultdict(list))
    for rule in sheet:
        if not hasattr(rule, "selectorList"):
            if verbose:
                sys.stderr.write("hmm: {}\n".format(type(rule)))
            continue
        for selector in rule.selectorList:
            sd = d[selector.selectorText]
            for prop in rule.style:
                sd[prop.name].append(prop.value)
    return d


# todo: remove
def pp(d):
    def default(o):
        return o.structure
    import json
    print(json.dumps(d, indent=2, default=default))


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=argparse.FileType('r'))
    parser.add_argument("dst", type=argparse.FileType('r'))
    parser.add_argument("--verbose", action="store_true", default=False)
    args = parser.parse_args()
    s0 = load(args.src, verbose=args.verbose)
    s1 = load(args.dst, verbose=args.verbose)
    print(s0.difference(s1).to_string())


if __name__ == "__main__":
    main()
