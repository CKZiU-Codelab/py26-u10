# Project – Print Layers

**Individual Project Brief – Week 6 · u10**

Start: Monday, 16 November 2026. Show the working program on Monday, 23 November 2026.

## The Idea

You build a preview of a print, layer by layer. The program reads a list of layers with their radius, draws the side view as an ASCII silhouette, draws the top view as a PGM picture of concentric circles, and computes how much filament the model needs — the length of every layer, the total length, and the mass in grams for a 1.75 mm PLA filament.

No printer is involved. The model exists only as numbers in a CSV file, and the program turns those numbers into a shape you can look at and a mass you can compare with what your slicer says. That is what a slicer does in its first pass, and doing it yourself makes the slicer much less magical.

## Why This Project Is Yours

You use a 3D printer and you asked to see what programming is actually for. This project answers that directly: a printer is a machine that follows a list of numbers, and a program is the thing that produces the list. It also matches what you know from Scratch — loops and a visible result — and adds the part Scratch hides: the calculation behind the picture.

## What You Already Have

- Lists, indexing, `for` loops, conditions and comparisons.
- `%s`, `%d` and `%.2f` formatting, and `int()`/`float()` conversions.
- Files inside `with`, the `csv` module, and the PGM format from last week.

## The New Thing

A circle is easy to draw with a pen and awkward with a grid of pixels. Find out how to:

1. What `math.pi` is used for, and what `2 * math.pi * r` computes.
2. How to decide whether a pixel at `(x, y)` belongs inside a circle of radius `r` around a centre — write the condition with multiplication, not with a square root.
3. Why comparing squared distances avoids one operation and one rounding problem.
4. What `%.1f` and `%.2f` do, and how the mass of a filament is computed from a length: cross-section × length × density.
5. What the cross-section area of a 1.75 mm filament is in square millimetres, and why the units have to be converted before the mass comes out in grams.
6. What happens when the same pixel belongs to two layers.

**Write it down:** Create `notes.md` with `## The New Thing – a circle on a grid`. Explain the condition in two sentences and give one example pixel that is inside and one that is outside your circle. Add `## The New Thing – from millimetres to grams` with the three factors of the calculation, one example with your own numbers, and a sentence about the unit that surprised you.

## The Plan

### Milestone 1 – The model

Create `layers.csv` by hand.

1. Two columns: `layer,radius_mm`.
2. Twenty layers with a profile of your choice: a vase that widens and narrows, a cone, or a cylinder with a rim.
3. The radius starts at `8` and stays between `5` and `20` millimetres.
4. Draw the profile on paper first, as a graph of radius against layer — that graph is the shape the side view will show.

### Milestone 2 – The side view

Create `layers.py`.

1. Read the file and print every layer with its radius.
2. Print an ASCII side view: one line per layer, with two bars of `#` whose width is proportional to the radius, and empty space between them.
3. Use a scale so that the widest layer fits in thirty characters on each side.
4. Check the silhouette against your paper graph.

At the end of this step the terminal shows the shape of your print from the side, upside down or not — decide which and write it down.

### Milestone 3 – The length of one layer

1. Compute the perimeter of every layer as `2 * math.pi * radius`.
2. Print every layer with its perimeter in millimetres, one decimal place.
3. Sum the perimeters with a loop, without `sum()`.
4. Print the total length in millimetres and in metres.

At the end of this step the total length is a number you can compare with the slicer's filament length for a similar model.

### Milestone 4 – From metres to grams

1. Ask for the filament diameter, with `1.75` as the default.
2. Compute the cross-section area in square millimetres and the volume of the print in cubic millimetres.
3. Convert the volume to cubic centimetres and multiply by the density of PLA, `1.24` g/cm³.
4. Print the length, the volume and the mass, each with a clear unit.
5. Compare the mass with a real spool — how many such prints fit on one kilogram?

### Milestone 5 – The top view

1. Create `top.pgm`, four hundred by four hundred pixels, all white.
2. For every layer, draw its circle as a dark outline and leave the inside light, so that the layers do not hide each other.
3. Mark the centre of the print, and keep the scale in a variable so that the picture can be resized.
4. Write `top.pgm` with a correct `P2` header and open it.

At the end of this step the picture shows the profile from above, with the widest layers outside and the narrowest inside.

### Milestone 6 – The estimate file

1. Write `estimate.csv` with `layer,radius_mm,perimeter_mm,length_total_mm` for every layer.
2. Write `estimate.txt` with the totals: layers, height in millimetres if every layer is `0.2` mm, total filament length, mass and the number of prints per kilogram.
3. Read `estimate.csv` back and print the last row, to prove the file is complete.
4. Print the side view and the totals on the screen in one run.

## Example

```text
Reading layers.csv (20 layers)
Layer  1  radius   8.0 mm  perimeter  50.3 mm
Layer  2  radius   8.4 mm  perimeter  52.8 mm
...

Side view (30 columns per side)
          ##############|##############
           #############|#############
            ############|############
...

Total filament length: 1043.2 mm (1.04 m)
Volume: 2.51 cm3
Mass: 3.11 g
Prints per kilogram: 321

estimate.txt
layers: 20
height: 4.0 mm
length: 1043.2 mm
mass: 3.11 g

Saved top.pgm (400x400)
Saved estimate.csv (20 rows)
```

The numbers above come from an example model. Your profile decides yours.

## Requirements

- One program, `layers.py`, started from the terminal with `python3 layers.py`.
- Radius and all derived values are read or computed, never typed into the drawing code.
- The circle test uses squared distances and no square root.
- Every total is computed with a loop, not with `sum()`.
- `top.pgm` has a correct header, one row of numbers per line, and a size taken from variables.
- `estimate.csv` is written with the `csv` module and contains one row per layer.
- Units appear in the output: millimetres, metres, cubic centimetres, grams.

## Files

```text
print_layers/
├── layers.csv
├── layers.py
├── top.pgm
├── estimate.csv
├── estimate.txt
├── notes.md
└── check.py
```

Commit the whole directory to your repository and push it before the Monday session. A directory that exists only on your laptop cannot be checked.

Run `python3 check.py` in the project directory before you commit. It reads the files your program produced, not your code, and prints one line per requirement.


## How It Will Be Checked

- The perimeter of the first layer matches `2 * pi * radius` by hand.
- The sum in `estimate.txt` equals the last value in `estimate.csv`.
- The widest layer in the side view is the widest layer in `top.pgm`.
- Changing one radius changes the totals, the CSV and both pictures.
- The mass is plausible: a small 20-layer test print weighs a few grams, not a few hundred.
- You can explain the circle condition and the unit conversion without the editor open.

**Hint:** Draw the outline of a circle, not a filled one. For every pixel, ask whether it is inside the circle of this layer but outside the circle of the previous layer — that thin band is the wall of the print at that height.

**Additional challenge:** Add a second column to `layers.csv` for the extrusion width and compute the number of lines around each layer, then the time the print needs at a given speed. Compare your time with the slicer's estimate for a similar model and write in `notes.md` which of the two guesses you trust more, and why.

## Suggested Learning Resources

- [The `math` module – `pi` and other functions](https://docs.python.org/3/library/math.html)
- [Numbers in Python – `int`, `float` and conversions](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)
- [The `csv` module – reading and writing tabular data](https://docs.python.org/3/library/csv.html)
- [Netpbm – description of the PGM format](https://netpbm.sourceforge.net/doc/pgm.html)

**Final goal:** By the end of this project, you should have a program that turns a list of layer radii into a side view, a top view and a filament estimate — using loops, conditions, arithmetic, lists and files from the first five weeks, and a formula from the `math` module that you looked up yourself.
