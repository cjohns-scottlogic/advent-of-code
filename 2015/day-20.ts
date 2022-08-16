const presents1 = (house: number) => {
  var count = 0;
  for (var elf = house; elf > 0; elf -= 1) {
    count += house % elf === 0 ? elf * 10 : 0;
  }
  return count;
};

const presents2 = (house: number) => {
  var count = 0;
  for (var elf = house; elf > 0; elf -= 1) {
    if (house <= elf * 50) count += house % elf === 0 ? elf * 11 : 0;
  }
  return count;
};

const target = 33100000;

var house1 = 750000;
while (presents1(house1) < target) house1 += 1;
console.log("Part 1:", house1);

var house2 = 750000;
while (presents2(house2) < target) house2 += 1;
console.log("Part 2:", house2);
