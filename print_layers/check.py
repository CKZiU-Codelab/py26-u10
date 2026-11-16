#!/usr/bin/env python3
"""Self-check for the project "Print Layers" (u10).

Run it in the project directory:

    python3 check.py

The script reads only the files your program produced. It never runs
your program, so generate the files first, then check them. Each
[fail] line names one requirement; fix it and run the script again.
"""

import csv
import html as html_lib
import os
import re
import sys


class Fail(Exception):
    pass


CHECKS = []
WARNINGS = []


def check(name):
    def register(function):
        CHECKS.append((name, function))
        return function
    return register


def warn(message):
    WARNINGS.append(message)


def read_text(path):
    if not os.path.exists(path):
        raise Fail("%s is missing" % path)
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def read_csv(path):
    if not os.path.exists(path):
        raise Fail("%s is missing" % path)
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        raise Fail("%s is empty" % path)
    return rows


def require_files(*names):
    missing = [name for name in names if not os.path.exists(name)]
    if missing:
        raise Fail("missing: %s" % ", ".join(missing))


def require_notes(*headings):
    text = read_text("notes.md")
    missing = [heading for heading in headings if heading not in text]
    if missing:
        raise Fail("notes.md has no section: %s" % " | ".join(missing))


def read_pnm(path):
    text = read_text(path)
    lines = [line.split("#")[0] for line in text.splitlines()]
    tokens = " ".join(lines).split()
    if not tokens:
        raise Fail("%s is empty" % path)
    magic = tokens[0]
    if magic not in ("P1", "P2", "P3"):
        raise Fail("%s starts with %r; use the text formats P1, P2 or P3" % (path, magic))
    try:
        width = int(tokens[1])
        height = int(tokens[2])
    except (IndexError, ValueError):
        raise Fail("%s: the width and the height are missing from the header" % path)
    index = 3
    maxval = 1
    if magic in ("P2", "P3"):
        try:
            maxval = int(tokens[3])
        except (IndexError, ValueError):
            raise Fail("%s: the maximum value is missing from the header" % path)
        index = 4
    channels = 3 if magic == "P3" else 1
    needed = width * height * channels
    values = tokens[index:]
    if len(values) != needed:
        raise Fail("%s: the header says %dx%d, which needs %d values, but the file has %d"
                   % (path, width, height, needed, len(values)))
    try:
        numbers = [int(value) for value in values]
    except ValueError:
        raise Fail("%s contains a value that is not an integer" % path)
    for number in numbers:
        if number < 0 or number > maxval:
            raise Fail("%s has the value %d, outside 0..%d" % (path, number, maxval))
    return {"magic": magic, "width": width, "height": height,
            "maxval": maxval, "values": numbers, "path": path}


def find_frames(minimum=8):
    if not os.path.isdir("frames"):
        raise Fail("the frames/ directory is missing")
    names = sorted(name for name in os.listdir("frames") if name.endswith(".pgm"))
    if not names:
        raise Fail("frames/ has no .pgm files")
    bad = [name for name in names if not re.match(r"^frame_\d\d\.pgm$", name)]
    if bad:
        raise Fail("these names do not use two digits: %s" % ", ".join(bad[:3]))
    if len(names) < minimum:
        raise Fail("only %d frames; the animation needs at least %d" % (len(names), minimum))
    return ["frames/" + name for name in names]


def numbers_in(text):
    return [float(value) for value in re.findall(r"-?\d+(?:\.\d+)?", text)]


def require_gif(path):
    if not os.path.exists(path):
        raise Fail("%s is missing; build it with the convert command from the brief" % path)
    with open(path, "rb") as handle:
        head = handle.read(6)
    if not head.startswith(b"GIF8"):
        raise Fail("%s does not start with GIF8; is it really a GIF?" % path)


def scan_sources(forbidden):
    for name in sorted(os.listdir(".")):
        if not name.endswith(".py") or name == "check.py":
            continue
        with open(name, encoding="utf-8") as handle:
            for number, line in enumerate(handle, start=1):
                code = line.split("#")[0]
                for token in forbidden:
                    if token in code:
                        warn("%s:%d uses %s; the brief asks for a different tool."
                             % (name, number, token))


