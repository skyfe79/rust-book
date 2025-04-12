# 숫자 맞추기 게임 프로그래밍

이제 실습 프로젝트를 통해 Rust 프로그래밍을 시작해보자! 이 장에서는 실제 프로그램을 작성하면서 Rust의 몇 가지 기본 개념을 소개한다. `let`, `match`, 메서드, 연관 함수, 외부 크레이트 등을 배우게 될 것이다. 이후 장에서 이 개념들을 더 깊이 있게 다룰 예정이지만, 이 장에서는 기본적인 사용법을 연습한다.

클래식한 초보자용 프로그래밍 문제인 숫자 맞추기 게임을 구현해볼 것이다. 게임의 규칙은 다음과 같다: 프로그램은 1부터 100 사이의 임의의 정수를 생성한다. 그런 다음 플레이어에게 숫자를 입력하라는 메시지를 표시한다. 플레이어가 숫자를 입력하면, 프로그램은 입력한 숫자가 너무 작은지, 너무 큰지, 아니면 정답인지를 알려준다. 정답을 맞추면 축하 메시지를 출력하고 게임을 종료한다.


## 새 프로젝트 설정하기

새 프로젝트를 설정하려면 1장에서 만든 _projects_ 디렉터리로 이동한 후, Cargo를 사용해 새 프로젝트를 생성한다. 다음과 같이 입력하면 된다:

```console
$ cargo new guessing_game
$ cd guessing_game
```

첫 번째 명령어인 `cargo new`는 프로젝트 이름(`guessing_game`)을 첫 번째 인자로 받는다. 두 번째 명령어는 새 프로젝트의 디렉터리로 이동한다.

생성된 _Cargo.toml_ 파일을 확인해 보자:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial
rm -rf no-listing-01-cargo-new
cargo new no-listing-01-cargo-new --name guessing_game
cd no-listing-01-cargo-new
cargo run > output.txt 2>&1
cd ../../..
-->

<span class="filename">Filename: Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/Cargo.toml}}
```

1장에서 보았듯이, `cargo new`는 "Hello, world!" 프로그램을 자동으로 생성한다. _src/main.rs_ 파일을 확인해 보자:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/src/main.rs}}
```

이제 이 "Hello, world!" 프로그램을 컴파일하고 실행해 보자. `cargo run` 명령어를 사용하면 한 번에 컴파일과 실행을 수행할 수 있다:

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/output.txt}}
```

`run` 명령어는 프로젝트를 빠르게 반복적으로 수정하고 테스트할 때 유용하다. 이 게임을 개발하면서 각 단계를 빠르게 테스트할 때 이 명령어를 활용할 것이다.

_src/main.rs_ 파일을 다시 열어 보자. 이 파일에 모든 코드를 작성할 예정이다.


## 추측값 처리하기

추측 게임 프로그램의 첫 번째 부분은 사용자 입력을 받고, 그 입력을 처리하며, 입력이 예상된 형식인지 확인한다. 먼저 플레이어가 추측값을 입력할 수 있도록 한다. _src/main.rs_ 파일에 리스트 2-1의 코드를 입력한다.

<Listing number="2-1" file-name="src/main.rs" caption="사용자로부터 추측값을 받아 출력하는 코드">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:all}}
```

</Listing>

이 코드는 많은 정보를 담고 있으므로 한 줄씩 살펴보자. 사용자 입력을 받고 그 결과를 출력하기 위해 `io` 입출력 라이브러리를 스코프로 가져와야 한다. `io` 라이브러리는 `std`로 알려진 표준 라이브러리에서 제공된다:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:io}}
```

기본적으로 Rust는 모든 프로그램의 스코프에 자동으로 포함되는 표준 라이브러리의 항목 집합을 가지고 있다. 이 집합을 _프렐루드(prelude)_ 라고 하며, [표준 라이브러리 문서][prelude]에서 모든 내용을 확인할 수 있다.

사용하려는 타입이 프렐루드에 포함되지 않았다면, `use` 문을 사용해 명시적으로 스코프로 가져와야 한다. `std::io` 라이브러리를 사용하면 사용자 입력을 받는 기능을 포함해 여러 유용한 기능을 활용할 수 있다.

1장에서 보았듯이, `main` 함수는 프로그램의 진입점이다:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:main}}
```

`fn` 구문은 새로운 함수를 선언한다. 괄호 `()`는 매개변수가 없음을 나타내고, 중괄호 `{`는 함수의 본문을 시작한다.

1장에서 배웠듯이, `println!`은 문자열을 화면에 출력하는 매크로이다:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print}}
```

이 코드는 게임이 무엇인지 설명하는 프롬프트를 출력하고 사용자로부터 입력을 요청한다.


### 변수를 사용해 값 저장하기

다음으로, 사용자 입력을 저장할 _변수_를 생성한다. 예시는 다음과 같다:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:string}}
```

이제 프로그램이 점점 흥미로워진다! 이 짧은 한 줄에 많은 일이 벌어진다. `let` 문을 사용해 변수를 생성한다. 또 다른 예시를 살펴보자:

```rust,ignore
let apples = 5;
```

이 코드는 `apples`라는 새 변수를 생성하고 값 5를 바인딩한다. Rust에서 변수는 기본적으로 불변이다. 즉, 변수에 값을 할당하면 그 값은 변경되지 않는다. 이 개념은 3장의 [“변수와 가변성”][variables-and-mutability]<!-- ignore --> 섹션에서 자세히 다룬다. 변수를 가변으로 만들려면 변수 이름 앞에 `mut`를 추가한다:

