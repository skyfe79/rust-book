## UTF-8 인코딩 텍스트를 문자열로 저장하기

4장에서 문자열에 대해 다뤘지만, 이번에는 더 깊이 알아보겠다. 새로운 Rust 개발자들은 주로 세 가지 이유로 문자열에서 막히곤 한다: Rust가 가능한 오류를 노출하는 경향, 문자열이 많은 프로그래머가 생각하는 것보다 더 복잡한 데이터 구조라는 점, 그리고 UTF-8 때문이다. 이러한 요소들이 합쳐져 다른 프로그래밍 언어에서 온 개발자에게는 어려워 보일 수 있다.

문자열을 컬렉션의 맥락에서 논의하는 이유는 문자열이 바이트의 컬렉션으로 구현되고, 이 바이트를 텍스트로 해석할 때 유용한 기능을 제공하는 메서드가 추가되기 때문이다. 이 섹션에서는 `String`에 대해 모든 컬렉션 타입이 가지는 연산들, 즉 생성, 업데이트, 읽기 등을 다룬다. 또한 `String`이 다른 컬렉션과 어떻게 다른지, 특히 사람과 컴퓨터가 `String` 데이터를 해석하는 방식의 차이로 인해 `String` 인덱싱이 복잡해지는 점에 대해서도 논의한다.


### 문자열이란 무엇인가?

먼저 _문자열_이라는 용어가 무엇을 의미하는지 정의해 보자. Rust의 코어 언어에는 단 하나의 문자열 타입만 존재한다. 바로 문자열 슬라이스 `str`이며, 이는 보통 빌린 형태인 `&str`로 나타난다. 4장에서 우리는 _문자열 슬라이스_에 대해 다뤘는데, 이는 다른 곳에 저장된 UTF-8로 인코딩된 문자열 데이터에 대한 참조다. 예를 들어, 문자열 리터럴은 프로그램의 바이너리에 저장되므로 문자열 슬라이스다.

Rust의 표준 라이브러리에서 제공하는 `String` 타입은 코어 언어에 내장된 것이 아니라, 크기가 늘어나고 변경 가능하며 소유권을 가진 UTF-8로 인코딩된 문자열 타입이다. Rust 개발자들이 Rust에서 "문자열"을 언급할 때, 그들은 `String`이나 문자열 슬라이스 `&str` 타입 중 하나를 의미할 수 있으며, 단일 타입만을 가리키는 것은 아니다. 이 섹션은 주로 `String`에 대해 다루지만, 두 타입 모두 Rust의 표준 라이브러리에서 광범위하게 사용되며, `String`과 문자열 슬라이스 모두 UTF-8로 인코딩된다.


### 새로운 문자열 생성하기

`Vec<T>`에서 사용할 수 있는 많은 연산이 `String`에서도 동일하게 사용 가능하다. 이는 `String`이 실제로 바이트 벡터를 기반으로 구현된 래퍼이기 때문이다. 다만, 몇 가지 추가적인 보장, 제약, 그리고 기능이 더해져 있다. `Vec<T>`와 `String`에서 동일하게 작동하는 함수의 예로는 인스턴스를 생성하는 `new` 함수가 있다. 이는 리스트 8-11에서 확인할 수 있다.

<Listing number="8-11" caption="새로운 빈 `String` 생성하기">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-11/src/main.rs:here}}
```

</Listing>

이 코드는 `s`라는 빈 문자열을 생성한다. 이 문자열에 이후 데이터를 로드할 수 있다. 종종 초기 데이터를 가지고 문자열을 시작하고 싶을 때가 있다. 이 경우 `to_string` 메서드를 사용한다. 이 메서드는 `Display` 트레잇을 구현한 모든 타입에서 사용할 수 있으며, 문자열 리터럴도 이에 해당한다. 리스트 8-12는 두 가지 예를 보여준다.

<Listing number="8-12" caption="`to_string` 메서드를 사용해 문자열 리터럴로부터 `String` 생성하기">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-12/src/main.rs:here}}
```

</Listing>

이 코드는 `initial contents`라는 내용을 가진 문자열을 생성한다.

또한 `String::from` 함수를 사용해 문자열 리터럴로부터 `String`을 생성할 수도 있다. 리스트 8-13의 코드는 `to_string`을 사용한 리스트 8-12의 코드와 동일한 기능을 수행한다.

