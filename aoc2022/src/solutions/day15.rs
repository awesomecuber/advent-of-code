use std::{
    collections::{HashMap, HashSet},
    ops::RangeInclusive,
};

use parse_display::FromStr;

use crate::{utils::Coord, Problem};

pub struct Day15 {
    sensor_beacon_pairs: Vec<(Coord, Coord)>,
}

#[derive(FromStr)]
#[display("Sensor at x={0}, y={1}: closest beacon is at x={2}, y={3}")]
struct Line(i64, i64, i64, i64);

impl Day15 {
    pub fn solve1(&self, yrow: i64) -> u64 {
        let mut ranges: Vec<RangeInclusive<i64>> = Vec::new();
        for &(sensor, beacon) in &self.sensor_beacon_pairs {
            let sensor_beacon_dist = sensor.manhattan_distance(beacon);
            let sensor_yrow_dist = sensor.1.abs_diff(yrow);
            // if sensor range of denial reaches the relevant yrow
            if sensor_beacon_dist >= sensor_yrow_dist {
                let excess = (sensor_beacon_dist - sensor_yrow_dist) as i64;
                ranges.push((sensor.0 - excess)..=(sensor.0 + excess));
            }
        }
        ranges.sort_by_key(|r| *r.start());
        let mut combined_ranges: Vec<RangeInclusive<i64>> = Vec::new();
        for range in ranges {
            match combined_ranges.last_mut() {
                Some(top) => {
                    if range.start() > top.end() {
                        // no overlap
                        combined_ranges.push(range);
                    } else if range.end() > top.end() {
                        // overlap and need to extend end of top
                        *top = (*top.start())..=(*range.end());
                    }
                }
                None => combined_ranges.push(range),
            }
        }
        let beacon_count_on_range = self
            .sensor_beacon_pairs
            .iter()
            .map(|(_, b)| b)
            .filter(|&b| b.1 == yrow && combined_ranges.iter().any(|r| r.contains(&b.0)))
            .collect::<HashSet<_>>()
            .len();

        let range_total: i64 = combined_ranges
            .into_iter()
            .map(|r| r.end() - r.start() + 1)
            .sum();
        range_total as u64 - beacon_count_on_range as u64
    }

    fn solve2(&self, grid_size: u64) -> u64 {
        let mut sensor_rois = HashMap::new();
        for &(sensor, beacon) in &self.sensor_beacon_pairs {
            sensor_rois.insert(sensor, sensor.manhattan_distance(beacon));
        }
        let uncovered_coord = Self::solve2inner(
            Coord(0, 0),
            Coord(grid_size as i64, grid_size as i64),
            &sensor_rois,
        )
        .unwrap();
        (uncovered_coord.0 * 4000000 + uncovered_coord.1) as u64
    }

    fn solve2inner(
        topleft: Coord,
        bottomright: Coord,
        sensor_rois: &HashMap<Coord, u64>,
    ) -> Option<Coord> {
        assert!(topleft.0 <= bottomright.0 && topleft.1 <= bottomright.1);

        if topleft == bottomright {
            // if the spot is not visiable by any sensor, that's the spot
            if sensor_rois
                .iter()
                .all(|(sensor, roi)| sensor.manhattan_distance(topleft) > *roi)
            {
                return Some(topleft);
            }
            return None;
        }

        let bottomleft = Coord(topleft.0, bottomright.1);
        let topright = Coord(bottomright.0, topleft.1);

        // if for some sensor, all four corners are visible by it, return None
        // since all spots in that region are visible by a sensor
        if sensor_rois.iter().any(|(sensor, roi)| {
            [topleft, bottomleft, topright, bottomright]
                .into_iter()
                .all(|spot| sensor.manhattan_distance(spot) <= *roi)
        }) {
            return None;
        }

        // otherwise, split box into 4 and recursively call
        let mid = Coord(
            (topleft.0 + bottomright.0) / 2,
            (topleft.1 + bottomright.1) / 2,
        );
        let topmid = Coord(mid.0, topleft.1);
        let bottommid = Coord(mid.0, bottomleft.1);
        let midleft = Coord(topleft.0, mid.1);
        let midright = Coord(topright.0, mid.1);

        let to_check = if topleft.0 == bottomright.0 {
            vec![(topleft, mid), (mid + Coord(0, 1), bottomright)]
        } else if topleft.1 == bottomright.1 {
            vec![(topleft, mid), (mid + Coord(1, 0), bottomright)]
        } else {
            vec![
                (topleft, mid),
                (topmid + Coord(1, 0), midright),
                (midleft + Coord(0, 1), bottommid),
                (mid + Coord(1, 1), bottomright),
            ]
        };

        for (from, to) in to_check {
            if let Some(spot) = Self::solve2inner(from, to, sensor_rois) {
                return Some(spot);
            }
        }

        None
    }
}

impl Problem for Day15 {
    type Output1 = u64;
    type Output2 = u64;

    fn new(input: &str) -> Self {
        let sensor_beacon_pairs = input
            .lines()
            .map(|l| {
                let Line(sx, sy, bx, by) = l.parse::<Line>().unwrap();
                (Coord(sx, sy), Coord(bx, by))
            })
            .collect();
        Day15 {
            sensor_beacon_pairs,
        }
    }

    fn part1(&self) -> Self::Output1 {
        self.solve1(2000000)
    }

    fn part2(&self) -> Self::Output2 {
        self.solve2(4000000)
    }
}

#[test]
fn example() {
    let problem = Day15::new(
        "Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3",
    );
    assert_eq!(26, problem.solve1(10));
    assert_eq!(56000011, problem.solve2(20));
}
