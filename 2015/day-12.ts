import * as path from "path";
import * as fs from "fs";

const count_in = (obj: any, exclude: string = ""): number => {
  if (typeof obj === "number") return obj;
  if (typeof obj === "string") return 0;
  if (typeof obj === "object") {
    var count = 0;
    for (var item in obj) {
      const child = obj[item];
      if (
        !(obj instanceof Array) &&
        typeof child === "string" &&
        child === exclude
      )
        return 0;
      count += count_in(child, exclude);
    }
    return count;
  }
  throw "Unknown type";
};

fs.readFile(path.join(__dirname, "input-12.json"), (err, data) => {
  if (err) throw err;

  const json = JSON.parse(data.toString());

  console.log("Part 1:", count_in(json));
  console.log("Part 2:", count_in(json, "red"));
});

/*

console.log("Part 1:", count_in(data));
*/
