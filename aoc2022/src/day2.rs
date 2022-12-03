use parse_display::FromStr;

use crate::Problem;

pub struct Day2 {
    strategies: Vec<Strategy>,
}

#[derive(Clone, Copy, FromStr)]
enum Left {
    #[display("A")]
    Rock,
    #[display("B")]
    Paper,
    #[display("C")]
    Scissors,
}

#[derive(Clone, Copy, FromStr)]
enum Right {
    X,
    Y,
    Z,
}

#[derive(FromStr)]
#[display("{left} {right}")]
pub struct Strategy {
    left: Left,
    right: Right,
}

impl Problem for Day2 {
    type Output = u64;

    fn new(input: &str) -> Self {
        Day2 {
            strategies: input.lines().map(|l| l.parse().unwrap()).collect(),
        }
    }

    fn part1(&self) -> Self::Output {
        self.strategies
            .iter()
            .map(|strategy| {
                let left = strategy.left;
                let right = strategy.right;
                let outcome_score = match (left, right) {
                    (Left::Rock, Right::X) => 3,
                    (Left::Rock, Right::Y) => 6,
                    (Left::Rock, Right::Z) => 0,
                    (Left::Paper, Right::X) => 0,
                    (Left::Paper, Right::Y) => 3,
                    (Left::Paper, Right::Z) => 6,
                    (Left::Scissors, Right::X) => 6,
                    (Left::Scissors, Right::Y) => 0,
                    (Left::Scissors, Right::Z) => 3,
                };
                let shape_score = match right {
                    Right::X => 1,
                    Right::Y => 2,
                    Right::Z => 3,
                };
                outcome_score + shape_score
            })
            .sum()
    }

    fn part2(&self) -> Self::Output {
        self.strategies
            .iter()
            .map(|strategy| {
                let left = strategy.left;
                let right = strategy.right;
                let outcome_score = match right {
                    Right::X => 0,
                    Right::Y => 3,
                    Right::Z => 6,
                };
                let shape_score = match (left, right) {
                    (Left::Rock, Right::X) => 3,
                    (Left::Rock, Right::Y) => 1,
                    (Left::Rock, Right::Z) => 2,
                    (Left::Paper, Right::X) => 1,
                    (Left::Paper, Right::Y) => 2,
                    (Left::Paper, Right::Z) => 3,
                    (Left::Scissors, Right::X) => 2,
                    (Left::Scissors, Right::Y) => 3,
                    (Left::Scissors, Right::Z) => 1,
                };
                outcome_score + shape_score
            })
            .sum()
    }
}
