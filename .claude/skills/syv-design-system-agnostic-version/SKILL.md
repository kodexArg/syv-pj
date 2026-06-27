---
name: syv-design-system-agnostic-version
description: >
  Load the full Subordinación y Valor design language into context — palettes,
  faction colors, typography, logo geometry, spacing, glow rules — in a
  platform-agnostic form. Invoke before designing, styling, or prompting
  anything in the SyV universe (CSS, Flutter/Dart, ComfyUI prompts, HTML,
  slides, game assets, pixel art). Triggers: "diseño SyV", "paleta de SyV",
  "colores de facción", "estilo del universo", "prompt de personaje", "avatares SyV",
  or any task that requires the SyV visual identity regardless of output target.
---

# SyV Design System — Agnostic Version

This skill loads the **complete visual identity of Subordinación y Valor** into
the agent's context. It is intentionally **platform-agnostic**: no CSS syntax,
no Flutter class names, no ComfyUI boilerplate — just the canonical values and
rules, expressed in plain language with hex codes, so any target (CSS, Dart,
ComfyUI positive prompt, pixel art direction, HTML, Figma, Godot) can consume
them without translation noise.

**SSOT:** `~/Dev/SyV/syv-design-system/tokens/syv.tokens.json` (DTCG) and
`~/Dev/SyV/syv-design-system/INDEX.md`. Read those files for the authoritative
values. This skill is a pre-digested summary that travels in context — never
the place to hand-edit token values.

---

## 1 — Mood & Atmosphere

*Subordinación y Valor* is a post-diluvio military-theocratic Argentina, late
22nd century. The visual language must carry:

- **Perpetual cold rain** — wet concrete, dim sodium light, mist.
- **Military austerity** — olive drab, no ornament, worn edges.
- **Ecclesiastical weight** — gold flickers, candlelight warmth bleeding
  through the dark.
- **Neon exception** — one hard neon-green glow per surface, off-center,
  like a radiation leak. Never decorative. Always unsettling.

For image generation (ComfyUI / SD prompts): dark atmospheric lighting,
under perpetual rain, wet surfaces, worn military or clerical textures,
cinematic low-key chiaroscuro, gritty realism.

---

## 2 — Core Palette (global, all factions)

| Role | Name | Hex |
|---|---|---|
| Deepest backdrop | ink.1000 | `#0C0B09` |
| Card/body surface | ink.900 | `#141210` |
| Raised surface | ink.850 | `#1A1714` |
| Hairline border | ink.600 | `#3A352F` |
| Muted/disabled | ink.500 | `#6B6358` |
| Primary text | cream.100 | `#F3EEE4` |
| Prose/parchment text | cream.200 | `#E4DAC8` |
| Secondary/metadata text | warm.200 | `#CDBFA8` |
| **LEAD accent — military olive drab** | green.500 | `#7B8A4E` |
| Hover/shimmer | green.400 | `#97A267` |
| Press/deepen | green.600 | `#5E6B3A` |
| Soft chips/tags | green.300 | `#B4BE8E` |
| Deep hairline | green.deep | `#4A5530` |
| **NEON EXCEPTION — glow only** | green.neon | `#34E867` |
| Institutional Argentina celeste | celeste.500 | `#8FB8D6` |
| Lighter celeste | celeste.300 | `#BCD6E8` |
| Military deep surface | moss.900 | `#1A201A` |
| Slate-green panel | moss.700 | `#373D35` |
| Military border/divider | moss.500 | `#4E564A` |
| Tool accent / amber voice | amber.500 | `#E0A23C` |
| Soft amber | amber.300 | `#EFC074` |
| Second voice / teal | teal.500 | `#4FA6AB` |
| Success | semantic.good | `#7B8A4E` |
| Warning | semantic.warn | `#E0A23C` |
| Error (warm red, never pure red) | semantic.bad | `#D9694E` |

**Glow rule:** One off-center neon-green radial halo (`#34E867` at 16% opacity)
per surface, placed behind content like a radiation leak. Never use `#34E867`
as fill, text, or border.

---

## 3 — Faction Color Keys

Each faction has a dominant palette accent that layers on top of the global
dark base. Use these to tint uniforms, insignia, backgrounds, and lighting in
character portraits.

