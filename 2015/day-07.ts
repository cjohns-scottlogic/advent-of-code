import * as fs from "fs";
import * as path from "path";

class Gate {
  constructor(spec: string) {
    const parts = spec.split(" ");
    switch (parts.length) {
      case 1:
        [this.a] = parts;
        break;
      case 2:
        [this.op, this.a] = parts;
        break;
      case 3:
        [this.a, this.op, this.b] = parts;
        break;
    }

    if (typeof this.a === "string") {
      var na = Number(this.a);
      if (!Number.isNaN(na)) this.a = na;
    }
    if (typeof this.b === "string") {
      var nb = Number(this.b);
      if (!Number.isNaN(nb)) this.b = nb;
    }
  }

  update(gates: Map<string, Gate>) {
    var a = this.a;
    var b = this.b;
    if (typeof this.a === "string") a = gates.get(this.a)!.value;
    if (typeof this.b === "string") b = gates.get(this.b)!.value;

    switch (this.op) {
      case undefined:
        if (typeof a === "number") {
          this.value = a & 0xffff;
        }
        break;
      case "NOT": {
        if (typeof a === "number") {
          this.value = ~a & 0xffff;
        }
        break;
      }
      case "AND": {
        if (typeof a === "number" && typeof b === "number") {
          this.value = a & b & 0xffff;
        }
        break;
      }
      case "OR": {
        if (typeof a === "number" && typeof b === "number") {
          this.value = (a | b) & 0xffff;
        }
        break;
      }
      case "RSHIFT": {
        if (typeof a === "number" && typeof b === "number") {
          this.value = (a >> b) & 0xffff;
        }
        break;
      }
      case "LSHIFT": {
        if (typeof a === "number" && typeof b === "number") {
          this.value = (a << b) & 0xffff;
        }
        break;
      }
    }
  }

  public value: number | undefined;
  private a: string | number | undefined;
  private b: string | number | undefined;
  private op: string | undefined;
}

const resolve = (wires: Map<string, Gate>) => {
  for (;;) {
    var unresolved = Array.from(wires.entries()).filter(
      (wire) => wire[1].value === undefined
    );

    if (unresolved.length === 0) break;

    unresolved.forEach((wire) => {
      wire[1].update(wires);
    });
  }
};

fs.readFile(path.join(__dirname, "input-07.txt"), (err, data) => {
  if (err) throw err;
  var wires = new Map<string, Gate>();
  data
    .toString()
    .split("\r\n")
    .forEach((line) => {
      var [gate, wire] = line.split(" -> ");
      wires.set(wire, new Gate(gate));
    });

  resolve(wires);

  var a_value = wires.get("a")!.value;
  console.log("Part 1: " + a_value);

  wires.forEach((wire) => (wire.value = undefined));
  wires.get("b")!.value = a_value;
  resolve(wires);

  var a_value = wires.get("a")!.value;
  console.log("Part 2: " + a_value);
});
