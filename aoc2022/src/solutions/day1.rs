use crate::Problem;

pub struct Day1 {
    elves: Vec<Vec<u64>>,
}

impl Problem for Day1 {
    type Output1 = u64;
    type Output2 = u64;

    fn new(input: &str) -> Self {
        let elves = input
            .split("\n\n")
            .map(|elf| elf.lines().map(|x| x.parse().unwrap()).collect())
            .collect();
        Day1 { elves }
    }

    fn part1(&self) -> Self::Output1 {
        self.elves.iter().map(|elf| elf.iter().sum()).max().unwrap()
    }

    fn part2(&self) -> Self::Output2 {
        let mut elve_calories = self
            .elves
            .iter()
            .map(|elf| elf.iter().sum())
            .collect::<Vec<u64>>();
        elve_calories.sort_unstable();
        elve_calories.into_iter().rev().take(3).sum()
    }
}

#[test]
fn example() {
    let problem = Day1::new(
        "1000
2000
3000

4000

5000
6000

7000
8000
9000

10000",
    );
    assert_eq!(24000, problem.part1());
    assert_eq!(45000, problem.part2());
}
