// Entry for make.fun news-image-20261117 ("Sum up 17 November's world news
// in one image"). The image itself, entry.png, is a 1024x1024 infographic
// drawn in this session; this program only places its bytes at the path
// the grader reads, so every run writes exactly the same file.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const image = readFileSync(new URL("./entry.png", import.meta.url));
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "entry.png"), image);
// The bytes written are exactly the bytes committed in entry.png, so two
// runs always produce identical output.
console.log(`wrote ${image.length} bytes to ${join(outDir, "entry.png")}`);
