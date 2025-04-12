## `use` 키워드로 경로를 스코프에 가져오기

함수를 호출할 때마다 경로를 일일이 작성하는 것은 번거롭고 반복적일 수 있다. 예제 7-7에서 `add_to_waitlist` 함수를 호출할 때마다 `front_of_house`와 `hosting`을 함께 지정해야 했다. 다행히 이 과정을 단순화할 방법이 있다. `use` 키워드를 사용해 경로에 대한 단축키를 한 번 만들면, 스코프 내에서는 더 짧은 이름을 사용할 수 있다.

예제 7-11에서 `crate::front_of_house::hosting` 모듈을 `eat_at_restaurant` 함수의 스코프로 가져온다. 이제 `eat_at_restaurant` 함수 내에서 `hosting::add_to_waitlist`만 지정해도 `add_to_waitlist` 함수를 호출할 수 있다.

<Listing number="7-11" file-name="src/lib.rs" caption="`use`로 모듈을 스코프에 가져오기">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-11/src/lib.rs}}
```

</Listing>

스코프에 `use`와 경로를 추가하는 것은 파일 시스템에서 심볼릭 링크를 만드는 것과 유사하다. 크레이트 루트에 `use crate::front_of_house::hosting`을 추가하면, `hosting`은 해당 스코프 내에서 유효한 이름이 된다. 마치 `hosting` 모듈이 크레이트 루트에 정의된 것처럼 작동한다. `use`로 가져온 경로도 다른 경로와 마찬가지로 프라이버시를 검사한다.

`use`는 해당 `use`가 발생한 특정 스코프에 대해서만 단축키를 생성한다는 점에 유의해야 한다. 예제 7-12에서 `eat_at_restaurant` 함수를 `customer`라는 새로운 자식 모듈로 이동시켰다. 이제 `use` 문과는 다른 스코프가 되었기 때문에 함수 본문이 컴파일되지 않는다.

<Listing number="7-12" file-name="src/lib.rs" caption="`use` 문은 해당 스코프 내에서만 적용된다.">

```rust,noplayground,test_harness,does_not_compile,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-12/src/lib.rs}}
```

</Listing>

컴파일러 오류는 `customer` 모듈 내에서 단축키가 더 이상 적용되지 않음을 보여준다:

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-12/output.txt}}
```

`use`가 더 이상 스코프 내에서 사용되지 않는다는 경고도 함께 나타난다. 이 문제를 해결하려면 `use`를 `customer` 모듈 내로 이동시키거나, 자식 `customer` 모듈 내에서 `super::hosting`으로 부모 모듈의 단축키를 참조해야 한다.


### 관용적인 `use` 경로 생성하기

리스트 7-11에서 `use crate::front_of_house::hosting`을 지정한 후 `eat_at_restaurant`에서 `hosting::add_to_waitlist`를 호출한 이유가 궁금할 수 있다. 리스트 7-13처럼 `add_to_waitlist` 함수까지 전체 경로를 지정해도 동일한 결과를 얻을 수 있지만, 리스트 7-11이 관용적인 방식이다.

<Listing number="7-13" file-name="src/lib.rs" caption="`use`로 `add_to_waitlist` 함수를 스코프로 가져오기 (비관용적)">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-13/src/lib.rs}}
```

</Listing>

리스트 7-11과 리스트 7-13은 동일한 작업을 수행하지만, 리스트 7-11이 `use`로 함수를 스코프로 가져오는 관용적인 방식이다. 함수의 상위 모듈을 `use`로 가져오면 함수를 호출할 때 상위 모듈을 지정해야 한다. 이렇게 하면 함수가 로컬에서 정의되지 않았음을 명확히 하면서도 전체 경로의 반복을 최소화할 수 있다. 리스트 7-13의 코드는 `add_to_waitlist`가 어디서 정의되었는지 불분명하다.

반면, `use`로 구조체, 열거형 등을 가져올 때는 전체 경로를 지정하는 것이 관용적이다. 리스트 7-14는 바이너리 크레이트에서 표준 라이브러리의 `HashMap` 구조체를 스코프로 가져오는 관용적인 방식을 보여준다.

<Listing number="7-14" file-name="src/main.rs" caption="관용적인 방식으로 `HashMap`을 스코프로 가져오기">

```rust
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-14/src/main.rs}}
```

</Listing>

이 관례에는 특별한 이유가 없다. 단지 이렇게 작성하는 것이 일반적이 되었고, 사람들이 이 방식으로 Rust 코드를 읽고 쓰는 데 익숙해졌을 뿐이다.

이 관례의 예외는 `use` 문으로 동일한 이름의 두 아이템을 스코프로 가져오는 경우다. Rust는 이를 허용하지 않기 때문이다. 리스트 7-15는 동일한 이름을 가졌지만 상위 모듈이 다른 두 `Result` 타입을 스코프로 가져오고 참조하는 방법을 보여준다.

<Listing number="7-15" file-name="src/lib.rs" caption="동일한 이름을 가진 두 타입을 같은 스코프로 가져오려면 상위 모듈을 사용해야 한다.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-15/src/lib.rs:here}}
```

