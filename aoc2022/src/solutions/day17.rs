use std::collections::HashSet;

use crate::{utils::Coord, Problem};

pub struct Day17 {
    pushes: Vec<Push>,
}

#[derive(Clone, Copy)]
pub enum Push {
    Left,
    Right,
}

fn get_shape_pieces(iter: usize) -> Vec<Coord> {
    match iter % 5 {
        0 => [Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(3, 0)].to_vec(),
        1 => [
            Coord(1, 0),
            Coord(0, 1),
            Coord(1, 1),
            Coord(2, 1),
            Coord(1, 2),
        ]
        .to_vec(),
        2 => [
            Coord(0, 0),
            Coord(1, 0),
            Coord(2, 0),
            Coord(2, 1),
            Coord(2, 2),
        ]
        .to_vec(),
        3 => [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(0, 3)].to_vec(),
        4 => [Coord(0, 0), Coord(1, 0), Coord(0, 1), Coord(1, 1)].to_vec(),
        _ => unreachable!(),
    }
}

fn collides(anchor: Coord, pieces: &[Coord], at_rest: &HashSet<Coord>) -> bool {
    pieces.iter().any(|&piece| {
        let abs_piece = anchor + piece;
        if abs_piece.0 < 0 || abs_piece.0 >= 7 {
            return true;
        }
        if abs_piece.1 < 0 {
            return true;
        }
        at_rest.contains(&abs_piece)
    })
}

impl Problem for Day17 {
    type Output1 = u64;
    type Output2 = u64;

    fn new(input: &str) -> Self {
        let pushes = input
            .chars()
            .map(|c| match c {
                '<' => Push::Left,
                '>' => Push::Right,
                _ => unreachable!(),
            })
            .collect();
        Day17 { pushes }
    }

    fn part1(&self) -> Self::Output1 {
        let mut highest_point = 0;
        let mut at_rest: HashSet<Coord> = HashSet::new();
        let mut pushes = self.pushes.iter().cycle();
        for i in 0..2022 {
            let mut anchor = Coord(2, highest_point + 3);
            let shape_pieces = get_shape_pieces(i);
            loop {
                // move sideways
                let next_anchor = match pushes.next().unwrap() {
                    Push::Left => anchor + Coord(-1, 0),
                    Push::Right => anchor + Coord(1, 0),
                };
                if !collides(next_anchor, &shape_pieces, &at_rest) {
                    anchor = next_anchor;
                }

                // move down
                if !collides(anchor + Coord(0, -1), &shape_pieces, &at_rest) {
                    anchor += Coord(0, -1);
                } else {
                    for &shape_piece in &shape_pieces {
                        let abs_piece = anchor + shape_piece;
                        highest_point = highest_point.max(abs_piece.1 + 1);
                        at_rest.insert(abs_piece);
                    }
                    break;
                }
            }
        }
        highest_point as u64
    }

    fn part2(&self) -> Self::Output2 {
        // same but 1000000000000
        0
    }
}

#[test]
fn example() {
    let problem = Day17::new(">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>");
    assert_eq!(3068, problem.part1());
    assert_eq!(1514285714288, problem.part2());
}
