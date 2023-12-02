use crate::Problem;

#[derive(Debug)]
pub struct Day2 {
    games: Vec<Game>,
}

#[derive(Debug)]
struct Game {
    cube_sets: Vec<CubeSet>,
}

#[derive(Debug, Default)]
struct CubeSet {
    red: u64,
    green: u64,
    blue: u64,
}

impl Problem for Day2 {
    type Output1 = u64;
    type Output2 = u64;

    fn new(input: &str) -> Self {
        let games = input
            .lines()
            .map(|line| {
                let (_, game_info) = line.split_once(": ").unwrap();
                let cube_sets = game_info
                    .split("; ")
                    .map(|s| {
                        let mut cube_set = CubeSet::default();
                        for term in s.split(", ") {
                            let (count, color) = term.split_once(' ').unwrap();
                            let count = count.parse::<u64>().unwrap();
                            match color {
                                "red" => cube_set.red = count,
                                "green" => cube_set.green = count,
                                "blue" => cube_set.blue = count,
                                _ => unreachable!(),
                            }
                        }
                        cube_set
                    })
                    .collect();
                Game { cube_sets }
            })
            .collect();
        Day2 { games }
    }

    fn part1(&self) -> Self::Output1 {
        self.games
            .iter()
            .enumerate()
            .filter(|(_, game)| {
                game.cube_sets.iter().all(|cube_set| {
                    cube_set.red <= 12 && cube_set.green <= 13 && cube_set.blue <= 14
                })
            })
            .map(|(i, _)| (i + 1) as u64)
            .sum()
    }

    fn part2(&self) -> Self::Output2 {
        self.games
            .iter()
            .map(|game| {
                let mut best_red = 0;
                let mut best_green = 0;
                let mut best_blue = 0;
                for cube_set in game.cube_sets.iter() {
                    best_red = best_red.max(cube_set.red);
                    best_green = best_green.max(cube_set.green);
                    best_blue = best_blue.max(cube_set.blue);
                }
                best_red * best_green * best_blue
            })
            .sum()
    }
}

#[test]
fn example() {
    let problem = Day2::new(
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
    );
    assert_eq!(8, problem.part1());
    assert_eq!(2286, problem.part2());
}
