import * as fs from "fs";
import * as path from "path";

const solve = (
  distances: Map<string, Map<string, number>>,
  path: Array<string>,
  cost: number,
  compare: (a: number, b: number) => boolean
): number => {
  // Places we can go next?
  var next: [string, number][];

  if (path.length > 0) {
    const next1 = distances.get(path[path.length - 1]);
    if (next1) {
      // Filter the possible destinations from here for ones we've already visited
      next = [...next1.entries()].filter(([place, _]) => !path.includes(place));
    } else throw "Item not found";
  } else next = [...distances.keys()].map((key) => [key, 0]);

  // None left? We've done.
  if (next.length === 0) {
    return cost;
  }

  // Try each path, and return the most 'compare' one
  return next
    .map(([value, dist]) =>
      solve(distances, new Array<string>(...path, value), cost + dist, compare)
    )
    .reduce((a, b) => (compare(a, b) ? a : b));
};

const add_distance = (
  distances: Map<string, Map<string, number>>,
  from: string,
  to: string,
  dist: number
) => {
  var f = distances.get(from);
  if (f) f.set(to, dist);
  else distances.set(from, new Map([[to, dist]]));
};

fs.readFile(path.join(__dirname, "input-09.txt"), (err, data) => {
  if (err) throw err;
  var distances = new Map<string, Map<string, number>>();
  data
    .toString()
    .split("\r\n")
    .forEach((line) => {
      const match = line.match(/(.*) to (.*) = (\d*)/);
      if (match) {
        const [, fm, to, d] = match;
        const dist = Number(d);

        add_distance(distances, fm, to, dist);
        add_distance(distances, to, fm, dist);
      }
    });

  console.log(
    "Part 1:",
    solve(distances, [], 0, (a, b) => a < b)
  );
  console.log(
    "Part 2:",
    solve(distances, [], 0, (a, b) => a > b)
  );
});
