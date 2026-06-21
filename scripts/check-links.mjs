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
