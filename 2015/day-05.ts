import * as fs from "fs";
import * as path from "path";

const part1 = (names: string[]) =>
  names.filter((name) => {
    const vowels = "aeiou".split("");
    var vowel_count = 0;
    var excluded = false;
    var repeated = false;

    for (var i = 0; i < name.length; ++i) {
      if (vowels.includes(name.charAt(i))) vowel_count++;
      repeated = repeated || (i > 0 && name.charAt(i - 1) == name.charAt(i));
    }

    "ab cd pq xy".split(" ").forEach((pat) => {
      if (name.includes(pat)) excluded = true;
    });

    return vowel_count >= 3 && repeated && !excluded;
  }).length;

const part2 = (names: string[]) =>
  names.filter((name) => {
    var xyx = false;
    var abab = false;

    for (var i = 1; i < name.length; ++i) {
      xyx = xyx || name.charAt(i - 2) === name.charAt(i);
      abab = abab || name.indexOf(name.slice(i - 1, i + 1), i + 1) !== -1;
    }

    return xyx && abab;
  }).length;

fs.readFile(path.join(__dirname, "input-05.txt"), (err, data) => {
  if (err) throw err;
  var names = data.toString().split("\r\n");

  console.log("Part 1: " + part1(names));
  console.log("Part 2: " + part2(names));
});