```rust,ignore
let apples = 5; // 불변
let mut bananas = 5; // 가변
```

> 참고: `//` 구문은 줄 끝까지 주석을 시작한다. Rust는 주석 내의 모든 내용을 무시한다. 주석에 대해 더 자세히 알아보려면 [3장][comments]<!-- ignore -->을 참고한다.

추측 게임 프로그램으로 돌아가서, `let mut guess`는 `guess`라는 가변 변수를 생성한다는 것을 이제 알 수 있다. 등호(`=`)는 Rust에게 변수에 무언가를 바인딩하겠다는 것을 알린다. 등호 오른쪽에는 `guess`가 바인딩될 값이 위치하며, 이 값은 `String::new` 함수를 호출한 결과다. `String::new`는 새로운 `String` 인스턴스를 반환하는 함수다. [`String`][string]<!-- ignore -->은 표준 라이브러리에서 제공하는 문자열 타입으로, UTF-8로 인코딩된 확장 가능한 텍스트다.

`::new` 줄의 `::` 구문은 `new`가 `String` 타입의 연관 함수임을 나타낸다. _연관 함수_는 특정 타입에 구현된 함수를 말하며, 여기서는 `String` 타입에 해당한다. 이 `new` 함수는 새로운 빈 문자열을 생성한다. 많은 타입에서 `new` 함수를 찾을 수 있는데, 이는 특정 종류의 새 값을 만드는 함수의 일반적인 이름이기 때문이다.

종합하면, `let mut guess = String::new();` 줄은 현재 새로운 빈 `String` 인스턴스에 바인딩된 가변 변수를 생성한다. 휴!


### 사용자 입력 받기

프로그램의 첫 줄에서 `use std::io;`를 통해 표준 라이브러리의 입출력 기능을 포함했다. 이제 `io` 모듈의 `stdin` 함수를 호출해 사용자 입력을 처리할 수 있다:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:read}}
```

만약 프로그램 시작 부분에서 `use std::io;`로 `io` 모듈을 임포트하지 않았다면, 이 함수 호출을 `std::io::stdin`으로 작성해도 동일하게 사용할 수 있다. `stdin` 함수는 [`std::io::Stdin`][iostdin]<!-- ignore --> 타입의 인스턴스를 반환한다. 이 타입은 터미널의 표준 입력을 나타내는 핸들이다.

다음으로 `.read_line(&mut guess)`는 표준 입력 핸들에서 [`read_line`][read_line]<!-- ignore --> 메서드를 호출해 사용자 입력을 받는다. `read_line`에 `&mut guess`를 인자로 전달해 사용자 입력을 저장할 문자열을 지정한다. `read_line`의 역할은 사용자가 표준 입력에 입력한 내용을 문자열에 추가하는 것이다(기존 내용을 덮어쓰지 않음). 따라서 문자열을 인자로 전달한다. 이 문자열 인자는 변경 가능해야 하므로 `mut` 키워드를 사용한다.

`&`는 이 인자가 _참조_임을 나타낸다. 참조는 코드의 여러 부분이 데이터를 여러 번 복사하지 않고도 동일한 데이터에 접근할 수 있게 해준다. 참조는 복잡한 기능이지만, Rust의 주요 장점 중 하나는 참조를 안전하고 쉽게 사용할 수 있다는 점이다. 이 프로그램을 완성하기 위해 참조에 대한 모든 세부 사항을 알 필요는 없다. 지금은 변수와 마찬가지로 참조도 기본적으로 불변(immutable)이라는 점만 알아두면 된다. 따라서 변경 가능한 참조를 만들기 위해 `&guess` 대신 `&mut guess`를 작성해야 한다. (참조에 대한 자세한 내용은 4장에서 다룬다.)

<!-- Old heading. Do not remove or links may break. -->

<a id="handling-potential-failure-with-the-result-type"></a>


### `Result`를 사용해 실패 가능성 처리하기

여전히 이 코드 라인을 다루고 있다. 세 번째 텍스트 라인에 대해 논의하고 있지만, 여전히 단일 논리적 코드 라인의 일부임을 기억하자. 다음 부분은 이 메서드다:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:expect}}
```

이 코드를 다음과 같이 작성할 수도 있다:

```rust,ignore
io::stdin().read_line(&mut guess).expect("Failed to read line");
```

하지만 한 줄로 길게 작성하면 가독성이 떨어지므로, 보통은 `.method_name()` 구문을 사용해 메서드를 호출할 때 긴 라인을 나누기 위해 개행과 공백을 추가하는 것이 좋다. 이제 이 라인이 무엇을 하는지 살펴보자.

앞서 언급했듯이, `read_line`은 사용자가 입력한 내용을 우리가 전달한 문자열에 저장하고, 동시에 `Result` 값을 반환한다. [`Result`][result]는 [_열거형_][enums]으로, 여러 가능한 상태 중 하나에 있을 수 있는 타입이다. 각 가능한 상태를 _변형체(variant)_라고 부른다.

[6장][enums]에서 열거형에 대해 더 자세히 다룰 것이다. 이 `Result` 타입의 목적은 오류 처리 정보를 인코딩하는 것이다.