### Fuerzas Armadas (Ejército Confederado)
- **Primary:** olive drab `#7B8A4E` (green.500) — uniforms, caps, collars
- **Secondary:** cream `#F3EEE4` — insignia, rank stripes
- **Deep surface:** moss `#1A201A` / `#373D35`
- **Accent:** celeste `#8FB8D6` for Argentine institutional touches
- **Atmosphere:** cold rain, mud, worn military wool, dim overhead fluorescent

### Iglesia de Dársena (Clerical)
- **Primary:** cream/ivory `#F3EEE4` — habits, albs, vestments
- **Secondary:** deep warm-black `#0C0B09` — cassocks, shadow
- **Gold accent:** amber `#E0A23C` — candlelight, gilded crosses, halos
- **Atmosphere:** candlelight, incense smoke, stone cathedral, stained glass

### Sagrada Inquisición Argentina (SIA)
- **Primary:** deep ink `#141210` — severe black robes
- **Secondary:** crimson-ish `#D9694E` (semantic.bad) — seal wax, threat
- **Accent:** amber `#E0A23C` — lanterns, burning texts
- **Atmosphere:** torchlight, interrogation rooms, shadow and flame

### La Unión / Resistencia Subterránea
- **Primary:** teal/petróleo `#4FA6AB` — clandestine markings, graffiti
- **Secondary:** worn amber `#E0A23C` — salvaged light sources
- **Deep surface:** rusted metal, concrete, ink.900
- **Atmosphere:** underground tunnels (Las Tuberías), water drips, neon flicker

### Gremio de Comercio
- **Primary:** amber gold `#E0A23C` — wealth, negotiation, trade seals
- **Secondary:** cream `#F3EEE4` — ledgers, merchant dress
- **Atmosphere:** candlelit counting rooms, port warehouses, river fog

### Arpistas
- **Primary:** teal `#4FA6AB` — hidden tech, encrypted signals
- **Secondary:** green.300 `#B4BE8E` — archive paper, old circuit boards
- **Atmosphere:** hidden libraries, pre-cataclysm tech, quiet conspiracy

### Refugiados / Parias (Las Tuberías)
- **Primary:** desaturated earth tones — rags, rust, mud
- **Secondary:** celeste `#8FB8D6` — faint sky memory, water
- **Atmosphere:** submerged ruins, salvaged lanterns, perpetual damp

---

## 4 — Typography

All rules are about *role*, not about syntax. Translate to your target language.

| Role | Family | Weight | Size | Notes |
|---|---|---|---|---|
| Display (h1) | Nunito | 800 | 35px | Tracking −0.02em |
| Headline (h2) | Nunito | 800 | 26px | Tracking −0.02em |
| Title (h3/card) | Nunito | 500 | 19px | |
| Body/UI copy | Nunito | 400 | 17px | Line-height 1.55 |
| Long prose (\<p\>) | Bitter (slab serif) | 400 | 17px | cream.200 color, line-height 1.62 |
| Code/terminal | DM Mono | 400 | 16px | |
| Kicker eyebrow | DM Mono | 400 | 12px | UPPERCASE, green.500, tracking +0.18em |
| Brand wordmark | Saira Stencil One | — | — | **Logo only** — never headings or body |

**Rules:**
- Lowercase almost everywhere. The kicker eyebrow is the **only** uppercase element.
- Nunito = interface voice (headings, labels, UI chrome).
- Bitter = reading voice (long-form prose, lore, character backstories).
- These two roles do **not** mix.

---

## 5 — Logo & Mark

**Geometry (96×96 grid):**
- A **cross** (vertical x=48 y1=16→46, horizontal y=28 x1=34→62, stroke-width 7)
  crowning **two sergeant chevrons**:
  - Chevron 1: `28,51 48,65 68,51` (stroke-width 8, rounded)
  - Chevron 2: `28,63 48,77 68,63` (stroke-width 8, rounded)
- Canonical SVG: `~/Dev/SyV/syv-design-system/assets/logo/syv-mark.svg`

