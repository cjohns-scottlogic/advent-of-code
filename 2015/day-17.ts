import * as fs from "fs";
import * as path from "path";

fs.readFile(path.join(__dirname, "input-17.txt"), (err, data) => {
  if (err) throw err;
  var containers = new Array();

  data
    .toString()
    .split("\r\n")
    .forEach((line) => {
      containers.push(Number(line));
    });

  const count = containers.length;
  var min = count;

  var part1 = 0;
  var part2 = 0;

  for (var i = 0; i < 1 << count; ++i) {
    const used = containers.filter((_, index) => i & (1 << index));
    const total = used.reduce((a, b) => a + b, 0);

    if (total === 150) {
      part1 += 1;
      if (used.length < min) {
        min = used.length;
        part2 = 1;
      } else if (used.length === min) part2 += 1;
    }
  }

  console.log("Part 1: " + part1);
  console.log("Part 2: " + part2);
});