`Result`의 변형체는 `Ok`와 `Err`이다. `Ok` 변형체는 작업이 성공했음을 나타내며, 성공적으로 생성된 값을 포함한다. `Err` 변형체는 작업이 실패했음을 의미하며, 작업이 실패한 이유나 방식에 대한 정보를 포함한다.

`Result` 타입의 값은 다른 타입의 값과 마찬가지로 메서드를 정의할 수 있다. `Result`의 인스턴스는 [`expect` 메서드][expect]를 호출할 수 있다. 만약 이 `Result` 인스턴스가 `Err` 값이라면, `expect`는 프로그램을 중단시키고 `expect`에 전달한 메시지를 출력한다. `read_line` 메서드가 `Err`를 반환한다면, 이는 대개 운영체제에서 발생한 오류의 결과일 가능성이 높다. 만약 이 `Result` 인스턴스가 `Ok` 값이라면, `expect`는 `Ok`가 담고 있는 반환 값을 가져와 그 값을 반환한다. 이 경우, 그 값은 사용자 입력의 바이트 수이다.

만약 `expect`를 호출하지 않는다면, 프로그램은 컴파일되지만 다음과 같은 경고가 발생한다:

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-02-without-expect/output.txt}}
```

Rust는 `read_line`에서 반환된 `Result` 값을 사용하지 않았다는 경고를 보여주며, 이는 프로그램이 가능한 오류를 처리하지 않았음을 나타낸다.

이 경고를 제거하는 올바른 방법은 실제로 오류 처리 코드를 작성하는 것이지만, 여기서는 문제가 발생할 때 프로그램을 중단시키기만 하면 되므로 `expect`를 사용할 수 있다. [9장][recover]에서 오류로부터 복구하는 방법에 대해 배울 것이다.


### `println!` 플레이스홀더로 값 출력하기

닫는 중괄호를 제외하고, 지금까지의 코드에서 다뤄야 할 줄은 단 하나뿐이다:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print_guess}}
```

이 줄은 사용자의 입력을 포함하는 문자열을 출력한다. `{}` 중괄호 세트는 플레이스홀더 역할을 한다. `{}`를 값 하나를 고정하는 작은 게 집게발로 생각하면 된다. 변수의 값을 출력할 때는 변수 이름을 중괄호 안에 넣을 수 있다. 표현식을 평가한 결과를 출력할 때는 형식 문자열에 빈 중괄호를 넣고, 그 뒤에 각 빈 중괄호 플레이스홀더에 출력할 표현식을 쉼표로 구분해 나열한다. 변수 하나와 표현식 하나의 결과를 `println!` 한 번 호출로 출력하는 코드는 다음과 같다:

```rust
let x = 5;
let y = 10;

println!("x = {x} and y + 2 = {}", y + 2);
```

이 코드는 `x = 5 and y + 2 = 12`를 출력한다.


첫 번째 단계의 추측 게임을 테스트해 보자. `cargo run` 명령어를 사용해 실행한다:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-01/
cargo clean
cargo run
input 6 -->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 6.44s
     Running `target/debug/guessing_game`
Guess the number!
Please input your guess.
6
You guessed: 6
```

이 시점에서 게임의 첫 번째 부분은 완료되었다. 키보드로부터 입력을 받고, 이를 출력한다.


## 비밀 숫자 생성하기

다음으로 사용자가 맞춰야 할 비밀 숫자를 생성해야 한다. 매번 다른 숫자가 나와야 게임을 여러 번 플레이해도 재미를 느낄 수 있다. 게임이 너무 어렵지 않도록 1부터 100 사이의 임의의 숫자를 사용한다. Rust는 아직 표준 라이브러리에 난수 생성 기능을 포함하지 않는다. 하지만 Rust 팀에서 제공하는 [`rand` 크레이트][randcrate]를 통해 이 기능을 사용할 수 있다.


### 크레이트를 활용해 기능 확장하기

크레이트는 러스트 소스 코드 파일의 모음이다. 지금까지 우리가 만든 프로젝트는 실행 가능한 _바이너리 크레이트_다. 반면 `rand` 크레이트는 _라이브러리 크레이트_로, 다른 프로그램에서 사용할 목적으로 작성된 코드를 포함하며 독자적으로 실행할 수 없다.

Cargo가 외부 크레이트를 관리하는 방식은 정말 뛰어나다. `rand`를 사용하려면 먼저 _Cargo.toml_ 파일을 수정해 `rand` 크레이트를 의존성으로 추가해야 한다. 파일을 열고 Cargo가 생성한 `[dependencies]` 섹션 헤더 아래에 다음 줄을 추가한다. 이 튜토리얼의 예제 코드가 동작하려면 `rand`를 정확히 아래와 같이 버전 번호까지 지정해야 한다:

<span class="filename">파일명: Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:8:}}
```

_Cargo.toml_ 파일에서 헤더 뒤에 오는 모든 내용은 해당 섹션에 속하며, 새로운 섹션이 시작될 때까지 계속된다. `[dependencies]` 섹션에서는 프로젝트가 의존하는 외부 크레이트와 필요한 버전을 지정한다. 여기서는 `rand` 크레이트를 시맨틱 버전 `0.8.5`로 지정했다. Cargo는 [시맨틱 버저닝][semver]을 이해한다. `0.8.5`는 실제로 `^0.8.5`의 축약형으로, 0.8.5 이상 0.9.0 미만의 모든 버전을 의미한다.

