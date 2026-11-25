/**
 * Entry for make.fun bounty news-image-20261124
 * "Sum up 24 November's world news in one image".
 *
 * The front page was composed once, offline (see generate.py), and the
 * resulting entry.png is committed next to this file. This program only
 * publishes that file, which is why the output is byte-identical on every
 * run: no clock, randomness, network or image library is involved.
 *
 * Contract:
 *   output  $MAKEFUN_OUTPUT_DIR/entry.png  (default /output/entry.png)
 *   limits  8-bit RGB PNG, at most 1024x1024 and 1 MiB
 *
 * Run locally:
 *   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
 */

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_SIDE = 1024;
const MAX_BYTES = 1024 * 1024;

const source = fileURLToPath(new URL("./entry.png", import.meta.url));
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outputDir, "entry.png");

const png = readFileSync(source);

if (png.length < 24 || !png.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error(`${source} is not a PNG file`);
}

// The IHDR chunk always follows the 8-byte signature: length, type, then
// width and height as big-endian uint32.
const width = png.readUInt32BE(16);
const height = png.readUInt32BE(20);

if (width < 1 || height < 1 || width > MAX_SIDE || height > MAX_SIDE) {
  throw new Error(`${width}x${height} is outside the 1..${MAX_SIDE} px limit`);
}
if (png.length > MAX_BYTES) {
  throw new Error(`${png.length} bytes is over the ${MAX_BYTES}-byte limit`);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(source, target);

console.log(`entry.png ${width}x${height}, ${png.length} bytes -> ${target}`);
