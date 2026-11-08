# Character (SVG)

The character is vector SVG paths only, with no embedded images. It was traced from the reference art,
so it matches the original closely. The paths are grouped by body part so you can animate them.

| File | What it is |
|---|---|
| `character.svg` | The static character |
| `character-animated.svg` | The same drawing with a CSS idle loop: breathing, head tilt and blinking. Open it in a browser. |
| `tools/` | The scripts that produced it: background removal, then splitting into parts and tracing each one |

## Animatable groups

| id | pivot (`transform-origin`) |
|---|---|
| `#head` (includes hair) | neck, 512 250 |
| `#eyelid-left`, `#eyelid-right` | top of the eye. They sit at `scaleY(0)`; animate them to `scaleY(1)` to blink |
| `#torso` | waist, 510 640 |
| `#arm-left`, `#arm-right` | shoulders |
| `#leg-left`, `#leg-right` | hips |
| `#shoe-left`, `#shoe-right` | soles |

Each part overlaps its neighbours by a few pixels, so small rotations don't open gaps between them.
Large moves, like a full arm wave, would show the cut, because the hidden parts were never painted in the original.

To animate `character.svg` with your own CSS, put it inline in your HTML. CSS can't reach inside an `<img>`.

```css
#arm-right { animation: wave 1s ease-in-out infinite; }
@keyframes wave { 50% { transform: rotate(-8deg); } }
```

## Regenerating

```
pip install vtracer scipy pillow numpy
python tools/cutout.py reference.png work/        # removes the checkerboard and writes work/cut.png and work/mask.npy
python tools/trace_parts.py work/ parts.txt       # traces each body part to <g> groups
```