Cargo는 이 버전들이 0.8.5와 호환되는 공개 API를 가진다고 간주한다. 이렇게 하면 이 장의 코드와 호환되는 최신 패치 버전을 자동으로 사용할 수 있다. 0.9.0 이상 버전은 다음 예제에서 사용하는 API와 동일할 것이라는 보장이 없다.

코드를 변경하지 않고 프로젝트를 빌드해 보자. 아래는 그 결과다.

<Listing number="2-2" caption="`rand` 크레이트를 의존성으로 추가한 후 `cargo build`를 실행한 결과">

```console
$ cargo build
  Updating crates.io index
   Locking 15 packages to latest Rust 1.85.0 compatible versions
    Adding rand v0.8.5 (available: v0.9.0)
 Compiling proc-macro2 v1.0.93
 Compiling unicode-ident v1.0.17
 Compiling libc v0.2.170
 Compiling cfg-if v1.0.0
 Compiling byteorder v1.5.0
 Compiling getrandom v0.2.15
 Compiling rand_core v0.6.4
 Compiling quote v1.0.38
 Compiling syn v2.0.98
 Compiling zerocopy-derive v0.7.35
 Compiling zerocopy v0.7.35
 Compiling ppv-lite86 v0.2.20
 Compiling rand_chacha v0.3.1
 Compiling rand v0.8.5
 Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
  Finished `dev` profile [unoptimized + debuginfo] target(s) in 2.48s
```

</Listing>

버전 번호는 다를 수 있지만(시맨틱 버저닝 덕분에 코드와 호환된다!) 운영체제에 따라 출력되는 줄이 다르거나 순서가 다를 수 있다.

외부 의존성을 추가하면 Cargo는 _레지스트리_에서 해당 의존성이 필요한 모든 것의 최신 버전을 가져온다. 레지스트리는 [Crates.io][cratesio]의 데이터 복사본이다. Crates.io는 러스트 생태계에서 사람들이 오픈소스 러스트 프로젝트를 공유하는 곳이다.

레지스트리를 업데이트한 후 Cargo는 `[dependencies]` 섹션을 확인하고 아직 다운로드하지 않은 크레이트를 다운로드한다. 이 경우 `rand`만 의존성으로 나열했지만, Cargo는 `rand`가 동작하기 위해 필요한 다른 크레이트도 함께 가져온다. 크레이트를 다운로드한 후 러스트는 이를 컴파일하고, 의존성을 사용할 수 있게 된 프로젝트를 컴파일한다.

만약 아무것도 변경하지 않고 바로 `cargo build`를 다시 실행하면 `Finished` 줄 외에는 아무런 출력이 없다. Cargo는 이미 의존성을 다운로드하고 컴파일했으며, _Cargo.toml_ 파일에서 아무것도 변경하지 않았다는 것을 알고 있다. 또한 코드도 변경하지 않았기 때문에 다시 컴파일하지 않는다. 할 일이 없으므로 그냥 종료한다.

_src/main.rs_ 파일을 열고 사소한 변경을 한 후 저장하고 다시 빌드하면 두 줄의 출력만 볼 수 있다:

```console
$ cargo build
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
```

이 줄들은 Cargo가 _src/main.rs_ 파일의 작은 변경만 반영해 빌드했음을 보여준다. 의존성은 변경되지 않았으므로 Cargo는 이미 다운로드하고 컴파일한 것을 재사용할 수 있다.


#### _Cargo.lock_ 파일로 재현 가능한 빌드 보장하기

Cargo는 여러분이나 다른 누군가가 코드를 빌드할 때마다 동일한 결과물을 재현할 수 있도록 보장하는 메커니즘을 제공한다. Cargo는 여러분이 명시적으로 변경하지 않는 한, 지정한 버전의 의존성만 사용한다. 예를 들어, 다음 주에 `rand` 크레이트의 0.8.6 버전이 출시되고, 이 버전에는 중요한 버그 수정이 포함되어 있지만, 동시에 여러분의 코드를 망가뜨리는 회귀 버그도 포함되어 있다고 가정해 보자. 이를 처리하기 위해 Rust는 `cargo build`를 처음 실행할 때 _Cargo.lock_ 파일을 생성한다. 이제 _guessing_game_ 디렉토리에는 이 파일이 존재하게 된다.

프로젝트를 처음 빌드할 때, Cargo는 지정된 기준에 맞는 모든 의존성의 버전을 찾아내고 이를 _Cargo.lock_ 파일에 기록한다. 이후 프로젝트를 다시 빌드할 때, Cargo는 _Cargo.lock_ 파일이 존재하는지 확인하고, 해당 파일에 명시된 버전을 사용한다. 이렇게 하면 다시 버전을 찾아내는 작업을 반복하지 않아도 되며, 자동으로 재현 가능한 빌드를 보장할 수 있다. 즉, _Cargo.lock_ 파일 덕분에 여러분의 프로젝트는 명시적으로 업그레이드하지 않는 한 0.8.5 버전을 유지하게 된다. _Cargo.lock_ 파일은 재현 가능한 빌드에 중요한 역할을 하기 때문에, 프로젝트의 나머지 코드와 함께 소스 제어 시스템에 체크인되는 경우가 많다.


