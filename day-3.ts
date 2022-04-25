import * as fs from "fs";
import * as path from "path";

class Santa {
  private xpos: number = 0;
  private ypos: number = 0;

  constructor(private houses: Map<string, number>) {}

  where() {
    return { x: this.xpos, y: this.ypos };
  }

  move(move: string) {
    switch (move) {
      case "<":
        this.xpos -= 1;
        break;
      case ">":
        this.xpos += 1;
        break;
      case "^":
        this.ypos -= 1;
        break;
      case "v":
        this.ypos += 1;
        break;
    }
    return this;
  }

  deliver() {
    let addr = JSON.stringify(this.where());
    this.houses.set(addr, (this.houses.get(addr) || 0) + 1);
  }
}

const part1 = (data: string) => {
  let houses = new Map<string, number>();
  let santa = new Santa(houses);
  santa.deliver();

  [...data].forEach((move) => {
    santa.move(move).deliver();
  });

  return houses.size;
};

const part2 = (data: string) => {
  let houses = new Map<string, number>();
  let santas = [new Santa(houses), new Santa(houses)];
  santas.forEach((santa) => santa.deliver());

  [...data].forEach((move, index) => {
    santas[index % 2].move(move).deliver();
  });

  return houses.size;
};

fs.readFile(path.join(__dirname, "input-3.txt"), (err, data) => {
  if (err) throw err;

  console.log("Part 1: " + part1(data.toString()));
  console.log("Part 2: " + part2(data.toString()));
});
