
use crate::nnce_parser::IRState;
use crate::nnce_parser::MemoryCell;

pub enum InterpretErr {

}

pub fn run(program: &mut IRState, input: &str) -> String {
    let mut pc = 0;
    let mut output = String::new();
    let mut input_idx: usize = 0;
    let len = program.memory.len();
    let mem = &mut program.memory;

    while pc < len - 1 {

        let next = mem[pc+1];
        println!("{:?}: {:?}", pc, mem[pc]);
        mem[pc+1] = match mem[pc] {
                   MemoryCell::INCR => { next.update_if_num(1) },
                   MemoryCell::DECR => { 
                       if next == MemoryCell::Number(0) { next }
                                else { next.update_if_num(-1) }
                   },
                   MemoryCell::READ => {
                            
                            input.chars().nth(input_idx).and_then(|chr| {
                                input_idx += 1;
                                Some(MemoryCell::Number(chr as u32))
                            }).unwrap_or(MemoryCell::Number(0))
                        },
                    _ => next
        };
        if mem[pc] == MemoryCell::COPY {
            let (src, dest) = match (next, mem.get(pc+2)) {
                (MemoryCell::Number(src), Some(MemoryCell::Number(dest))) => {
                    if (*dest as usize) < len && (src as usize) < len {
                        (src as usize, *dest as usize)
                    }
                    else {
                        (0,0)
                    }
                },
                _ => { 
                    (0, 0)
                }
            };

            mem[dest] = mem[src];
        };
        if mem[pc] == MemoryCell::WRIT {
            println!("{:?}: {:?}", pc, mem[pc]);
            let next_num = next.as_num();
            if next_num.is_some() {
                output.push(next_num.unwrap() as u8 as char);
            }
        }

        pc = match mem[pc] { 
            MemoryCell::GOTO => { println!("{:?}:", next.as_num()); next.as_num().unwrap_or_default() as usize},
            MemoryCell::DECR => { 
                if next == MemoryCell::Number(0) { 98 }
                        else { pc + 1 }
            },           
            _ => { pc + 1 }
        };



    }

    return output;
}