#### 크레이트를 새로운 버전으로 업데이트하기

크레이트를 업데이트하고 싶을 때, Cargo는 `update` 커맨드를 제공한다. 이 커맨드는 _Cargo.lock_ 파일을 무시하고 _Cargo.toml_에 명시된 조건에 맞는 최신 버전을 찾아낸다. 그리고 그 버전을 _Cargo.lock_ 파일에 기록한다. 이 경우, Cargo는 0.8.5보다 크고 0.9.0보다 작은 버전만 찾는다. 만약 `rand` 크레이트가 0.8.6과 0.9.0 두 가지 새로운 버전을 출시했다면, `cargo update`를 실행하면 다음과 같은 결과를 볼 수 있다:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
cargo update
assuming there is a new 0.8.x version of rand; otherwise use another update
as a guide to creating the hypothetical output shown here -->

```console
$ cargo update
    Updating crates.io index
     Locking 1 package to latest Rust 1.85.0 compatible version
    Updating rand v0.8.5 -> v0.8.6 (available: v0.9.0)
```

Cargo는 0.9.0 버전을 무시한다. 이 시점에서 _Cargo.lock_ 파일에 `rand` 크레이트의 버전이 0.8.6으로 변경된 것을 확인할 수 있다. `rand` 버전 0.9.0이나 0.9._x_ 시리즈의 버전을 사용하려면, _Cargo.toml_ 파일을 다음과 같이 수정해야 한다:

```toml
[dependencies]
rand = "0.9.0"
```

다음으로 `cargo build`를 실행하면, Cargo는 크레이트 레지스트리를 업데이트하고 지정한 새로운 버전에 따라 `rand` 요구사항을 다시 평가한다.

[Cargo][doccargo]<!-- ignore -->와 [그 생태계][doccratesio]<!-- ignore -->에 대해 더 많은 이야기가 있지만, 이는 14장에서 다룰 예정이다. 지금은 이 정도만 알아두면 충분하다. Cargo는 라이브러리 재사용을 매우 쉽게 만들어주기 때문에, Rust 개발자들은 여러 패키지를 조합해 작은 프로젝트를 작성할 수 있다.


### 랜덤 숫자 생성하기

이제 `rand`를 사용해 추측할 숫자를 생성해 보자. 다음 단계는 _src/main.rs_ 파일을 예제 2-3과 같이 업데이트하는 것이다.

<Listing number="2-3" file-name="src/main.rs" caption="랜덤 숫자 생성을 위한 코드 추가">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:all}}
```

</Listing>

먼저 `use rand::Rng;` 라인을 추가한다. `Rng` 트레이트는 랜덤 숫자 생성기가 구현해야 하는 메서드를 정의하며, 이 트레이트가 스코프 내에 있어야 해당 메서드를 사용할 수 있다. 트레이트에 대해서는 10장에서 자세히 다룰 것이다.

다음으로 중간에 두 줄을 추가한다. 첫 번째 줄에서는 `rand::thread_rng` 함수를 호출한다. 이 함수는 현재 실행 중인 스레드에 특화된 랜덤 숫자 생성기를 반환하며, 운영체제가 제공하는 시드 값을 사용한다. 그런 다음 랜덤 숫자 생성기에서 `gen_range` 메서드를 호출한다. 이 메서드는 `use rand::Rng;` 문으로 스코프에 가져온 `Rng` 트레이트에 정의되어 있다. `gen_range` 메서드는 범위 표현식을 인자로 받아 해당 범위 내의 랜덤 숫자를 생성한다. 여기서 사용한 범위 표현식은 `start..=end` 형태이며, 하한과 상한을 모두 포함한다. 따라서 1부터 100 사이의 숫자를 생성하려면 `1..=100`을 지정해야 한다.

> 참고: 어떤 트레이트를 사용하고, 어떤 메서드와 함수를 호출해야 하는지 단번에 알기는 어렵다. 각 크레이트는 사용 방법을 설명하는 문서를 제공한다. Cargo의 유용한 기능 중 하나는 `cargo doc --open` 명령을 실행하면 모든 의존성의 문서를 로컬에서 빌드하고 브라우저에서 열어준다는 점이다. 예를 들어, `rand` 크레이트의 다른 기능이 궁금하다면 `cargo doc --open`을 실행하고 왼쪽 사이드바에서 `rand`를 클릭하면 된다.

두 번째 새 줄은 비밀 숫자를 출력한다. 프로그램을 개발하면서 테스트할 때 유용하지만, 최종 버전에서는 이 줄을 삭제할 것이다. 프로그램이 시작하자마자 정답을 출력한다면 게임이 되지 않을 테니 말이다.

프로그램을 몇 번 실행해 보자:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-03/
cargo run
4
cargo run
5
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 7
Please input your guess.
4
You guessed: 4

$ cargo run
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 83
Please input your guess.
5
You guessed: 5
```

매번 다른 랜덤 숫자가 생성되며, 모든 숫자가 1부터 100 사이여야 한다. 잘 했다!


## 추측 값과 비밀 숫자 비교하기

이제 사용자 입력과 랜덤 숫자를 비교할 준비가 되었다. 이 과정은 목록 2-4에 나와 있다. 이 코드는 아직 컴파일되지 않음을 주의하자. 이유는 곧 설명할 것이다.

