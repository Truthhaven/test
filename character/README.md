# Character (pure SVG)

The reference character drawn entirely in hand-written SVG. There are no raster images in it.

| File | What it is |
|---|---|
| `character.svg` | The static character. Every body part is its own `<g id>` |
| `character-animated.svg` | The same drawing with a built-in CSS idle loop (breathing, head tilt, loc sway, blinking). Open it in a browser. |

## Animatable parts

Each group already has a `transform-origin` at its natural pivot (shoulder, elbow, neck, crown…),
so you can rotate or translate it with CSS, the Web Animations API, GSAP and similar tools without extra setup.

```
#figure
├─ #hair-back      (#locs-back)
├─ #arm-left       #upperarm-left  #forearm-left
├─ #arm-right      #upperarm-right #forearm-right
├─ #legs           #leg-left (#rip-left)  #leg-right (#rip-right)  #waist
├─ #shoe-left  #shoe-right
├─ #torso
├─ #hands          #hand-left  #hand-right (#bracelet)
├─ #neck
├─ #head           #eyes (#eye-left, #eye-right)  #mouth (#teeth)  #glasses
│                  #earring-left  #earring-right
└─ #hair-front     #locs-left  #locs-right
```

The locs are stroked paths defined once in `<defs>` (`#locsBack`, `#locsL`, `#locsR`).
Each group draws them as several `<use>` layers: rim light, base colour and twist texture.
Edit one path and every layer follows. You can also animate the `d` attribute of a strand to make it swing.

To animate the static file, inline it in HTML (CSS can't reach inside an `<img>`):

```css
#arm-right { animation: wave 1s ease-in-out infinite; }
@keyframes wave { 50% { transform: rotate(-25deg); } }
```
