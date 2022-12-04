use std::{env, fmt, fs};

mod solutions;

pub trait Problem {
    type Output: fmt::Display;

    fn new(input: &str) -> Self;
    fn part1(&self) -> Self::Output;
    fn part2(&self) -> Self::Output;
}

fn solve<P: Problem>(input: &str) -> (P::Output, P::Output) {
    let input = fs::read_to_string(input).unwrap();
    let problem = <P>::new(&input);
    (problem.part1(), problem.part2())
}

fn main() {
    let day: u64 = env::args()
        .nth(1)
        .expect("Expected day to be provided")
        .parse()
        .expect("Expected integer");
    let solve = match day {
        1 => solve::<solutions::Day1>,
        2 => solve::<solutions::Day2>,
        3 => solve::<solutions::Day3>,
        4 => solve::<solutions::Day4>,
        _ => panic!("invalid day"),
    };
    let (part1, part2) = solve(&format!("./inputs/day{day}.txt"));
    println!("Part 1: {part1}\nPart 2: {part2}");
}