<Listing number="8-13" caption="`String::from` 함수를 사용해 문자열 리터럴로부터 `String` 생성하기">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-13/src/main.rs:here}}
```

</Listing>

문자열은 매우 다양한 용도로 사용되기 때문에, 문자열을 다루는 다양한 일반적인 API를 활용할 수 있다. 이는 우리에게 많은 선택지를 제공한다. 일부 API는 중복되어 보일 수 있지만, 각각의 API는 고유의 용도가 있다! 이 경우 `String::from`과 `to_string`은 동일한 기능을 수행하므로, 어떤 것을 선택할지는 스타일과 가독성의 문제이다.

문자열은 UTF-8로 인코딩되어 있으므로, 올바르게 인코딩된 모든 데이터를 포함할 수 있다. 이는 리스트 8-14에서 확인할 수 있다.

<Listing number="8-14" caption="다양한 언어의 인사말을 문자열에 저장하기">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:here}}
```

</Listing>

이 모든 값들은 유효한 `String` 값이다.


### 문자열 업데이트

`String`은 `Vec<T>`와 마찬가지로 크기가 늘어나고 내용이 변경될 수 있다. 더 많은 데이터를 추가하면 크기가 증가한다. 또한, `+` 연산자나 `format!` 매크로를 사용해 `String` 값을 간편하게 연결할 수 있다.


#### `push_str`과 `push`를 사용해 문자열에 추가하기

`push_str` 메서드를 사용하면 문자열 슬라이스를 추가하여 `String`을 확장할 수 있다. 이는 Listing 8-15에서 확인할 수 있다.

<Listing number="8-15" caption="`push_str` 메서드를 사용해 문자열 슬라이스를 `String`에 추가하기">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-15/src/main.rs:here}}
```

</Listing>

이 두 줄의 코드를 실행한 후, `s`는 `foobar`를 포함하게 된다. `push_str` 메서드는 문자열 슬라이스를 인자로 받는데, 이는 매개변수의 소유권을 가져갈 필요가 없기 때문이다. 예를 들어, Listing 8-16의 코드에서는 `s2`의 내용을 `s1`에 추가한 후에도 `s2`를 계속 사용할 수 있다.

<Listing number="8-16" caption="문자열 슬라이스를 `String`에 추가한 후에도 사용하기">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-16/src/main.rs:here}}
```

</Listing>

만약 `push_str` 메서드가 `s2`의 소유권을 가져갔다면, 마지막 줄에서 `s2`의 값을 출력할 수 없었을 것이다. 하지만 이 코드는 예상대로 동작한다!

`push` 메서드는 단일 문자를 인자로 받아 `String`에 추가한다. Listing 8-17은 `push` 메서드를 사용해 문자 _l_ 을 `String`에 추가하는 예제를 보여준다.

<Listing number="8-17" caption="`push` 메서드를 사용해 `String`에 한 문자 추가하기">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-17/src/main.rs:here}}
```

</Listing>

결과적으로, `s`는 `lol`을 포함하게 된다.


#### `+` 연산자와 `format!` 매크로를 사용한 문자열 결합

두 개의 기존 문자열을 결합해야 하는 경우가 종종 있다. 이를 수행하는 한 가지 방법은 `+` 연산자를 사용하는 것이다. 이는 리스트 8-18에서 확인할 수 있다.

<Listing number="8-18" caption="두 개의 `String` 값을 결합하여 새로운 `String` 값을 생성하기 위해 `+` 연산자 사용">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-18/src/main.rs:here}}
```

</Listing>

문자열 `s3`은 `Hello, world!`를 포함한다. `s1`이 더 이상 유효하지 않은 이유와 `s2`에 대한 참조를 사용한 이유는 `+` 연산자를 사용할 때 호출되는 메서드의 시그니처와 관련이 있다. `+` 연산자는 `add` 메서드를 사용하며, 이 메서드의 시그니처는 다음과 같다:

```rust,ignore
fn add(self, s: &str) -> String {
```

표준 라이브러리에서 `add`는 제네릭과 연관 타입을 사용해 정의된다. 여기서는 구체적인 타입을 대입했는데, 이는 `String` 값으로 이 메서드를 호출할 때 발생한다. 제네릭에 대해서는 10장에서 자세히 다룬다. 이 시그니처는 `+` 연산자의 복잡한 부분을 이해하기 위한 단서를 제공한다.

