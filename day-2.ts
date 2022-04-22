import * as fs from "fs";
import * as path from "path";

const part1 = (input: string[]) => {
  let total = 0;
  input.forEach((present) => {
    const dims = present
      .split("x")
      .map((value) => Number(value))
      .sort((a, b) => a - b);
    const [l, h, w] = dims;

    total += 2 * l * w + 2 * w * h + 2 * h * l;
    total += dims.slice(0, 2).reduce((p, c) => p * c);
  });
  return total;
};

const part2 = (input: string[]) => {
  let total = 0;
  input.forEach((present) => {
    const dims = present
      .split("x")
      .map((value) => Number(value))
      .sort((a, b) => a - b);

    total += dims.slice(0, 2).reduce((p, c) => p * 2 + c * 2);
    total += dims.reduce((p, c) => p * c);
  });
  return total;
};

fs.readFile(path.join(__dirname, "input-2.txt"), (err, data) => {
  if (err) throw err;
  let sizes = data.toString().split("\r\n");

  console.log("Part 1: " + part1(sizes));
  console.log("Part 2: " + part2(sizes));
});
