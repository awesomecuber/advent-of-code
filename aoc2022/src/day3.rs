use std::collections::HashSet;

use itertools::Itertools;

use crate::Problem;

pub struct Day3;

fn priority(char: char) -> u64 {
    assert!(char.is_ascii_alphabetic());
    let utf8_code_point: u64 = char.into();
    if char.is_ascii_lowercase() {
        utf8_code_point - 96
    } else {
        utf8_code_point - 38
    }
}

#[test]
fn test_priority() {
    assert_eq!(2, priority('b'));
    assert_eq!(29, priority('C'));
}

impl Problem for Day3 {
    type Data = Vec<String>;

    type Output = u64;

    fn to_data(input: &str) -> Self::Data {
        input
            .lines()
            .map(|l| l.into())
            .collect()
    }

    fn part1(data: &Self::Data) -> Self::Output {
        data.iter()
            .map(|line| {
                let left: HashSet<_> = line[line.len() / 2..].chars().collect();
                let right: HashSet<_> = line[..line.len() / 2].chars().collect();

                let intersection = &left & &right;
                assert_eq!(1, intersection.len());
                priority(*intersection.iter().next().unwrap())
            })
            .sum()
    }

    fn part2(data: &Self::Data) -> Self::Output {
        data.iter().tuples().map(|(a, b, c)| {
            let a: HashSet<_> = a.chars().collect();
            let b: HashSet<_> = b.chars().collect();
            let c: HashSet<_> = c.chars().collect();
            let intersection = &(&a & &b) & &c;
            assert_eq!(1, intersection.len());
            priority(*intersection.iter().next().unwrap())
        }).sum()
    }
}
