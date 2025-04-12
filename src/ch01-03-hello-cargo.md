## Cargo, 안녕!

Cargo는 Rust의 빌드 시스템이자 패키지 관리자다. 대부분의 Rust 개발자는 이 도구를 사용해 Rust 프로젝트를 관리한다. Cargo는 코드를 빌드하고, 코드가 의존하는 라이브러리를 다운로드하며, 해당 라이브러리를 빌드하는 등 다양한 작업을 대신 처리해준다. (코드가 필요로 하는 라이브러리를 _의존성_이라고 부른다.)

지금까지 작성한 것처럼 가장 간단한 Rust 프로그램은 의존성이 없다. 만약 "Hello, world!" 프로젝트를 Cargo로 빌드했다면, Cargo의 코드 빌드 기능만 사용했을 것이다. 더 복잡한 Rust 프로그램을 작성하게 되면 의존성을 추가하게 되는데, Cargo로 프로젝트를 시작하면 의존성을 추가하는 작업이 훨씬 쉬워진다.

대부분의 Rust 프로젝트가 Cargo를 사용하기 때문에, 이 책의 나머지 부분도 여러분이 Cargo를 사용한다고 가정한다. [설치][installation]<!-- ignore --> 섹션에서 설명한 공식 설치 프로그램을 사용했다면, Rust와 함께 Cargo도 설치되어 있을 것이다. 다른 방법으로 Rust를 설치했다면, 터미널에 다음 명령어를 입력해 Cargo가 설치되어 있는지 확인해보자.

```console
$ cargo --version
```

버전 번호가 표시된다면 Cargo가 설치된 것이다. 만약 `command not found` 같은 오류가 발생한다면, 설치 방법에 대한 문서를 참고해 Cargo를 별도로 설치해야 한다.


### Cargo를 사용해 프로젝트 생성하기

Cargo를 사용해 새로운 프로젝트를 생성하고, 이전에 만든 "Hello, world!" 프로젝트와 어떻게 다른지 살펴보자. 먼저 _projects_ 디렉토리로 이동하거나 코드를 저장할 위치로 이동한다. 그런 다음, 운영체제에 상관없이 다음 명령어를 실행한다:

```console
$ cargo new hello_cargo
$ cd hello_cargo
```

첫 번째 명령어는 _hello_cargo_라는 이름의 새 디렉토리와 프로젝트를 생성한다. 프로젝트 이름을 _hello_cargo_로 지정했으므로, Cargo는 동일한 이름의 디렉토리에 파일을 생성한다.

_hello_cargo_ 디렉토리로 이동해 파일 목록을 확인해 보면, Cargo가 두 개의 파일과 하나의 디렉토리를 생성한 것을 볼 수 있다. _Cargo.toml_ 파일과 _src_ 디렉토리, 그리고 그 안에 있는 _main.rs_ 파일이 생성된다.

또한 Cargo는 새로운 Git 저장소와 _.gitignore_ 파일도 함께 초기화한다. 이미 Git 저장소 내에서 `cargo new`를 실행하면 Git 파일은 생성되지 않지만, `cargo new --vcs=git` 명령어를 사용해 이 동작을 재정의할 수 있다.

> 참고: Git은 일반적으로 사용되는 버전 관리 시스템이다. `--vcs` 플래그를 사용해 `cargo new`가 다른 버전 관리 시스템을 사용하도록 설정하거나 버전 관리를 사용하지 않도록 설정할 수 있다. `cargo new --help`를 실행해 사용 가능한 옵션을 확인할 수 있다.

선택한 텍스트 편집기로 _Cargo.toml_ 파일을 열어보자. Listing 1-2의 코드와 비슷한 내용이 보일 것이다.

<Listing number="1-2" file-name="Cargo.toml" caption="`cargo new`로 생성된 *Cargo.toml* 파일 내용">

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

</Listing>

이 파일은 [TOML][toml]<!-- ignore --> (_Tom’s Obvious, Minimal Language_) 형식으로 작성되었으며, Cargo의 설정 파일 형식이다.

첫 번째 줄인 `[package]`는 이어지는 내용이 패키지 설정임을 나타내는 섹션 헤더다. 이 파일에 더 많은 정보를 추가할 때, 다른 섹션도 추가할 것이다.

다음 세 줄은 Cargo가 프로그램을 컴파일하는 데 필요한 설정 정보를 지정한다: 프로젝트 이름, 버전, 사용할 Rust 버전이다. `edition` 키에 대해서는 [부록 E][appendix-e]<!-- ignore -->에서 다룰 것이다.

