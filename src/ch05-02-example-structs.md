## 구조체를 사용한 예제 프로그램

구조체를 사용해야 하는 상황을 이해하기 위해, 사각형의 넓이를 계산하는 프로그램을 작성해 보자. 먼저 단일 변수를 사용해 시작한 후, 프로그램을 리팩터링하여 구조체를 사용하도록 변경할 것이다.

_rectangles_라는 이름의 새로운 바이너리 프로젝트를 Cargo로 생성한다. 이 프로젝트는 픽셀 단위로 지정된 사각형의 너비와 높이를 받아 넓이를 계산한다. 리스트 5-8은 프로젝트의 _src/main.rs_ 파일에서 이를 구현한 간단한 프로그램을 보여준다.

<Listing number="5-8" file-name="src/main.rs" caption="분리된 너비와 높이 변수로 지정된 사각형의 넓이 계산">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:all}}
```

</Listing>

이제 `cargo run` 명령어로 프로그램을 실행한다:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/output.txt}}
```

이 코드는 각 차원을 `area` 함수에 전달하여 사각형의 넓이를 계산하는 데 성공한다. 하지만 이 코드를 더 명확하고 읽기 쉽게 만들 수 있다.

이 코드의 문제점은 `area` 함수의 시그니처에서 명확히 드러난다:

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:here}}
```

`area` 함수는 하나의 사각형 넓이를 계산해야 하지만, 작성한 함수는 두 개의 매개변수를 가지고 있다. 그리고 프로그램 어디에서도 이 매개변수들이 서로 관련이 있다는 것이 명확하지 않다. 너비와 높이를 함께 묶어서 표현하면 더 읽기 쉽고 관리하기 편할 것이다. 이미 [“튜플 타입”][the-tuple-type]<!-- ignore --> 섹션에서 이를 구현할 수 있는 한 가지 방법을 논의했다: 튜플을 사용하는 것이다.


### 튜플을 활용한 리팩토링

리스트 5-9는 튜플을 사용한 프로그램의 또 다른 버전을 보여준다.

<Listing number="5-9" file-name="src/main.rs" caption="튜플을 사용해 직사각형의 너비와 높이 지정">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-09/src/main.rs}}
```

</Listing>

어떤 면에서는 이 프로그램이 더 나아졌다. 튜플을 사용해 약간의 구조를 추가했고, 이제 단 하나의 인자만 전달한다. 하지만 다른 측면에서는 이 버전이 덜 명확하다. 튜플은 요소에 이름을 붙이지 않기 때문에 튜플의 각 부분에 접근하려면 인덱스를 사용해야 한다. 이로 인해 계산 과정이 덜 직관적이 된다.

너비와 높이를 혼동해도 면적 계산에는 문제가 없지만, 화면에 직사각형을 그리려면 문제가 된다. `width`가 튜플의 인덱스 `0`이고 `height`가 인덱스 `1`이라는 점을 기억해야 한다. 다른 사람이 이 코드를 사용한다면 이를 파악하고 기억하기가 더 어려울 것이다. 코드에서 데이터의 의미를 명확히 전달하지 않았기 때문에 오류가 발생하기 쉬워진 것이다.


### 구조체를 사용한 리팩토링: 의미 추가하기

데이터에 의미를 부여하기 위해 구조체를 사용한다. 튜플을 구조체로 변환하면 전체와 각 부분에 이름을 붙일 수 있다. 리스트 5-10에서 이를 확인할 수 있다.

