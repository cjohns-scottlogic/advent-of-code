import * as fs from "fs";
import * as path from "path";

const permutations = <Type>(arr: Array<Type>): Array<Array<Type>> => {
  if (arr.length <= 2)
    return arr.length === 2 ? [arr, [arr[1], arr[0]]] : [arr];
  return arr.reduce(
    (acc: any, item: Type, i: number) =>
      acc.concat(
        permutations([...arr.slice(0, i), ...arr.slice(i + 1)]).map(
          (val: Array<Type>) => [item, ...val]
        )
      ),
    []
  );
};

//   var people = new Map<string, Map<string, number>>();

const bestSeating = (people: Map<string, Map<string, number>>): number => {
  const arragements = permutations([...people.keys()]);
  const happyness = arragements.map((arragement) => {
    var value = 0;
    arragement.forEach((item, index, array) => {
      const other = index < array.length - 1 ? array[index + 1] : array[0];
      value += people.get(item)!.get(other)!;
      value += people.get(other)!.get(item)!;
    });
    return value;
  });

  return happyness.reduce((a, b) => Math.max(a, b));
};

fs.readFile(path.join(__dirname, "input-13.txt"), (err, data) => {
  if (err) throw err;
  var people = new Map<string, Map<string, number>>();

  data
    .toString()
    .split("\r\n")
    .forEach((line) => {
      const match = line.match(
        /(.*) would (.*) (\d*) happiness units by sitting next to (.*)\./
      );
      if (match) {
        const [_, a, gl, c, b] = match;
        const v = Number(c) * (gl === "lose" ? -1 : 1);

        var ent = people.get(a);
        if (ent) ent.set(b, v);
        else people.set(a, new Map([[b, v]]));
      }
    });

  console.log("Part 1: " + bestSeating(people));

  [...people.keys()].forEach((person) => {
    people.get(person)!.set("Me", 0);

    var ent = people.get("Me");
    if (ent) ent.set(person, 0);
    else people.set("Me", new Map([[person, 0]]));
  });

  console.log("Part 2: " + bestSeating(people));
});
