use parse_display::FromStr;

use crate::Problem;

pub struct Day11 {
    monkeys: Vec<Monkey>,
}

#[derive(Clone, Debug)]
pub struct Monkey {
    items: Vec<u64>,
    operation: Operation,
    test_disible_by: u64,
    if_true: usize,
    if_false: usize,
}

#[derive(Clone, Debug, FromStr)]
pub enum Operation {
    #[display("new = old + {0}")]
    Plus(u64),
    #[display("new = old * {0}")]
    Times(u64),
    #[display("new = old * old")]
    Square,
}

impl Operation {
    fn new_worry(&self, old_worry: u64) -> u64 {
        match self {
            Operation::Plus(n) => old_worry + n,
            Operation::Times(n) => old_worry * n,
            Operation::Square => old_worry * old_worry,
        }
    }
}

impl Problem for Day11 {
    type Output1 = u64;
    type Output2 = u64;

    fn new(input: &str) -> Self {
        let mut monkeys = Vec::new();
        for lines in input.lines().collect::<Vec<_>>().split(|l| l.is_empty()) {
            let items = lines[1]
                .strip_prefix("  Starting items: ")
                .unwrap()
                .split(", ")
                .map(|s| s.parse().unwrap())
                .collect();
            let operation = lines[2]
                .strip_prefix("  Operation: ")
                .unwrap()
                .parse()
                .unwrap();
            let test_disible_by = lines[3]
                .strip_prefix("  Test: divisible by ")
                .unwrap()
                .parse()
                .unwrap();
            let if_true = lines[4]
                .strip_prefix("    If true: throw to monkey ")
                .unwrap()
                .parse()
                .unwrap();
            let if_false = lines[5]
                .strip_prefix("    If false: throw to monkey ")
                .unwrap()
                .parse()
                .unwrap();
            monkeys.push(Monkey {
                items,
                operation,
                test_disible_by,
                if_true,
                if_false,
            })
        }
        Day11 { monkeys }
    }

    fn part1(&self) -> Self::Output1 {
        let mut monkeys = self.monkeys.clone();
        let mut inspect_counts = vec![0u64; monkeys.len()];
        for _ in 0..20 {
            for i in 0..monkeys.len() {
                let items = std::mem::take(&mut monkeys[i].items);
                inspect_counts[i] += items.len() as u64;
                for item in items {
                    let worry_level = monkeys[i].operation.new_worry(item) / 3;
                    if worry_level % monkeys[i].test_disible_by == 0 {
                        let if_true = monkeys[i].if_true;
                        monkeys[if_true].items.push(worry_level);
                    } else {
                        let if_false = monkeys[i].if_false;
                        monkeys[if_false].items.push(worry_level);
                    }
                }
            }
        }
        inspect_counts.sort_unstable();
        inspect_counts.iter().rev().take(2).product()
    }

    fn part2(&self) -> Self::Output2 {
        let mut monkeys = self.monkeys.clone();
        let mut inspect_counts = vec![0u64; monkeys.len()];
        let cap: u64 = monkeys.iter().map(|m| m.test_disible_by).product();
        for _ in 0..10000 {
            for i in 0..monkeys.len() {
                let items = std::mem::take(&mut monkeys[i].items);
                inspect_counts[i] += items.len() as u64;
                for item in items {
                    let worry_level = monkeys[i].operation.new_worry(item) % cap;
                    if worry_level % monkeys[i].test_disible_by == 0 {
                        let if_true = monkeys[i].if_true;
                        monkeys[if_true].items.push(worry_level);
                    } else {
                        let if_false = monkeys[i].if_false;
                        monkeys[if_false].items.push(worry_level);
                    }
                }
            }
        }
        inspect_counts.sort_unstable();
        inspect_counts.iter().rev().take(2).product()
    }
}

#[test]
fn example() {
    let problem = Day11::new(
        "Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1",
    );
    assert_eq!(10605, problem.part1());
    assert_eq!(2713310158, problem.part2());
}
