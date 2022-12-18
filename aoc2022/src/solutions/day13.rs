use std::{iter::Peekable, str};

use itertools::Itertools;

use crate::Problem;

pub struct Day13 {
    pairs: Vec<(Item, Item)>,
}

#[derive(Debug)]
pub enum Item {
    List(Vec<Item>),
    Int(u64),
}

impl Item {
    fn new(item: &str) -> Self {
        let mut iter = item.chars().peekable();
        Self::get_first_item(&mut iter)
    }

    fn get_first_item(iter: &mut Peekable<impl Iterator<Item = char>>) -> Self {
        match *iter.peek().unwrap() {
            '[' => {
                let mut children = Vec::new();
                loop {
                    match iter.next().unwrap() {
                        '[' | ',' => children.push(Self::get_first_item(iter)),
                        ']' => return Self::List(children),
                        _ => unreachable!(),
                    }
                }
            }
            ']' => Self::List(Vec::new()),
            '0'..='9' => Self::Int(Self::consume_number(iter)),
            _ => unreachable!(),
        }
    }

    fn consume_number(iter: &mut Peekable<impl Iterator<Item = char>>) -> u64 {
        iter.peeking_take_while(|b| b.is_ascii_digit())
            .collect::<String>()
            .parse()
            .unwrap()
    }
}

impl Eq for Item {}

impl PartialEq for Item {
    fn eq(&self, other: &Self) -> bool {
        match (self, other) {
            (Item::List(l), Item::List(r)) => l == r,
            (Item::Int(l), Item::Int(r)) => l == r,
            (Item::List(l), Item::Int(r)) => l == &vec![Item::Int(*r)],
            (Item::Int(l), Item::List(r)) => &vec![Item::Int(*l)] == r,
        }
    }
}

impl Ord for Item {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        match (self, other) {
            (Item::List(l), Item::List(r)) => {
                for (l_child, r_child) in std::iter::zip(l, r) {
                    if l_child != r_child {
                        return l_child.cmp(r_child);
                    }
                }
                l.len().cmp(&r.len())
            }
            (Item::List(_), Item::Int(r)) => self.cmp(&Item::List(Vec::from([Item::Int(*r)]))),
            (Item::Int(l), Item::List(_)) => Item::List(Vec::from([Item::Int(*l)])).cmp(other),
            (Item::Int(l), Item::Int(r)) => l.cmp(r),
        }
    }
}

impl PartialOrd for Item {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

impl Problem for Day13 {
    type Output1 = u64;
    type Output2 = u64;

    fn new(input: &str) -> Self {
        let pairs = input
            .lines()
            .collect::<Vec<_>>()
            .split(|l| l.is_empty())
            .map(|pair| (Item::new(pair[0]), Item::new(pair[1])))
            .collect();
        Day13 { pairs }
    }

    fn part1(&self) -> Self::Output1 {
        (1..)
            .zip(&self.pairs)
            .filter_map(|(i, (l, r))| if l < r { Some(i) } else { None })
            .sum()
    }

    fn part2(&self) -> Self::Output2 {
        let mut all = self
            .pairs
            .iter()
            .flat_map(|(l, r)| [l, r].into_iter())
            .collect::<Vec<_>>();
        let divider1 = Item::new("[[2]]");
        let divider2 = Item::new("[[6]]");
        all.push(&divider1);
        all.push(&divider2);

        all.sort();
        let i1 = all.iter().position(|&c| c == &divider1).unwrap() + 1;
        let i2 = all.iter().position(|&c| c == &divider2).unwrap() + 1;
        (i1 * i2) as u64
    }
}

#[test]
fn example() {
    let problem = Day13::new(
        "[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]",
    );
    assert_eq!(13, problem.part1());
    assert_eq!(140, problem.part2());
}
