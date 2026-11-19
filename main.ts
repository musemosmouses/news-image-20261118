// "The World in One Image - 18 November 2026" (Node 22, stdlib only).
//
// The entry image is entry.png, drawn by draw.py and kept beside this file.
// This program places a copy of it in the grader's output directory
// (MAKEFUN_OUTPUT_DIR, default /output), making the directory first so
// the copy always lands somewhere writable.
//
// Run locally:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
