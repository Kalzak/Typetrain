use std::io::{stdin, stdout, Write};

use termion::color;
use termion::event::Key;
use termion::input::TermRead;
use termion::raw::IntoRawMode;

fn main() {
    let stdin = stdin();
    let mut stdout = stdout().into_raw_mode().unwrap();

    let sentence = "Short sentence with mistakes".to_string();

    let mut error = "".to_string();
    let mut done = "".to_string();
    let mut current = 0;

    display(&mut stdout, &done, &error, &sentence);

    for c in stdin.keys() {
        match c.unwrap() {
            Key::Ctrl('c') => return,
            Key::Char(c) => {
                let current_char = sentence.chars().nth(current).unwrap();
                if current_char == c && error.is_empty() {
                    done = format!("{}{}", done, current_char);
                    current += 1;
                } else if current < sentence.len() - 1 {
                    error = format!("{}{}", error, current_char);
                    current += 1;
                }
                if current == sentence.len() && error.is_empty() {
                    print!(
                        "{}{}{}{}complete!{}{}",
                        color::Fg(color::LightGreen),
                        current_char,
                        termion::cursor::Goto(1, 2),
                        color::Fg(color::White),
                        termion::cursor::Goto(1, 3),
                        termion::cursor::SteadyBlock,
                    );
                    stdout.flush().unwrap();
                    return;
                }
            }
            Key::Backspace => {
                if current > 0
                    && (!error.is_empty() || sentence.chars().nth(current - 1).unwrap() != ' ')
                {
                    current -= 1;
                    if !error.is_empty() {
                        error.remove(error.len() - 1);
                    } else if !done.is_empty() {
                        done.remove(done.len() - 1);
                    }
                }
            }
            _ => return,
        }

        display(&mut stdout, &done, &error, &sentence[current..]);
    }
}

fn display(stdout: &mut std::io::Stdout, done: &str, error: &str, left: &str) {
    let cursor_position = done.len() + error.len() + 1;
    write!(
        stdout,
        "{}{}{}{}{}{}{}{}{}{}",
        termion::clear::All,
        termion::cursor::Goto(1, 1),
        color::Fg(color::LightGreen),
        done,
        color::Fg(color::Red),
        error,
        color::Fg(color::LightBlack),
        left,
        termion::cursor::Goto(cursor_position.try_into().unwrap(), 1),
        termion::cursor::BlinkingBar,
    )
    .unwrap();

    stdout.flush().unwrap();
}
