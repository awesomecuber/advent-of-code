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

    fn successors_back(&self, curr: Coord) -> Vec<Coord> {
        let curr_height = self.grid.coord_get(curr).unwrap();
        curr.get_adjacent()
            .into_iter()
            .filter(|&other| {
                self.grid.coord_get(other).is_some()
                    && *self.grid.coord_get(other).unwrap() >= curr_height - 1
            })
            .collect()
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
        utils::bfs(&self.start, |&n| self.successors(n), |&n| self.end == n)
            .map(|a| a.len() as u64)
            .unwrap()
    }

    fn part2(&self) -> Self::Output2 {
        utils::bfs(
            &self.end,
            |&n| self.successors_back(n),
            |&n| *self.grid.coord_get(n).unwrap() == b'a',
        )
        .map(|a| a.len() as u64)
        .unwrap()
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
