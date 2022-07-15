import * as fs from "fs";
import * as path from "path";

const neighbours = (lights: string[][], row: number, col: number) => {
  const clen = lights[row].length - 1;
  const rlen = lights.length - 1;
  var on = 0;

  if (row > 0) {
    if (col > 0) on += lights[row - 1][col - 1] === "#" ? 1 : 0;
    on += lights[row - 1][col] === "#" ? 1 : 0;
    if (col < clen) on += lights[row - 1][col + 1] === "#" ? 1 : 0;
  }

  if (col > 0) on += lights[row][col - 1] === "#" ? 1 : 0;
  if (col < clen) on += lights[row][col + 1] === "#" ? 1 : 0;

  if (row < rlen) {
    if (col > 0) on += lights[row + 1][col - 1] === "#" ? 1 : 0;
    on += lights[row + 1][col] === "#" ? 1 : 0;
    if (col < clen) on += lights[row + 1][col + 1] === "#" ? 1 : 0;
  }

  return on;
};

const step = (lights: string[][], part: 1 | 2) =>
  lights.map((row, rindex) =>
    row.map((value, cindex) => {
      if (
        part === 2 &&
        (rindex === 0 || rindex === lights.length - 1) &&
        (cindex === 0 || cindex == lights[rindex].length - 1)
      )
        return "#";

      const n = neighbours(lights, rindex, cindex);
      return (value === "#" ? n === 2 || n === 3 : n === 3) ? "#" : ".";
    })
  );

fs.readFile(path.join(__dirname, "input-18.txt"), (err, data) => {
  if (err) throw err;

  var lights: string[][] = [];
  data
    .toString()
    .split("\r\n")
    .forEach((line) => {
      lights.push([...line]);
    });

  var lights1 = lights;
  var lights2 = lights;

  for (var s = 0; s < 100; ++s) {
    lights1 = step(lights1, 1);
    lights2 = step(lights2, 2);
  }

  const count = (lights: string[][]) =>
    lights
      .map((row) =>
        row
          .map((value) => (value === "#" ? Number(1) : Number(0)))
          .reduce((p, c) => p + c, 0)
      )
      .reduce((p, c) => p + c, 0);

  console.log("Part 1: " + count(lights1));
  console.log("Part 2: " + count(lights2));
});
