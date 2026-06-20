# Empty Brain IA Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the Empty Brain Quartz vault from a flat `content/AI/` folder into a technology-based reference tree with task-collection and tutorial overlay layers, a two-door landing page, and an agent operations memo.

**Architecture:** Reference lives in folders by technology (the only physical home for files). Tasks and Tutorial are overlay layers that only link into the tree. Landing offers two doors (learn / solve). Cross-cuts handled by a short closed tag set, not file duplication.

**Tech Stack:** Quartz v4 (static site, publishes only `content/`), Markdown + Obsidian wikilinks (`[[name]]` resolved by filename, not path), Node 20, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-06-20-empty-brain-ia-redesign.md`

---

## Conventions used in this plan

- **Wikilinks resolve by filename**, not path. `git mv` of a file does NOT break
  `[[links]]` to it as long as the filename stays unique. Renames/merges DO
  require updating links — those tasks call it out explicitly.
- **Phase gate** = the two checks below pass, then commit. Run after every phase:
  - `npx quartz build` exits 0 (built into `scripts/check-build.sh`)
  - `node scripts/check-links.mjs` reports no broken wikilinks
- Use `git mv` (not `mv`) to preserve history.
- Commit after each phase. Do NOT `git push` — that is the final task and
  requires explicit user confirmation.

---

## Deviations from spec (decided here, easy to revisit during execution)

1. **3D domain added.** Spec lists 4 domains; actual content has `Генерация 3D`
   and `TripoSR`. Added `3D-модели` as a 5th technology domain.
2. **Companies get a physical folder** `content/AI/Компании/` as fact-notes. Spec
   says companies stop being a navigation axis — the folder is NOT linked from
   the catalog/landing; it exists only so company files have a home and stay
   reachable via search/graph/links.
3. **`NeuroCamp.md`** technology is ambiguous from its name — Task 2.9 inspects it
   and routes it; defaults to `Несортированное` if unclear.

---

## Target structure

```
content/
  _index.md                      ← landing: two doors
  AI/
    _index.md                    ← reference catalog (the tree root)
    Языковые модели/
      _index.md
      Агенты и автоматизация/    (tools · MCP · харнессы)
    Модели изображений/
      _index.md
    Видеомодели/
      _index.md
    3D-модели/
      _index.md
    Аудиомодели/
      _index.md
    Запуск и железо/             ← shared infra (cloud GPU, aggregators)
      _index.md
    Компании/                    ← fact-notes, not a nav axis
    Задачи/                      ← curated task collections (overlay)
      _index.md
    Учебник/                     ← linear tutorial (overlay), starts with theory
      _index.md
    Несортированное.md           ← inbox (kept)
    Легаси.md                    ← archive (kept)
```

---

## Migration map (current file → home)

Sporny entries are marked **(confirm)** — apply the default, flag if it feels wrong.

### → Языковые модели/
- `Генерация текста.md`, `текста.md` (merge into the домен index in Phase 3)
- `Настройка GPT.md`, `OpenSouce LLM.md`, `Cloude tutorials.md`
- `xAI Grok.md`, `cohere.md`, `deepseek.md`, `Mistral.md`, `character.ai.md`,
  `Perplexity.md`, `GigaChat.md`
- `LM Studio.md` (local LLM runner) **(confirm: could go to Запуск и железо)**

### → Языковые модели/Агенты и автоматизация/
- `Агенты, автоматизация, аналитические утилиты.md`, `MCP.md`

### → Модели изображений/
- `Генерация изображения (web).md`, `Генерация изображений (local+cloud).md`,
  `Генерация графики.md` (merge in Phase 3)
- `Stable Diffusion.md`, `Flux.md`, `Flux Kontext.md`, `Midjourney.md`,
  `Dall-e.md`, `Adobe FireFly.md`, `Krea.ai.md`, `Шедеврум.md`, `Кандинский.md`
- `ComfyUI.md`, `ComfyUI workflows.md`, `Automatic 1111.md`, `ControlNet.md`
- `inswapper.md` (faceswap)

### → Видеомодели/
- `Генерация видео.md`, `Runway.md`
- `Minimaxi.md` **(confirm: MiniMax is multi-modal; default video, tag others)**

### → 3D-модели/
- `Генерация 3D.md`, `TripoSR.md`

### → Аудиомодели/
- `Генерация звука.md`, `suno tutorial.md`, `SoundFeel.md`,
  `Транскрибация речи.md` (STT — audio home, tag `#текст`)

