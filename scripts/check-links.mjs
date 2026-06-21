// scripts/check-links.mjs
// Scans content/ for [[wikilinks]] whose target file does not exist.
// Resolves by filename (Quartz shortest-path), ignores headings/aliases.
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, basename, dirname, extname } from "node:path";

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
// A note is reachable by its filename and by aliases in its frontmatter.
// NOTE: folder-index pages (`_index.md`) are NOT reachable via [[FolderName]]
// in Quartz "shortest" resolution (their slug ends in /index, not the folder
// name) nor in Obsidian. So a folder name does NOT make [[FolderName]] valid —
// use a folder-note (`Folder/Folder.md`) instead.
const names = new Set();
function addAliases(text) {
  const fm = text.match(/^---\n([\s\S]*?)\n---/);
  if (!fm) return;
  const block = fm[1].match(/^aliases:[ \t]*(.*(?:\n[ \t]+-.*)*)/m);
  if (!block) return;
  const inline = block[1].trim();
  if (inline && !inline.startsWith("-")) names.add(inline.replace(/['"]/g, ""));
  for (const m of block[1].matchAll(/^[ \t]+-\s*(.+)$/gm)) {
    names.add(m[1].trim().replace(/['"]/g, ""));
  }
}
for (const f of files) {
  const base = basename(f, ".md");
  // _index/index pages are not [[name]]-addressable; skip their basename.
  if (base !== "_index" && base !== "index") names.add(base);
  addAliases(readFileSync(f, "utf8"));
}

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
