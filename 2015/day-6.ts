import * as fs from "fs";
import * as path from "path";

enum Request {
  TurnOff,
  TurnOn,
  Toggle,
}

class Point {
  x: number;
  y: number;

  constructor(str: string) {
    var [xs, ys] = str.split(",");
    this.x = Number(xs);
    this.y = Number(ys);
  }
}

class Command {
  constructor(command: string) {
    var parts = command.split(" ");
    switch (parts.shift()) {
      case "toggle":
        this.command = Request.Toggle;
        break;
      case "turn":
        {
          switch (parts.shift()) {
            case "on":
              this.command = Request.TurnOn;
              break;
            case "off":
              this.command = Request.TurnOff;
              break;
            default:
              throw RangeError("Unknown turn command");
          }
        }
        break;
      default:
        throw RangeError("Unknown command");
    }

    this.from = new Point(String(parts.shift()));
    parts.shift();
    this.to = new Point(String(parts.shift()));
  }
  command: Request;
  from: Point;
  to: Point;
}

const xyStr = (x: number, y: number) => x + "," + y;

const part1 = (commands: Command[]) => {
  var on = new Map<string, boolean>();
  commands.forEach((command) => {
    for (var x = command.from.x; x <= command.to.x; ++x) {
      for (var y = command.from.y; y <= command.to.y; ++y) {
        const str = xyStr(x, y);
        switch (command.command) {
          case Request.TurnOff:
            on.set(str, false);
            break;
          case Request.TurnOn:
            on.set(str, true);
            break;
          case Request.Toggle:
            on.set(str, on.get(str) !== true);
            break;
        }
      }
    }
  });
  return Array.from(on.values()).filter((value) => value === true).length;
};

const part2 = (commands: Command[]) => {
  var brightness = new Map<string, number>();
  commands.forEach((command) => {
    for (var x = command.from.x; x <= command.to.x; ++x) {
      for (var y = command.from.y; y <= command.to.y; ++y) {
        const str = xyStr(x, y);
        switch (command.command) {
          case Request.TurnOff:
            brightness.set(str, Math.max(0, (brightness.get(str) || 1) - 1));
            break;
          case Request.TurnOn:
            brightness.set(str, (brightness.get(str) || 0) + 1);
            break;
          case Request.Toggle:
            brightness.set(str, (brightness.get(str) || 0) + 2);
            break;
        }
      }
    }
  });
  return Array.from(brightness.values()).reduce((p, c) => p + c);
};

fs.readFile(path.join(__dirname, "input-6.txt"), (err, data) => {
  if (err) throw err;
  var commands = data
    .toString()
    .split("\r\n")
    .map((command) => new Command(command));

  console.log("Part 1: " + part1(commands));
  console.log("Part 2: " + part2(commands));
});
