## Cargo 워크스페이스

12장에서는 바이너리 크레이트와 라이브러리 크레이트를 포함하는 패키지를 만들었다. 프로젝트가 발전하면서 라이브러리 크레이트가 점점 커지고, 이를 여러 개의 라이브러리 크레이트로 나누고 싶을 수 있다. Cargo는 _워크스페이스_라는 기능을 제공하는데, 이는 함께 개발되는 여러 관련 패키지를 관리하는 데 도움을 준다.


### 워크스페이스 생성하기

_워크스페이스_는 동일한 _Cargo.lock_ 파일과 출력 디렉터리를 공유하는 패키지들의 집합이다. 이제 워크스페이스를 사용해 프로젝트를 만들어 보자. 구조에 집중하기 위해 간단한 코드를 사용할 것이다. 워크스페이스를 구성하는 방법은 여러 가지가 있지만, 여기서는 일반적으로 많이 사용되는 방식 하나를 소개한다. 워크스페이스는 하나의 바이너리와 두 개의 라이브러리로 구성된다. 주요 기능을 제공하는 바이너리는 두 라이브러리에 의존한다. 하나의 라이브러리는 `add_one` 함수를 제공하고, 다른 라이브러리는 `add_two` 함수를 제공한다. 이 세 개의 크레이트는 동일한 워크스페이스에 속한다. 먼저 워크스페이스를 위한 새 디렉터리를 생성한다:

```console
$ mkdir add
$ cd add
```

다음으로, _add_ 디렉터리 안에서 전체 워크스페이스를 설정할 _Cargo.toml_ 파일을 생성한다. 이 파일에는 `[package]` 섹션이 없다. 대신 `[workspace]` 섹션으로 시작하며, 이를 통해 워크스페이스에 멤버를 추가할 수 있다. 또한 워크스페이스에서 Cargo의 최신 리졸버 알고리즘을 사용하기 위해 `resolver`를 `"3"`으로 설정한다.

<span class="filename">파일명: Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-01-workspace/add/Cargo.toml}}
```

이제 _add_ 디렉터리 안에서 `cargo new` 명령을 실행해 `adder` 바이너리 크레이트를 생성한다:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-01-adder-crate/add
remove `members = ["adder"]` from Cargo.toml
rm -rf adder
cargo new adder
copy output below
-->

```console
$ cargo new adder
    Creating binary (application) `adder` package
      Adding `adder` as member of workspace at `file:///projects/add`
```

워크스페이스 내부에서 `cargo new`를 실행하면, 새로 생성된 패키지가 자동으로 워크스페이스 `Cargo.toml` 파일의 `[workspace]` 정의에 `members` 키로 추가된다. 다음과 같이:

```toml
{{#include ../listings/ch14-more-about-cargo/output-only-01-adder-crate/add/Cargo.toml}}
```

이 시점에서 `cargo build`를 실행해 워크스페이스를 빌드할 수 있다. _add_ 디렉터리의 파일 구조는 다음과 같다:

```text
├── Cargo.lock
├── Cargo.toml
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

워크스페이스는 최상위 레벨에 하나의 _target_ 디렉터리를 가지며, 컴파일된 결과물은 이곳에 저장된다. `adder` 패키지는 자체 _target_ 디렉터리를 갖지 않는다. _adder_ 디렉터리 내부에서 `cargo build`를 실행하더라도, 컴파일된 결과물은 _add/adder/target_이 아닌 _add/target_에 저장된다. Cargo가 워크스페이스의 _target_ 디렉터리를 이렇게 구성하는 이유는, 워크스페이스 내의 크레이트들이 서로 의존하기 때문이다. 각 크레이트가 자체 _target_ 디렉터리를 갖는다면, 각 크레이트는 워크스페이스 내 다른 크레이트들을 다시 컴파일해 자신의 _target_ 디렉터리에 결과물을 저장해야 한다. 하나의 _target_ 디렉터리를 공유함으로써, 크레이트들은 불필요한 재빌드를 피할 수 있다.


### 워크스페이스에 두 번째 패키지 생성하기

이제 워크스페이스에 새로운 멤버 패키지를 추가해보자. 이 패키지는 `add_one`이라는 이름으로 생성할 것이다. 새로운 라이브러리 크레이트를 `add_one`이라는 이름으로 생성한다:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-02-add-one/add
remove `"add_one"` from `members` list in Cargo.toml
rm -rf add_one
cargo new add_one --lib
copy output below
-->

```console
$ cargo new add_one --lib
    Creating library `add_one` package
      Adding `add_one` as member of workspace at `file:///projects/add`
```

이제 최상위 _Cargo.toml_ 파일의 `members` 목록에 _add_one_ 경로가 추가된다:

<span class="filename">파일명: Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/Cargo.toml}}
```

_add_ 디렉토리의 구조는 이제 다음과 같다:

```text
├── Cargo.lock
├── Cargo.toml
├── add_one
│   ├── Cargo.toml
│   └── src
│       └── lib.rs
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

_add_one/src/lib.rs_ 파일에 `add_one` 함수를 추가한다:

<span class="filename">파일명: add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/add_one/src/lib.rs}}
```

이제 바이너리 크레이트인 `adder`가 라이브러리 크레이트인 `add_one`에 의존하도록 설정할 수 있다. 먼저 _adder/Cargo.toml_에 `add_one`에 대한 경로 의존성을 추가한다.

<span class="filename">파일명: adder/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/adder/Cargo.toml:6:7}}
```

Cargo는 워크스페이스 내의 크레이트들이 서로 의존할 것이라고 가정하지 않으므로, 의존 관계를 명시적으로 설정해야 한다.

다음으로, `adder` 크레이트에서 `add_one` 크레이트의 `add_one` 함수를 사용해보자. _adder/src/main.rs_ 파일을 열고 `main` 함수를 수정하여 `add_one` 함수를 호출한다. 이 내용은 Listing 14-7에 나와 있다.

<Listing number="14-7" file-name="adder/src/main.rs" caption="`adder` 크레이트에서 `add_one` 라이브러리 크레이트 사용하기">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-07/add/adder/src/main.rs}}
```

