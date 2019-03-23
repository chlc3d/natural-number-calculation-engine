mod nnce_parser;
mod nnce_interpreter;
use std::env;
extern crate regex;

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut program = nnce_parser::parse(match args.len() { 0...1 => "./cat.nnce", _ => &args[1] },
                                        nnce_parser::Features { symbols: true});
    println!("{:?}", program);
    println!("{:?}", nnce_interpreter::run(&mut program, "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+."));
    
}