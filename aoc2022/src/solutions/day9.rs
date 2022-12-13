use std::collections::HashSet;

use parse_display::FromStr;

use crate::{utils::Coord, Problem};

pub struct Day9 {
    instructions: Vec<Instruction>,
}

#[derive(FromStr)]
#[display("{direction} {count}")]
pub struct Instruction {
    direction: Direction,
    count: u64,
}

#[derive(FromStr)]
pub enum Direction {
    #[display("U")]
    Up,
    #[display("L")]
    Left,
    #[display("D")]
    Down,
    #[display("R")]
    Right,
}

impl Direction {
    fn get_incr(&self) -> Coord {
        match self {
            Direction::Up => Coord(0, 1),
            Direction::Left => Coord(-1, 0),
            Direction::Down => Coord(0, -1),
            Direction::Right => Coord(1, 0),
        }
    }
}

fn diff(head: Coord, tail: Coord) -> Coord {
    let diff = head - tail;
    if diff.0.abs() <= 1 && diff.1.abs() <= 1 {
        return Coord(0, 0);
    }
    Coord(diff.0.signum(), diff.1.signum())
}

impl Day9 {
    fn solve(&self, string_size: usize) -> u64 {
        let mut string = vec![Coord(0, 0); string_size];
        let mut positions_seen = HashSet::new();
        positions_seen.insert(*string.last().unwrap());
        for instruction in &self.instructions {
            let incr = instruction.direction.get_incr();
            for _ in 0..instruction.count {
                string[0] += incr;
                for i in 0..(string.len() - 1) {
                    let diff = diff(string[i], string[i + 1]);
                    if diff == Coord(0, 0) {
                        break;
                    }
                    string[i + 1] += diff;
                }
                positions_seen.insert(*string.last().unwrap());
            }
        }
        positions_seen.len() as u64
    }
}

impl Problem for Day9 {
    type Output1 = u64;
    type Output2 = u64;

    fn new(input: &str) -> Self {
        Day9 {
            instructions: input.lines().map(|l| l.parse().unwrap()).collect(),
        }
    }

    fn part1(&self) -> Self::Output1 {
        self.solve(2)
    }

    fn part2(&self) -> Self::Output2 {
        self.solve(10)
    }
}

#[test]
fn example() {
    let problem = Day9::new(
        "R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2",
    );
    assert_eq!(13, problem.part1());
    assert_eq!(1, problem.part2());
}

#[test]
fn example2() {
    let problem = Day9::new(
        "R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20",
    );
    assert_eq!(36, problem.part2());
}
