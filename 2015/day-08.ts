import * as fs from "fs";
import * as path from "path";

const part1 = (line: string): number => {
  var reduced = 2; // The enclosing quotes
  var escape = false;

  [...line].forEach((char) => {
    if (escape) {
      escape = false;
      if (char == "\\" || char == '"') reduced += 1;
      if (char == "x") reduced += 3;
    } else {
      if (char === "\\") escape = true;
    }
  });

  return reduced;
};

const part2 = (line: string): number => {
  var extended = 2; // The enclosing quotes

  [...line].forEach((char) => {
    if (char == "\\" || char == '"') extended += 1;
  });

  return extended;
};

fs.readFile(path.join(__dirname, "input-08.txt"), (err, data) => {
  if (err) throw err;
  var lines = data.toString().split("\r\n");

  console.log("Part 1: " + lines.map(part1).reduce((p, c) => p + c));
  console.log("Part 2: " + lines.map(part2).reduce((p, c) => p + c));
});
