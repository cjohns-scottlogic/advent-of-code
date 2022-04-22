import * as fs from "fs";
import * as path from "path";

const part1 = (input: string) => {
  let floor = 0;
  [...input].forEach((item) => {
    if (item == "(") floor += 1;
    else if (item == ")") floor -= 1;
    else console.log(item);
  });
  return floor;
};

const part2 = (input: string) => {
  let floor = 0;
  let pos = 0;
  [...input].some((item) => {
    pos += 1;
    if (item == "(") floor += 1;
    else if (item == ")") floor -= 1;
    return floor < 0;
  });
  return pos;
};

fs.readFile(path.join(__dirname, "input-1.txt"), (err, data) => {
  if (err) throw err;
  console.log("Part 1: " + part1(data.toString()));
  console.log("Part 2: " + part2(data.toString()));
});
