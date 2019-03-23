use std::fs;
use std::vec::Vec;
use std::str::FromStr;
use std::collections::HashMap;
use regex::Regex;

#[derive(Debug, Clone)]
pub enum ParseStatus {
    InvalidCommand(String),
    InvalidAddress(String),
    InvalidAddressLiteral(usize),
    EmptyLine,
    InternalError,
 }

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MemoryCell {
    INCR,
    DECR,
    WRIT,
    READ,
    COPY,
    GOTO,
    Number(u32),
}
impl MemoryCell {
    pub fn as_num(&self) -> Option<u32> {
        match *self {
            MemoryCell::Number(n) => {Some(n)},
            _ => { None }
        }
    }

    pub fn update_if_num(self, amt: i32) -> Self {
        match self {

            MemoryCell::Number(n) => {MemoryCell::Number((n as i32  + amt) as u32)},
            _ => { self }
        }
    }
}

impl FromStr for MemoryCell {
    type Err = ParseStatus;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
    //     	String of form (\s*((Command|Number)?(#.*)?)\s*\n)*
	// Command = INCR|DECR|WRIT|READ|COPY|GOTO
	// Number = \d+

        let r = Regex::new(r"((INCR|DECR|WRIT|READ|COPY|GOTO)|(\d+))$").unwrap();
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
                        _ => Err(ParseStatus::InternalError)
                    }
                } else if mat.get(3).is_some() {
                    match u32::from_str(&mat[3]) {
                        Ok(v) => Ok(MemoryCell::Number(v)),
                        _ => Err(ParseStatus::InternalError)   
                    }
                } else {
                    Err(ParseStatus::InternalError)
                }
            },
            None => {
                Err(ParseStatus::InvalidCommand(String::from(s)))
            }
        }
    }
}

enum Address {
    Number(usize),
    Variable(String),
}

struct SymTab {
    table: HashMap<String, usize>,
    references: HashMap<usize, String>
}

#[derive(Debug)]
pub struct IRState {
    pub memory: Vec<MemoryCell>,
}

pub struct Features {
    pub symbols: bool
}

pub fn parse(path: &str, features: Features) -> IRState {
    let program = fs::read_to_string(path).expect("oh no!");

    let mut mem: Vec<MemoryCell>=  Vec::new();
    let mut symtab = SymTab { table: HashMap::new(), references: HashMap::new() };
    for line in program.lines() {
        let line_impl = line.split('#').next().unwrap();
        
        let mut line_impl_parts = line_impl.split('$');
        let line_command: &str = line_impl_parts.next().unwrap().trim();
        let line_address = line_impl_parts.next();

        let address = match line_address {
            Some(addr) => {
                match usize::from_str(addr) {
                    Ok(u_addr) => {
                        Ok(Address::Number(u_addr))
                    },
                    Err(_) => {
                        let addr_str = String::from(addr);
                        if features.symbols { Ok(Address::Variable(addr_str.trim().to_string())) } else { Err(ParseStatus::InvalidAddress(addr_str)) }
                    }
                }                
            },
            _ => { Err(ParseStatus::EmptyLine)}
        };
        match address {
            Ok(Address::Variable(v)) => {
                symtab.table.insert(v, mem.len());
            },
            Ok(Address::Number(n)) => {
                if n >= mem.len() {
                    mem.resize(n, MemoryCell::Number(0));
                } else {
                    println!("{:?}", ParseStatus::InvalidAddressLiteral(n));
                }

            },
            Err(ParseStatus::EmptyLine) => { },
            Err(e) => {println!("{:?}", e)}
        }

        if !line_command.is_empty() {
            if features.symbols && line_command.starts_with("^") {
                symtab.references.insert(mem.len(), String::from(&line_command[1..]));
                mem.push(MemoryCell::Number(0)) // placeholder
            } else {
                match MemoryCell::from_str(line_command) {
                    Ok(cell) => {
                        mem.push(cell);
                    },
                    Err(e) => {println!("{:?}", e)
                }
            };
            }
        }

    }

    if features.symbols {
        for (line, variable) in symtab.references {
            mem[line] = match symtab.table.get(&variable) {
                Some(addr) => {
                    MemoryCell::Number(*addr as u32)
                },
                _ => {
                    println!("{}", variable);
                    MemoryCell::Number(1000)
                }
            };
        }
        println!("{:?}", symtab.table);
    }

    IRState { memory: mem}
}