### → Запуск и железо/
- `AI платформы.md`

### → Компании/
- `OpenAi.md`, `Anthropic.md`, `Google DeepMind.md`, `Meta.md`, `Сбер.md`,
  `Яндекс.md`, `Stability AI.md`, `Black Forest Labs.md`,
  `Компании и стартапы.md`

### → Учебник/ (theory becomes tutorial start)
- `ИИ Теория.md`, `Принципы работы ИИ.md`, `Теория о языковых моделях.md`,
  `Пиксели и перцептроны.md`, `Кейсы применения AI.md`

### Kept where useful / inbox / resources
- `AI_Tools.md` → becomes the catalog (Phase 4); for now stays put
- `Несортированное.md`, `Легаси.md` → keep in `AI/`
- `Лист подписок AI.md` → keep in `AI/` (resources) **(confirm)**
- `AI Бенчмарки.md` → inspect; if empty delete, else → `Запуск и железо` or
  `Учебник` **(confirm in Task 2.9)**

---

## Phase 0 — Baseline & link checker

### Task 0.1: Confirm the site builds today

**Files:** none (baseline check)

- [ ] **Step 1: Install deps if needed**

Run: `npm ci`
Expected: completes without error.

- [ ] **Step 2: Build**

Run: `npx quartz build`
Expected: exits 0, prints "Emitted … files". This is the green baseline; if it
fails now, stop and fix the build before any restructuring.

### Task 0.2: Add a reusable broken-wikilink checker

**Files:**
- Create: `scripts/check-links.mjs`
- Create: `scripts/check-build.sh`

- [ ] **Step 1: Write the link checker**

```javascript
// scripts/check-links.mjs
// Scans content/ for [[wikilinks]] whose target file does not exist.
// Resolves by filename (Quartz shortest-path), ignores headings/aliases.
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, basename, extname } from "node:path";

const ROOT = "content";
const IGNORE = new Set([".obsidian", "notes"]);

function walk(dir) {
  const out = [];
  for (const e of readdirSync(dir)) {
    if (IGNORE.has(e)) continue;
    const p = join(dir, e);
    if (statSync(p).isDirectory()) out.push(...walk(p));
    else if (extname(p) === ".md") out.push(p);
  }
  return out;
}

const files = walk(ROOT);
const names = new Set(files.map((f) => basename(f, ".md")));

const linkRe = /\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]/g;
let broken = 0;
for (const f of files) {
  const text = readFileSync(f, "utf8");
  for (const m of text.matchAll(linkRe)) {
    const target = m[1].trim();
    if (!names.has(target)) {
      console.log(`BROKEN  ${f}  ->  [[${target}]]`);
      broken++;
    }
  }
}
if (broken === 0) console.log("OK: no broken wikilinks");
else { console.log(`\n${broken} broken wikilink(s)`); process.exit(1); }
```

- [ ] **Step 2: Write the build gate wrapper**

```bash
# scripts/check-build.sh
#!/usr/bin/env bash
set -euo pipefail
npx quartz build
echo "BUILD OK"
```

- [ ] **Step 3: Run both checks (record current state)**

Run: `node scripts/check-links.mjs`
Expected: `OK: no broken wikilinks` (we fixed the known ones earlier). If any
appear, fix them before continuing.

Run: `bash scripts/check-build.sh`
Expected: ends with `BUILD OK`.

