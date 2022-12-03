use crate::Problem;

pub struct Day1 {
    elves: Vec<Vec<u64>>,
}

impl Problem for Day1 {
    type Output = u64;

    fn new(input: &str) -> Self {
        let elves = input
            .split("\n\n")
            .map(|elf| elf.lines().map(|x| x.parse().unwrap()).collect())
            .collect();
        Day1 { elves }
    }

    fn part1(&self) -> Self::Output {
        self.elves.iter().map(|elf| elf.iter().sum()).max().unwrap()
    }

    fn part2(&self) -> Self::Output {
        let mut elve_calories = self
            .elves
            .iter()
            .map(|elf| elf.iter().sum())
            .collect::<Vec<u64>>();
        elve_calories.sort_unstable();
        elve_calories.into_iter().rev().take(3).sum()
    }
}