<Listing number="2-4" file-name="src/main.rs" caption="두 숫자를 비교한 결과값 처리하기">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-04/src/main.rs:here}}
```

</Listing>

먼저 `std::cmp::Ordering` 타입을 스코프로 가져오기 위해 `use` 문을 추가한다. `Ordering`은 열거형으로, `Less`, `Greater`, `Equal` 세 가지 변형 값을 가진다. 이 값들은 두 값을 비교했을 때 가능한 결과를 나타낸다.

그런 다음 `Ordering` 타입을 사용하는 다섯 줄의 코드를 추가한다. `cmp` 메서드는 두 값을 비교하며, 비교 가능한 모든 대상에 대해 호출할 수 있다. 이 메서드는 비교 대상에 대한 참조를 인자로 받는다. 여기서는 `guess`와 `secret_number`를 비교한다. 그리고 `use` 문으로 가져온 `Ordering` 열거형의 변형 값을 반환한다. `match` 표현식을 사용해 `cmp` 메서드가 반환한 `Ordering` 변형 값에 따라 다음 동작을 결정한다.

`match` 표현식은 *팔*로 구성된다. 각 팔은 매칭할 *패턴*과, `match`에 주어진 값이 해당 팔의 패턴과 일치할 때 실행할 코드로 이루어진다. Rust는 `match`에 주어진 값을 순서대로 각 팔의 패턴과 비교한다. 패턴과 `match` 구조는 Rust의 강력한 기능이다. 이 기능들은 코드가 마주칠 수 있는 다양한 상황을 표현하고, 모든 경우를 처리하도록 보장한다. 이 기능들은 각각 6장과 19장에서 자세히 다룰 것이다.

여기서 사용한 `match` 표현식의 동작을 예제로 살펴보자. 사용자가 50을 추측했고, 이번에 생성된 비밀 숫자가 38이라고 가정하자.

코드가 50과 38을 비교하면, `cmp` 메서드는 50이 38보다 크므로 `Ordering::Greater`를 반환한다. `match` 표현식은 `Ordering::Greater` 값을 받아 각 팔의 패턴을 확인한다. 첫 번째 팔의 패턴인 `Ordering::Less`를 확인하고, `Ordering::Greater`가 `Ordering::Less`와 일치하지 않으므로 해당 팔의 코드를 무시하고 다음 팔로 넘어간다. 다음 팔의 패턴은 `Ordering::Greater`로, `Ordering::Greater`와 일치한다! 따라서 해당 팔의 코드가 실행되어 `Too big!`을 화면에 출력한다. `match` 표현식은 첫 번째로 성공한 매칭 이후 종료되므로, 이 시나리오에서는 마지막 팔을 확인하지 않는다.

하지만 목록 2-4의 코드는 아직 컴파일되지 않는다. 실행해 보자:

```console
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-04/output.txt}}
```

에러의 핵심은 *타입 불일치*다. Rust는 강력한 정적 타입 시스템을 갖추고 있다. 하지만 타입 추론도 지원한다. `let mut guess = String::new()`를 작성했을 때, Rust는 `guess`가 `String` 타입이어야 한다고 추론했고, 타입을 명시하도록 요구하지 않았다. 반면 `secret_number`는 숫자 타입이다. Rust에는 1부터 100 사이의 값을 가질 수 있는 여러 숫자 타입이 있다: 32비트 숫자인 `i32`, 부호 없는 32비트 숫자인 `u32`, 64비트 숫자인 `i64`, 그리고 다른 타입들도 있다. 별도로 지정하지 않으면 Rust는 `i32`를 기본값으로 사용한다. 따라서 `secret_number`는 `i32` 타입이다. 에러의 원인은 Rust가 문자열과 숫자 타입을 비교할 수 없기 때문이다.

궁극적으로는 프로그램이 입력으로 받은 `String`을 숫자 타입으로 변환해 비밀 숫자와 비교할 수 있도록 해야 한다. 이를 위해 `main` 함수에 다음 줄을 추가한다:

<span class="filename">파일명: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/src/main.rs:here}}
```

추가한 줄은 다음과 같다:

```rust,ignore
let guess: u32 = guess.trim().parse().expect("Please type a number!");
```

`guess`라는 변수를 새로 만든다. 잠깐, 이미 `guess`라는 변수가 있지 않나? 맞다. 하지만 Rust는 이전 `guess` 값을 새로운 값으로 가리는 *섀도잉*을 허용한다. 섀도잉은 `guess_str`과 `guess`처럼 두 개의 고유한 변수를 만들지 않고도 `guess` 변수명을 재사용할 수 있게 해준다. 이 기능은 3장에서 자세히 다룰 것이다. 지금은 이 기능이 한 타입의 값을 다른 타입으로 변환할 때 자주 사용된다는 점만 알아두자.

새 변수는 `guess.trim().parse()` 표현식에 바인딩된다. 이 표현식의 `guess`는 사용자 입력을 담고 있는 원래의 `guess` 변수를 가리킨다. `String` 인스턴스의 `trim` 메서드는 문자열 앞뒤의 공백을 제거한다. 문자열을 `u32`로 변환하기 전에 이 작업을 수행해야 한다. `u32`는 숫자 데이터만 포함할 수 있기 때문이다. 사용자는 `read_line`을 만족시키기 위해 <kbd>enter</kbd>를 눌러야 하므로, 문자열에 개행 문자가 추가된다. 예를 들어 사용자가 <kbd>5</kbd>를 입력하고 <kbd>enter</kbd>를 누르면 `guess`는 `5\n`이 된다. `\n`은 "개행"을 나타낸다. (Windows에서는 <kbd>enter</kbd>를 누르면 캐리지 리턴과 개행 문자인 `\r\n`이 추가된다.) `trim` 메서드는 `\n`이나 `\r\n`을 제거해 `5`만 남긴다.

