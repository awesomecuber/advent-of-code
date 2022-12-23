use std::collections::{HashMap, HashSet};

use parse_display::FromStr;

use crate::Problem;

pub struct Day16 {
    valves: HashMap<String, (u64, HashSet<String>)>,
}

#[derive(FromStr, Debug)]
#[display("Valve {0} has flow rate={1}; tunnels lead to valves {2}")]
struct Line(String, u64, String);

impl Day16 {
    fn get_paths(&self, start: &str) -> HashMap<String, HashSet<(String, u64)>> {
        let mut paths = HashMap::new();
        for (valve, (flow, _)) in &self.valves {
            if valve == start || *flow != 0 {
                paths.insert(valve.to_owned(), self.dists_from(valve));
            }
        }
        paths
    }

    fn dists_from(&self, valve: &str) -> HashSet<(String, u64)> {
        let mut dists = HashSet::new();

        let mut seen = HashSet::new();
        let mut horizon = HashSet::new();
        seen.insert(valve);
        horizon.insert(valve);

        let mut dist = 0;
        while !horizon.is_empty() {
            for node in std::mem::take(&mut horizon) {
                let (flow, connected) = self.valves.get(node).unwrap();
                if *flow != 0 && dist != 0 {
                    dists.insert((node.to_owned(), dist));
                }
                for neighbor in connected {
                    if seen.insert(neighbor) {
                        horizon.insert(neighbor);
                    }
                }
            }
            dist += 1;
        }
        dists
    }

    fn best_from(
        &self,
        currently_at: &str,
        open_valves: &mut HashSet<String>,
        minutes_left: u64,
        paths: &HashMap<String, HashSet<(String, u64)>>,
    ) -> u64 {
        let mut other_scores = Vec::new();

        let can_go = paths.get(currently_at).unwrap();
        for (dest, dist) in can_go {
            if open_valves.contains(dest) || minutes_left <= *dist {
                continue;
            }
            let new_minutes_left = minutes_left - dist - 1;
            let (flow, _) = self.valves.get(dest).unwrap();
            open_valves.insert(dest.to_owned());
            other_scores.push(
                flow * new_minutes_left
                    + self.best_from(dest, open_valves, new_minutes_left, paths),
            );
            open_valves.remove(dest);
        }

        other_scores.into_iter().max().unwrap_or(0)
    }
}

impl Problem for Day16 {
    type Output1 = u64;
    type Output2 = u64;

    fn new(input: &str) -> Self {
        let mut valves = HashMap::new();
        for line in input.lines().map(|l| {
            let line = l.to_owned();
            let line = line.replace("tunnel leads to valve", "tunnels lead to valves");
            line.parse::<Line>().unwrap()
        }) {
            valves.insert(
                line.0,
                (line.1, line.2.split(", ").map(|s| s.to_owned()).collect()),
            );
        }
        Day16 { valves }
    }

    fn part1(&self) -> Self::Output1 {
        self.best_from("AA", &mut HashSet::new(), 30, &self.get_paths("AA"))
    }

    fn part2(&self) -> Self::Output2 {
        0
    }
}

#[test]
fn example() {
    let problem = Day16::new(
        "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II",
    );
    assert_eq!(1651, problem.part1());
}
