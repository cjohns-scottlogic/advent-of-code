const input = "hxbxwxba";

const validate = (password: string): boolean => {
  var foundStr = false;
  var doubles = [];
  var lastDouble = -3;
  var foundInval = false;

  if (password.length !== 8) return false;

  for (var pos = 0; pos < password.length; pos += 1) {
    if ("iol".search(password.charAt(pos)) !== -1) foundInval = true;

    if (pos > 2 && !foundStr) {
      if (
        password.charCodeAt(pos) === password.charCodeAt(pos - 1) + 1 &&
        password.charCodeAt(pos) === password.charCodeAt(pos - 2) + 2
      )
        foundStr = true;
    }

    if (pos > 1 && pos > lastDouble + 2) {
      if (password.charAt(pos) === password.charAt(pos - 1)) {
        doubles.push(password.charAt(pos));
        lastDouble = pos;
      }
    }
  }

  return !foundInval && foundStr && doubles.length >= 2;
};

const increment = (password: string): string => {
  var carry = true;
  var pos = password.length - 1;
  var newpass = "";

  while (carry && pos >= 0) {
    if (password.charAt(pos) === "z") {
      newpass = "a" + newpass;
      carry = true;
    } else {
      newpass = String.fromCharCode(password.charCodeAt(pos) + 1) + newpass;
      carry = false;
    }
    pos -= 1;
  }

  return password.substring(0, pos + 1) + newpass;
};

const next_pass = (old_pass: string): string => {
  var password = old_pass;
  do {
    password = increment(password);
  } while (!validate(password));
  return password;
};

const part1 = next_pass(input);
console.log("Part 1:", part1);

const part2 = next_pass(part1);
console.log("Part 2:", part2);
