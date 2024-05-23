use assert_cmd::Command;
use tempfile::TempDir;

#[test]
fn self_check() {
    let tmpdir = TempDir::new().unwrap();
    let tmpdir = tmpdir.into_path();
    let mut cmd = Command::cargo_bin("coua").unwrap();
    cmd.arg("-o")
        .arg(tmpdir)
        .arg("-s")
        .arg("ontologies/do178c/")
        .assert()
        .success();
}