문자열의 [`parse` 메서드][parse]<!-- ignore -->는 문자열을 다른 타입으로 변환한다. 여기서는 문자열을 숫자로 변환한다. `let guess: u32`를 사용해 Rust에게 원하는 정확한 숫자 타입을 알려준다. `guess` 뒤의 콜론(`:`)은 변수의 타입을 명시한다는 것을 의미한다. Rust에는 여러 내장 숫자 타입이 있다. 여기서 사용한 `u32`는 부호 없는 32비트 정수다. 작은 양수에는 적합한 기본 선택지다. 다른 숫자 타입은 3장에서 배울 것이다.

또한 이 예제 프로그램에서 `u32` 타입을 명시하고 `secret_number`와 비교하므로, Rust는 `secret_number`도 `u32` 타입이어야 한다고 추론한다. 이제 두 값은 같은 타입으로 비교된다!

`parse` 메서드는 논리적으로 숫자로 변환할 수 있는 문자에서만 동작하므로, 쉽게 에러를 발생시킬 수 있다. 예를 들어 문자열에 `A👍%`가 포함되어 있다면, 이를 숫자로 변환할 방법이 없다. 실패할 가능성이 있으므로, `parse` 메서드는 `Result` 타입을 반환한다. 이는 앞서 다룬 `read_line` 메서드와 비슷하다. 이 `Result`도 `expect` 메서드를 사용해 처리한다. `parse`가 문자열에서 숫자를 만들 수 없어 `Err` 변형 값을 반환하면, `expect` 호출은 게임을 종료하고 주어진 메시지를 출력한다. `parse`가 문자열을 성공적으로 숫자로 변환하면 `Ok` 변형 값을 반환하고, `expect`는 `Ok` 값에서 원하는 숫자를 반환한다.

이제 프로그램을 실행해 보자:

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.26s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 58
Please input your guess.
  76
You guessed: 76
Too big!
```

잘 작동한다! 추측 값 앞에 공백이 추가되었음에도 프로그램은 사용자가 76을 추측했다는 것을 알아냈다. 프로그램을 여러 번 실행해 다양한 입력에 따른 동작을 확인해 보자: 숫자를 정확히 맞추거나, 너무 높은 숫자를 추측하거나, 너무 낮은 숫자를 추측해 보는 것이다.

이제 게임의 대부분이 작동한다. 하지만 사용자는 한 번만 추측할 수 있다. 이제 반복문을 추가해 이를 바꿔보자!


## 여러 번 추측할 수 있도록 루프 추가하기

`loop` 키워드는 무한 루프를 생성한다. 사용자가 여러 번 추측할 수 있도록 루프를 추가해 보자:

<span class="filename">파일명: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-04-looping/src/main.rs:here}}
```

보는 바와 같이, 추측값 입력 프롬프트 이후의 모든 내용을 루프 안으로 옮겼다. 루프 내부의 각 줄을 4칸씩 들여쓰기하고 프로그램을 다시 실행해 보자. 이제 프로그램은 계속해서 추측값을 요청할 것이다. 하지만 이는 새로운 문제를 야기한다. 사용자가 프로그램을 종료할 방법이 없는 것처럼 보인다.

사용자는 언제나 <kbd>ctrl</kbd>-<kbd>c</kbd> 단축키를 사용해 프로그램을 중단할 수 있다. 하지만 ["추측값과 비밀번호 비교하기"](#comparing-the-guess-to-the-secret-number)<!-- ignore -->에서 `parse`에 대해 논의할 때 언급했듯이, 이 무한 루프에서 벗어나는 또 다른 방법이 있다. 사용자가 숫자가 아닌 답을 입력하면 프로그램이 충돌할 것이다. 이를 활용해 사용자가 게임을 종료할 수 있도록 할 수 있다:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-04-looping/
touch src/main.rs
cargo run
(too small guess)
(too big guess)
(correct guess)
quit
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.23s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 59
Please input your guess.
45
You guessed: 45
Too small!
Please input your guess.
60
You guessed: 60
Too big!
Please input your guess.
59
You guessed: 59
You win!
Please input your guess.
quit

thread 'main' panicked at src/main.rs:28:47:
Please type a number!: ParseIntError { kind: InvalidDigit }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

`quit`을 입력하면 게임이 종료되지만, 다른 숫자가 아닌 입력도 동일하게 게임을 종료시킨다. 이는 최적의 방법이 아니다. 정답을 맞췄을 때도 게임이 멈추길 원한다.


### 정답을 맞췄을 때 종료하기

사용자가 정답을 맞췄을 때 게임을 종료하도록 프로그램을 수정해보자. 이를 위해 `break` 문을 추가한다:

<span class="filename">파일명: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-05-quitting/src/main.rs:here}}
```

`You win!` 메시지 뒤에 `break` 문을 추가하면 사용자가 비밀번호를 맞췄을 때 루프를 종료한다. 루프가 `main` 함수의 마지막 부분이므로, 루프를 종료하는 것은 프로그램을 종료하는 것과 같다.


### 잘못된 입력 처리하기

프로그램이 사용자가 숫자가 아닌 값을 입력했을 때 충돌(crash)하지 않도록, 이제는 그런 입력을 무시하고 계속해서 추측할 수 있게 개선해보자. 이를 위해 `guess`를 `String`에서 `u32`로 변환하는 부분을 수정하면 된다. Listing 2-5에서 그 방법을 확인할 수 있다.

<Listing number="2-5" file-name="src/main.rs" caption="숫자가 아닌 추측값을 무시하고 프로그램 충돌 대신 다시 추측값을 요청하기">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:here}}
```

