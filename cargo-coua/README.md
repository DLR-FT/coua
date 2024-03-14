# cargo-coua

Runs Coua checks in your Rust project.

```sh
cargo run cargo-coua --output coua.json
# or if installed as `cargo-coua`
cargo coua --output coua.json
```

The result is written to `target/coua_trace.json`.

cargo-coua uses the unstable [register_tool](https://doc.rust-lang.org/unstable-book/language-features/register-tool.html) feature of rustc.
In the target's main file (e.g. `src/lib.rs`) add:

```rust
#![feature(register_tool)]
#![register_tool(coua)]
```

Then annotate any tests that should trace to requirements using the `coua::trace` attribute, where `ReqXX` is your requirement identifier.

```rust
#[coua::trace = "ReqXX"]
#[test]
fn my_test() {
  // ...
}
```

## Features

- [X] Extract a list of traced requirements with spans and test case names from checked project
- [ ] Use list to check if all requirements from `requirements.toml` are traced by at least one test case
