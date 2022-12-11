use parse_display::FromStr;

use crate::Problem;

pub struct Day7 {
    commands: Vec<Command>,
}

#[derive(Debug)]
pub enum Command {
    Cd(CdArg),
    Ls(Vec<LsOutput>),
}

#[derive(Debug, FromStr)]
pub enum CdArg {
    #[display("/")]
    Start,
    #[display("{0}")]
    In(String),
    #[display("..")]
    Out,
}

#[derive(Debug, FromStr)]
pub enum LsOutput {
    #[display("dir {0}")]
    Dir(String),
    #[display("{1} {0}")]
    File(String, u64),
}

#[derive(Debug)]
enum FileSystem {
    File(String, u64),
    Dir(String, Vec<FileSystem>),
}

impl FileSystem {
    fn new_dir<'a, I>(dir_name: &str, commands: &mut I) -> Self
    where
        I: Iterator<Item = &'a Command>,
    {
        let mut children = Vec::new();
        while let Some(command) = commands.next() {
            match command {
                Command::Cd(arg) => match arg {
                    CdArg::Start => unreachable!(), // doesn't happen after line 1
                    CdArg::In(subdir) => children.push(FileSystem::new_dir(subdir, commands)),
                    CdArg::Out => break,
                },
                Command::Ls(outputs) => {
                    for output in outputs {
                        match output {
                            LsOutput::Dir(_) => {} // will be covered when we CD into the dir
                            LsOutput::File(name, size) => {
                                children.push(FileSystem::File(name.to_owned(), *size))
                            }
                        }
                    }
                }
            }
        }
        FileSystem::Dir(dir_name.to_owned(), children)
    }

    fn get_dir_sizes(&self) -> (Vec<u64>, u64) {
        match self {
            FileSystem::File(_, size) => (Vec::new(), *size),
            FileSystem::Dir(_, children) => {
                let (mut vec, total_size) = children.iter().map(|c| c.get_dir_sizes()).fold(
                    (Vec::new(), 0),
                    |(vec, total_size), (child_vec, size)| {
                        (
                            Vec::from_iter(vec.into_iter().chain(child_vec.into_iter())),
                            total_size + size,
                        )
                    },
                );
                vec.push(total_size);
                (vec, total_size)
            }
        }
    }
}

impl Problem for Day7 {
    type Output1 = u64;
    type Output2 = u64;

    fn new(input: &str) -> Self {
        let mut commands = Vec::new();

        let mut lines = input.lines().peekable();
        while let Some(line) = lines.next() {
            if line.starts_with("$ ls") {
                let mut output = Vec::new();
                while let Some(line) = lines.next() {
                    output.push(line.parse().unwrap());
                    let next_line = lines.peek();
                    if next_line.is_some() && next_line.unwrap().starts_with('$') {
                        break;
                    }
                }
                commands.push(Command::Ls(output));
            } else if let Some(arg) = line.strip_prefix("$ cd ") {
                commands.push(Command::Cd(arg.parse().unwrap()));
            } else {
                panic!("unexpected command");
            }
        }
        Day7 { commands }
    }

    fn part1(&self) -> Self::Output1 {
        // first line is cd /
        let home_dir = FileSystem::new_dir("/", &mut self.commands.iter().skip(1));
        let (dir_sizes, _) = home_dir.get_dir_sizes();
        dir_sizes.iter().filter(|&s| *s <= 100000).sum()
    }

    fn part2(&self) -> Self::Output2 {
        // first line is cd /
        let home_dir = FileSystem::new_dir("/", &mut self.commands.iter().skip(1));
        let (dir_sizes, total_size) = home_dir.get_dir_sizes();
        let need_to_remove = total_size - (70000000 - 30000000);
        *dir_sizes
            .iter()
            .filter(|&s| *s >= need_to_remove)
            .min()
            .unwrap()
    }
}

#[test]
fn example() {
    let problem = Day7::new(
        "$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k",
    );
    println!("{:#?}", problem.commands);
    assert_eq!(95437, problem.part1());
    assert_eq!(24933642, problem.part2());
}
