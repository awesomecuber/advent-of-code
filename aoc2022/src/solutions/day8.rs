use std::collections::HashSet;

use crate::{
    utils::{Coord, Grid},
    Problem,
};

pub struct Day8 {
    trees: Grid<u64>,
}

enum Dir {
    Left,
    Top,
    Right,
    Bot,
}

impl Dir {
    fn get_pos(&self, pos: i64, depth: i64, size: i64) -> Coord {
        match self {
            Dir::Left => Coord(depth, pos),
            Dir::Top => Coord(pos, depth),
            Dir::Right => Coord(size - 1 - depth, pos),
            Dir::Bot => Coord(pos, size - 1 - depth),
        }
    }

    fn incr_pos(&self, curr: Coord, depth: i64, size: i64) -> Option<Coord> {
        let Coord(x, y) = curr;
        assert!(x < size);
        assert!(y < size);
        match self {
            Dir::Left => {
                if depth > x {
                    None
                } else {
                    Some(Coord(x - depth, y))
                }
            }
            Dir::Top => {
                if depth > y {
                    None
                } else {
                    Some(Coord(x, y - depth))
                }
            }
            Dir::Right => {
                if x >= size - depth {
                    None
                } else {
                    Some(Coord(x + depth, y))
                }
            }
            Dir::Bot => {
                if y >= size - depth {
                    None
                } else {
                    Some(Coord(x, y + depth))
                }
            }
        }
    }
}

impl Problem for Day8 {
    type Output1 = u64;
    type Output2 = u64;

    fn new(input: &str) -> Self {
        let trees = input
            .lines()
            .map(|l| l.chars().map(|c| c.to_digit(10).unwrap() as u64).collect())
            .collect();
        Day8 {
            trees: Grid { grid: trees },
        }
    }

    fn part1(&self) -> Self::Output1 {
        let mut can_see: HashSet<Coord> = HashSet::new();
        let size = self.trees.width(); // width == height

        for dir in [Dir::Left, Dir::Top, Dir::Right, Dir::Bot] {
            for pos in 0..size {
                let cur_pos = dir.get_pos(pos as i64, 0, size as i64);
                let cur = self.trees.coord_get(cur_pos);
                can_see.insert(cur_pos);
                let mut highest = cur;
                for depth in 1..size {
                    let cur_pos = dir.get_pos(pos as i64, depth as i64, size as i64);
                    let cur = self.trees.coord_get(cur_pos);
                    if cur > highest {
                        can_see.insert(cur_pos);
                        highest = cur;
                    }
                }
            }
        }

        can_see.len() as u64
    }

    fn part2(&self) -> Self::Output2 {
        let mut best_total = 0;
        let size = self.trees.width(); // width == height

        for x in 1..(size - 1) {
            for y in 1..(size - 1) {
                let mut total = 1;
                let curr = Coord(x as i64, y as i64);
                let start_height = self.trees.coord_get(curr);
                for dir in [Dir::Left, Dir::Top, Dir::Right, Dir::Bot] {
                    let mut dir_score = 0;
                    for depth in 1.. {
                        let spot = match dir.incr_pos(curr, depth, size as i64) {
                            Some(spot) => spot,
                            None => break,
                        };
                        dir_score += 1;
                        let other_height = self.trees.coord_get(spot);
                        if other_height >= start_height {
                            break;
                        }
                    }
                    total *= dir_score;
                }
                best_total = best_total.max(total)
            }
        }
        best_total
    }
}

#[test]
fn example() {
    let problem = Day8::new(
        "30373
25512
65332
33549
35390",
    );
    assert_eq!(21, problem.part1());
    assert_eq!(8, problem.part2());
}
