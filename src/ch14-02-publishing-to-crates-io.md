## 크레이트를 Crates.io에 게시하기

우리는 프로젝트의 의존성으로 [crates.io](https://crates.io/)<!-- ignore -->의 패키지를 사용해 왔다. 하지만 여러분도 직접 만든 패키지를 다른 사람들과 공유할 수 있다. [crates.io](https://crates.io/)<!-- ignore -->의 크레이트 레지스트리는 패키지의 소스 코드를 배포하므로, 주로 오픈 소스 코드를 호스팅한다.

Rust와 Cargo는 여러분이 게시한 패키지를 다른 사람들이 쉽게 찾고 사용할 수 있도록 돕는 다양한 기능을 제공한다. 다음으로 이러한 기능 중 몇 가지를 살펴보고, 패키지를 게시하는 방법을 설명한다.


### 유용한 문서 주석 작성하기

패키지를 정확하게 문서화하면 다른 사용자가 이를 어떻게, 언제 사용해야 하는지 쉽게 이해할 수 있다. 따라서 문서 작성에 시간을 투자할 가치가 있다. 3장에서는 두 개의 슬래시(`//`)를 사용해 Rust 코드에 주석을 다는 방법에 대해 설명했다. Rust는 또한 **문서 주석**이라는 특별한 형태의 주석을 제공한다. 이 주석은 HTML 문서를 생성하며, 패키지의 공개 API 항목에 대한 문서를 프로그래머가 쉽게 이해할 수 있도록 돕는다. 문서 주석은 패키지의 구현 방식이 아니라 **사용 방법**에 초점을 맞춘다.

문서 주석은 두 개의 슬래시 대신 세 개의 슬래시(`///`)를 사용하며, Markdown 문법을 지원해 텍스트를 서식화할 수 있다. 문서 주석은 해당 항목 바로 앞에 위치시킨다. 아래 예제는 `my_crate`라는 크레이트 내 `add_one` 함수에 대한 문서 주석을 보여준다.

<Listing number="14-1" file-name="src/lib.rs" caption="함수에 대한 문서 주석">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-01/src/lib.rs}}
```

</Listing>

여기서는 `add_one` 함수가 어떤 역할을 하는지 설명하고, `Examples`라는 섹션을 시작한 후 `add_one` 함수를 사용하는 방법을 보여주는 예제 코드를 제공한다. 이 문서 주석을 기반으로 HTML 문서를 생성하려면 `cargo doc` 명령을 실행하면 된다. 이 명령은 Rust와 함께 배포되는 `rustdoc` 도구를 실행하고, 생성된 HTML 문서를 _target/doc_ 디렉토리에 저장한다.

편의를 위해 `cargo doc --open` 명령을 실행하면 현재 크레이트의 문서(및 모든 종속성의 문서)에 대한 HTML을 빌드하고 웹 브라우저에서 결과를 열어준다. `add_one` 함수로 이동하면 문서 주석의 텍스트가 어떻게 렌더링되는지 확인할 수 있다. 아래 그림은 `add_one` 함수에 대한 HTML 문서를 보여준다.

<img alt="`my_crate`의 `add_one` 함수에 대한 렌더링된 HTML 문서" src="img/trpl14-01.png" class="center" />

<span class="caption">그림 14-1: `add_one` 함수에 대한 HTML 문서</span>


#### 자주 사용되는 섹션

Listing 14-1에서는 `# Examples` 마크다운 헤딩을 사용해 HTML에서 "Examples"라는 제목의 섹션을 만들었다. 문서화에서 크레이트 작성자들이 자주 사용하는 다른 섹션들은 다음과 같다:

