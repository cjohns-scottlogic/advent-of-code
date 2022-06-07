import * as fs from "fs";
import * as path from "path";

class Reindeer {
  public readonly name: string;
  public readonly speed: number;
  public readonly time: number;
  public readonly rest: number;

  public constructor(data: string[]) {
    this.name = data[1];
    this.speed = Number(data[2]);
    this.time = Number(data[3]);
    this.rest = Number(data[4]);
  }

  public distanceAfter(seconds: number) {
    const cycles = Math.floor(seconds / (this.time + this.rest));
    const remain = seconds - cycles * (this.time + this.rest);
    const flying = cycles * this.time + Math.min(remain, this.time);
    return flying * this.speed;
  }
}

fs.readFile(path.join(__dirname, "input-14.txt"), (err, data) => {
  if (err) throw err;
  var reindeer = new Array<Reindeer>();

  data
    .toString()
    .split("\r\n")
    .forEach((line) => {
      const match = line.match(
        /(.*) can fly (.*) km\/s for (\d*) seconds, but then must rest for (.*) seconds\./
      );
      if (match) {
        var r = new Reindeer(match);
        reindeer.push(r);
      }
    });

  console.log(
    "Part 1: " + Math.max(...reindeer.map((value) => value.distanceAfter(2503)))
  );

  var points = new Map<string, number>(reindeer.map((r) => [r.name, 0]));

  for (var i = 1; i <= 2503; ++i) {
    var positions = new Map<string, number>(
      reindeer.map((r) => [r.name, r.distanceAfter(i)])
    );
    const lead = Math.max(...positions.values());
    [...[...positions.entries()].filter((entry) => entry[1] === lead)].forEach(
      (item) => points.set(item[0], points.get(item[0])! + 1)
    );
  }

  console.log("Part 2: " + Math.max(...[...points].map((entry) => entry[1])));
});
