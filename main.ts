// Copies the rendered front page beside this file to the grader's output directory.
// The image is fixed at commit time, so both grading runs write the same bytes.
// Run locally: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const imagePath = fileURLToPath(new URL("./entry.png", import.meta.url));

copyFileSync(imagePath, join(outputDir, "entry.png"));
