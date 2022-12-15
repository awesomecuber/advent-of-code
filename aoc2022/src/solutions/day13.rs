use std::str;

use crate::Problem;

pub struct Day13 {
    pairs: Vec<(Item, Item)>,
}

// two items:
// - list: [X, Y, ..., Z]
// - integer: 1

#[derive(Debug)]
pub enum Item {
    List(Vec<Item>),
    Int(u64),
}

impl Item {
    fn new(item: &[u8]) -> Self {
        println!("{:?}", str::from_utf8(item).unwrap());
        if item[0] == b'[' {
            assert!(item[item.len() - 1] == b']');
            let inside = &item[1..item.len() - 1];
            let mut children = Vec::new();
            for inner in inside.split(|&c| c == b',') {
                children.push(Self::new(inner));
            }
            Self::List(children)
        } else {
            Self::Int(str::from_utf8(item).unwrap().parse().unwrap())
        }
    }
}

impl Problem for Day13 {
    type Output1 = u64;
    type Output2 = u64;

    fn new(input: &str) -> Self {
        let item = Item::new(input.lines().nth(3).unwrap().as_bytes());
        println!("{:?}", item);
        todo!()
    }

    fn part1(&self) -> Self::Output1 {
        todo!()
    }

    fn part2(&self) -> Self::Output2 {
        todo!()
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
}
