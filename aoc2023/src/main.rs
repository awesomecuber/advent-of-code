use std::{env, fmt, fs};

mod solutions;
mod utils;

pub trait Problem {
    type Output1: fmt::Display + 'static;
    type Output2: fmt::Display + 'static;

    fn new(input: &str) -> Self;
    fn part1(&self) -> Self::Output1;
    fn part2(&self) -> Self::Output2;
}

fn solve<P: Problem>(input: &str) -> (Box<dyn fmt::Display>, Box<dyn fmt::Display>) {
    let input = fs::read_to_string(input).unwrap();
    let problem = <P>::new(&input);
    (Box::new(problem.part1()), Box::new(problem.part2()))
}

fn main() {
    match env::args().nth(1) {
        Some(day) => solve_day(day.parse().expect("Expected integer")),
        None => {
            for day in 1..=2 {
                println!("\nDAY {day}");
                solve_day(day);
            }
        }
    }
}

fn solve_day(day: u64) {
    let solve = match day {
        1 => solve::<solutions::Day1>,
        2 => solve::<solutions::Day2>,
        _ => panic!("Invalid day"),
    };
    let (part1, part2) = solve(&format!("./inputs/day{day}.txt"));
    println!("Part 1: {part1}\nPart 2: {part2}");
}
