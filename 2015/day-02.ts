import * as fs from "fs";
import * as path from "path";

const area = ([l, h, w]: number[]) => {
  return 2 * l * w + 2 * w * h + 2 * h * l;
};

const part1 = (input: number[][]) =>
  input
    .map(
      (item) =>
        area(item) +
        item
          .sort((a, b) => a - b)
          .slice(0, 2)
          .reduce((p, c) => p * c)
    )
    .reduce((p, c) => p + c, 0);

const part2 = (input: number[][]) =>
  input
    .map(
      (item) =>
        item
          .sort((a, b) => a - b)
          .slice(0, 2)
          .reduce((p, c) => p * 2 + c * 2) + item.reduce((p, c) => p * c)
    )
    .reduce((p, c) => p + c, 0);

fs.readFile(path.join(__dirname, "input-02.txt"), (err, data) => {
  if (err) throw err;
  let dims = data
    .toString()
    .split("\r\n")
    .map((size) => size.split("x").map((value) => Number(value)));

  console.log("Part 1: " + part1(dims));
  console.log("Part 2: " + part2(dims));
});
