mod day1;
mod day2;
mod day3;

pub trait Problem {
    type Data;
    type Output;

    fn to_data(input: &str) -> Self::Data;
    fn part1(data: &Self::Data) -> Self::Output;
    fn part2(data: &Self::Data) -> Self::Output;
}

macro_rules! solve {
    ($day:ty, $input_str:expr) => {
        let input = std::fs::read_to_string($input_str).unwrap();
        let data = <$day>::to_data(&input);
        let part1 = <$day>::part1(&data);
        let part2 = <$day>::part2(&data);
        println!("Part 1: {}\nPart 2: {}", part1, part2);
    };
}

fn main() {
    // solve!(day1::Day1, "./inputs/day1.txt");
    // solve!(day2::Day2, "./inputs/day2.txt");
    solve!(day3::Day3, "./inputs/day3.txt");
}
