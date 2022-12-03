use crate::Problem;

pub struct Day1;

impl Problem for Day1 {
    type Data = Vec<Vec<u64>>;
    type Output = u64;

    fn to_data(input: &str) -> Self::Data {
        input
            .split("\n\n")
            .map(|elf| elf.lines().map(|x| x.parse().unwrap()).collect())
            .collect()
    }

    fn part1(data: &Self::Data) -> Self::Output {
        data.iter()
            .map(|elf| elf.iter().sum())
            .max()
            .unwrap()
    }

    fn part2(data: &Self::Data) -> Self::Output {
        let mut elves = data
            .iter()
            .map(|elf| elf.iter().sum())
            .collect::<Vec<u64>>();
        elves.sort_unstable();
        elves.into_iter().rev().take(3).sum()
    }
}
