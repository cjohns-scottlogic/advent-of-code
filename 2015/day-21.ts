type Item = [name: string, cost: number, damage: number, armor: number];

const Weapons: Item[] = [
  ["Dagger", 8, 4, 0],
  ["Shortsword", 10, 5, 0],
  ["Warhammer", 25, 6, 0],
  ["Longsword", 40, 7, 0],
  ["Greataxe", 74, 8, 0],
];

const Armors: Item[] = [
  ["None", 0, 0, 0],
  ["Leather", 13, 0, 1],
  ["Chainmail", 31, 0, 2],
  ["Splintmail", 53, 0, 3],
  ["Bandedmail", 75, 0, 4],
  ["Platemail", 102, 0, 5],
];

const Rings: Item[] = [
  ["None", 0, 0, 0],
  ["None", 0, 0, 0],
  ["Damage +1", 25, 1, 0],
  ["Damage +2", 50, 2, 0],
  ["Damage +3", 100, 3, 0],
  ["Defense +1", 20, 0, 1],
  ["Defense +2", 40, 0, 2],
  ["Defense +3", 80, 0, 3],
];

type Player = [hp: number, damage: number, armor: number];

const battle = (player: Player, boss: Player) => {
  while (true) {
    boss[0] -= Math.max(1, player[1] - boss[2]);
    if (boss[0] < 1) return true;
    player[0] -= Math.max(1, boss[1] - player[2]);
    if (player[0] < 1) return false;
  }
};

var part1 = 9999;
var part2 = 0;

Weapons.forEach((weapon) =>
  Armors.forEach((armor) => {
    for (var r1 = 0; r1 < Rings.length; r1++) {
      for (var r2 = r1 + 1; r2 < Rings.length; r2++) {
        const ring1 = Rings[r1];
        const ring2 = Rings[r2];

        const cost = weapon[1] + armor[1] + ring1[1] + ring2[1];
        const boss: Player = [100, 8, 2];
        const player: Player = [
          100,
          weapon[2] + armor[2] + ring1[2] + ring2[2],
          weapon[3] + armor[3] + ring1[3] + ring2[3],
        ];

        if (battle(player, boss)) part1 = Math.min(part1, cost);
        else part2 = Math.max(part2, cost);
      }
    }
  })
);

console.log("Part 1:", part1);
console.log("Part 2:", part2);