**Variants (recolor only — geometry never changes):**
| Variant | Colors |
|---|---|
| `militar` (default) | Cross: cream.100 `#F3EEE4` · Chevron1: green.400 `#97A267` · Chevron2: green.neon `#34E867` |
| `argentina` | Cross+Chevron2: celeste.500 `#8FB8D6` |
| `clerical` | Cross: cream.100 `#F3EEE4` · Chevron2: warm.200 `#CDBFA8` |

**Wordmark:** "SUBORDINACIÓN / y VALOR" in Saira Stencil One, to the right of
the mark. Never vectorize — always live text. Sub-line tint: green.500.

For image generation: describe the mark as "a military cross above two
sergeant chevrons, stencil style, worn metal, military insignia" with
the variant's accent color.

---

## 6 — Spacing & Shape

**4px base scale:**
xs=4 · sm=8 · md=12 · lg=16 · xl=20 · 2xl=24 · 3xl=28 · 4xl=32 · 5xl=48 · 6xl=56 · 7xl=64

**Border radius (squared/austere military):**
- Chips/badges: 4px
- Buttons/inputs: 6px
- Cards: 12px
- Dots/avatars: pill (999px)

**Border:** 1.5px hairline (ink.600). No elevation shadows — depth = glow + hairline + radius.

---

## 7 — Character Portrait Guidelines (ComfyUI / SD / pixel art)

When generating character portraits, build the positive prompt in this order:

1. **Quality tags** (model-specific, e.g. `score_9, score_8_up, score_7_up` for Pony/Zavy)
2. **Style anchor:** `dark atmospheric portrait, cinematic lighting, under perpetual cold rain, gritty realism, detailed face`
3. **Character description:** age, gender, physical traits, expression
4. **Faction uniform/appearance:** derived from §3 faction color keys above
5. **Palette call-out:** list the 3–4 dominant hex colors explicitly
6. **Lighting/mood:** `dark near-black backdrop (#0C0B09), single off-center neon-green glow (#34E867), wet surfaces, mist`

**For pixel art (retro RPG portrait style):** add
`pixel art, retro 16-bit RPG character portrait, clean visible square pixel grid,
dithered shading, nostalgic aesthetic, 64x64 style, nearest-exact upscale`

**Negative (always include):**
`source_pony, source_furry, score_4_up, score_5_up, score_6_up,
malformed, deformed, worst quality, simple background, bad hands, bad feet,
watermark, censored, blurry, smooth, 3d render, photorealistic`

**Sampler defaults that work well with zavyfantasiaxlPDXL_v20:**
- Sampler: Euler a · Scheduler: normal · Steps: 35–40 · CFG: 6–7
- Resolution: 896×1152 (portrait) or 768×960 (VRAM-safe)
- Seed: fixed per character for reproducibility

---

## 8 — Mock Character Roster (syv-pj generated)

These are the personajes disponibles from the syv-pj character creator. Each
entry: faction, visual keys derived from §3, suggested portrait seed.

The mock personaje used in the pixel art workflow was:
- **Ignacio "El Monje" Riestra** — Confederación/Fuerzas Armadas, fusilero de línea
  - Palette: olive drab #7B8A4E · celeste #8FB8D6 · cream #F3EEE4 · near-black #0C0B09
  - Traits: stern 27yo male officer, rugged face, short grey stubble, cold eyes,
    olive-drab military cap and high collar, perpetual cold rain

For new mocks, read the live personajes from the API or from
`~/Dev/SyV/syv-pj/resources/` and build the prompt following §7.
Map faction from identidad.tags `faccion/*` → §3 color key.

---

## 9 — How to Use This Skill

**For CSS/web:** translate §2 values to `--syv-*` custom properties. See
`~/Dev/SyV/syv-design-system/astro+svelte/syv.tokens.css` for the generated file.

**For Flutter/Dart:** use `SyvColors.*` constants from
`~/Dev/SyV/syv-design-system/flutter/syv_tokens.dart`.

**For ComfyUI prompts:** follow §7 directly. No translation needed — use hex
values and descriptive English/Spanish in the prompt text.

**For pixel art (ComfyUI):** combine §7 with `nearest-exact` downscale to
64×64 then upscale to 512×512 to preserve pixel grid.

**For any output:** the mood in §1 and the faction color keys in §3 are
the most important context. Apply them first; the rest is refinement.
