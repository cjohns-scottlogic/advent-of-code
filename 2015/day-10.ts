const input = "3113322113";

const look_and_say = (input: string): string =>
  (input.match(/(.)\1*/g) || [])
    .map((nums: string) => String(nums.length) + String(nums[0]))
    .reduce((a, b) => a + b);

var value = input;

for (var i = 0; i < 40; ++i) value = look_and_say(value);
const part1 = value;

for (var i = 0; i < 10; ++i) value = look_and_say(value);
const part2 = value;

console.log("Part 1:", part1.length);
console.log("Part 2:", part2.length);
