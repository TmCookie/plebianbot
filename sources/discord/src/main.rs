#![allow(dead_code)]
#![feature(str_escape)]
extern crate discord;

use discord::Discord;
use discord::model::Event;
use std::env;
use std::io::prelude::*;
use std::fs::File;
use std::path::Path;
use std::process::Command;


fn main() {
    // variable to store apitoken
    let mut apitoken = String::new();

    // open apitoken.txt and read its content to apitoken
    let mut file = File::open("apitoken").expect("could not open apitoken.txt");
    file.read_to_string(&mut apitoken).expect("could not read apitoken");
    apitoken.pop();

	// Log in to Discord using a bot token from the environment
    env::set_var("DISCORD_TOKEN", apitoken);
	let discord = Discord::from_bot_token(
		&env::var("DISCORD_TOKEN").expect("Expected token"),
	).expect("login failed");

	// Establish and use a websocket connection
	let (mut connection, _) = discord.connect().expect("connect failed");

	println!("Ready.");

    loop {
		match connection.recv_event() {

			Ok(Event::MessageCreate(message)) => {

                let massage: String;

                if message.content.starts_with("plz ") {
                    massage = message.content.replace("plz ", "");
                } else {
                    massage = String::from("NOP");
                }

                match massage.trim() {
                    "die" => {
                        if message.author.id.eq( &discord::model::UserId(105663166159073280) )
                        || message.author.id.eq( &discord::model::UserId(120490309246386177) ) {
                            println!("shutting down as ordered.");
                            discord.send_message(&message.channel_id, "kms", "", false)
                                .expect("failed to send self-shutdown message, this can be ignored");
                            break
                        }
                    }

                    "NOP" => {}

                    _ => {
                        match run_command(massage) {
                            Ok(v) => {
                                println!("{:?}", v);
                                discord.send_message(&message.channel_id , v.as_str(), "", false)
                                    .expect("failed to send a message to discord");
                            }

                            Err(err) => {
                                println!("{:?}", err);
                                discord.send_message(&message.channel_id, err.as_str(), "", false)
                                    .expect("failed to send an error message");
                            }
                        }
                    }
                }
            }

            Ok(_) => {}
			Err(discord::Error::Closed(code, body)) => {
				println!("Gateway closed on us with code {:?}: {}", code, body);
				break
			}
			Err(err) => { println!("Receive error: {:?}", err) }
		}
	}
}

fn run_command(input: String) -> Result<String, String> {
    let mut cli = input.split(" ");
    let command = format!("./scripts/{}",cli.nth(0).expect("cli argument not found"));
    let script_path = Path::new(&command);
    let script = File::open(&script_path);

    if script.is_ok() {
        match Command::new(&command).output() {
            Ok(v) => return Ok( String::from_utf8_lossy(&v.stdout).escape_default() ),
            Err(err) => return Err(format!("{:?}", err).escape_default())
        }
    } else {
        return Err("script does not exist".escape_default())
    }
}