마지막 줄인 `[dependencies]`는 프로젝트의 의존성을 나열하는 섹션의 시작이다. Rust에서는 코드 패키지를 _크레이트(crate)_라고 부른다. 이 프로젝트에서는 다른 크레이트가 필요하지 않지만, 2장의 첫 번째 프로젝트에서는 필요하므로 그때 이 의존성 섹션을 사용할 것이다.

이제 _src/main.rs_ 파일을 열어보자:

<span class="filename">파일명: src/main.rs</span>

```rust
fn main() {
    println!("Hello, world!");
}
```

Cargo가 Listing 1-1에서 작성한 것과 동일한 "Hello, world!" 프로그램을 생성했다! 지금까지 우리가 만든 프로젝트와 Cargo가 생성한 프로젝트의 차이점은 Cargo가 코드를 _src_ 디렉토리에 배치하고 최상위 디렉토리에 _Cargo.toml_ 설정 파일을 생성했다는 점이다.

Cargo는 소스 파일이 _src_ 디렉토리에 위치할 것으로 기대한다. 최상위 프로젝트 디렉토리는 README 파일, 라이선스 정보, 설정 파일 등 코드와 직접 관련 없는 파일을 위한 공간이다. Cargo를 사용하면 프로젝트를 체계적으로 관리할 수 있다. 모든 것이 제자리에 있고, 각자 할 일을 분명히 할 수 있다.

Cargo를 사용하지 않고 프로젝트를 시작했다면, "Hello, world!" 프로젝트에서 그랬듯이 Cargo를 사용하는 프로젝트로 변환할 수 있다. 프로젝트 코드를 _src_ 디렉토리로 이동하고 적절한 _Cargo.toml_ 파일을 생성하면 된다. _Cargo.toml_ 파일을 쉽게 생성하려면 `cargo init` 명령어를 실행하면 자동으로 파일이 생성된다.


### Cargo 프로젝트 빌드와 실행

이제 Cargo를 사용해 "Hello, world!" 프로그램을 빌드하고 실행하는 과정을 살펴보자. _hello_cargo_ 디렉터리에서 다음 명령어를 입력해 프로젝트를 빌드한다:

```console
$ cargo build
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 2.85 secs
```

이 명령어는 현재 디렉터리가 아닌 _target/debug/hello_cargo_ (또는 윈도우에서는 _target\debug\hello_cargo.exe_)에 실행 파일을 생성한다. 기본적으로 디버그 빌드를 수행하기 때문에, Cargo는 바이너리 파일을 _debug_라는 디렉터리에 저장한다. 이 실행 파일은 다음 명령어로 실행할 수 있다:

```console
$ ./target/debug/hello_cargo # or .\target\debug\hello_cargo.exe on Windows
Hello, world!
```

모든 것이 정상적으로 진행되었다면, 터미널에 `Hello, world!`가 출력된다. `cargo build`를 처음 실행하면, Cargo는 최상위 디렉터리에 _Cargo.lock_ 파일을 생성한다. 이 파일은 프로젝트의 의존성 버전을 정확히 기록한다. 현재 프로젝트에는 의존성이 없기 때문에 파일 내용이 간단하다. 이 파일은 수동으로 수정할 필요가 없으며, Cargo가 자동으로 관리한다.

지금까지 `cargo build`로 프로젝트를 빌드하고 `./target/debug/hello_cargo`로 실행했지만, `cargo run`을 사용하면 코드를 컴파일한 후 실행 파일을 한 번에 실행할 수 있다:

```console
$ cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

`cargo run`은 `cargo build`를 실행한 후 바이너리 파일의 전체 경로를 기억할 필요 없이 편리하게 사용할 수 있기 때문에, 대부분의 개발자가 이 명령어를 선호한다.

이번에는 Cargo가 `hello_cargo`를 컴파일했다는 출력이 보이지 않는다. Cargo는 파일이 변경되지 않았다는 것을 감지하고, 다시 빌드하지 않고 바이너리 파일만 실행했다. 만약 소스 코드를 수정했다면, Cargo는 실행 전에 프로젝트를 다시 빌드하고 다음과 같은 출력을 보여줬을 것이다:

```console
$ cargo run
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.33 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

Cargo는 `cargo check`라는 명령어도 제공한다. 이 명령어는 코드가 컴파일되는지 빠르게 확인하지만, 실행 파일은 생성하지 않는다:

```console
$ cargo check
   Checking hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.32 secs
```