- **Panics**: 문서화 중인 함수가 패닉을 일으킬 수 있는 시나리오를 설명한다. 함수를 호출하는 측에서 프로그램이 패닉을 일으키지 않도록 하려면 이러한 상황에서 함수를 호출하지 않도록 주의해야 한다.
- **Errors**: 함수가 `Result`를 반환하는 경우, 어떤 종류의 오류가 발생할 수 있는지와 어떤 조건에서 이러한 오류가 반환될 수 있는지 설명한다. 이를 통해 호출자는 다양한 종류의 오류를 다르게 처리하는 코드를 작성할 수 있다.
- **Safety**: 함수가 `unsafe`로 선언된 경우 (20장에서 안전하지 않은 코드에 대해 다룬다), 왜 이 함수가 안전하지 않은지와 함수가 호출자에게 기대하는 불변 조건(invariants)을 설명하는 섹션을 추가해야 한다.

대부분의 문서화 주석은 이러한 모든 섹션을 필요로 하지는 않지만, 이 목록은 사용자들이 알고 싶어할 코드의 다양한 측면을 상기시키는 데 유용한 체크리스트 역할을 한다.


#### 문서 주석을 테스트로 활용하기

문서 주석에 예제 코드 블록을 추가하면 라이브러리 사용법을 명확히 보여줄 수 있다. 이 방법에는 또 다른 장점이 있다. `cargo test`를 실행하면 문서에 포함된 예제 코드를 테스트로 실행한다! 예제가 포함된 문서만큼 좋은 것은 없다. 하지만 문서가 작성된 이후 코드가 변경되어 예제가 동작하지 않는다면 그만큼 나쁜 것도 없다. 리스트 14-1의 `add_one` 함수에 대한 문서를 가지고 `cargo test`를 실행하면, 테스트 결과에 다음과 같은 섹션이 나타난다:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-01/
cargo test
copy just the doc-tests section below
-->

```text
   Doc-tests my_crate

running 1 test
test src/lib.rs - add_one (line 5) ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.27s
```

이제 함수나 예제를 변경하여 예제의 `assert_eq!`가 패닉을 일으키도록 한 후 다시 `cargo test`를 실행하면, 문서 테스트가 예제와 코드가 서로 일치하지 않음을 감지한다!


#### 포함된 항목에 대한 주석 작성

`//!` 스타일의 문서 주석은 주석 뒤에 오는 항목이 아니라, 주석을 포함하는 항목에 대한 문서를 추가한다. 일반적으로 이러한 문서 주석은 크레이트 루트 파일(관례적으로 _src/lib.rs_)이나 모듈 내부에서 크레이트 또는 모듈 전체를 설명하는 데 사용한다.

예를 들어, `add_one` 함수를 포함하는 `my_crate` 크레이트의 목적을 설명하는 문서를 추가하려면, _src/lib.rs_ 파일의 시작 부분에 `//!`로 시작하는 문서 주석을 추가한다. 이는 아래 Listing 14-2와 같다:

<Listing number="14-2" file-name="src/lib.rs" caption="`my_crate` 크레이트 전체에 대한 문서">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-02/src/lib.rs:here}}
```

</Listing>

`//!`로 시작하는 마지막 줄 뒤에는 어떤 코드도 없다. `///` 대신 `//!`로 주석을 시작했기 때문에, 이 주석은 주석 뒤에 오는 항목이 아니라 주석을 포함하는 항목에 대한 문서를 작성한다. 이 경우, 그 항목은 크레이트 루트인 _src/lib.rs_ 파일이다. 이 주석들은 크레이트 전체를 설명한다.

`cargo doc --open` 명령을 실행하면, 이러한 주석은 `my_crate`의 문서 첫 페이지에 크레이트의 공개 항목 목록 위에 표시된다. 이는 Figure 14-2와 같다.

<img alt="크레이트 전체에 대한 주석이 포함된 렌더링된 HTML 문서" src="img/trpl14-02.png" class="center" />

<span class="caption">Figure 14-2: `my_crate`에 대한 렌더링된 문서, 크레이트 전체를 설명하는 주석 포함</span>

