class Player {
  hp: number = 50;
  mana: number = 500;
  shield: number = 0;
  poison: number = 0;
  recharge: number = 0;
}

class Boss {
  hp: number = 51;
  damage: number = 9;
}

class State {
  cost: number = 0;
  move: "player" | "boss" | "win" | "lose" = "player";
  player: Player = new Player();
  boss: Boss = new Boss();

  clone(): State {
    var that = new State();
    that.cost = this.cost;
    that.move = this.move;
    that.player = { ...this.player };
    that.boss = { ...this.boss };
    return that;
  }

  spend(amount: number): State | null {
    var s = this.clone();
    s.player.mana -= amount;
    s.cost += amount;
    return s.player.mana >= 0 ? s : null;
  }

  // Returns the next states from here, if any.
  next(hard: boolean) {
    if (this.move === "lose" || this.move === "win") return [];
  }
}

const next = (from: State, hard: boolean) => {
  // No next move from here.
  if (from.move === "lose" || from.move === "win") return [];

  var s = from.clone();

  if (hard && s.move === "player") {
    s.player.hp -= 1;
    if (s.player.hp <= 0) {
      s.move = "lose";
      return [s];
    }
  }

  if (s.player.poison > 0) {
    s.boss.hp -= 3;
    s.player.poison--;
  }
  if (s.player.recharge > 0) {
    s.player.mana += 101;
    s.player.recharge--;
  }
  if (s.player.shield > 0) {
    s.player.shield--;
  }

  if (s.boss.hp <= 0) {
    s.move = "win";
    return [s];
  }

  if (s.move === "player") {
    var n: Array<State> = [];
    s.move = "boss";

    // Magic Missle
    var mm = s.spend(53);
    if (mm) {
      mm.boss.hp -= 4;
      mm.move = mm.boss.hp > 0 ? "boss" : "win";
      n.push(mm);
    }

    // Drain
    var d = s.spend(73);
    if (d) {
      d.boss.hp -= 2;
      d.player.hp += 2;
      d.move = d.boss.hp > 0 ? "boss" : "win";
      n.push(d);
    }

    // Shield
    var h = s.player.shield === 0 ? s.spend(113) : null;
    if (h) {
      h.player.shield = 6;
      n.push(h);
    }

    var p = s.player.poison === 0 ? s.spend(173) : null;
    if (p) {
      p.player.poison = 6;
      n.push(p);
    }

    var r = s.player.recharge === 0 ? s.spend(229) : null;
    if (r) {
      r.player.recharge = 5;
      n.push(r);
    }

    return n;
  }

  if (s.move === "boss") {
    const armor = s.player.shield ? 7 : 0;
    s.player.hp -= Math.max(1, s.boss.damage - armor);
    s.move = s.player.hp > 0 ? "player" : "lose";
    return [s];
  }

  return [];
};

var part1 = 9999;
var states = [new State()];

for (var i = 0; i < states.length; ++i) {
  if (states[i].move === "win" && states[i].cost < part1)
    part1 = states[i].cost;
  if (states[i].cost < part1) states.push(...next(states[i], false));
}

console.log("Part 1: " + part1);

var part2 = 9999;
var states = [new State()];

for (var i = 0; i < states.length; ++i) {
  if (states[i].move === "win" && states[i].cost < part2)
    part2 = states[i].cost;

  if (states[i].cost < part2) states.push(...next(states[i], true));
}

console.log("Part 2: " + part2);