- [ ] **Step 4: Commit**

```bash
git add scripts/check-links.mjs scripts/check-build.sh
git commit -m "Add build + broken-wikilink check scripts"
```

---

## Phase 1 — Domain skeleton (folders + index pages)

### Task 1.1: Create domain folders with folder-page index files

**Files (create):**
- `content/AI/Языковые модели/_index.md`
- `content/AI/Языковые модели/Агенты и автоматизация/_index.md`
- `content/AI/Модели изображений/_index.md`
- `content/AI/Видеомодели/_index.md`
- `content/AI/3D-модели/_index.md`
- `content/AI/Аудиомодели/_index.md`
- `content/AI/Запуск и железо/_index.md`
- `content/AI/Задачи/_index.md`
- `content/AI/Учебник/_index.md`

- [ ] **Step 1: Create the folders**

```bash
cd content/AI
mkdir -p "Языковые модели/Агенты и автоматизация" \
  "Модели изображений" "Видеомодели" "3D-модели" "Аудиомодели" \
  "Запуск и железо" "Компании" "Задачи" "Учебник"
cd ../..
```

- [ ] **Step 2: Write each `_index.md`** (folder landing pages)

`content/AI/Языковые модели/_index.md`:
```markdown
---
title: Языковые модели
---
Модели для работы с текстом: чат, генерация, кодинг. Здесь же — надстройки над
текстовым стеком: [[Агенты и автоматизация]].

## Чат и генерация текста
## Кодинг
## Запуск локально
```

`content/AI/Языковые модели/Агенты и автоматизация/_index.md`:
```markdown
---
title: Агенты и автоматизация
---
Надстройка над языковыми моделями: агенты, инструменты (tools), MCP, харнессы.

## Агенты
## MCP
## Харнессы и инструменты
```

`content/AI/Модели изображений/_index.md`:
```markdown
---
title: Модели изображений
---
## Генерация (text-to-image)
## Редактирование (image-to-image, inpaint, faceswap)
## Запуск
```

`content/AI/Видеомодели/_index.md`:
```markdown
---
title: Видеомодели
---
## Генерация
## Редактирование
```

`content/AI/3D-модели/_index.md`:
```markdown
---
title: 3D-модели
---
Создание 3D-моделей по тексту и фото, сканирование объектов и пространств.

## Генерация
## Сканирование / фотограмметрия
```

`content/AI/Аудиомодели/_index.md`:
```markdown
---
title: Аудиомодели
---
## Генерация музыки
## Синтез речи (TTS)
## Транскрибация (STT)
## Обработка звука
```

`content/AI/Запуск и железо/_index.md`:
```markdown
---
title: Запуск и железо
---
Общая инфраструктура для запуска моделей: облачные GPU-хостинги и
платформы-агрегаторы. Доменно-специфичный запуск (оболочки под конкретный стек)
живёт внутри своего домена.
```

`content/AI/Задачи/_index.md`:
```markdown
---
title: Задачи
---
Подборки инструментов под конкретный результат. В отличие от справочника, здесь
ось — «что нужно сделать», а не «чем сделано».

- [[Сделать видео]]
- [[Убрать фон]]
```

`content/AI/Учебник/_index.md`:
```markdown
---
title: Учебник
---
Последовательный маршрут от основ к конкретике. Повторяет технический скелет
справочника, но связным рассказом. Читается сверху вниз.

1. [[ИИ Теория]]
2. [[Принципы работы ИИ]]
3. [[Теория о языковых моделях]]
```

- [ ] **Step 3: Phase gate**

Run: `bash scripts/check-build.sh` → `BUILD OK`
Run: `node scripts/check-links.mjs` — broken links to `[[Сделать видео]]`,
`[[Убрать фон]]` are EXPECTED here (created in Phase 5); note them, do not fail
the phase on those two. All others must resolve.

- [ ] **Step 4: Commit**