먼저, `s2`에는 `&`가 붙어있는데, 이는 두 번째 문자열의 _참조_를 첫 번째 문자열에 추가한다는 의미다. 이는 `add` 함수의 `s` 매개변수 때문이다. `String`에 `&str`만 추가할 수 있으며, 두 `String` 값을 함께 추가할 수는 없다. 그런데 `&s2`의 타입은 `add`의 두 번째 매개변수로 지정된 `&str`이 아니라 `&String`이다. 그렇다면 리스트 8-18이 왜 컴파일될까?

`add` 호출에서 `&s2`를 사용할 수 있는 이유는 컴파일러가 `&String` 인수를 `&str`로 _강제 변환_할 수 있기 때문이다. `add` 메서드를 호출할 때 Rust는 _역참조 강제 변환_을 사용하며, 여기서 `&s2`를 `&s2[..]`로 변환한다. 역참조 강제 변환에 대해서는 15장에서 더 깊이 다룬다. `add`는 `s` 매개변수의 소유권을 가지지 않기 때문에, 이 작업 이후에도 `s2`는 여전히 유효한 `String`이다.

두 번째로, 시그니처에서 `add`가 `self`의 소유권을 가져간다는 것을 알 수 있다. 이는 `self`에 `&`가 없기 때문이다. 이는 리스트 8-18에서 `s1`이 `add` 호출로 이동되고 이후에는 더 이상 유효하지 않음을 의미한다. 따라서 `let s3 = s1 + &s2;`는 두 문자열을 복사하여 새로운 문자열을 생성하는 것처럼 보이지만, 실제로는 `s1`의 소유권을 가져가고 `s2`의 내용을 복사한 후 결과의 소유권을 반환한다. 즉, 많은 복사가 일어나는 것처럼 보이지만 실제로는 그렇지 않다. 구현은 복사보다 더 효율적이다.

여러 문자열을 결합해야 하는 경우, `+` 연산자의 동작은 다루기 어려워진다:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-01-concat-multiple-strings/src/main.rs:here}}
```

이 시점에서 `s`는 `tic-tac-toe`가 된다. 모든 `+`와 `"` 문자 때문에 무슨 일이 일어나고 있는지 파악하기 어렵다. 더 복잡한 방식으로 문자열을 결합해야 한다면, 대신 `format!` 매크로를 사용할 수 있다:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-02-format/src/main.rs:here}}
```

이 코드 또한 `s`를 `tic-tac-toe`로 설정한다. `format!` 매크로는 `println!`과 유사하게 동작하지만, 출력을 화면에 표시하는 대신 내용을 담은 `String`을 반환한다. `format!`을 사용한 코드 버전은 훨씬 읽기 쉽고, `format!` 매크로가 생성하는 코드는 참조를 사용하기 때문에 이 호출은 어떤 매개변수의 소유권도 가져가지 않는다.


### 문자열 인덱싱

다른 많은 프로그래밍 언어에서는 문자열의 개별 문자를 인덱스를 통해 접근하는 것이 일반적이고 유효한 작업이다. 하지만 Rust에서 문자열의 일부를 인덱싱 문법을 사용해 접근하려고 하면 오류가 발생한다. 다음은 유효하지 않은 코드 예제이다.

<Listing number="8-19" caption="String에 인덱싱 문법을 사용하려는 시도">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-19/src/main.rs:here}}
```

</Listing>

이 코드는 다음과 같은 오류를 발생시킨다:

```console
{{#include ../listings/ch08-common-collections/listing-08-19/output.txt}}
```

오류 메시지와 설명을 통해 알 수 있듯이, Rust의 문자열은 인덱싱을 지원하지 않는다. 그렇다면 왜 그럴까? 이 질문에 답하려면 Rust가 문자열을 메모리에 어떻게 저장하는지 알아야 한다.


#### 내부 표현

