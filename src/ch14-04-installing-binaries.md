<!-- Old link, do not remove -->

<a id="installing-binaries-from-cratesio-with-cargo-install"></a>


## `cargo install`로 바이너리 설치하기

`cargo install` 명령어를 사용하면 로컬에서 바이너리 크레이트를 설치하고 실행할 수 있다. 이 명령어는 시스템 패키지를 대체하기 위한 것이 아니라, Rust 개발자들이 [crates.io](https://crates.io/)<!-- ignore -->에 공유된 도구를 편리하게 설치할 수 있도록 제공된다. 단, 이 명령어로는 바이너리 타겟을 가진 패키지만 설치할 수 있다. **바이너리 타겟**은 크레이트가 _src/main.rs_ 파일이나 다른 바이너리로 지정된 파일을 포함할 때 생성되는 실행 가능한 프로그램을 의미한다. 이는 독립적으로 실행할 수 없고 다른 프로그램에 포함되도록 설계된 라이브러리 타겟과는 다르다. 일반적으로 크레이트의 _README_ 파일에는 해당 크레이트가 라이브러리인지, 바이너리 타겟을 가지고 있는지, 혹은 둘 다인지에 대한 정보가 포함되어 있다.

`cargo install`로 설치된 모든 바이너리는 설치 루트의 _bin_ 폴더에 저장된다. _rustup.rs_를 사용해 Rust를 설치했고 커스텀 설정을 하지 않았다면, 이 디렉토리는 *$HOME/.cargo/bin*이 된다. `cargo install`로 설치한 프로그램을 실행하려면 이 디렉토리가 `$PATH`에 포함되어 있는지 확인해야 한다.

예를 들어, 12장에서는 파일 검색을 위한 `grep` 도구의 Rust 구현체인 `ripgrep`을 소개했다. `ripgrep`을 설치하려면 아래 명령어를 실행하면 된다:

```console
$ cargo install ripgrep
    Updating crates.io index
  Downloaded ripgrep v14.1.1
  Downloaded 1 crate (213.6 KB) in 0.40s
  Installing ripgrep v14.1.1
--snip--
   Compiling grep v0.3.2
    Finished `release` profile [optimized + debuginfo] target(s) in 6.73s
  Installing ~/.cargo/bin/rg
   Installed package `ripgrep v14.1.1` (executable `rg`)
```

출력 결과에서 마지막에서 두 번째 줄은 설치된 바이너리의 위치와 이름을 보여준다. `ripgrep`의 경우 이는 `rg`이다. 앞서 언급한 대로 설치 디렉토리가 `$PATH`에 포함되어 있다면, `rg --help`를 실행해 파일 검색을 위한 더 빠르고 Rust 스타일의 도구를 사용할 수 있다!