```bash
git add content/AI
git commit -m "Add domain folder skeleton with index pages"
```

---

## Phase 2 — Migrate reference files into homes

Each task = move one batch with `git mv`, then run the phase gate, then commit.
Wikilinks survive the moves (filenames unchanged).

### Task 2.1: Language models

- [ ] **Step 1: Move**

```bash
cd content/AI
git mv "xAI Grok.md" "cohere.md" "deepseek.md" "Mistral.md" \
  "character.ai.md" "Perplexity.md" "GigaChat.md" "Настройка GPT.md" \
  "OpenSouce LLM.md" "Cloude tutorials.md" "LM Studio.md" "Языковые модели/"
git mv "Агенты, автоматизация, аналитические утилиты.md" "MCP.md" \
  "Языковые модели/Агенты и автоматизация/"
cd ../..
```

- [ ] **Step 2: Gate** — `bash scripts/check-build.sh` and `node scripts/check-links.mjs` (only the Phase-5 placeholders may be broken).
- [ ] **Step 3: Commit** — `git add -A && git commit -m "Migrate language-model files into domain"`

### Task 2.2: Image models

- [ ] **Step 1: Move**

```bash
cd content/AI
git mv "Stable Diffusion.md" "Flux.md" "Flux Kontext.md" "Midjourney.md" \
  "Dall-e.md" "Adobe FireFly.md" "Krea.ai.md" "Шедеврум.md" "Кандинский.md" \
  "ComfyUI.md" "ComfyUI workflows.md" "Automatic 1111.md" "ControlNet.md" \
  "inswapper.md" "Модели изображений/"
cd ../..
```

- [ ] **Step 2: Gate.**
- [ ] **Step 3: Commit** — `git commit -am "Migrate image-model files into domain"`

### Task 2.3: Video models

- [ ] **Step 1: Move**

```bash
cd content/AI
git mv "Runway.md" "Minimaxi.md" "Видеомодели/"
cd ../..
```

- [ ] **Step 2: Gate.**
- [ ] **Step 3: Commit** — `git commit -am "Migrate video-model files into domain"`

### Task 2.4: 3D models

- [ ] **Step 1: Move**

```bash
cd content/AI
git mv "Генерация 3D.md" "TripoSR.md" "3D-модели/"
cd ../..
```

- [ ] **Step 2: Gate.**
- [ ] **Step 3: Commit** — `git commit -am "Migrate 3D-model files into domain"`

### Task 2.5: Audio models

- [ ] **Step 1: Move**

```bash
cd content/AI
git mv "suno tutorial.md" "SoundFeel.md" "Транскрибация речи.md" "Аудиомодели/"
cd ../..
```

- [ ] **Step 2: Gate.**
- [ ] **Step 3: Commit** — `git commit -am "Migrate audio-model files into domain"`

### Task 2.6: Shared infrastructure

- [ ] **Step 1: Move**

```bash
cd content/AI
git mv "AI платформы.md" "Запуск и железо/"
cd ../..
```

- [ ] **Step 2: Gate.**
- [ ] **Step 3: Commit** — `git commit -am "Migrate shared-infra page"`

### Task 2.7: Companies (fact-notes)

- [ ] **Step 1: Move**

```bash
cd content/AI
git mv "OpenAi.md" "Anthropic.md" "Google DeepMind.md" "Meta.md" "Сбер.md" \
  "Яндекс.md" "Stability AI.md" "Black Forest Labs.md" \
  "Компании и стартапы.md" "Компании/"
cd ../..
```

- [ ] **Step 2: Gate.**
- [ ] **Step 3: Commit** — `git commit -am "Move company pages to fact-note folder"`

### Task 2.8: Theory → tutorial

- [ ] **Step 1: Move**

```bash
cd content/AI
git mv "ИИ Теория.md" "Принципы работы ИИ.md" "Теория о языковых моделях.md" \
  "Пиксели и перцептроны.md" "Кейсы применения AI.md" "Учебник/"
cd ../..
```