`String`은 `Vec<u8>`을 감싼 래퍼다. 리스트 8-14에서 제대로 인코딩된 UTF-8 예제 문자열을 살펴보자. 먼저 이 예제를 보자:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:spanish}}
```

이 경우 `len`은 `4`가 되며, 이는 문자열 `"Hola"`를 저장하는 벡터가 4바이트 길이라는 것을 의미한다. 이 문자열의 각 글자는 UTF-8로 인코딩될 때 1바이트를 차지한다. 그러나 다음 줄은 조금 놀라울 수 있다(이 문자열은 숫자 3이 아니라 키릴 문자 대문자 _Ze_로 시작한다는 점에 주목하라):

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:russian}}
```

이 문자열의 길이를 묻는다면, 아마 12라고 답할 것이다. 그러나 Rust의 답은 24다. 이는 "Здравствуйте"를 UTF-8로 인코딩하는 데 필요한 바이트 수이며, 이 문자열의 각 유니코드 스칼라 값이 2바이트를 차지하기 때문이다. 따라서 문자열의 바이트 인덱스가 항상 유효한 유니코드 스칼라 값과 일치하지는 않는다. 이를 확인하기 위해 다음의 유효하지 않은 Rust 코드를 살펴보자:

```rust,ignore,does_not_compile
let hello = "Здравствуйте";
let answer = &hello[0];
```

이미 알고 있듯이, `answer`는 첫 번째 글자인 `З`가 아니다. UTF-8로 인코딩된 `З`의 첫 번째 바이트는 `208`이고 두 번째 바이트는 `151`이므로, `answer`는 사실 `208`이어야 할 것 같다. 그러나 `208`은 단독으로 유효한 문자가 아니다. 이 문자열의 첫 번째 글자를 요청했을 때 `208`을 반환하는 것은 사용자가 원하는 결과가 아닐 것이다. 하지만 Rust가 바이트 인덱스 0에서 가진 데이터는 이것뿐이다. 사용자는 일반적으로 바이트 값을 원하지 않는다. 문자열이 라틴 문자만 포함하더라도 마찬가지다: `&"hi"[0]`이 바이트 값을 반환하는 유효한 코드였다면, `h`가 아니라 `104`를 반환했을 것이다.

따라서 Rust는 예상치 못한 값을 반환하고 즉시 발견되지 않을 수 있는 버그를 방지하기 위해, 이 코드를 아예 컴파일하지 않고 개발 과정 초기에 오해를 방지한다.


#### 바이트, 스칼라 값, 그리고 그래핌 클러스터! 이해하기

UTF-8과 관련해 Rust에서는 문자열을 세 가지 방식으로 바라볼 수 있다. 바이트, 스칼라 값, 그리고 그래핌 클러스터(일반적으로 '글자'라고 부르는 것에 가장 가까운 개념)가 그것이다.

힌디어 단어 "नमस्ते"를 데바나가리 문자로 작성할 때, 이 문자열은 다음과 같은 `u8` 값의 벡터로 저장된다:

```text
[224, 164, 168, 224, 164, 174, 224, 164, 184, 224, 165, 141, 224, 164, 164,
224, 165, 135]
```

이 데이터는 총 18바이트로, 컴퓨터가 최종적으로 저장하는 방식이다. 이 데이터를 Rust의 `char` 타입인 유니코드 스칼라 값으로 보면 다음과 같다:

```text
['न', 'म', 'स', '्', 'त', 'े']
```

여기에는 6개의 `char` 값이 있지만, 네 번째와 여섯 번째는 글자가 아니다. 이들은 독립적으로는 의미가 없는 발음 구별 기호다. 마지막으로, 이 데이터를 그래핌 클러스터로 보면 힌디어 단어를 구성하는 네 개의 글자로 인식한다:

```text
["न", "म", "स्", "ते"]
```

Rust는 컴퓨터가 저장한 원시 문자열 데이터를 다양한 방식으로 해석할 수 있도록 지원한다. 이를 통해 각 프로그램은 데이터가 어떤 인간의 언어로 되어 있든 상관없이 필요한 해석 방식을 선택할 수 있다.

Rust가 `String`에 인덱스를 사용해 문자를 가져오는 것을 허용하지 않는 마지막 이유는, 인덱싱 연산이 항상 일정한 시간(O(1)) 내에 수행될 것으로 기대되기 때문이다. 그러나 `String`의 경우 이 성능을 보장할 수 없다. Rust는 인덱스까지 유효한 문자가 몇 개인지 확인하기 위해 처음부터 내용을 순회해야 하기 때문이다.


