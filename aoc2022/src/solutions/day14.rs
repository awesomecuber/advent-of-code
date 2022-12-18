use std::collections::HashSet;

use itertools::Itertools;

use crate::{utils::Coord, Problem};

pub struct Day14 {
    walls: HashSet<Coord>,
}

impl Day14 {
    fn move_sand(&self, sand: Coord, resting_sand: &HashSet<Coord>) -> Option<Coord> {
        let down = Coord(0, 1);
        let downleft = Coord(-1, 1);
        let downright = Coord(1, 1);

        if self.can_move_to(sand + down, resting_sand) {
            Some(sand + down)
        } else if self.can_move_to(sand + downleft, resting_sand) {
            Some(sand + downleft)
        } else if self.can_move_to(sand + downright, resting_sand) {
            Some(sand + downright)
        } else {
            None
        }
    }

    fn can_move_to(&self, coord: Coord, sand: &HashSet<Coord>) -> bool {
        !self.walls.contains(&coord) && !sand.contains(&coord)
    }
}

impl Problem for Day14 {
    type Output1 = u64;
    type Output2 = u64;

    fn new(input: &str) -> Self {
        let mut walls = HashSet::new();
        for line in input.lines() {
            line.split(" -> ")
                .map(|n| n.parse::<Coord>().unwrap())
                .tuple_windows()
                .for_each(|(start, end)| {
                    assert!(start.0 == end.0 || start.1 == end.1);
                    let diff = end - start;
                    let incr = Coord(diff.0.signum(), diff.1.signum());
                    let mut curr = start;
                    while curr != end {
                        walls.insert(curr);
                        curr += incr;
                    }
                    walls.insert(curr); // to get the end
                });
        }
        Day14 { walls }
    }

    fn part1(&self) -> Self::Output1 {
        let mut resting_sand = HashSet::new();

        let lowest_wall = self.walls.iter().map(|c| c.1).max().unwrap();

        loop {
            let mut sand = Coord(500, 0);
            loop {
                let Some(new_spot) = self.move_sand(sand, &resting_sand) else {
                    resting_sand.insert(sand);
                    break;
                };
                sand = new_spot;
                if sand.1 > lowest_wall {
                    return resting_sand.len() as u64;
                }
            }
        }
    }

    fn part2(&self) -> Self::Output2 {
        let mut resting_sand = HashSet::new();

        let lowest_wall = self.walls.iter().map(|c| c.1).max().unwrap();

        loop {
            let mut sand = Coord(500, 0);
            loop {
                let Some(new_spot) = self.move_sand(sand, &resting_sand) else {
                    resting_sand.insert(sand);
                    break;
                };
                sand = new_spot;
                if sand.1 > lowest_wall {
                    resting_sand.insert(sand);
                    break;
                }
            }
            if sand == Coord(500, 0) {
                return resting_sand.len() as u64;
            }
        }
    }
}

#[test]
fn example() {
    let problem = Day14::new(
        "498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9",
    );
    assert_eq!(24, problem.part1());
    assert_eq!(93, problem.part2());
}