- [ ] **Step 2: Gate.**
- [ ] **Step 3: Commit** — `git commit -am "Move theory pages into tutorial layer"`

### Task 2.9: Inspect & route leftovers

Remaining in `content/AI/` root should be: `AI_Tools.md`, `Несортированное.md`,
`Легаси.md`, `Лист подписок AI.md`, `AI Бенчмарки.md`, `NeuroCamp.md`,
`текста.md`, `Генерация текста.md`, `Генерация изображения (web).md`,
`Генерация изображений (local+cloud).md`, `Генерация графики.md`,
`Генерация звука.md`, `Генерация видео.md`. (The "Генерация *" list pages are
handled in Phase 3 merges.)

- [ ] **Step 1: Inspect the two ambiguous files**

Run: `wc -l "content/AI/AI Бенчмарки.md" "content/AI/NeuroCamp.md"`
Read both. Decide:
- `AI Бенчмарки.md`: if empty → `git rm`; else `git mv` to `Учебник/` (it is
  evaluative/reference reading).
- `NeuroCamp.md`: route by content — if it's a course/learning resource →
  `Учебник/`; if a tool → its domain; if unclear → leave in `Несортированное`
  context (move into root stays acceptable).

- [ ] **Step 2: Apply the decision** (example if benchmarks non-empty, neurocamp a course)

```bash
cd content/AI
git mv "AI Бенчмарки.md" "NeuroCamp.md" "Учебник/"
cd ../..
```

- [ ] **Step 3: Gate.**
- [ ] **Step 4: Commit** — `git commit -am "Route remaining ambiguous files"`

---

## Phase 3 — Merge duplicate "Генерация *" list pages into domain indexes

The old per-modality list pages overlap with the new domain `_index.md` files.
Fold their live content into the domain index, then delete the originals.

### Task 3.1: Image generation pages → Модели изображений/_index.md

**Files:**
- Modify: `content/AI/Модели изображений/_index.md`
- Delete: `content/AI/Генерация изображения (web).md`,
  `content/AI/Генерация изображений (local+cloud).md`,
  `content/AI/Генерация графики.md`

- [ ] **Step 1: Read all three source pages**

Run: `cat "content/AI/Генерация изображения (web).md" "content/AI/Генерация изображений (local+cloud).md" "content/AI/Генерация графики.md"`

- [ ] **Step 2: Fold their non-stale entries** under the matching `##` sections
of `Модели изображений/_index.md` (`## Генерация`, `## Редактирование`,
`## Запуск`). Keep named links `[text](url)`, drop dead/struck entries. Preserve
`[[ComfyUI]]`, `[[Stable Diffusion]]`, `[[Automatic 1111]]` wikilinks.

- [ ] **Step 3: Update inbound links** to the deleted pages

Run: `node scripts/check-links.mjs` after deletion to find any `[[Генерация изображения (web)]]` etc. references; repoint them to `[[Модели изображений]]`.

- [ ] **Step 4: Delete originals**

```bash
cd content/AI
git rm "Генерация изображения (web).md" "Генерация изображений (local+cloud).md" "Генерация графики.md"
cd ../..
```

- [ ] **Step 5: Gate** (links must be clean now) **and Commit**

```bash
git add -A && git commit -m "Merge image generation pages into domain index"
```

### Task 3.2: Text pages → Языковые модели/_index.md

**Files:**
- Modify: `content/AI/Языковые модели/_index.md`
- Delete: `content/AI/Генерация текста.md`, `content/AI/текста.md`