</Listing>

보는 바와 같이, 상위 모듈을 사용하면 두 `Result` 타입을 구분할 수 있다. 만약 `use std::fmt::Result`와 `use std::io::Result`를 지정하면 같은 스코프에 두 `Result` 타입이 존재하게 되고, Rust는 `Result`를 사용할 때 어느 것을 의미하는지 알 수 없다.


### `as` 키워드로 새로운 이름 제공하기

동일한 이름의 두 타입을 같은 스코프로 가져오는 문제를 해결하는 또 다른 방법은 `use`를 사용할 때 경로 뒤에 `as`와 함께 새로운 로컬 이름, 즉 _별칭_을 지정하는 것이다. Listing 7-16은 `as`를 사용해 두 `Result` 타입 중 하나의 이름을 바꿔 Listing 7-15의 코드를 다시 작성한 예제다.

<Listing number="7-16" file-name="src/lib.rs" caption="`as` 키워드를 사용해 스코프로 가져올 때 타입 이름 변경하기">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-16/src/lib.rs:here}}
```

</Listing>

두 번째 `use` 문에서 `std::io::Result` 타입에 `IoResult`라는 새로운 이름을 선택했다. 이렇게 하면 `std::fmt`의 `Result`와 충돌하지 않는다. Listing 7-15와 Listing 7-16은 모두 관용적인 방식으로 간주되므로, 어떤 방식을 선택할지는 여러분의 선택에 달려 있다!


### `pub use`로 이름 다시 내보내기

`use` 키워드를 사용해 이름을 스코프로 가져오면, 해당 이름은 임포트한 스코프 내에서만 비공개로 사용된다. 이 이름을 외부 스코프에서도 마치 해당 스코프에 정의된 것처럼 참조할 수 있게 하려면 `pub`과 `use`를 함께 사용한다. 이 기법을 _다시 내보내기(re-exporting)_라고 부르며, 아이템을 스코프로 가져오는 동시에 다른 스코프에서도 사용할 수 있도록 공개하는 역할을 한다.

Listing 7-17은 Listing 7-11의 코드에서 루트 모듈의 `use`를 `pub use`로 변경한 예제를 보여준다.

<Listing number="7-17" file-name="src/lib.rs" caption="`pub use`를 사용해 새로운 스코프에서 이름을 공개하기">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-17/src/lib.rs}}
```

</Listing>

이 변경 전에는 외부 코드에서 `add_to_waitlist` 함수를 호출하려면 `restaurant::front_of_house::hosting::add_to_waitlist()`와 같은 경로를 사용해야 했으며, `front_of_house` 모듈도 `pub`으로 표시되어야 했다. 이제 `pub use`를 통해 루트 모듈에서 `hosting` 모듈을 다시 내보냈으므로, 외부 코드는 `restaurant::hosting::add_to_waitlist()`와 같은 간단한 경로를 사용할 수 있다.

다시 내보내기는 코드의 내부 구조와 이를 호출하는 프로그래머가 생각하는 도메인 구조가 다를 때 유용하다. 예를 들어, 레스토랑 비유에서 레스토랑을 운영하는 사람들은 "전면(front of house)"과 "후면(back of house)"을 구분해 생각할 수 있다. 하지만 레스토랑을 방문하는 고객은 이러한 용어로 레스토랑의 구조를 생각하지 않을 것이다. `pub use`를 사용하면 코드는 한 구조로 작성하되, 다른 구조로 공개할 수 있다. 이렇게 하면 라이브러리를 개발하는 프로그래머와 라이브러리를 호출하는 프로그래머 모두에게 잘 조직된 라이브러리를 제공할 수 있다. `pub use`의 또 다른 예제와 이 기능이 크레이트의 문서에 미치는 영향에 대해서는 14장의 ["`pub use`로 편리한 공개 API 내보내기"][ch14-pub-use]<!-- ignore -->에서 살펴볼 것이다.


### 외부 패키지 사용하기

2장에서는 랜덤 숫자를 얻기 위해 `rand`라는 외부 패키지를 사용하는 추측 게임 프로젝트를 만들었다. 프로젝트에서 `rand`를 사용하려면 _Cargo.toml_ 파일에 다음 줄을 추가했다:

<!-- `rand` 버전을 업데이트할 때, 다음 파일에서도 `rand` 버전을 업데이트하여 일치시켜야 한다:
* ch02-00-guessing-game-tutorial.md
* ch14-03-cargo-workspaces.md
-->

