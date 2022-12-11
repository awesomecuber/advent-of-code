use std::{env, fmt, fs};

mod solutions;

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
            for day in 1..=11 {
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
        3 => solve::<solutions::Day3>,
        4 => solve::<solutions::Day4>,
        5 => solve::<solutions::Day5>,
        6 => solve::<solutions::Day6>,
        7 => solve::<solutions::Day7>,
        8 => solve::<solutions::Day8>,
        9 => solve::<solutions::Day9>,
        10 => solve::<solutions::Day10>,
        11 => solve::<solutions::Day11>,
        _ => panic!("Invalid day"),
    };
    let (part1, part2) = solve(&format!("./inputs/day{day}.txt"));
    println!("Part 1: {part1}\nPart 2: {part2}");
}
