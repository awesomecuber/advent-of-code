use itertools::Itertools;

use crate::Problem;

pub struct Day6 {
    buffer: String,
}

impl Day6 {
    fn solve(&self, window_size: usize) -> u64 {
        (self
            .buffer
            .chars()
            .collect::<Vec<_>>()
            .windows(window_size)
            .position(|w| w.iter().all_unique())
            .unwrap()
            + window_size) as u64
    }
}

impl Problem for Day6 {
    type Output = u64;

    fn new(input: &str) -> Self {
        Day6 {
            buffer: input.to_owned(),
        }
    }

    fn part1(&self) -> Self::Output {
        self.solve(4)
    }

    fn part2(&self) -> Self::Output {
        self.solve(14)
    }
}

#[test]
fn examples() {
    for (input, solution1, solution2) in [
        ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7, 19),
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5, 23),
        ("nppdvjthqldpwncqszvftbrmjlhg", 6, 23),
        ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, 29),
        ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, 26),
    ] {
        let problem = Day6::new(input);
        assert_eq!(solution1, problem.part1());
        assert_eq!(solution2, problem.part2());
    }
}