- [ ] **Step 1: Read** `cat "content/AI/Генерация текста.md" "content/AI/текста.md"`
- [ ] **Step 2: Fold** live entries under `## Чат и генерация текста` / `## Кодинг`.
- [ ] **Step 3: Repoint inbound links** to `[[Языковые модели]]` (run checker).
- [ ] **Step 4: Delete** — `cd content/AI && git rm "Генерация текста.md" "текста.md" && cd ../..`
- [ ] **Step 5: Gate & Commit** — `git add -A && git commit -m "Merge text pages into language-model index"`

### Task 3.3: Audio & video list pages → domain indexes

**Files:**
- Modify: `content/AI/Аудиомодели/_index.md`, `content/AI/Видеомодели/_index.md`
- Delete: `content/AI/Генерация звука.md`, `content/AI/Генерация видео.md`

- [ ] **Step 1: Read** both source pages.
- [ ] **Step 2: Fold** audio entries under the four audio `##` sections; video
  entries under `## Генерация` / `## Редактирование`.
- [ ] **Step 3: Repoint inbound links** (`[[Генерация звука]]`,
  `[[Генерация видео]]`) to `[[Аудиомодели]]` / `[[Видеомодели]]` (run checker).
- [ ] **Step 4: Delete** — `cd content/AI && git rm "Генерация звука.md" "Генерация видео.md" && cd ../..`
- [ ] **Step 5: Gate & Commit** — `git add -A && git commit -m "Merge audio/video list pages into domain indexes"`

---

## Phase 4 — Landing (two doors) + reference catalog

### Task 4.1: Rebuild the reference catalog from AI_Tools.md

**Files:**
- Modify: `content/AI/_index.md` (currently absent — create it as the AI section
  root / catalog) using the curated section list from `AI_Tools.md`
- Modify/retire: `content/AI/AI_Tools.md`

- [ ] **Step 1: Read** `cat content/AI/AI_Tools.md`
- [ ] **Step 2: Create `content/AI/_index.md`** as the catalog — annotated links
  to the five domains plus shared infra, keeping the intro callout from
  AI_Tools. Drop the "Компании" entry (no longer a nav axis).

```markdown
---
title: ИИ инструменты
tags:
  - artificial_intelligence
  - нейросети
aliases:
  - ИИ
  - Нейронки
enableToc: true
---
> [!info]- Об этой странице
> Справочник по нейросетевым инструментам, сгруппированный по технологии.
> Ищешь решение задачи — загляни в [[Задачи]]. Хочешь разобраться с нуля —
> [[Учебник]].

### [[Языковые модели]]
Текст, чат, кодинг и надстройки над ними — агенты, MCP, харнессы.

### [[Модели изображений]]
Генерация и редактирование изображений, локальный/облачный запуск.

### [[Видеомодели]]
Генерация и редактирование видео.

### [[3D-модели]]
3D по тексту и фото, сканирование.

### [[Аудиомодели]]
Музыка, синтез речи, транскрибация, обработка звука.

### [[Запуск и железо]]
Облачные GPU и платформы-агрегаторы — общее для всех моделей.

---
### [[Несортированное]]
Инбокс для неразобранных ссылок.

[[Легаси]] — потерявшее актуальность, хранится для истории.
```

- [ ] **Step 3: Retire AI_Tools.md** — replace its body with a redirect note so
  old inbound `[[AI_Tools]]` links keep working:

```markdown
---
title: ИИ инструменты (переехало)
aliases:
  - AI_Tools
---
Эта страница переехала: см. [[ИИ инструменты]].
```

- [ ] **Step 4: Gate & Commit** — `git add -A && git commit -m "Rebuild reference catalog as AI/_index.md"`

### Task 4.2: Two-door landing

**Files:**
- Modify: `content/_index.md`

- [ ] **Step 1: Rewrite** `content/_index.md`:

```markdown
---
title: 🐘 Empty Brain
enableToc: false
---
Открытая база знаний про нейросетевые инструменты.

## Зачем ты здесь?

- **Разобраться с нуля** → [[Учебник]] — последовательный маршрут от основ.
- **Решить задачу** → [[Задачи]] — подборки инструментов под результат.

Или просто смотреть всё по типам → [[ИИ инструменты|каталог справочника]].
```