<Listing number="5-10" file-name="src/main.rs" caption="`Rectangle` 구조체 정의">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-10/src/main.rs}}
```

</Listing>

여기서 `Rectangle`이라는 이름의 구조체를 정의했다. 중괄호 안에 `width`와 `height`라는 필드를 정의했으며, 두 필드 모두 `u32` 타입을 가진다. 그런 다음 `main` 함수에서 `Rectangle`의 특정 인스턴스를 생성했는데, 이 인스턴스의 너비는 `30`, 높이는 `50`이다.

이제 `area` 함수는 하나의 파라미터를 받는다. 이 파라미터는 `rectangle`이라는 이름으로, `Rectangle` 구조체 인스턴스의 불변 참조 타입이다. 4장에서 언급했듯이, 구조체의 소유권을 가져가는 대신 참조를 사용한다. 이렇게 하면 `main` 함수가 소유권을 유지하고 `rect1`을 계속 사용할 수 있다. 그래서 함수 시그니처와 함수 호출 시 `&`를 사용한다.

`area` 함수는 `Rectangle` 인스턴스의 `width`와 `height` 필드에 접근한다(참조된 구조체 인스턴스의 필드에 접근할 때 필드 값이 이동하지 않는다는 점을 기억하자. 이 때문에 구조체의 참조를 자주 보게 된다). 이제 `area` 함수의 시그니처는 정확히 우리가 의도한 바를 나타낸다: `Rectangle`의 `width`와 `height` 필드를 사용해 면적을 계산한다. 이는 너비와 높이가 서로 관련이 있음을 전달하며, 튜플의 인덱스 값인 `0`과 `1`을 사용하는 대신 설명적인 이름을 제공한다. 이는 코드의 명확성을 높이는 데 도움이 된다.


### 파생 트레이트를 통한 유용한 기능 추가

프로그램을 디버깅할 때 `Rectangle` 인스턴스를 출력하고 모든 필드의 값을 확인할 수 있다면 매우 유용할 것이다. 목록 5-11에서는 이전 장에서 사용했던 [`println!` 매크로][println]<!-- ignore -->를 사용해 보았다. 하지만 이 방법은 작동하지 않는다.

<목록 번호="5-11" 파일 이름="src/main.rs" 설명="`Rectangle` 인스턴스를 출력하려는 시도">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/src/main.rs}}
```

</목록>

이 코드를 컴파일하면 다음과 같은 오류 메시지가 나타난다:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:3}}
```

`println!` 매크로는 다양한 형식의 포맷팅을 지원하며, 기본적으로 중괄호는 `println!`에게 `Display` 형식을 사용하라고 지시한다. 이 형식은 최종 사용자에게 직접 보여주기 위한 출력을 의미한다. 지금까지 본 기본 타입들은 기본적으로 `Display`를 구현하고 있다. 왜냐하면 `1`이나 다른 기본 타입을 사용자에게 보여주는 방법은 한 가지뿐이기 때문이다. 하지만 구조체의 경우 `println!`이 출력을 어떻게 포맷해야 하는지 명확하지 않다. 쉼표를 사용할지, 중괄호를 출력할지, 모든 필드를 보여줄지 등 다양한 가능성이 있기 때문이다. 이러한 모호성 때문에 Rust는 우리가 원하는 것을 추측하려고 하지 않으며, 구조체는 `println!`과 `{}` 자리 표시자와 함께 사용할 수 있는 `Display` 구현을 제공하지 않는다.

오류를 계속 읽어보면 다음과 같은 유용한 메시지를 찾을 수 있다:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:9:10}}
```

한번 시도해 보자! 이제 `println!` 매크로 호출은 `println!("rect1 is {rect1:?}");`와 같이 보일 것이다. 중괄호 안에 `:?` 지정자를 넣으면 `println!`에게 `Debug`라는 출력 형식을 사용하라고 지시한다. `Debug` 트레이트는 개발자가 코드를 디버깅할 때 유용하도록 구조체를 출력할 수 있게 해준다.

이 변경 사항으로 코드를 컴파일해 보자. 아직도 오류가 발생한다:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:3}}
```

하지만 다시 컴파일러가 유용한 메시지를 제공한다:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:9:10}}
```

Rust는 디버깅 정보를 출력하는 기능을 포함하고 있지만, 우리의 구조체에 대해 이 기능을 사용하려면 명시적으로 선택해야 한다. 이를 위해 구조체 정의 바로 앞에 `#[derive(Debug)]` 외부 속성을 추가한다. 목록 5-12에서 이를 확인할 수 있다.

<목록 번호="5-12" 파일 이름="src/main.rs" 설명="`Debug` 트레이트를 파생하기 위한 속성 추가 및 디버그 포맷팅을 사용해 `Rectangle` 인스턴스 출력">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/src/main.rs}}
```

</목록>

이제 프로그램을 실행하면 오류가 발생하지 않으며 다음과 같은 출력을 확인할 수 있다:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/output.txt}}
```

