## 부록 D - 유용한 개발 도구

이 부록에서는 Rust 프로젝트에서 제공하는 유용한 개발 도구 몇 가지를 소개한다. 자동 포매팅, 경고 수정을 빠르게 적용하는 방법, 린터, 그리고 IDE와의 통합에 대해 살펴본다.


### `rustfmt`로 자동 코드 포맷팅하기

`rustfmt`는 커뮤니티에서 정한 코드 스타일에 맞게 코드를 재포맷팅하는 도구이다. 많은 협업 프로젝트에서 `rustfmt`를 사용해 Rust 코드 작성 시 스타일 논쟁을 방지한다. 모든 개발자가 이 도구를 사용해 코드를 일관된 스타일로 포맷한다.

Rust 설치 시 기본적으로 `rustfmt`가 포함되어 있으므로, 시스템에 `rustfmt`와 `cargo-fmt` 명령어가 이미 존재할 것이다. 이 두 명령어는 `rustc`와 `cargo`와 유사하게 동작한다. `rustfmt`는 세밀한 제어가 가능하고, `cargo-fmt`는 Cargo를 사용하는 프로젝트의 규칙을 이해한다. Cargo 프로젝트를 포맷하려면 다음 명령어를 실행한다:

```sh
$ cargo fmt
```

이 명령어를 실행하면 현재 크레이트의 모든 Rust 코드가 재포맷팅된다. 코드 스타일만 변경되고, 코드의 의미는 변하지 않는다.

이 명령어는 `rustfmt`와 `cargo-fmt`를 제공한다. 이는 Rust가 `rustc`와 `cargo`를 제공하는 방식과 유사하다. Cargo 프로젝트를 포맷하려면 다음 명령어를 실행한다:

```console
$ cargo fmt
```

이 명령어를 실행하면 현재 크레이트의 모든 Rust 코드가 재포맷팅된다. 코드 스타일만 변경되고, 코드의 의미는 변하지 않는다. `rustfmt`에 대한 더 자세한 정보는 [공식 문서][rustfmt]를 참고한다.

[rustfmt]: https://github.com/rust-lang/rustfmt


### `rustfix`로 코드 수정하기

`rustfix` 도구는 Rust 설치 시 함께 포함되며, 문제를 해결할 수 있는 명확한 방법이 있는 컴파일러 경고를 자동으로 수정한다. 이전에 컴파일러 경고를 본 적이 있을 것이다. 예를 들어, 다음 코드를 살펴보자:

<span class="filename">파일명: src/main.rs</span>

```rust
fn main() {
    let mut x = 42;
    println!("{x}");
}
```

여기서 변수 `x`를 가변(mutable)으로 정의했지만, 실제로는 값을 변경하지 않는다. Rust는 이에 대해 다음과 같이 경고를 표시한다:

```console
$ cargo build
   Compiling myprogram v0.1.0 (file:///projects/myprogram)
warning: variable does not need to be mutable
 --> src/main.rs:2:9
  |
2 |     let mut x = 0;
  |         ----^
  |         |
  |         help: remove this `mut`
  |
  = note: `#[warn(unused_mut)]` on by default
```

경고는 `mut` 키워드를 제거하라고 제안한다. 이 제안을 자동으로 적용하려면 `cargo fix` 명령어를 사용하면 된다:

```console
$ cargo fix
    Checking myprogram v0.1.0 (file:///projects/myprogram)
      Fixing src/main.rs (1 fix)
    Finished dev [unoptimized + debuginfo] target(s) in 0.59s
```

다시 _src/main.rs_ 파일을 확인해보면, `cargo fix`가 코드를 다음과 같이 변경한 것을 볼 수 있다:

<span class="filename">파일명: src/main.rs</span>

```rust
fn main() {
    let x = 42;
    println!("{x}");
}
```

이제 `x` 변수는 불변(immutable)이 되었고, 경고 메시지도 더 이상 나타나지 않는다.

`cargo fix` 명령어는 Rust의 다른 에디션(edition) 간에 코드를 전환할 때도 사용할 수 있다. 에디션에 대한 자세한 내용은 [부록 E][editions]에서 다룬다.


### Clippy로 더 많은 린트 적용하기

Clippy는 코드를 분석해 흔히 발생하는 실수를 잡아내고 Rust 코드를 개선할 수 있도록 도와주는 린트 도구 모음이다. Clippy는 표준 Rust 설치에 포함되어 있다.

Cargo 프로젝트에서 Clippy의 린트를 실행하려면 다음 명령어를 입력한다:

```console
$ cargo clippy
```

예를 들어, 수학 상수인 파이(π)의 근사값을 사용하는 프로그램을 작성했다고 가정해 보자:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = 3.1415;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

이 프로젝트에서 `cargo clippy`를 실행하면 다음과 같은 에러가 발생한다:

```text
error: approximate value of `f{32, 64}::consts::PI` found
 --> src/main.rs:2:13
  |
2 |     let x = 3.1415;
  |             ^^^^^^
  |
  = note: `#[deny(clippy::approx_constant)]` on by default
  = help: consider using the constant directly
  = help: for further information visit https://rust-lang.github.io/rust-clippy/master/index.html#approx_constant
```

이 에러는 Rust에서 이미 더 정확한 `PI` 상수가 정의되어 있음을 알려준다. 따라서 상수를 직접 사용하는 것이 더 정확하다. 이제 코드를 수정해 `PI` 상수를 사용하도록 변경한다. 다음 코드는 Clippy에서 에러나 경고를 발생시키지 않는다:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = std::f64::consts::PI;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

Clippy에 대한 더 많은 정보는 [공식 문서][clippy]를 참고한다.

[clippy]: https://github.com/rust-lang/rust-clippy


### `rust-analyzer`를 활용한 IDE 통합

Rust 커뮤니티는 IDE 통합을 위해 [`rust-analyzer`][rust-analyzer]<!-- ignore --> 사용을 권장한다. 이 도구는 컴파일러 중심의 유틸리티 세트로, [Language Server Protocol][lsp]<!-- ignore -->을 지원한다. 이 프로토콜은 IDE와 프로그래밍 언어가 서로 통신할 수 있도록 설계된 표준이다. 다양한 클라이언트가 `rust-analyzer`를 사용할 수 있으며, 예를 들어 [Visual Studio Code용 Rust 분석기 플러그인][vscode]이 있다.

[lsp]: http://langserver.org/
[vscode]: https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer

`rust-analyzer` 프로젝트의 [홈페이지][rust-analyzer]<!-- ignore -->를 방문해 설치 방법을 확인한 후, 사용 중인 IDE에 언어 서버 지원을 설치한다. 이를 통해 IDE는 자동 완성, 정의로 이동, 인라인 오류 표시 등의 기능을 활용할 수 있게 된다.

[rust-analyzer]: https://rust-analyzer.github.io
[editions]: appendix-05-editions.md