</Listing>

이제 최상위 _add_ 디렉토리에서 `cargo build`를 실행하여 워크스페이스를 빌드한다!

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.22s
```

_add_ 디렉토리에서 바이너리 크레이트를 실행하려면, `cargo run` 명령어에 `-p` 인자와 패키지 이름을 지정하여 실행할 패키지를 선택한다:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo run -p adder
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo run -p adder
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running `target/debug/adder`
Hello, world! 10 plus one is 11!
```

이 명령어는 _adder/src/main.rs_의 코드를 실행하며, 이 코드는 `add_one` 크레이트에 의존한다.


#### 워크스페이스에서 외부 패키지 사용하기

워크스페이스는 각 크레이트 디렉토리마다 _Cargo.lock_ 파일을 두지 않고, 최상위 레벨에 단 하나의 _Cargo.lock_ 파일만을 갖는다. 이렇게 하면 모든 크레이트가 동일한 버전의 의존성을 사용할 수 있다. 만약 _adder/Cargo.toml_과 _add_one/Cargo.toml_ 파일에 `rand` 패키지를 추가하면, Cargo는 두 파일 모두에서 동일한 버전의 `rand`를 사용하도록 해결하고, 이를 단일 _Cargo.lock_ 파일에 기록한다. 워크스페이스 내 모든 크레이트가 동일한 의존성을 사용하면, 크레이트 간 호환성이 항상 보장된다. 이제 `add_one` 크레이트에서 `rand` 크레이트를 사용할 수 있도록 _add_one/Cargo.toml_ 파일의 `[dependencies]` 섹션에 `rand` 크레이트를 추가해 보자:

<!-- `rand` 버전을 업데이트할 때는 다음 파일에서도 동일한 버전을 사용하도록 업데이트해야 한다:
* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
-->

<span class="filename">파일명: add_one/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add/add_one/Cargo.toml:6:7}}
```

이제 _add_one/src/lib.rs_ 파일에 `use rand;`를 추가하고, _add_ 디렉토리에서 `cargo build`를 실행하면 전체 워크스페이스를 빌드할 때 `rand` 크레이트를 가져와 컴파일한다. 하지만 `rand`를 사용하지 않았기 때문에 다음과 같은 경고가 발생한다:

<!-- 수동 재생성
cd listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add
cargo build
아래 출력을 복사하세요; 출력 업데이트 스크립트는 경로의 하위 디렉토리를 제대로 처리하지 못함
-->

```console
$ cargo build
    Updating crates.io index
  Downloaded rand v0.8.5
   --snip--
   Compiling rand v0.8.5
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
warning: unused import: `rand`
 --> add_one/src/lib.rs:1:5
  |
