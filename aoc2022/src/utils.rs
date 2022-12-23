use std::collections::{BinaryHeap, HashMap};
use std::fmt::Debug;
use std::fmt::Display;
use std::hash::Hash;
use std::ops::{Add, AddAssign, Sub};

use parse_display::FromStr;

#[derive(Clone, Copy, Debug, Eq, PartialEq, Hash, FromStr)]
#[display("{0},{1}")]
pub struct Coord(pub i64, pub i64);

impl Coord {
    pub fn get_adjacent(self) -> Vec<Self> {
        vec![
            self + Coord(1, 0),
            self + Coord(-1, 0),
            self + Coord(0, 1),
            self + Coord(0, -1),
        ]
    }

    // pub fn get_adjacent_with_corners(self) -> Vec<Self> {
    //     let mut adjacent = self.get_adjacent();
    //     adjacent.extend_from_slice(&[
    //         self + Coord(1, 1),
    //         self + Coord(-1, 1),
    //         self + Coord(1, -1),
    //         self + Coord(-1, -1),
    //     ]);
    //     adjacent
    // }

    pub fn manhattan_distance(self, other: Self) -> u64 {
        self.0.abs_diff(other.0) + self.1.abs_diff(other.1)
    }
}

impl Add for Coord {
    type Output = Coord;

    fn add(self, rhs: Self) -> Self::Output {
        Coord(self.0 + rhs.0, self.1 + rhs.1)
    }
}

impl AddAssign for Coord {
    fn add_assign(&mut self, rhs: Self) {
        self.0 += rhs.0;
        self.1 += rhs.1;
    }
}

impl Sub for Coord {
    type Output = Coord;

    fn sub(self, rhs: Self) -> Self::Output {
        Coord(self.0 - rhs.0, self.1 - rhs.1)
    }
}

#[derive(Debug)]
pub struct Grid<T> {
    pub grid: Vec<Vec<T>>,
}

impl<T> Grid<T> {
    pub fn width(&self) -> usize {
        self.grid[0].len()
    }

    // pub fn height(&self) -> usize {
    //     self.grid.len()
    // }

    pub fn coord_get(&self, coord: Coord) -> Option<&T> {
        if coord.0 < 0 || coord.1 < 0 {
            return None;
        }
        self.grid.get(coord.1 as usize)?.get(coord.0 as usize)
    }

    // pub fn coord_get_mut(&mut self, coord: Coord) -> Option<&mut T> {
    //     if coord.0 < 0 && coord.1 < 0 {
    //         return None;
    //     }
    //     self.grid
    //         .get_mut(coord.1 as usize)?
    //         .get_mut(coord.0 as usize)
    // }
}

impl Display for Grid<char> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for row in &self.grid {
            for item in row {
                write!(f, "{}", item)?;
            }
            writeln!(f, "\n")?;
        }
        Ok(())
    }
}

impl Display for Grid<u8> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for row in &self.grid {
            writeln!(f, "{:?}\n", String::from_utf8(row.clone()).unwrap())?;
        }
        Ok(())
    }
}

#[test]
fn example() {
    let grid = Grid {
        grid: vec![vec![1, 2], vec![3, 4]],
    };
    assert_eq!(grid.coord_get(Coord(1, 0)), Some(&2));
}

#[derive(Debug)]
struct Container<T> {
    node: T,
    cost: u64,
}

impl<T> PartialEq for Container<T> {
    fn eq(&self, other: &Self) -> bool {
        self.cost == other.cost
    }
}

impl<T> Eq for Container<T> {}

impl<T> Ord for Container<T> {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        other.cost.cmp(&self.cost)
    }
}

impl<T> PartialOrd for Container<T> {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

// This function is heavily inspired from the pathfinding crate. I thought I'd
// use dijkstra's for day 16, so I made this function (and made the BFS function
// call this one), but it turns out that I didn't need dijkstras...
pub fn dijkstras<N, FN, IN, FS>(start: &N, successors: FN, success: FS) -> Option<(Vec<N>, u64)>
where
    N: Eq + Hash + Clone + Debug,
    FN: Fn(&N) -> IN,
    IN: IntoIterator<Item = (N, u64)>,
    FS: Fn(&N) -> bool,
{
    let mut horizon = BinaryHeap::new();
    // maps to parent (if exists) and cost to get there
    let mut seen: HashMap<N, (Option<N>, u64)> = HashMap::new();
    horizon.push(Container {
        node: start.clone(),
        cost: 0,
    });
    seen.insert(start.clone(), (None, 0));
    while let Some(curr) = horizon.pop() {
        if let Some((_, other_cost)) = seen.get(&curr.node) {
            if *other_cost != curr.cost {
                continue;
            }
        }
        if success(&curr.node) {
            let mut to_return = vec![curr.node.clone()];
            let mut node = curr.node;
            while let Some((val, _)) = seen.get(&node) {
                if let Some(val) = val {
                    to_return.push(val.clone());
                    node = val.clone();
                } else {
                    break;
                }
            }
            to_return.reverse();
            return Some((to_return, curr.cost));
        }

        for (successor, step_cost) in successors(&curr.node) {
            let explore = seen
                .get(&successor)
                .map(|(_, other_cost)| curr.cost + step_cost < *other_cost)
                .unwrap_or(true);

            if explore {
                horizon.push(Container {
                    node: successor.clone(),
                    cost: curr.cost + step_cost,
                });
                seen.insert(
                    successor.clone(),
                    (Some(curr.node.clone()), curr.cost + step_cost),
                );
            }
        }
    }
    None
}

pub fn bfs<N, FN, IN, FS>(start: &N, successors: FN, success: FS) -> Option<Vec<N>>
where
    N: Eq + Hash + Clone + Debug,
    FN: Fn(&N) -> IN,
    IN: IntoIterator<Item = N>,
    FS: Fn(&N) -> bool,
{
    dijkstras(
        start,
        |n| successors(n).into_iter().map(|n| (n, 1)),
        success,
    )
    .map(|(l, _)| l)
}
