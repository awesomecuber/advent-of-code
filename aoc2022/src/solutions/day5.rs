use std::str::from_utf8;

use parse_display::FromStr;

use crate::Problem;

pub struct Day5 {
    crate_piles: Vec<Vec<u8>>,
    instructions: Vec<Inst>,
}

#[derive(FromStr)]
#[display("move {count} from {from} to {to}")]
struct Inst {
    count: u64,
    from: usize,
    to: usize,
}

fn read_crate_piles(piles: &[Vec<u8>]) -> String {
    String::from_utf8(piles.iter().map(|p| *p.last().unwrap()).collect()).unwrap()
}

impl Problem for Day5 {
    type Output = String;

    fn new(input: &str) -> Self {
        let lines: Vec<_> = input.lines().map(|l| l.as_bytes()).collect();
        let empty_line = lines.iter().position(|&l| l.is_empty()).unwrap();
        let crates = &lines[..empty_line - 1];
        let instructions = &lines[empty_line + 1..];

        let mut crate_piles = Vec::new();
        for col in (1..).step_by(4) {
            if crates[0].get(col).is_none() {
                break;
            }
            let mut pile = Vec::new();
            for row in (0..crates.len()).rev() {
                match crates[row][col] {
                    b' ' => {}
                    crate_letter => {
                        pile.push(crate_letter);
                    }
                }
            }
            crate_piles.push(pile);
        }

        let instructions = instructions
            .iter()
            .map(|&inst| from_utf8(inst).unwrap().parse().unwrap())
            .collect();

        Day5 {
            crate_piles,
            instructions,
        }
    }

    fn part1(&self) -> Self::Output {
        let mut crate_piles = self.crate_piles.to_vec();
        for inst in &self.instructions {
            for _ in 0..inst.count {
                let removed = crate_piles[inst.from - 1].pop().unwrap();
                crate_piles[inst.to - 1].push(removed);
            }
        }
        read_crate_piles(&crate_piles)
    }

    fn part2(&self) -> Self::Output {
        let mut crate_piles = self.crate_piles.to_vec();
        for inst in &self.instructions {
            let mut all_removed = Vec::new();
            for _ in 0..inst.count {
                let removed = crate_piles[inst.from - 1].pop().unwrap();
                all_removed.push(removed);
            }
            crate_piles[inst.to - 1].extend(all_removed.iter().rev());
        }
        read_crate_piles(&crate_piles)
    }
}

#[test]
fn example() {
    let problem = Day5::new(
        "    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2",
    );
    assert_eq!("CMZ".to_owned(), problem.part1());
    assert_eq!("MCD".to_owned(), problem.part2());
}