### 문자열 슬라이싱

문자열을 인덱스로 접근하는 것은 일반적으로 좋은 방법이 아니다. 문자열 인덱싱 연산의 반환 타입이 무엇인지 명확하지 않기 때문이다. 바이트 값, 문자, 그래핀 클러스터, 문자열 슬라이스 중 무엇을 반환해야 할지 애매하다. 따라서 Rust에서는 인덱스를 사용해 문자열 슬라이스를 생성하려면 더 명확하게 지정하도록 요구한다.

단일 숫자를 사용해 `[]`로 인덱싱하는 대신, 범위를 사용해 `[]`로 특정 바이트를 포함하는 문자열 슬라이스를 생성할 수 있다.

```rust
let hello = "Здравствуйте";

let s = &hello[0..4];
```

여기서 `s`는 문자열의 처음 4바이트를 포함하는 `&str` 타입이 된다. 앞서 언급했듯이, 이 문자들은 각각 2바이트를 차지하므로 `s`는 `Зд`가 된다.

만약 `&hello[0..1]`과 같이 문자 바이트의 일부만 슬라이스하려고 하면, Rust는 벡터에서 유효하지 않은 인덱스에 접근할 때와 마찬가지로 런타임에 패닉을 발생시킨다.

```console
{{#include ../listings/ch08-common-collections/output-only-01-not-char-boundary/output.txt}}
```

범위를 사용해 문자열 슬라이스를 생성할 때는 주의해야 한다. 그렇지 않으면 프로그램이 비정상 종료될 수 있다.


### 문자열을 순회하는 방법

문자열의 일부를 처리할 때는 문자를 다룰지 바이트를 다룰지 명확히 정하는 것이 중요하다. 유니코드 스칼라 값(Unicode scalar value)을 다루려면 `chars` 메서드를 사용한다. "Зд"에 `chars`를 호출하면 두 개의 `char` 타입 값으로 분리되어 반환된다. 그런 다음 결과를 순회하면서 각 요소에 접근할 수 있다:

```rust
for c in "Зд".chars() {
    println!("{c}");
}
```

이 코드는 다음과 같이 출력한다:

```text
З
д
```

반면 `bytes` 메서드는 각 원시 바이트를 반환한다. 이 방법은 특정 도메인에서 적합할 수 있다:

```rust
for b in "Зд".bytes() {
    println!("{b}");
}
```

이 코드는 해당 문자열을 구성하는 네 개의 바이트를 출력한다:

```text
208
151
208
180
```

하지만 유효한 유니코드 스칼라 값이 하나 이상의 바이트로 구성될 수 있다는 점을 반드시 기억해야 한다.

데바나가리 문자와 같은 그래핌 클러스터(grapheme cluster)를 문자열에서 추출하는 작업은 복잡하다. 따라서 이러한 기능은 표준 라이브러리에서 제공하지 않는다. 만약 이 기능이 필요하다면 [crates.io](https://crates.io/)<!-- ignore -->에서 관련 크레이트를 찾을 수 있다.


### 문자열은 단순하지 않다

요약하자면, 문자열은 복잡하다. 각 프로그래밍 언어는 이 복잡성을 프로그래머에게 어떻게 보여줄지 다른 선택을 한다. Rust는 모든 Rust 프로그램에서 `String` 데이터를 올바르게 처리하는 것을 기본 동작으로 선택했다. 이는 프로그래머가 UTF-8 데이터를 처음부터 더 신경 써서 처리해야 한다는 것을 의미한다. 이러한 트레이드오프는 다른 프로그래밍 언어에서는 드러나지 않는 문자열의 복잡성을 더 많이 노출시키지만, 개발 주기 후반에 비ASCII 문자와 관련된 오류를 처리해야 하는 상황을 방지한다.

좋은 소식은 표준 라이브러리가 `String`과 `&str` 타입을 기반으로 이러한 복잡한 상황을 올바르게 처리할 수 있는 많은 기능을 제공한다는 것이다. 문자열 내에서 검색을 수행하는 `contains`나 문자열의 일부를 다른 문자열로 대체하는 `replace`와 같은 유용한 메서드에 대한 문서를 꼭 확인해 보자.

이제 조금 덜 복잡한 주제인 해시 맵으로 넘어가 보자!