1 | use rand;
  |     ^^^^
  |
  = note: `#[warn(unused_imports)]` on by default

warning: `add_one` (lib) generated 1 warning (run `cargo fix --lib -p add_one` to apply 1 suggestion)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.95s
```

이제 최상위 _Cargo.lock_ 파일에는 `add_one`이 `rand`에 의존한다는 정보가 포함된다. 하지만 `rand`가 워크스페이스 내 어딘가에서 사용된다고 해도, 다른 크레이트에서 `rand`를 사용하려면 해당 크레이트의 _Cargo.toml_ 파일에도 `rand`를 추가해야 한다. 예를 들어, `adder` 패키지의 _adder/src/main.rs_ 파일에 `use rand;`를 추가하면 다음과 같은 에러가 발생한다:

<!-- 수동 재생성
cd listings/ch14-more-about-cargo/output-only-03-use-rand/add
cargo build
아래 출력을 복사하세요; 출력 업데이트 스크립트는 경로의 하위 디렉토리를 제대로 처리하지 못함
-->

```console
$ cargo build
  --snip--
   Compiling adder v0.1.0 (file:///projects/add/adder)
error[E0432]: unresolved import `rand`
 --> adder/src/main.rs:2:5
  |
2 | use rand;
  |     ^^^^ no external crate `rand`
```

이 문제를 해결하려면 `adder` 패키지의 _Cargo.toml_ 파일을 수정하고, `rand`가 의존성임을 명시해야 한다. `adder` 패키지를 빌드하면 _Cargo.lock_ 파일에 `adder`의 의존성 목록에 `rand`가 추가되지만, `rand`의 추가 복사본은 다운로드되지 않는다. Cargo는 워크스페이스 내 모든 패키지의 크레이트가 `rand` 패키지를 사용할 때 동일한 버전을 사용하도록 보장한다. 이를 통해 공간을 절약하고, 워크스페이스 내 크레이트 간 호환성을 유지한다.

만약 워크스페이스 내 크레이트가 동일한 의존성의 호환되지 않는 버전을 지정하면, Cargo는 각각을 해결하되 가능한 한 적은 버전을 사용하도록 노력한다.


#### 워크스페이스에 테스트 추가하기

다음으로, `add_one` 크레이트 내부의 `add_one::add_one` 함수에 대한 테스트를 추가해 보자.

<span class="filename">파일명: add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add/add_one/src/lib.rs}}
```

이제 최상위 _add_ 디렉토리에서 `cargo test`를 실행해 보자. 이렇게 구성된 워크스페이스에서 `cargo test`를 실행하면 워크스페이스 내 모든 크레이트의 테스트가 실행된다.

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test
copy output below; the output updating script doesn't handle subdirectories in
paths properly
-->

```console
$ cargo test
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.20s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/debug/deps/adder-3a47283c568d2b6a)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

출력의 첫 번째 부분은 `add_one` 크레이트의 `it_works` 테스트가 통과했음을 보여준다. 다음 부분은 `adder` 크레이트에서 테스트가 발견되지 않았음을 나타내고, 마지막 부분은 `add_one` 크레이트에서 문서 테스트가 발견되지 않았음을 보여준다.

또한 최상위 디렉토리에서 `-p` 플래그를 사용해 특정 크레이트의 테스트만 실행할 수도 있다. 이때 테스트할 크레이트의 이름을 지정하면 된다.

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test -p add_one
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo test -p add_one
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

이 출력은 `cargo test`가 `add_one` 크레이트의 테스트만 실행했고, `adder` 크레이트의 테스트는 실행하지 않았음을 보여준다.

만약 워크스페이스 내의 크레이트를 [crates.io](https://crates.io/)에 공개하려면, 각 크레이트를 개별적으로 공개해야 한다. `cargo test`와 마찬가지로, `-p` 플래그를 사용해 특정 크레이트를 공개할 수 있다.

추가 연습으로, `add_one` 크레이트와 유사한 방식으로 `add_two` 크레이트를 이 워크스페이스에 추가해 보자!

프로젝트가 커지면 워크스페이스를 사용하는 것을 고려해 보자. 워크스페이스는 하나의 큰 코드 덩어리보다 작고 이해하기 쉬운 컴포넌트로 작업할 수 있게 해준다. 또한, 크레이트를 워크스페이스에 유지하면 동시에 변경되는 경우 크레이트 간의 조정이 더 쉬워진다.