- [ ] **Step 2: Gate & Commit** — `git add -A && git commit -m "Two-door landing page"`

---

## Phase 5 — Task layer (scaffold + two worked examples)

### Task 5.1: Create the two placeholder task pages referenced earlier

**Files (create):**
- `content/AI/Задачи/Сделать видео.md`
- `content/AI/Задачи/Убрать фон.md`

- [ ] **Step 1: Write `Сделать видео.md`** — a curated collection that resolves
  the video-via-code paradox explicitly:

```markdown
---
title: Сделать видео
tags:
  - задача
---
Способы получить видео — от профильных моделей до обходных путей.

## Профильные видеомодели
Классический путь. См. [[Видеомодели]].

## Через языковые модели и код
Анимация через генерируемый HTML/код — работает там, где видеомодели пасуют
(анимированный текст, графика). См. [[Агенты и автоматизация]].
```

- [ ] **Step 2: Write `Убрать фон.md`**:

```markdown
---
title: Убрать фон
tags:
  - задача
---
Инструменты и модели для удаления фона. См. раздел редактирования в
[[Модели изображений]].
```

- [ ] **Step 3: Gate** — now `node scripts/check-links.mjs` must be FULLY clean
  (the two placeholders from Phase 1 now exist). **Commit.**

```bash
git add -A && git commit -m "Add worked task-collection examples"
```

---

## Phase 6 — Tutorial layer ordering

### Task 6.1: Sequence the tutorial index against migrated theory files

**Files:**
- Modify: `content/AI/Учебник/_index.md`

- [ ] **Step 1: List** what landed in the tutorial folder

Run: `ls "content/AI/Учебник/"`

- [ ] **Step 2: Rewrite the index** as an ordered reading path that mirrors the
  technical skeleton (theory → domains), linking the real files present and the
  domain indexes for the "далее, конкретика" steps. Use only `[[links]]` that
  resolve (verify against the `ls` output).

- [ ] **Step 3: Gate & Commit** — `git add -A && git commit -m "Order tutorial reading path"`

---

## Phase 7 — Facet tags

### Task 7.1: Define and apply the closed tag set

**Files:**
- Modify: domain `_index.md` files and the cross-cut pages identified below.

- [ ] **Step 1: Lock the closed facet set** (document it at the top of
  `CLAUDE.md` in Phase 8). Initial set:
  - access: `#облако`, `#локально`
  - cross-modality: `#через-код`
  - audience: `#для-дизайна`
  - role: `#агенты`
  - task pages already use `#задача`

- [ ] **Step 2: Apply tags only where they add cross-cut reach** — e.g.
  `Транскрибация речи.md` gets `#текст`-stage note via tag, MiniMax page gets the
  modalities it spans, local runners get `#локально`. Do NOT bulk-tag every file.

- [ ] **Step 3: Gate & Commit** — `git add -A && git commit -m "Apply closed facet tag set to cross-cut pages"`

---

## Phase 8 — Agent ops memo + Explorer sanity

### Task 8.1: Write root CLAUDE.md (operations memo)

**Files:**
- Create: `CLAUDE.md` (repo root)

- [ ] **Step 1: Write the memo** — a short operational distillation of the spec:

```markdown
# Empty Brain — как раскладывать контент

База знаний про нейросети, публикуется через Quartz (только `content/`).
Полное обоснование: `docs/superpowers/specs/2026-06-20-empty-brain-ia-redesign.md`.

## Принципы
- **Один дом по технологии.** Файл лежит в домене по тому, ЧЕМ сделан инструмент,
  а не что на выходе. Пересечения — тегами и подборками, не копией файла.
- **Домены:** Языковые модели · Модели изображений · Видеомодели · 3D-модели ·
  Аудиомодели. Общий запуск — «Запуск и железо». Агенты/MCP/харнессы — внутри
  языковых моделей.
- **Транскрибация** = аудио (вход — звук), стык с текстом — тег `#текст`.
- **Компании** — не ось навигации, лежат в `AI/Компании/` как факт-заметки.
- **Внутри домена дробим по типу модели**, не по задаче.
- **Органический порог:** инструмент = строка в списке; перерос (туториал,
  свои под-ссылки) → отдельный файл; группа файлов разрослась → папка.
