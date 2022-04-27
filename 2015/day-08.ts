import * as fs from "fs";
import * as path from "path";

fs.readFile(path.join(__dirname, "input-08.txt"), (err, data) => {
  if (err) throw err;
  var lines = data.toString().split("\r\n");

  var len1 = lines.map((line) => line.length).reduce((p, c) => p + c);

  var decoded = lines.map((line) => eval("String(" + line + ")"));
  var len2 = decoded.map((line) => line.length).reduce((p, c) => p + c);
  console.log("Part 1: " + (len1 - len2));

  var encoded = lines.map(
    (line) => '"' + line.replace(/\\/g, "\\\\").replace(/\"/g, '\\"') + '"'
  );
  var len3 = encoded.map((line) => line.length).reduce((p, c) => p + c);
  console.log("Part 2: " + (len3 - len1));
});
