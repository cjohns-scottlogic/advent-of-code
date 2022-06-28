import { assert } from "console";
import * as fs from "fs";
import * as path from "path";

const puzzle_input = `children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1`;

const map_data = (data: string, split: string): [string, number][] =>
  data.split(split).map((value) => {
    var [item, count] = value.split(":");
    return [item.trim(), Number(count)];
  });

const puzzle = new Map(map_data(puzzle_input, "\n"));

fs.readFile(path.join(__dirname, "input-16.txt"), (err, data) => {
  if (err) throw err;
  var aunts = new Map();

  data
    .toString()
    .split("\r\n")
    .forEach((line) => {
      const pos = line.indexOf(":");
      aunts.set(
        line.substring(0, pos),
        new Map(map_data(line.substring(pos + 2), ","))
      );
    });

  const part1 = [...aunts].filter((item) => {
    return [...item[1]].every((value) => {
      const [item, count] = value;
      return puzzle.get(item) === count;
    });
  });

  const part2 = [...aunts].filter((item) => {
    return [...item[1]].every((value) => {
      const [item, count] = value;
      assert(puzzle.has(item));
      const got = puzzle.get(item);
      if (got === undefined) throw new Error(`'${item}' not found`);

      if (item == "cats" || item == "trees") return count > got;
      if (item == "pomeranians" || item == "goldfish") return count < got;
      return puzzle.get(item) === count;
    });
  });

  assert(part1.length == 1);
  assert(part2.length == 1);

  console.log("Part 1: " + part1[0][0]);
  console.log("Part 2: " + part2[0][0]);
});