항목 내부의 문서 주석은 특히 크레이트와 모듈을 설명하는 데 유용하다. 이를 사용해 컨테이너의 전체 목적을 설명함으로써 사용자가 크레이트의 구조를 이해하는 데 도움을 줄 수 있다.


### `pub use`로 편리한 공개 API 내보내기

크레이트를 공개할 때 공개 API의 구조는 중요한 고려 사항이다. 크레이트를 사용하는 사람들은 개발자보다 모듈 구조에 덜 익숙할 수 있으며, 모듈 계층이 복잡하면 필요한 기능을 찾기 어려울 수 있다.

7장에서는 `pub` 키워드를 사용해 아이템을 공개하고, `use` 키워드로 아이템을 스코프로 가져오는 방법을 다뤘다. 하지만 개발 중에 효율적으로 느껴지는 구조가 사용자에게는 불편할 수 있다. 예를 들어, 구조체를 여러 계층으로 구성하면 특정 타입을 찾기 어려울 수 있다. 사용자가 `my_crate::some_module::another_module::UsefulType` 대신 `my_crate::UsefulType`처럼 간단하게 사용할 수 있도록 하고 싶을 것이다.

다행히 내부 구조를 재구성하지 않고도 `pub use`를 사용해 아이템을 재내보내면 공개 구조를 조정할 수 있다. *재내보내기*는 한 위치의 공개 아이템을 다른 위치에서도 공개할 수 있게 해준다. 마치 해당 아이템이 다른 위치에 정의된 것처럼 사용할 수 있다.

예를 들어, 예술 개념을 모델링하는 `art` 라이브러리를 만들었다고 가정하자. 이 라이브러리에는 두 개의 모듈이 있다: `PrimaryColor`와 `SecondaryColor` 열거형을 포함하는 `kinds` 모듈, 그리고 `mix` 함수를 포함하는 `utils` 모듈이다. 아래는 그 예제다:

<Listing number="14-3" file-name="src/lib.rs" caption="`kinds`와 `utils` 모듈로 구성된 `art` 라이브러리">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-03/src/lib.rs:here}}
```

</Listing>

그림 14-3은 `cargo doc`으로 생성된 이 크레이트의 문서 첫 페이지를 보여준다:

<img alt="`art` 크레이트의 문서 첫 페이지. `kinds`와 `utils` 모듈이 나열됨" src="img/trpl14-03.png" class="center" />

<span class="caption">그림 14-3: `art` 크레이트의 문서 첫 페이지. `kinds`와 `utils` 모듈이 나열됨</span>

`PrimaryColor`와 `SecondaryColor` 타입, 그리고 `mix` 함수는 첫 페이지에 나열되지 않는다. 이들을 보려면 `kinds`와 `utils`를 클릭해야 한다.

이 라이브러리를 사용하는 다른 크레이트는 `art`의 아이템을 스코프로 가져오기 위해 현재 정의된 모듈 구조를 지정해야 한다. 아래 예제는 `art` 크레이트의 `PrimaryColor`와 `mix`를 사용하는 크레이트를 보여준다:

<Listing number="14-4" file-name="src/main.rs" caption="`art` 크레이트의 내부 구조를 그대로 사용하는 크레이트">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-04/src/main.rs}}
```

</Listing>

`art` 크레이트를 사용하는 코드 작성자는 `PrimaryColor`가 `kinds` 모듈에 있고 `mix`가 `utils` 모듈에 있다는 것을 알아내야 했다. `art` 크레이트의 모듈 구조는 이를 개발하는 사람에게는 적합하지만, 사용자에게는 혼란을 줄 수 있다. 내부 구조는 크레이트를 사용하는 방법을 이해하는 데 도움이 되지 않으며, 사용자가 어디를 찾아야 하는지 알아내고 `use` 문에서 모듈 이름을 지정해야 하는 불편함을 초래한다.

공개 API에서 내부 구조를 제거하기 위해 `art` 크레이트 코드를 수정해 `pub use` 문을 추가하여 아이템을 최상위 수준으로 재내보낼 수 있다. 아래는 그 예제다:

<Listing number="14-5" file-name="src/lib.rs" caption="아이템을 재내보내기 위해 `pub use` 문 추가">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-05/src/lib.rs:here}}
```

</Listing>

이제 `cargo doc`으로 생성된 API 문서는 첫 페이지에 재내보낸 아이템을 나열하고 링크한다. 그림 14-4는 이를 보여준다:

<img alt="재내보낸 아이템이 첫 페이지에 나열된 `art` 크레이트의 문서" src="img/trpl14-04.png" class="center" />

<span class="caption">그림 14-4: 재내보낸 아이템이 나열된 `art` 크레이트의 문서 첫 페이지</span>

`art` 크레이트 사용자는 여전히 리스팅 14-3의 내부 구조를 사용할 수 있지만, 리스팅 14-5의 더 편리한 구조를 사용할 수도 있다. 아래 예제는 재내보낸 아이템을 사용하는 프로그램을 보여준다:

<Listing number="14-6" file-name="src/main.rs" caption="`art` 크레이트의 재내보낸 아이템을 사용하는 프로그램">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-06/src/main.rs:here}}
```

</Listing>

중첩된 모듈이 많은 경우, `pub use`로 타입을 최상위 수준으로 재내보내면 사용자 경험이 크게 개선될 수 있다. `pub use`의 또 다른 일반적인 용도는 의존성의 정의를 현재 크레이트에서 재내보내어 해당 크레이트의 정의를 공개 API의 일부로 만드는 것이다.

유용한 공개 API 구조를 만드는 것은 과학보다는 예술에 가깝다. 사용자에게 가장 적합한 API를 찾기 위해 반복 작업을 할 수 있다. `pub use`를 선택하면 내부 구조를 유연하게 구성할 수 있으며, 내부 구조와 사용자에게 보여지는 구조를 분리할 수 있다. 설치한 크레이트의 코드를 살펴보면 내부 구조와 공개 API가 어떻게 다른지 확인할 수 있다.


### Crates.io 계정 설정하기