def main():
    print("")
    print("Checking the project in %s" % os.getcwd())
    print("")
    passed = 0
    failed = 0
    for name, function in CHECKS:
        try:
            function()
        except Fail as error:
            failed += 1
            print("[fail] %s" % name)
            print("       %s" % error)
        except Exception as error:
            failed += 1
            print("[fail] %s" % name)
            print("       the check itself stopped: %s: %s" % (type(error).__name__, error))
        else:
            passed += 1
            print("[ok]   %s" % name)
    print("")
    for message in WARNINGS:
        print("[warn] %s" % message)
    if WARNINGS:
        print("")
    print("%d passed, %d failed" % (passed, failed))
    if failed:
        print("NOT READY YET - fix the [fail] lines above and run the script again.")
        return 1
    print("PROJECT READY - every automatic check passed. Show the program and notes.md.")
    return 0



def layers_data():
    rows = read_csv("layers.csv")
    if len(rows) < 21:
        raise Fail("layers.csv has %d lines; a header and twenty layers are expected" % len(rows))
    layers = []
    for number, row in enumerate(rows[1:], start=2):
        if len(row) != 2:
            raise Fail("line %d has %d cells, two expected" % (number, len(row)))
        try:
            layer = int(row[0])
            radius = float(row[1])
        except ValueError:
            raise Fail("line %d is not two numbers" % number)
        if radius < 5 or radius > 20:
            raise Fail("line %d: radius %.1f is outside 5..20 mm" % (number, radius))
        layers.append((layer, radius))
    return layers


def estimate_data():
    layers = layers_data()
    rows = read_csv("estimate.csv")
    if len(rows) - 1 != len(layers):
        raise Fail("estimate.csv has %d data rows, layers.csv has %d layers"
                   % (len(rows) - 1, len(layers)))
    if len(rows[0]) != 4:
        raise Fail("estimate.csv has %d columns; four were asked for" % len(rows[0]))
    previous = -1.0
    for index, (layer, radius) in enumerate(layers):
        row = rows[index + 1]
        try:
            perimeter = float(row[2])
            total = float(row[3])
        except ValueError:
            raise Fail("row %d of estimate.csv is not numeric" % (index + 2))
        expected = 2 * 3.141592653589793 * radius
        if abs(perimeter - expected) > 0.5:
            raise Fail("row %d of estimate.csv: %.2f mm, expected about %.2f mm"
                       % (index + 2, perimeter, expected))
        if total < previous:
            raise Fail("row %d of estimate.csv: the running total goes down" % (index + 2))
        previous = total
    return previous


@check("the files named in the brief exist")
def files():
    require_files("layers.csv", "layers.py", "top.pgm", "estimate.csv",
                  "estimate.txt", "notes.md")


@check("layers.csv has twenty layers with a radius between 5 and 20 mm")
def layers():
    layers_data()


@check("estimate.csv repeats every layer and computes its perimeter")
def estimate():
    estimate_data()


@check("estimate.txt has a mass that matches the length, the filament and PLA")
def mass():
    total_length = estimate_data()
    expected = total_length * 3.141592653589793 * (1.75 / 2.0) ** 2 * 1.24 / 1000.0
    text = read_text("estimate.txt")
    for value in numbers_in(text):
        if abs(value - expected) <= expected * 0.08:
            return
    raise Fail("estimate.txt does not show a mass of about %.2f g for %.1f mm of filament"
               % (expected, total_length))


@check("top.pgm is a 400 by 400 PGM picture")
def top():
    image = read_pnm("top.pgm")
    if image["magic"] != "P2":
        raise Fail("top.pgm is %s; the picture uses the PGM format P2" % image["magic"])
    if (image["width"], image["height"]) != (400, 400):
        raise Fail("the picture is %dx%d; the brief asks for 400x400"
                   % (image["width"], image["height"]))


@check("notes.md has both research notes and the side-view note")
def notes():
    require_notes("## The New Thing – a circle on a grid",
                  "## The New Thing – from millimetres to grams",
                  "## Milestone 2 – which way up the side view is")


scan_sources(["sum("])

if __name__ == "__main__":
    sys.exit(main())