- **Задачи** (`AI/Задачи/`) — курируемые подборки по результату, пишутся вручную.
- **Учебник** (`AI/Учебник/`) — линейный нарратив, ссылается и пересказывает,
  не копирует справочник.

## Закрытый набор тегов-фасетов
`#облако` `#локально` `#через-код` `#для-дизайна` `#агенты` `#задача`
Новые теги добавлять обдуманно — набор держим коротким.

## Перед коммитом
- `bash scripts/check-build.sh` (Quartz собирается)
- `node scripts/check-links.mjs` (нет битых `[[ссылок]]`)
```

- [ ] **Step 2: Commit** — `git add CLAUDE.md && git commit -m "Add agent ops memo"`

### Task 8.2: Verify Explorer now shows a real tree

**Files:** none (manual/visual verification) — optionally `quartz.layout.ts` if a tweak is needed.

- [ ] **Step 1: Build and serve**

Run: `npx quartz build --serve`
Open the local URL. Confirm the left Explorer panel now shows the domain folders
as a nested tree (not a flat alphabetical list), and the landing shows two doors.

- [ ] **Step 2: If Explorer ordering/labels need tuning**, adjust
  `Component.Explorer()` options in `quartz.layout.ts` (sort/order). Otherwise no
  change. Re-run the gate if edited.

- [ ] **Step 3: Commit if changed** — `git commit -am "Tune Explorer ordering"` (skip if no change)

---

## Phase 9 — Final verification & publish

### Task 9.1: Full gate + push (with confirmation)

- [ ] **Step 1: Final checks**

Run: `node scripts/check-links.mjs` → `OK: no broken wikilinks`
Run: `bash scripts/check-build.sh` → `BUILD OK`

- [ ] **Step 2: Review the diff summary**

Run: `git log --oneline main@{1}..HEAD` and `git status`
Confirm only intended content/structure changed.

- [ ] **Step 3: Ask the user before pushing.** Pushing redeploys the live site
  via GitHub Actions. Do NOT push without explicit confirmation. On confirmation:

```bash
git push origin main
```

- [ ] **Step 4: Verify deploy** — after Actions completes, load
  `bloorgard.github.io/empty-brain` and spot-check the landing, a domain page,
  and Explorer.

---

## Self-review notes (author checklist, already applied)

- **Spec coverage:** two-door landing (P4), tech tree with 5 domains (P1–P2),
  agents inside language models (P1/P2.1), transcription→audio+tag (P2.5/P7),
  companies de-axed (P2.7), shared-vs-domain infra (P1/P2.6), task layer
  (P5), tutorial layer (P2.8/P6), facet tags (P7), organic-growth rule
  (CLAUDE.md P8), CLAUDE.md memo (P8). 3D-domain gap closed (deviation #1).
- **Placeholders:** the only intentional deferred decisions are the **(confirm)**
  routings in the migration map and Task 2.9 inspection — all have explicit
  defaults and apply-commands.
- **Naming consistency:** wikilink targets used in indexes/landing
  (`[[Языковые модели]]`, `[[Модели изображений]]`, `[[Видеомодели]]`,
  `[[3D-модели]]`, `[[Аудиомодели]]`, `[[Запуск и железо]]`, `[[Задачи]]`,
  `[[Учебник]]`, `[[ИИ инструменты]]`, `[[Сделать видео]]`, `[[Убрать фон]]`)
  match the `_index.md` titles / filenames created in P1, P4, P5.
```
