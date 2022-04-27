import * as fs from "fs";
import * as path from "path";

const move = (move: string) => {
  switch (move) {
    case "(":
      return Number(1);
    case ")":
      return Number(-1);
    default:
      return Number(0);
  }
};
const part1 = (input: string) => [...input].map(move).reduce((p, c) => p + c);

const part2 = (input: string) => {
  let floor = 0;
  let pos = 0;
  [...input].some((item) => {
    pos += 1;
    floor += move(item);
    return floor < 0;
  });
  return pos;
};

fs.readFile(path.join(__dirname, "input-01.txt"), (err, data) => {
  if (err) throw err;
  console.log("Part 1: " + part1(data.toString()));
  console.log("Part 2: " + part2(data.toString()));
});