</Listing>

여기서는 `expect` 호출을 `match` 표현식으로 바꿔서, 오류 발생 시 프로그램을 종료하는 대신 오류를 처리하도록 했다. `parse`는 `Result` 타입을 반환하고, `Result`는 `Ok`와 `Err` 두 가지 변형(variant)을 가진 열거형(enum)이다. 앞서 `cmp` 메서드의 `Ordering` 결과를 처리할 때와 마찬가지로 `match` 표현식을 사용했다.

`parse`가 문자열을 숫자로 성공적으로 변환할 수 있다면, 결과 숫자를 담은 `Ok` 값을 반환한다. 이 `Ok` 값은 `match`의 첫 번째 패턴과 일치하며, `match` 표현식은 `parse`가 생성한 `num` 값을 반환한다. 이 값은 새로운 `guess` 변수에 저장된다.

반면 `parse`가 문자열을 숫자로 변환하지 못하면, 오류 정보를 담은 `Err` 값을 반환한다. 이 `Err` 값은 첫 번째 `match` 패턴인 `Ok(num)`과 일치하지 않지만, 두 번째 패턴인 `Err(_)`와는 일치한다. 여기서 언더스코어(`_`)는 모든 값을 포괄하는 와일드카드 패턴이다. 이 예제에서는 `Err` 값 내부에 어떤 정보가 있든 상관없이 모든 `Err` 값을 처리하겠다는 의미다. 따라서 프로그램은 두 번째 패턴의 코드인 `continue`를 실행한다. 이는 프로그램에게 루프의 다음 반복으로 이동해 다시 추측값을 요청하라는 뜻이다. 결과적으로 프로그램은 `parse`가 만날 수 있는 모든 오류를 무시하게 된다.

이제 프로그램의 모든 부분이 예상대로 동작할 것이다. 한번 실행해보자:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-05/
cargo run
(too small guess)
(too big guess)
foo
(correct guess)
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 61
Please input your guess.
10
You guessed: 10
Too small!
Please input your guess.
99
You guessed: 99
Too big!
Please input your guess.
foo
Please input your guess.
61
You guessed: 61
You win!
```

훌륭하다! 이제 마지막으로 작은 수정을 하나 더 하면 추측 게임이 완성된다. 현재 프로그램은 여전히 비밀 숫자를 출력하고 있다. 테스트할 때는 유용했지만, 실제 게임에서는 문제가 된다. 비밀 숫자를 출력하는 `println!`을 삭제해보자. Listing 2-6은 최종 코드를 보여준다.

<Listing number="2-6" file-name="src/main.rs" caption="완성된 추측 게임 코드">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-06/src/main.rs}}
```

</Listing>

이제 여러분은 성공적으로 추측 게임을 만들었다. 축하한다!


## 요약

이 프로젝트는 여러분에게 다양한 새로운 Rust 개념을 실제로 경험할 수 있는 기회를 제공한다. `let`, `match`, 함수, 외부 크레이트 사용 등을 다뤘다. 다음 몇 장에서는 이러한 개념을 더 자세히 배울 것이다. 3장에서는 변수, 데이터 타입, 함수 등 대부분의 프로그래밍 언어에서 공통적으로 사용되는 개념을 다루고, Rust에서 이를 어떻게 사용하는지 설명한다. 4장에서는 Rust를 다른 언어와 차별화하는 특징인 소유권(ownership)에 대해 탐구한다. 5장에서는 구조체(struct)와 메서드 문법을 논의하고, 6장에서는 열거형(enums)이 어떻게 동작하는지 설명한다.

[prelude]: ../std/prelude/index.html
[variables-and-mutability]: ch03-01-variables-and-mutability.html#variables-and-mutability
[comments]: ch03-04-comments.html
[string]: ../std/string/struct.String.html
[iostdin]: ../std/io/struct.Stdin.html
[read_line]: ../std/io/struct.Stdin.html#method.read_line
[result]: ../std/result/enum.Result.html
[enums]: ch06-00-enums.html
[expect]: ../std/result/enum.Result.html#method.expect
[recover]: ch09-02-recoverable-errors-with-result.html
[randcrate]: https://crates.io/crates/rand
[semver]: http://semver.org
[cratesio]: https://crates.io/
[doccargo]: https://doc.rust-lang.org/cargo/
[doccratesio]: https://doc.rust-lang.org/cargo/reference/publishing.html
[match]: ch06-02-match.html
[shadowing]: ch03-01-variables-and-mutability.html#shadowing
[parse]: ../std/primitive.str.html#method.parse
[integers]: ch03-02-data-types.html#integer-types


