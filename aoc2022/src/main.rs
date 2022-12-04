use std::fmt;

mod day1;
mod day2;
mod day3;
mod day4;

pub trait Problem {
    type Output: fmt::Display;

    fn new(input: &str) -> Self;
    fn part1(&self) -> Self::Output;
    fn part2(&self) -> Self::Output;
}

fn solve<P: Problem>(input: &str) {
    let input = std::fs::read_to_string(input).unwrap();
    let problem = <P>::new(&input);
    println!("Part 1: {}\nPart 2: {}", problem.part1(), problem.part2());
}

fn main() {
    // solve::<day1::Day1>("./inputs/day1.txt");
    // solve::<day2::Day2>("./inputs/day2.txt");
    // solve::<day3::Day3>("./inputs/day3.txt");
    solve::<day4::Day4>("./inputs/day4.txt");
}