<Listing file-name="Cargo.toml">

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:9:}}
```

</Listing>

_Cargo.toml_에 `rand`를 의존성으로 추가하면 Cargo는 [crates.io](https://crates.io/)에서 `rand` 패키지와 필요한 의존성을 다운로드하고 프로젝트에서 사용할 수 있게 한다.

그런 다음, `rand`의 정의를 패키지 스코프로 가져오기 위해 크레이트 이름인 `rand`로 시작하는 `use` 줄을 추가하고 스코프로 가져올 항목을 나열했다. 2장의 ["랜덤 숫자 생성하기"][rand]<!-- ignore -->에서 `Rng` 트레이트를 스코프로 가져오고 `rand::thread_rng` 함수를 호출한 것을 기억할 것이다:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:ch07-04}}
```

Rust 커뮤니티의 멤버들은 [crates.io](https://crates.io/)에 많은 패키지를 제공하고 있으며, 이들 중 어떤 것을 프로젝트에 포함시키려면 동일한 단계를 거친다: 패키지의 _Cargo.toml_ 파일에 나열하고 `use`를 사용해 해당 크레이트의 항목을 스코프로 가져온다.

표준 `std` 라이브러리도 프로젝트 외부의 크레이트라는 점에 유의하라. 표준 라이브러리는 Rust 언어와 함께 제공되므로 _Cargo.toml_을 변경해 `std`를 포함시킬 필요는 없다. 하지만 스코프로 항목을 가져오려면 `use`를 사용해 참조해야 한다. 예를 들어, `HashMap`을 사용하려면 다음과 같이 작성한다:

```rust
use std::collections::HashMap;
```

이는 표준 라이브러리 크레이트의 이름인 `std`로 시작하는 절대 경로이다.


### 중첩 경로를 사용해 긴 `use` 목록 정리하기

같은 크레이트나 모듈에서 정의된 여러 항목을 사용할 때, 각 항목을 한 줄씩 나열하면 파일에서 많은 세로 공간을 차지한다. 예를 들어, 2장의 추측 게임에서 사용했던 다음 두 `use` 문은 `std`에서 항목을 가져온다:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-01-use-std-unnested/src/main.rs:here}}
```

</Listing>

대신, 중첩 경로를 사용해 한 줄로 같은 항목을 가져올 수 있다. 경로의 공통 부분을 지정한 다음, 두 개의 콜론을 붙이고, 중괄호로 감싸서 경로의 다른 부분을 나열한다. 이는 리스트 7-18에서 보여준다.

<Listing number="7-18" file-name="src/main.rs" caption="같은 접두사를 가진 여러 항목을 범위로 가져오기 위해 중첩 경로 지정">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-18/src/main.rs:here}}
```

</Listing>

더 큰 프로그램에서는 중첩 경로를 사용해 같은 크레이트나 모듈에서 많은 항목을 가져오면 필요한 `use` 문의 수를 크게 줄일 수 있다!

경로의 어떤 수준에서든 중첩 경로를 사용할 수 있으며, 이는 하위 경로를 공유하는 두 개의 `use` 문을 결합할 때 유용하다. 예를 들어, 리스트 7-19는 두 개의 `use` 문을 보여준다. 하나는 `std::io`를 가져오고, 다른 하나는 `std::io::Write`를 가져온다.

<Listing number="7-19" file-name="src/lib.rs" caption="하나가 다른 하나의 하위 경로인 두 개의 `use` 문">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-19/src/lib.rs}}
```

</Listing>

이 두 경로의 공통 부분은 `std::io`이며, 이는 첫 번째 경로의 전체이다. 이 두 경로를 하나의 `use` 문으로 결합하려면, 중첩 경로에서 `self`를 사용할 수 있다. 이는 리스트 7-20에서 보여준다.

<Listing number="7-20" file-name="src/lib.rs" caption="리스트 7-19의 경로를 하나의 `use` 문으로 결합">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-20/src/lib.rs}}
```

</Listing>

이 한 줄은 `std::io`와 `std::io::Write`를 범위로 가져온다.


### Glob 연산자

특정 경로에 정의된 모든 공개 항목을 범위로 가져오려면, 해당 경로 뒤에 `*` Glob 연산자를 지정한다:

```rust
use std::collections::*;
```

이 `use` 문은 `std::collections`에 정의된 모든 공개 항목을 현재 범위로 가져온다. 하지만 Glob 연산자를 사용할 때는 주의해야 한다. Glob은 어떤 이름이 범위 내에 있는지, 프로그램에서 사용된 이름이 어디에서 정의되었는지 파악하기 어렵게 만들 수 있다.

Glob 연산자는 주로 테스트 시 `tests` 모듈로 테스트 대상의 모든 항목을 가져올 때 사용한다. 이에 대해서는 11장 [“테스트 작성 방법”][writing-tests]<!-- ignore -->에서 자세히 다룬다. 또한 Glob 연산자는 prelude 패턴의 일부로 사용되기도 한다. 이 패턴에 대한 자세한 내용은 [표준 라이브러리 문서](../std/prelude/index.html#other-preludes)<!-- ignore -->를 참고한다.

[ch14-pub-use]: ch14-02-publishing-to-crates-io.html#exporting-a-convenient-public-api-with-pub-use
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number
[writing-tests]: ch11-01-writing-tests.html#how-to-write-tests


