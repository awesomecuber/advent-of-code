use std::collections::HashSet;

use crate::Problem;

pub struct Day8 {
    trees: Vec<Vec<u64>>,
}

enum Dir {
    Left,
    Top,
    Right,
    Bot,
}

impl Dir {
    fn get_pos(&self, pos: usize, depth: usize, size: usize) -> (usize, usize) {
        match self {
            Dir::Left => (depth, pos),
            Dir::Top => (pos, depth),
            Dir::Right => (size - 1 - depth, pos),
            Dir::Bot => (pos, size - 1 - depth),
        }
    }

    fn incr_pos(&self, x: usize, y: usize, depth: usize, size: usize) -> Option<(usize, usize)> {
        assert!(x < size);
        assert!(y < size);
        match self {
            Dir::Left => {
                if depth > x {
                    None
                } else {
                    Some((x - depth, y))
                }
            }
            Dir::Top => {
                if depth > y {
                    None
                } else {
                    Some((x, y - depth))
                }
            }
            Dir::Right => {
                if x + depth >= size {
                    None
                } else {
                    Some((x + depth, y))
                }
            }
            Dir::Bot => {
                if y + depth >= size {
                    None
                } else {
                    Some((x, y + depth))
                }
            }
        }
    }
}

impl Problem for Day8 {
    type Output = u64;

    fn new(input: &str) -> Self {
        let trees = input
            .lines()
            .map(|l| l.chars().map(|c| c.to_digit(10).unwrap() as u64).collect())
            .collect();
        Day8 { trees }
    }

    fn part1(&self) -> Self::Output {
        let mut can_see: HashSet<(usize, usize)> = HashSet::new();
        let size = self.trees[0].len();

        for dir in [Dir::Left, Dir::Top, Dir::Right, Dir::Bot] {
            for pos in 0..size {
                let cur_pos = dir.get_pos(pos, 0, size);
                let cur = self.trees[cur_pos.1][cur_pos.0];
                can_see.insert(cur_pos);
                let mut highest = cur;
                for depth in 1..size {
                    let cur_pos = dir.get_pos(pos, depth, size);
                    let cur = self.trees[cur_pos.1][cur_pos.0];
                    if cur > highest {
                        can_see.insert(cur_pos);
                        highest = cur;
                    }
                }
            }
        }

        can_see.len() as u64
    }

    fn part2(&self) -> Self::Output {
        let mut best_total = 0;

        let size = self.trees[0].len();
        for x in 1..(size - 1) {
            for y in 1..(size - 1) {
                let mut total = 1;
                let start_height = self.trees[y][x];
                for dir in [Dir::Left, Dir::Top, Dir::Right, Dir::Bot] {
                    let mut dir_score = 0;
                    for depth in 1.. {
                        let spot = match dir.incr_pos(x, y, depth, size) {
                            Some(spot) => spot,
                            None => break,
                        };
                        dir_score += 1;
                        let other_height = self.trees[spot.1][spot.0];
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
