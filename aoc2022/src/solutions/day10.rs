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
        let mut x = 1;
        let mut signal_strengths = 0;
        let mut inst_iter = self.instructions.iter();
        let mut delay_add = None;

        for cycle in 1..=220 {
            if (cycle - 20) % 40 == 0 {
                signal_strengths += cycle * x;
            }
            match delay_add {
                Some(arg) => {
                    x += arg;
                    delay_add = None;
                }
                None => match inst_iter.next().unwrap() {
                    Instruction::Addx(arg) => {
                        delay_add = Some(arg);
                    }
                    Instruction::Noop => {}
                },
            }
        }
        signal_strengths as u64
    }

    fn part2(&self) -> Self::Output2 {
        let mut x = 1;
        let mut picture = String::new();
        let mut inst_iter = self.instructions.iter();
        let mut delay_add = None;

        for cycle in 1..=240 {
            if cycle % 40 == 1 {
                // also on cycle 1, to display better in terminal
                picture.push('\n');
            }
            if ((x - 1)..=(x + 1)).contains(&((cycle - 1) % 40)) {
                picture.push('#');
            } else {
                picture.push('.');
            }
            match delay_add {
                Some(arg) => {
                    x += arg;
                    delay_add = None;
                }
                None => match inst_iter.next().unwrap() {
                    Instruction::Addx(arg) => {
                        delay_add = Some(arg);
                    }
                    Instruction::Noop => {}
                },
            }
        }
        picture
    }
}

#[test]
fn example() {
    let problem = Day10::new(include_str!("day10ex.txt"));
    assert_eq!(13140, problem.part1());
    assert_eq!(
        "
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....",
        problem.part2()
    );
}
