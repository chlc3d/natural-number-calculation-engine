use std::fs;
use std::vec::Vec;
use std::str::FromStr;
use regex::Regex;

#[derive(Debug)]
pub enum MemoryCell {
    INCR,
    DECR,
    WRIT,
    READ,
    COPY,
    GOTO,
    Number(u64),
}

pub enum ParseCommandStatus {
    Error,
    EmptyLine,
 }

impl FromStr for MemoryCell {
    type Err = ParseCommandStatus;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        
        

    //     	String of form (\s*((Command|Number)?(#.*)?)\s*\n)*
	// Command = INCR|DECR|WRIT|READ|COPY|GOTO
	// Number = \d+

        let r = Regex::new(r"^\s*((INCR|DECR|WRIT|READ|COPY|GOTO)|(\d+))\s*(#.*)?$").unwrap();
        match r.captures(s) {
            Some(mat) => {
                if  mat.get(2).is_some() {
                    match &mat[2] {
                        "INCR" => Ok(MemoryCell::INCR),
                        "DECR" => Ok(MemoryCell::DECR),
                        "WRIT" => Ok(MemoryCell::WRIT),
                        "READ" => Ok(MemoryCell::READ),
                        "COPY" => Ok(MemoryCell::COPY),
                        "GOTO" => Ok(MemoryCell::GOTO),
                        _ => Err(ParseCommandStatus {})
                    }
                } else if mat.get(3).is_some() {
                    match u64::from_str(&mat[3]) {
                        Ok(v) => Ok(MemoryCell::Number(v)),
                        _ => Err(ParseCommandStatus {})   
                    }
                } else {
                    Err(ParseCommandStatus {})
                }
            },
            None => {
                Err(ParseCommandStatus {} )
            }
        }
        // let s = r.captures(s).map(|mat| {
        //     &mat[2]
        // });




        // Ok(MemoryCell::INCR);
        // let coords: Vec<&str> = s.trim_matches(|p| p == '(' || p == ')' )
        //                          .split(',')
        //                          .collect();

        // let x_fromstr = coords[0].parse::<i32>()?;
        // let y_fromstr = coords[1].parse::<i32>()?;

        // Ok(Point { x: x_fromstr, y: y_fromstr })
    }
}

#[derive(Debug)]
pub struct IRState {
    pub memory: Vec<MemoryCell>,
}

pub fn parse(path: &str) -> IRState {
    let program = fs::read_to_string(path).expect("oh no!");

    let mut mem: Vec<MemoryCell>=  Vec::new();
    let mut pc = 0;
    for line in program.split('\n') {
        match MemoryCell::from_str(line) {
            Ok(cell) => {
                mem.push(cell);
                pc += 1;
            },
            Err(_) => {}
        };
    }

    IRState { memory: mem}
}