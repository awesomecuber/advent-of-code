use std::collections::{HashMap, VecDeque};
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

    pub fn height(&self) -> usize {
        self.grid.len()
    }

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

pub fn bfs<N, FN, IN, FS>(start: &N, successors: FN, success: FS) -> Option<Vec<N>>
where
    N: Eq + Hash + Clone + Debug,
    FN: Fn(&N) -> IN,
    IN: IntoIterator<Item = N>,
    FS: Fn(&N) -> bool,
{
    let mut horizon = VecDeque::new();
    let mut parents: HashMap<N, Option<N>> = HashMap::new();
    horizon.push_front(start.clone());
    parents.insert(start.clone(), None);
    while let Some(curr) = horizon.pop_front() {
        for successor in successors(&curr) {
            if success(&successor) {
                let mut to_return = vec![curr.clone()];
                let mut node = curr;
                while let Some(val) = parents.get(&node) {
                    if let Some(val) = val {
                        to_return.push(val.clone());
                        node = val.clone();
                    } else {
                        break;
                    }
                }
                to_return.reverse();
                return Some(to_return);
            }
            if !parents.contains_key(&successor) {
                horizon.push_back(successor.clone());
                parents.insert(successor.clone(), Some(curr.clone()));
            }
        }
    }
    None
}
