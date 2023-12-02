use crate::Problem;

pub struct Day1 {
    lines: Vec<String>,
}

impl Problem for Day1 {
    type Output1 = u64;
    type Output2 = u64;

    fn new(input: &str) -> Self {
        let lines = input.lines().map(|s| s.to_owned()).collect::<Vec<_>>();
        Day1 { lines }
    }

    fn part1(&self) -> Self::Output1 {
        self.lines
            .iter()
            .map(|line| {
                let leftmost = line.chars().find_map(|c| c.to_digit(10)).unwrap();
                let rightmost = line.chars().rev().find_map(|c| c.to_digit(10)).unwrap();
                (leftmost * 10 + rightmost) as u64
            })
            .sum()
    }

    fn part2(&self) -> Self::Output2 {
        self.lines
            .iter()
            .map(|line| {
                let to_digit = |(i, char): (usize, char)| {
                    char.to_digit(10).or_else(|| {
                        [
                            ("one", 1),
                            ("two", 2),
                            ("three", 3),
                            ("four", 4),
                            ("five", 5),
                            ("six", 6),
                            ("seven", 7),
                            ("eight", 8),
                            ("nine", 9),
                        ]
                        .into_iter()
                        .find_map(|(num_str, num)| {
                            if line[i..].starts_with(num_str) {
                                Some(num)
                            } else {
                                None
                            }
                        })
                    })
                };
                let a = line.chars().enumerate().find_map(to_digit).unwrap();
                let b = line
                    .chars()
                    .rev()
                    .enumerate()
                    .map(|(i, char)| (line.len() - i - 1, char)) // change the index so that it counts backwards, since to_digit wants the index to the start of the substring
                    .find_map(to_digit)
                    .unwrap();
                (a * 10 + b) as u64
            })
            .sum()
    }
}

#[test]
fn example() {
    let problem = Day1::new(
        "1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet",
    );
    assert_eq!(142, problem.part1());

    let problem = Day1::new(
        "two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen",
    );
    assert_eq!(281, problem.part2());
}
