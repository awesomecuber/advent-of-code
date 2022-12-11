use parse_display::FromStr;

use crate::Problem;

pub struct Day10 {
    instructions: Vec<Instruction>,
}

#[derive(FromStr)]
pub enum Instruction {
    #[display("addx {0}")]
    Addx(i64),
    #[display("noop")]
    Noop,
}

impl Problem for Day10 {
    type Output1 = u64;
    type Output2 = String;

    fn new(input: &str) -> Self {
        Day10 {
            instructions: input.lines().map(|l| l.parse().unwrap()).collect(),
        }
    }

    fn part1(&self) -> Self::Output1 {
        let mut cycle = 1;
        let mut signal_strengths = 0;
        let mut x = 1;
        for instruction in &self.instructions {
            if cycle % 20 == 0 && cycle % 40 == 20 {
                signal_strengths += cycle * x;
            }
            match instruction {
                Instruction::Addx(arg) => {
                    // for this case, we compensate for otherwise skipping the above if statement
                    if (cycle + 1) % 20 == 0 && (cycle + 1) % 40 == 20 {
                        signal_strengths += (cycle + 1) * x;
                    }
                    x += arg;
                    cycle += 2;
                }
                Instruction::Noop => {
                    cycle += 1;
                }
            }
            if cycle > 220 {
                break;
            }
        }
        signal_strengths as u64
    }

    fn part2(&self) -> Self::Output2 {
        "".to_owned()
    }
}

#[test]
fn example() {
    let problem = Day10::new(include_str!("day10ex.txt"));
    assert_eq!(13140, problem.part1());
}
