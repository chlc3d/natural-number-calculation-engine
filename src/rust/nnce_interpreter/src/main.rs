mod nnce_parser;
extern crate regex;

fn main() {
    let f = nnce_parser::MemoryCell::INCR;
    let y = nnce_parser::MemoryCell::Number(40);
    println!("{:?}",f);
    println!("{:?}",y);
    println!("Hello, world!");
    println!("{:?}", nnce_parser::parse("./cat.nnce"));
    
}