크레이트를 배포하기 전에, 먼저 [crates.io](https://crates.io/)<!-- ignore -->에 계정을 만들고 API 토큰을 발급받아야 한다. 이를 위해 [crates.io](https://crates.io/)<!-- ignore --> 홈페이지를 방문해 GitHub 계정으로 로그인한다. (현재는 GitHub 계정이 필수지만, 추후 다른 방식의 계정 생성도 지원될 수 있다.) 로그인한 후, [https://crates.io/me/](https://crates.io/me/)<!-- ignore -->에서 계정 설정 페이지로 이동해 API 키를 확인한다. 그런 다음 `cargo login` 명령어를 실행하고, 프롬프트가 나타나면 API 키를 붙여넣는다. 예를 들면 다음과 같다:

```console
$ cargo login
abcdefghijklmnopqrstuvwxyz012345
```

이 명령어는 Cargo에게 API 토큰을 알려주고, 이를 로컬의 _~/.cargo/credentials_ 파일에 저장한다. 이 토큰은 **비밀**이기 때문에 절대 다른 사람과 공유하면 안 된다. 만약 어떤 이유로든 토큰을 공유했다면, [crates.io](https://crates.io/)<!-- ignore -->에서 토큰을 취소하고 새로운 토큰을 생성해야 한다.


### 새로운 크레이트에 메타데이터 추가하기

여러분이 배포하려는 크레이트가 있다고 가정해 보자. 배포하기 전에 크레이트의 _Cargo.toml_ 파일에 있는 `[package]` 섹션에 몇 가지 메타데이터를 추가해야 한다.

크레이트에는 고유한 이름이 필요하다. 로컬에서 작업할 때는 크레이트에 어떤 이름이든 붙일 수 있다. 하지만 [crates.io](https://crates.io/)<!-- ignore -->에 올라가는 크레이트 이름은 선착순으로 할당된다. 한 번 사용된 크레이트 이름은 다른 사람이 사용할 수 없다. 크레이트를 배포하기 전에 원하는 이름을 검색해 보자. 이미 사용된 이름이라면 다른 이름을 찾아야 하며, _Cargo.toml_ 파일의 `[package]` 섹션에 있는 `name` 필드를 새로운 이름으로 수정해야 한다. 예를 들면 다음과 같다:

<span class="filename">파일명: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
```

고유한 이름을 선택했다 하더라도, 이 상태에서 `cargo publish`를 실행해 크레이트를 배포하려고 하면 경고와 함께 에러가 발생한다:

<!-- manual-regeneration
Create a new package with an unregistered name, making no further modifications
  to the generated package, so it is missing the description and license fields.
cargo publish
copy just the relevant lines below
-->

```console
$ cargo publish
    Updating crates.io index
warning: manifest has no description, license, license-file, documentation, homepage or repository.
See https://doc.rust-lang.org/cargo/reference/manifest.html#package-metadata for more info.
--snip--
error: failed to publish to registry at https://crates.io

Caused by:
  the remote server responded with an error (status 400 Bad Request): missing or empty metadata fields: description, license. Please see https://doc.rust-lang.org/cargo/reference/manifest.html for more information on configuring these fields
```

이 에러는 중요한 정보가 누락되었기 때문에 발생한다. 크레이트의 기능과 사용 조건을 알려주기 위해 설명과 라이선스가 필요하다. _Cargo.toml_ 파일에 간단한 설명을 추가하자. 이 설명은 검색 결과에서 크레이트와 함께 표시된다. `license` 필드에는 _라이선스 식별자 값_을 입력해야 한다. [Linux Foundation의 Software Package Data Exchange (SPDX)][spdx]에서 사용할 수 있는 식별자 목록을 확인할 수 있다. 예를 들어, 크레이트에 MIT 라이선스를 적용하려면 `MIT` 식별자를 추가하면 된다:

<span class="filename">파일명: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
license = "MIT"
```

SPDX에 없는 라이선스를 사용하려면 해당 라이선스 텍스트를 파일에 저장하고, 프로젝트에 포함시킨 다음, `license` 키 대신 `license-file`을 사용해 파일명을 지정해야 한다.

프로젝트에 적합한 라이선스를 선택하는 방법은 이 책의 범위를 벗어난다. Rust 커뮤니티의 많은 사람들은 Rust와 동일한 방식으로 `MIT OR Apache-2.0` 듀얼 라이선스를 사용한다. 이 방식은 여러 라이선스를 `OR`로 구분해 지정할 수 있음을 보여준다.

고유한 이름, 버전, 설명, 라이선스를 추가한 후, 배포 준비가 된 프로젝트의 _Cargo.toml_ 파일은 다음과 같을 수 있다:

<span class="filename">파일명: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
version = "0.1.0"
edition = "2024"
description = "A fun game where you guess what number the computer has chosen."
license = "MIT OR Apache-2.0"

[dependencies]
```

[Cargo 문서](https://doc.rust-lang.org/cargo/)를 참고하면 다른 메타데이터를 지정해 크레이트를 더 쉽게 발견하고 사용할 수 있도록 하는 방법을 확인할 수 있다.


### Crates.io에 배포하기

이제 계정을 만들고 API 토큰을 저장했으며, 크레이트 이름을 정하고 필요한 메타데이터를 지정했다면, 배포할 준비가 된 것이다. 크레이트를 배포하면 특정 버전이 [crates.io](https://crates.io/)<!-- ignore -->에 업로드되어 다른 사람들이 사용할 수 있게 된다.

주의할 점은, 배포는 **영구적**이라는 것이다. 버전은 덮어쓸 수 없고, 코드도 삭제할 수 없다. [crates.io](https://crates.io/)<!-- ignore -->의 주요 목표 중 하나는 코드의 영구적인 저장소 역할을 하는 것이다. 이를 통해 [crates.io](https://crates.io/)<!-- ignore -->의 크레이트에 의존하는 모든 프로젝트의 빌드가 계속 작동할 수 있도록 한다. 버전 삭제를 허용하면 이 목표를 달성할 수 없다. 그러나 배포할 수 있는 크레이트 버전의 수에는 제한이 없다.

다시 `cargo publish` 명령어를 실행해 보자. 이제 성공할 것이다:

<!-- manual-regeneration
go to some valid crate, publish a new version
cargo publish
copy just the relevant lines below
-->

```console
$ cargo publish
    Updating crates.io index
   Packaging guessing_game v0.1.0 (file:///projects/guessing_game)
   Verifying guessing_game v0.1.0 (file:///projects/guessing_game)
   Compiling guessing_game v0.1.0
(file:///projects/guessing_game/target/package/guessing_game-0.1.0)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.19s
   Uploading guessing_game v0.1.0 (file:///projects/guessing_game)
```

축하한다! 이제 Rust 커뮤니티와 코드를 공유했으며, 누구나 쉽게 프로젝트의 의존성으로 이 크레이트를 추가할 수 있다.


### 기존 크레이트의 새 버전 출시하기

크레이트에 변경 사항을 적용하고 새 버전을 출시할 준비가 되면, _Cargo.toml_ 파일에 지정된 `version` 값을 수정하고 다시 출시한다. [시맨틱 버저닝 규칙][semver]을 참고해 변경된 내용에 맞는 적절한 다음 버전 번호를 결정한다. 그런 다음 `cargo publish` 명령어를 실행해 새 버전을 업로드한다.

<!-- Old link, do not remove -->

<a id="removing-versions-from-cratesio-with-cargo-yank"></a>


### `cargo yank`로 크레이트 버전 사용 중단하기

이전에 출시한 크레이트 버전을 완전히 삭제할 수는 없지만, 새로운 프로젝트가 해당 버전을 의존성으로 추가하지 못하도록 막을 수 있다. 크레이트 버전이 어떤 이유로든 문제가 생겼을 때 유용한 기능이다. 이런 상황에서 Cargo는 크레이트 버전을 사용 중단(yank)하는 기능을 제공한다.

버전을 사용 중단하면 새로운 프로젝트가 해당 버전을 의존성으로 추가하지 못하게 된다. 하지만 이미 해당 버전을 사용 중인 프로젝트는 계속 정상적으로 동작한다. 즉, _Cargo.lock_ 파일이 있는 모든 프로젝트는 문제 없이 동작하며, 앞으로 생성되는 _Cargo.lock_ 파일에서는 사용 중단된 버전을 사용하지 않는다.

크레이트 버전을 사용 중단하려면, 이전에 출시한 크레이트의 디렉터리에서 `cargo yank` 명령을 실행하고 사용 중단할 버전을 지정하면 된다. 예를 들어, `guessing_game` 크레이트의 1.0.1 버전을 출시했고 이를 사용 중단하려면, `guessing_game` 프로젝트 디렉터리에서 다음 명령을 실행한다:

<!-- manual-regeneration:
cargo yank carol-test --version 2.1.0
cargo yank carol-test --version 2.1.0 --undo
-->

```console
$ cargo yank --vers 1.0.1
    Updating crates.io index
        Yank guessing_game@1.0.1
```

명령에 `--undo` 옵션을 추가하면, 사용 중단을 취소하고 프로젝트가 다시 해당 버전을 의존성으로 사용할 수 있게 할 수 있다:

```console
$ cargo yank --vers 1.0.1 --undo
    Updating crates.io index
      Unyank guessing_game@1.0.1
```

사용 중단은 코드를 삭제하지 않는다. 예를 들어, 실수로 업로드한 비밀키를 삭제할 수 없다. 이런 경우에는 즉시 해당 비밀키를 재설정해야 한다.

[spdx]: http://spdx.org/licenses/
[semver]: http://semver.org/


