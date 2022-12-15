use crate::{
    utils::{self, Coord, Grid},
    Problem,
};

pub struct Day12 {
    grid: Grid<u8>,
    start: Coord,
    end: Coord,
}

impl Day12 {
    fn successors(&self, curr: Coord) -> Vec<Coord> {
        let curr_height = self.grid.coord_get(curr).unwrap();
        curr.get_adjacent()
            .into_iter()
            .filter(|&other| {
                self.grid.coord_get(other).is_some()
                    && *self.grid.coord_get(other).unwrap() <= curr_height + 1
            })
            .collect()
    }

    fn solve_from(&self, start: Coord) -> Option<u64> {
        utils::bfs(&start, |&n| self.successors(n), |&n| self.end == n).map(|a| a.len() as u64)
    }
}

impl Problem for Day12 {
    type Output1 = u64;
    type Output2 = u64;

    fn new(input: &str) -> Self {
        let mut start = None;
        let mut end = None;
        let grid = Grid {
            grid: input
                .lines()
                .enumerate()
                .map(|(y, l)| {
                    l.bytes()
                        .enumerate()
                        .map(|(x, c)| match c {
                            b'a'..=b'z' => c,
                            b'S' => {
                                start = Some(Coord(x as i64, y as i64));
                                b'a'
                            }
                            b'E' => {
                                end = Some(Coord(x as i64, y as i64));
                                b'z'
                            }
                            _ => unreachable!(),
                        })
                        .collect()
                })
                .collect(),
        };

        Day12 {
            grid,
            start: start.unwrap(),
            end: end.unwrap(),
        }
    }

    fn part1(&self) -> Self::Output1 {
        self.solve_from(self.start).unwrap()
    }

    fn part2(&self) -> Self::Output2 {
        // very unoptimized!
        // better way would be to only look at "a" spots if they
        // haven't been in a path already
        let mut best = None;
        for y in 0..self.grid.height() {
            for x in 0..self.grid.width() {
                let curr = Coord(x as i64, y as i64);
                if *self.grid.coord_get(curr).unwrap() == b'a' {
                    let this_solution = self.solve_from(curr);
                    if let Some(dist) = this_solution {
                        best = match best {
                            Some(curr) => Some(dist.min(curr)),
                            None => Some(dist),
                        }
                    }
                }
            }
        }
        best.unwrap()
    }
}

#[test]
fn example() {
    let problem = Day12::new(
        "Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi",
    );
    assert_eq!(31, problem.part1());
    assert_eq!(29, problem.part2());
}
