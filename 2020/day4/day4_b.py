import os
import re
import sys

with open(os.path.join(sys.path[0], "day4.txt")) as f:
    puzzle_input = f.read().splitlines()

current_passport = []
valid_count = 0
for line in puzzle_input + [""]:
    if line != "":
        current_passport += [term.split(":") for term in line.split()]
    else:
        passport = dict(current_passport)
        if "cid" in passport:
            passport.pop("cid")
        if len(passport) == 7:
            invalid = False
            if not 1920 <= int(passport["byr"]) <= 2002:
                invalid = True
            if not 2010 <= int(passport["iyr"]) <= 2020:
                invalid = True
            if not 2020 <= int(passport["eyr"]) <= 2030:
                invalid = True

            if passport["hgt"].find("cm") != -1:
                if not 150 <= int(passport["hgt"][:-2]) <= 193:
                    invalid = True
            elif passport["hgt"].find("in") != -1:
                if not 59 <= int(passport["hgt"][:-2]) <= 76:
                    invalid = True
            else:
                invalid = True

            if not re.match("#([0-9]|[a-f]){6}", passport["hcl"]):
                invalid = True

            if not passport["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
                invalid = True

            if not len(passport["pid"]) == 9:
                invalid = True

            if not invalid:
                valid_count += 1
        current_passport = []
print(valid_count)