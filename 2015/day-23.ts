import * as fs from "fs";
import * as path from "path";

const run = (program: string[], a: number, b: number) => {
  var regs = new Map<string, number>([
    ["a", a],
    ["b", b],
  ]);
  var pc = 0;

  while (pc < program.length) {
    var [op, r, arg] = program[pc++].split(" ");
    if (r.endsWith(",")) r = r.substring(0, r.length - 1);

    switch (op) {
      case "hlf":
        regs.set(r, regs.get(r)! / 2);
        break;
      case "tpl":
        regs.set(r, regs.get(r)! * 3);
        break;
      case "inc":
        regs.set(r, regs.get(r)! + 1);
        break;
      case "jmp":
        pc += Number(r) - 1;
        break;
      case "jie":
        if (regs.get(r)! % 2 == 0) pc += Number(arg) - 1;
        break;
      case "jio":
        if (regs.get(r)! == 1) pc += Number(arg) - 1;
        break;
    }
  }
  return { a: regs.get("a"), b: regs.get("b") };
};

fs.readFile(path.join(__dirname, "input-23.txt"), (err, data) => {
  if (err) throw err;

  const program = data.toString().split("\r\n");

  console.log("Part 1: " + run(program, 0, 0).b);
  console.log("Part 2: " + run(program, 1, 0).b);
});
