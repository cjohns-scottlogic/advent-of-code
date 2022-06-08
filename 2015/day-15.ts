import * as fs from "fs";
import * as path from "path";

class Ingredient {
  public readonly name: string;
  public readonly capacity: number;
  public readonly durability: number;
  public readonly flavor: number;
  public readonly texture: number;
  public readonly calories: number;

  public constructor(data: string[]) {
    this.name = data[1];
    [this.capacity, this.durability, this.flavor, this.texture, this.calories] =
      data.splice(2, 6).map((v) => Number(v));
  }
}

const score = (ingredients: Ingredient[], recipe: number[]): number => {
  if (ingredients.length !== recipe.length) return 0;
  var capacity = 0;
  var durability = 0;
  var flavor = 0;
  var texture = 0;
  for (var i = 0; i < recipe.length; ++i) {
    capacity += ingredients[i].capacity * recipe[i];
    durability += ingredients[i].durability * recipe[i];
    flavor += ingredients[i].flavor * recipe[i];
    texture += ingredients[i].texture * recipe[i];
  }
  return (
    Math.max(0, capacity) *
    Math.max(0, durability) *
    Math.max(0, flavor) *
    Math.max(0, texture)
  );
};

const calories = (ingredients: Ingredient[], recipe: number[]): number => {
  if (ingredients.length !== recipe.length) return 0;
  var calories = 0;
  for (var i = 0; i < recipe.length; ++i) {
    calories += ingredients[i].calories * recipe[i];
  }
  return calories;
};

const mix = (
  ingredients: Ingredient[],
  left: number,
  sofar: number[],
  cals: number | undefined
): number => {
  if (sofar.length === ingredients.length - 1) {
    const recipe = sofar.concat(left);

    if (cals === undefined || calories(ingredients, recipe) === cals)
      return score(ingredients, recipe);
    else return 0;
  }

  var best = 0;
  for (var s = 0; s <= left; ++s) {
    // add 's' spoons of index to the mix
    best = Math.max(best, mix(ingredients, left - s, sofar.concat(s), cals));
  }
  return best;
};

fs.readFile(path.join(__dirname, "input-15.txt"), (err, data) => {
  if (err) throw err;
  var ingredients = new Array<Ingredient>();

  data
    .toString()
    .split("\r\n")
    .forEach((line) => {
      const match = line.match(
        /(.*)\: capacity ([-]?\d*), durability ([-]?\d*), flavor ([-]?\d*), texture ([-]?\d*), calories (\d*)/
      );
      if (match) {
        ingredients.push(new Ingredient(match));
      }
    });

  console.log("Part 1: " + mix(ingredients, 100, [], undefined));
  console.log("Part 2: " + mix(ingredients, 100, [], 500));
});
