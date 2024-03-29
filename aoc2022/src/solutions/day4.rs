use std::ops::RangeInclusive;

use parse_display::FromStr;

use crate::Problem;

pub struct Day4 {
    assignment_pairs: Vec<AssignmentPair>,
}

struct AssignmentPair {
    smaller: RangeInclusive<u64>,
    larger: RangeInclusive<u64>,
}

#[derive(FromStr)]
#[display("{a}-{b},{c}-{d}")]
struct Line {
    a: u64,
    b: u64,
    c: u64,
    d: u64,
}

impl Problem for Day4 {
    type Output1 = u64;
    type Output2 = u64;

    fn new(input: &str) -> Self {
        let assignment_pairs = input
            .lines()
            .map(|l| {
                let Line { a, b, c, d } = l.parse::<Line>().unwrap();
                if b - a < d - c {
                    AssignmentPair {
                        smaller: a..=b,
                        larger: c..=d,
                    }
                } else {
                    AssignmentPair {
                        smaller: c..=d,
                        larger: a..=b,
                    }
                }
            })
            .collect();
        Day4 { assignment_pairs }
    }

    fn part1(&self) -> Self::Output1 {
        self.assignment_pairs
            .iter()
            .filter(|AssignmentPair { smaller, larger }| {
                smaller.start() >= larger.start() && smaller.end() <= larger.end()
            })
            .count() as u64
    }

    fn part2(&self) -> Self::Output2 {
        self.assignment_pairs
            .iter()
            .filter(|AssignmentPair { smaller, larger }| {
                smaller.start() <= larger.end() && larger.start() <= smaller.end()
            })
            .count() as u64
    }
}

#[test]
fn example() {
    let problem = Day4::new(
        "2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8",
    );
    assert_eq!(2, problem.part1());
    assert_eq!(4, problem.part2());
}
