all : release discord

debug : c-test rust-test cs-test

release : rng

help : sources/help/src/main.rs
	cargo build --manifest-path sources/help/Cargo.toml
	cp sources/help/target/debug/help scripts/

discord : sources/discord/src/main.rs
	cargo build --manifest-path sources/discord/Cargo.toml
	cp sources/discord/target/debug/discord ./

c-test : sources/c-test.c
	clang sources/c-test.c -o scripts/c-test

trim : sources/trim.c
	clang sources/trim.c -o scripts/trim

rng : sources/rng.c
	clang sources/rng.c -o scripts/rng

rust-test : sources/rust-test.rs
	rustc sources/rust-test.rs
	mv rust-test scripts/rust-test

cs-test : cs-test.exe
cs-test.exe : sources/cs-test.cs
	mcs sources/cs-test.cs
	mv sources/cs-test.exe scripts/cs-test.exe