좋다! 가장 예쁜 출력은 아니지만, 이 인스턴스의 모든 필드 값을 보여주므로 디버깅 중에 확실히 도움이 될 것이다. 더 큰 구조체를 다룰 때는 읽기 쉬운 출력이 유용할 수 있다. 이 경우 `println!` 문자열에서 `{:?}` 대신 `{:#?}`를 사용할 수 있다. 이 예제에서 `{:#?}` 스타일을 사용하면 다음과 같은 출력이 나타난다:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-02-pretty-debug/output.txt}}
```

`Debug` 형식으로 값을 출력하는 또 다른 방법은 [`dbg!` 매크로][dbg]<!-- ignore -->를 사용하는 것이다. 이 매크로는 표현식의 소유권을 가져간다(`println!`은 참조를 가져가는 반면). 그리고 코드에서 `dbg!` 매크로 호출이 발생한 파일과 줄 번호를 출력하며, 해당 표현식의 결과 값을 출력한 후 값의 소유권을 반환한다.

> 참고: `dbg!` 매크로를 호출하면 표준 오류 콘솔 스트림(`stderr`)에 출력된다. 반면 `println!`은 표준 출력 콘솔 스트림(`stdout`)에 출력한다. `stderr`와 `stdout`에 대해서는 12장의 ["표준 출력 대신 표준 오류에 에러 메시지 쓰기" 섹션][err]<!-- ignore -->에서 더 자세히 다룰 것이다.

다음 예제에서는 `width` 필드에 할당되는 값과 `rect1`의 전체 구조체 값을 확인하고자 한다:

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/src/main.rs}}
```

`dbg!`를 `30 * scale` 표현식 주위에 배치할 수 있다. `dbg!`가 표현식의 값에 대한 소유권을 반환하기 때문에 `width` 필드는 `dbg!` 호출이 없을 때와 동일한 값을 얻는다. `dbg!`가 `rect1`의 소유권을 가져가지 않도록 다음 호출에서는 `rect1`에 대한 참조를 사용한다. 이 예제의 출력은 다음과 같다:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/output.txt}}
```

출력의 첫 번째 부분은 _src/main.rs_의 10번째 줄에서 `30 * scale` 표현식을 디버깅한 결과이며, 그 결과 값은 `60`이다(정수에 대한 `Debug` 포맷팅은 값만 출력한다). _src/main.rs_의 14번째 줄에서 `dbg!` 호출은 `&rect1`의 값을 출력하며, 이는 `Rectangle` 구조체이다. 이 출력은 `Rectangle` 타입의 예쁜 `Debug` 포맷팅을 사용한다. `dbg!` 매크로는 코드가 무엇을 하는지 파악하려고 할 때 매우 유용할 수 있다!

`Debug` 트레이트 외에도 Rust는 `derive` 속성과 함께 사용할 수 있는 여러 트레이트를 제공하여 커스텀 타입에 유용한 동작을 추가할 수 있다. 이러한 트레이트와 그 동작은 [부록 C][app-c]<!-- ignore -->에 나열되어 있다. 10장에서는 커스텀 동작으로 이러한 트레이트를 구현하는 방법과 자신만의 트레이트를 만드는 방법을 다룰 것이다. 또한 `derive` 외에도 많은 속성이 있다. 더 많은 정보는 [Rust Reference의 "Attributes" 섹션][attributes]을 참조하라.

우리의 `area` 함수는 매우 구체적이다. 이 함수는 직사각형의 면적만 계산한다. 이 동작을 `Rectangle` 구조체와 더 밀접하게 연결하는 것이 도움이 될 것이다. 왜냐하면 이 함수는 다른 타입에서는 작동하지 않기 때문이다. 이제 `area` 함수를 `Rectangle` 타입에 정의된 `area` _메서드_로 리팩토링하는 방법을 살펴보자.

[the-tuple-type]: ch03-02-data-types.html#the-tuple-type
[app-c]: appendix-03-derivable-traits.md
[println]: ../std/macro.println.html
[dbg]: ../std/macro.dbg.html
[err]: ch12-06-writing-to-stderr-instead-of-stdout.html
[attributes]: ../reference/attributes.html


