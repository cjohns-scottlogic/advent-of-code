import { Md5 } from "ts-md5/dist/md5";

const mine = (key: string, find: string) => {
  var guess = 0;
  do {
    guess += 1;
  } while (Md5.hashStr(key + guess).startsWith(find) === false);
  return guess;
};

const key = "iwrupvqb";
console.log("Part 1: " + mine(key, "00000"));
console.log("Part 2: " + mine(key, "000000"));