왜 실행 파일을 생성하지 않을까? `cargo check`는 실행 파일을 생성하는 단계를 건너뛰기 때문에 `cargo build`보다 훨씬 빠르다. 코드를 작성하면서 지속적으로 작업을 확인할 때 `cargo check`를 사용하면 프로젝트가 여전히 컴파일되는지 빠르게 확인할 수 있다. 따라서 많은 Rust 개발자는 코드를 작성하면서 주기적으로 `cargo check`를 실행하고, 실행 파일을 사용할 준비가 되면 `cargo build`를 실행한다.

지금까지 Cargo에 대해 배운 내용을 정리해 보자:

- `cargo new`로 프로젝트를 생성할 수 있다.
- `cargo build`로 프로젝트를 빌드할 수 있다.
- `cargo run`으로 한 번에 프로젝트를 빌드하고 실행할 수 있다.
- `cargo check`로 바이너리 파일을 생성하지 않고 오류를 확인할 수 있다.
- 빌드 결과를 코드와 같은 디렉터리에 저장하지 않고 _target/debug_ 디렉터리에 저장한다.

Cargo를 사용하는 또 다른 장점은 운영체제에 상관없이 동일한 명령어를 사용할 수 있다는 것이다. 따라서 이제부터는 리눅스, macOS, 윈도우에 대한 별도의 지침을 제공하지 않는다.


### 릴리즈 빌드하기

프로젝트가 마침내 릴리즈 준비가 되면, `cargo build --release` 명령어를 사용해 최적화된 상태로 컴파일할 수 있다. 이 명령어는 _target/debug_ 대신 _target/release_ 디렉터리에 실행 파일을 생성한다. 최적화는 Rust 코드를 더 빠르게 실행할 수 있게 해주지만, 컴파일 시간이 길어지는 단점이 있다. 이 때문에 두 가지 프로파일이 존재한다: 하나는 빠르고 자주 다시 빌드해야 하는 개발 단계를 위한 것이고, 다른 하나는 반복적으로 다시 빌드할 필요가 없고 가능한 한 빠르게 실행되어야 하는 최종 프로그램을 위한 것이다. 코드의 실행 시간을 벤치마킹할 때는 반드시 `cargo build --release`를 실행하고 _target/release_ 디렉터리의 실행 파일로 벤치마크를 진행해야 한다.


### Cargo의 관례

간단한 프로젝트에서는 `rustc`를 직접 사용하는 것에 비해 Cargo가 제공하는 가치가 크지 않다. 하지만 프로그램이 복잡해지면 Cargo의 진가를 발휘한다. 프로그램이 여러 파일로 구성되거나 의존성이 필요한 경우, Cargo가 빌드를 조율하는 것이 훨씬 편리하다.

`hello_cargo` 프로젝트는 단순하지만, 앞으로 Rust 개발 과정에서 사용할 실제 도구의 대부분을 이미 활용하고 있다. 기존 프로젝트를 작업하려면 다음 명령어를 사용해 코드를 체크아웃하고, 프로젝트 디렉토리로 이동한 뒤 빌드할 수 있다.

```console
$ git clone example.org/someproject
$ cd someproject
$ cargo build
```

Cargo에 대한 더 자세한 정보는 [공식 문서][cargo]를 참고한다.

<!-- Links -->
[cargo]: https://doc.rust-lang.org/cargo/


## 요약

여러분은 이미 러스트 여정에서 좋은 시작을 했다! 이번 장에서 다음 내용을 배웠다:

- `rustup`을 사용해 최신 안정 버전의 러스트를 설치하는 방법
- 더 새로운 러스트 버전으로 업데이트하는 방법
- 로컬에 설치된 문서를 여는 방법
- `rustc`를 직접 사용해 "Hello, world!" 프로그램을 작성하고 실행하는 방법
- Cargo의 규칙을 따라 새 프로젝트를 만들고 실행하는 방법

이제 러스트 코드를 읽고 쓰는 데 익숙해지기 위해 더 큰 프로그램을 만들어 볼 좋은 시기다. 따라서 2장에서는 숫자 맞추기 게임 프로그램을 만들어 볼 것이다. 만약 일반적인 프로그래밍 개념이 러스트에서 어떻게 동작하는지 먼저 배우고 싶다면 3장을 먼저 보고 2장으로 돌아오길 바란다.

[installation]: ch01-01-installation.html#installation
[toml]: https://toml.io
[appendix-e]: appendix-05-editions.html
[cargo]: https://doc.rust-lang.org/cargo/


