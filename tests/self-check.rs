use assert_cmd::Command;
use tempfile::TempDir;

#[test]
fn self_check() {
    let tmpdir = TempDir::new().unwrap();
    let mut cmd = Command::cargo_bin("coua").unwrap();
    cmd.arg("-o").arg(tmpdir.into_path()).assert().success();
}
