use std::fs;

fn main() {
    let paths = fs::read_dir("./scripts/").unwrap();

    for path in paths {
        println!("Name: {}", path.unwrap().path().display())
    }
}
