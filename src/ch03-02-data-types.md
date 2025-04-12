## 데이터 타입

Rust의 모든 값은 특정 _데이터 타입_을 가지며, 이는 Rust에게 어떤 종류의 데이터인지 알려주어 해당 데이터를 어떻게 처리할지 결정한다. 여기서는 두 가지 데이터 타입 하위 집합인 스칼라(scalar)와 복합(compound) 타입을 살펴본다.

Rust는 _정적 타입_ 언어라는 점을 기억하자. 이는 컴파일 시점에 모든 변수의 타입을 알아야 한다는 의미다. 컴파일러는 일반적으로 값과 사용 방식을 기반으로 우리가 사용하려는 타입을 추론할 수 있다. 하지만 [“추리한 값과 비밀번호 비교하기”][comparing-the-guess-to-the-secret-number]<!-- ignore --> 섹션에서 `parse`를 사용해 `String`을 숫자 타입으로 변환할 때와 같이 여러 타입이 가능한 경우에는 다음과 같이 타입 어노테이션을 추가해야 한다:

```rust
let guess: u32 = "42".parse().expect("숫자가 아닙니다!");
```

위 코드에서 `: u32` 타입 어노테이션을 추가하지 않으면 Rust는 다음과 같은 에러를 표시한다. 이는 컴파일러가 우리가 사용하려는 타입을 알기 위해 더 많은 정보가 필요하다는 의미다:

```console
{{#include ../listings/ch03-common-programming-concepts/output-only-01-no-type-annotations/output.txt}}
```

다른 데이터 타입에 대해서도 다양한 타입 어노테이션을 확인할 수 있다.


### 스칼라 타입

_스칼라_ 타입은 단일 값을 나타낸다. Rust는 네 가지 주요 스칼라 타입을 제공한다: 정수, 부동소수점 숫자, 불리언, 그리고 문자. 다른 프로그래밍 언어에서도 이러한 타입을 접해봤을 것이다. 이제 Rust에서 이 타입들이 어떻게 동작하는지 살펴보자.


#### 정수 타입

_정수_는 소수 부분이 없는 숫자를 말한다. 2장에서 `u32` 타입을 사용했는데, 이 타입 선언은 해당 값이 32비트 공간을 차지하는 부호 없는 정수임을 나타낸다. 부호 있는 정수 타입은 `u` 대신 `i`로 시작한다. 표 3-1은 Rust에 내장된 정수 타입을 보여준다. 이 중 어떤 타입을 사용해도 정수 값의 타입을 선언할 수 있다.

<span class="caption">표 3-1: Rust의 정수 타입</span>

| 길이   | 부호 있음 | 부호 없음 |
| ------ | --------- | --------- |
| 8비트  | `i8`      | `u8`      |
| 16비트 | `i16`     | `u16`     |
| 32비트 | `i32`     | `u32`     |
| 64비트 | `i64`     | `u64`     |
| 128비트| `i128`    | `u128`    |
| 아키텍처 | `isize` | `usize`   |

각 타입은 부호 있음 또는 부호 없음으로 나뉘며 명시적인 크기를 가진다. _부호 있음_과 _부호 없음_은 숫자가 음수가 될 수 있는지 여부를 나타낸다. 즉, 숫자에 부호가 필요한지(부호 있음) 아니면 항상 양수여서 부호 없이 표현할 수 있는지(부호 없음)를 의미한다. 종이에 숫자를 쓸 때를 생각해보면, 부호가 중요한 경우에는 숫자에 더하기 또는 빼기 기호를 붙이지만, 숫자가 양수임이 명확한 경우에는 부호를 생략한다. 부호 있는 숫자는 [2의 보수][twos-complement]<!-- ignore --> 표현법을 사용해 저장된다.

각 부호 있는 타입은 −(2<sup>n − 1</sup>)부터 2<sup>n − 1</sup> − 1까지의 숫자를 저장할 수 있으며, 여기서 _n_은 해당 타입이 사용하는 비트 수다. 예를 들어, `i8`은 −(2<sup>7</sup>)부터 2<sup>7</sup> − 1까지, 즉 −128부터 127까지의 숫자를 저장할 수 있다. 부호 없는 타입은 0부터 2<sup>n</sup> − 1까지의 숫자를 저장할 수 있으므로, `u8`은 0부터 2<sup>8</sup> − 1까지, 즉 0부터 255까지의 숫자를 저장할 수 있다.

또한, `isize`와 `usize` 타입은 프로그램이 실행되는 컴퓨터의 아키텍처에 따라 달라지며, 표에서 "아키텍처"로 표시된 부분이다. 64비트 아키텍처에서는 64비트를 사용하고, 32비트 아키텍처에서는 32비트를 사용한다.

정수 리터럴은 표 3-2에 나온 형태 중 어떤 것으로도 작성할 수 있다. 여러 숫자 타입이 가능한 숫자 리터럴의 경우, `57u8`과 같이 타입 접미사를 붙여 타입을 지정할 수 있다. 또한, 숫자 리터럴은 `_`를 시각적 구분자로 사용해 숫자를 더 읽기 쉽게 만들 수 있다. 예를 들어, `1_000`은 `1000`과 동일한 값을 가진다.

<span class="caption">표 3-2: Rust의 정수 리터럴</span>

| 숫자 리터럴      | 예시          |
| ---------------- | ------------- |
| 10진수           | `98_222`      |
| 16진수           | `0xff`        |
| 8진수            | `0o77`        |
| 2진수            | `0b1111_0000` |
| 바이트 (`u8`만)  | `b'A'`        |

그렇다면 어떤 정수 타입을 사용해야 할까? 확실하지 않다면 Rust의 기본값을 사용하는 것이 일반적으로 좋은 시작점이다. 정수 타입은 기본적으로 `i32`를 사용한다. `isize`나 `usize`를 사용하는 주요 상황은 어떤 종류의 컬렉션을 인덱싱할 때다.

> ##### 정수 오버플로우
>
> 0부터 255까지의 값을 저장할 수 있는 `u8` 타입의 변수가 있다고 가정해보자. 이 변수를 해당 범위를 벗어나는 값, 예를 들어 256으로 변경하려고 하면 _정수 오버플로우_가 발생하며, 이는 두 가지 동작 중 하나를 초래할 수 있다. 디버그 모드에서 컴파일할 때, Rust는 정수 오버플로우를 검사하며, 이 동작이 발생하면 런타임에 프로그램이 _패닉_을 일으키게 한다. Rust는 프로그램이 오류와 함께 종료될 때 _패닉_이라는 용어를 사용한다. 패닉에 대해서는 9장의 [“`panic!`을 사용한 복구 불가능한 오류”][unrecoverable-errors-with-panic]<!-- ignore --> 섹션에서 더 자세히 다룬다.
>
> `--release` 플래그와 함께 릴리스 모드로 컴파일할 때, Rust는 패닉을 일으키는 정수 오버플로우 검사를 포함하지 않는다. 대신, 오버플로우가 발생하면 Rust는 _2의 보수 래핑_을 수행한다. 간단히 말해, 타입이 저장할 수 있는 최대값보다 큰 값은 타입이 저장할 수 있는 최소값으로 "래핑"된다. `u8`의 경우, 값 256은 0이 되고, 257은 1이 되는 식이다. 프로그램은 패닉을 일으키지 않지만, 변수는 예상치 못한 값을 가질 수 있다. 정수 오버플로우의 래핑 동작에 의존하는 것은 오류로 간주된다.
>
> 오버플로우 가능성을 명시적으로 처리하려면, 기본 숫자 타입을 위한 표준 라이브러리에서 제공하는 다음과 같은 메서드 패밀리를 사용할 수 있다:
>
> - 모든 모드에서 래핑을 수행하는 `wrapping_*` 메서드, 예를 들어 `wrapping_add`.
> - 오버플로우가 발생하면 `None` 값을 반환하는 `checked_*` 메서드.
> - 값과 오버플로우 발생 여부를 나타내는 불리언 값을 반환하는 `overflowing_*` 메서드.
> - 값의 최소 또는 최대값에서 포화시키는 `saturating_*` 메서드.


#### 부동소수점 타입

Rust는 소수점이 있는 숫자인 _부동소수점 숫자_를 표현하기 위해 두 가지 기본 타입을 제공한다. Rust의 부동소수점 타입은 `f32`와 `f64`로, 각각 32비트와 64비트 크기를 가진다. 기본 타입은 `f64`인데, 현대 CPU에서는 `f32`와 거의 같은 속도를 내면서 더 높은 정밀도를 제공하기 때문이다. 모든 부동소수점 타입은 부호를 가진다.

다음은 부동소수점 숫자를 사용하는 예제이다:

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-06-floating-point/src/main.rs}}
```

부동소수점 숫자는 IEEE-754 표준에 따라 표현된다.


#### 숫자 연산

Rust는 모든 숫자 타입에 대해 기본적인 수학 연산을 지원한다. 덧셈, 뺄셈, 곱셈, 나눗셈, 그리고 나머지 연산이 포함된다. 정수 나눗셈의 경우, 0 방향으로 가장 가까운 정수로 버림 처리된다. 아래 코드는 `let` 문에서 각 숫자 연산을 어떻게 사용하는지 보여준다:

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-07-numeric-operations/src/main.rs}}
```

이 문장의 각 표현식은 수학 연산자를 사용하며, 단일 값으로 평가된 후 변수에 바인딩된다. [부록 B][appendix_b]<!-- ignore -->에는 Rust가 제공하는 모든 연산자 목록이 포함되어 있다.


#### 불리언 타입

대부분의 프로그래밍 언어와 마찬가지로, Rust에서 불리언 타입은 두 가지 가능한 값을 가진다: `true`와 `false`. 불리언은 1바이트 크기를 차지한다. Rust에서 불리언 타입은 `bool`로 지정한다. 예를 들어:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-08-boolean/src/main.rs}}
```

불리언 값을 사용하는 주요 방법은 `if` 표현식과 같은 조건문을 통해서다. Rust에서 `if` 표현식이 어떻게 동작하는지는 [“제어 흐름”][control-flow]<!-- ignore --> 섹션에서 다룬다.


#### 문자 타입

Rust의 `char` 타입은 언어에서 가장 기본적인 알파벳 타입이다. 다음은 `char` 값을 선언하는 몇 가지 예제이다:

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-09-char/src/main.rs}}
```

문자열 리터럴은 쌍따옴표를 사용하지만, `char` 리터럴은 작은따옴표를 사용한다는 점에 유의한다. Rust의 `char` 타입은 4바이트 크기이며, 유니코드 스칼라 값을 나타낸다. 이는 단순한 ASCII를 넘어 다양한 문자를 표현할 수 있음을 의미한다. 악센트가 있는 문자, 중국어, 일본어, 한국어 문자, 이모지, 그리고 너비가 없는 공백까지 모두 Rust에서 유효한 `char` 값이다. 유니코드 스칼라 값은 `U+0000`부터 `U+D7FF`, 그리고 `U+E000`부터 `U+10FFFF`까지 포함한다. 그러나 유니코드에서 "문자"는 실제로 개념이 아니기 때문에, 여러분이 생각하는 "문자"와 Rust의 `char`가 일치하지 않을 수 있다. 이 주제에 대해서는 8장의 ["문자열에 UTF-8 인코딩 텍스트 저장하기"][strings]<!-- ignore -->에서 자세히 다룰 것이다.


### 복합 타입(Compound Types)

**복합 타입**은 여러 값을 하나의 타입으로 묶을 수 있다. Rust는 두 가지 기본 복합 타입을 제공한다: 튜플(tuples)과 배열(arrays).


#### 튜플 타입

_튜플_은 다양한 타입의 값을 하나의 복합 타입으로 묶는 일반적인 방법이다. 튜플은 고정된 길이를 가지며, 한번 선언되면 크기를 늘리거나 줄일 수 없다.

튜플을 생성하려면 괄호 안에 쉼표로 구분된 값 목록을 작성한다. 튜플의 각 위치에는 타입이 있으며, 튜플 내의 서로 다른 값들의 타입이 같을 필요는 없다. 다음 예제에서는 선택적 타입 어노테이션을 추가했다:

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-10-tuples/src/main.rs}}
```

변수 `tup`은 튜플 전체에 바인딩된다. 튜플은 단일 복합 엘리먼트로 간주되기 때문이다. 튜플에서 개별 값을 추출하려면 패턴 매칭을 사용해 튜플 값을 구조 분해할 수 있다. 예를 들어 다음과 같다:

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-11-destructuring-tuples/src/main.rs}}
```

이 프로그램은 먼저 튜플을 생성하고 변수 `tup`에 바인딩한다. 그런 다음 `let`과 함께 패턴을 사용해 `tup`을 세 개의 개별 변수 `x`, `y`, `z`로 분해한다. 이를 _구조 분해_라고 부르며, 단일 튜플을 세 부분으로 나누는 과정이다. 마지막으로 프로그램은 `y`의 값인 `6.4`를 출력한다.

또한, 마침표(`.`) 뒤에 접근하려는 값의 인덱스를 사용해 튜플 요소에 직접 접근할 수도 있다. 예를 들어:

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-12-tuple-indexing/src/main.rs}}
```

이 프로그램은 튜플 `x`를 생성한 후 각 요소에 해당하는 인덱스를 사용해 튜플의 각 요소에 접근한다. 대부분의 프로그래밍 언어와 마찬가지로 튜플의 첫 번째 인덱스는 0이다.

값이 없는 튜플은 특별한 이름인 _유닛_을 가진다. 이 값과 해당 타입은 모두 `()`로 표기되며, 빈 값이나 빈 반환 타입을 나타낸다. 표현식이 다른 값을 반환하지 않으면 암묵적으로 유닛 값을 반환한다.


#### 배열 타입

여러 값을 담는 또 다른 방법은 _배열_을 사용하는 것이다. 튜플과 달리 배열의 모든 요소는 같은 타입이어야 한다. 다른 언어의 배열과는 다르게, Rust의 배열은 길이가 고정되어 있다.

배열의 값은 대괄호 안에 쉼표로 구분된 목록으로 작성한다:

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-13-arrays/src/main.rs}}
```

배열은 데이터를 스택에 할당하고 싶을 때 유용하다. 이는 지금까지 살펴본 다른 타입들과 마찬가지로, 힙이 아닌 스택에 데이터를 할당한다는 의미이다(스택과 힙에 대해서는 [4장][stack-and-heap]<!-- ignore -->에서 더 자세히 다룬다). 또는 요소의 개수가 항상 고정되어 있어야 할 때도 배열을 사용한다. 하지만 배열은 벡터 타입만큼 유연하지 않다. _벡터_는 표준 라이브러리에서 제공하는 유사한 컬렉션 타입으로, 크기가 늘어나거나 줄어들 수 있다. 배열과 벡터 중 어떤 것을 사용해야 할지 확신이 서지 않는다면, 대부분의 경우 벡터를 사용하는 것이 좋다. [8장][vectors]<!-- ignore -->에서 벡터에 대해 더 자세히 다룬다.

그러나 요소의 개수가 변하지 않을 것이라고 확신할 때는 배열이 더 유용하다. 예를 들어, 프로그램에서 월 이름을 사용한다면, 항상 12개의 요소를 포함할 것이므로 벡터보다는 배열을 사용할 가능성이 높다:

```rust
let months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];
```

배열의 타입은 대괄호 안에 각 요소의 타입, 세미콜론, 그리고 배열의 요소 개수를 순서대로 작성하여 표현한다:

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```

여기서 `i32`는 각 요소의 타입이다. 세미콜론 뒤의 숫자 `5`는 배열이 5개의 요소를 포함한다는 것을 나타낸다.

또한, 모든 요소를 같은 값으로 초기화할 수도 있다. 초기값을 지정한 뒤, 세미콜론과 배열의 길이를 대괄호 안에 작성하면 된다:

```rust
let a = [3; 5];
```

이렇게 하면 `a`라는 배열은 초기값으로 `3`을 가진 5개의 요소를 포함하게 된다. 이는 `let a = [3, 3, 3, 3, 3];`와 동일하지만, 더 간결한 표현 방식이다.


##### 배열 요소 접근

배열은 고정된 크기의 메모리 덩어리로, 스택에 할당할 수 있다. 배열의 요소는 인덱스를 사용해 접근할 수 있다. 예를 들면 다음과 같다:

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-14-array-indexing/src/main.rs}}
```

이 예제에서 `first`라는 변수는 배열의 인덱스 `[0]`에 있는 값 `1`을 가진다. `second`라는 변수는 배열의 인덱스 `[1]`에 있는 값 `2`를 가진다.


##### 잘못된 배열 요소 접근

배열의 끝을 넘어선 요소에 접근하려고 하면 어떤 일이 발생하는지 살펴보자. 2장의 숫자 맞추기 게임과 유사하게, 사용자로부터 배열의 인덱스를 입력받는 다음 코드를 실행한다고 가정해 보자:

<span class="filename">파일명: src/main.rs</span>

```rust,ignore,panics
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access/src/main.rs}}
```

이 코드는 성공적으로 컴파일된다. `cargo run`을 사용해 이 코드를 실행하고 `0`, `1`, `2`, `3`, 또는 `4`를 입력하면 프로그램은 해당 인덱스에 있는 배열의 값을 출력한다. 그러나 배열의 끝을 넘어선 숫자, 예를 들어 `10`을 입력하면 다음과 같은 출력을 확인할 수 있다:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access
cargo run
10
-->

```console
thread 'main' panicked at src/main.rs:19:19:
index out of bounds: the len is 5 but the index is 10
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

프로그램은 잘못된 값을 사용해 인덱싱을 시도하는 지점에서 _런타임_ 오류를 발생시켰다. 프로그램은 오류 메시지를 출력하고 마지막 `println!` 문을 실행하지 않은 채 종료되었다. Rust는 인덱싱을 통해 요소에 접근하려고 할 때, 지정한 인덱스가 배열의 길이보다 작은지 확인한다. 인덱스가 배열의 길이보다 크거나 같으면 Rust는 패닉을 발생시킨다. 이 검사는 런타임에 이루어져야 하는데, 특히 이 경우에는 컴파일러가 사용자가 나중에 코드를 실행할 때 어떤 값을 입력할지 알 수 없기 때문이다.

이는 Rust의 메모리 안전성 원칙이 실제로 작동하는 예시이다. 많은 저수준 언어에서는 이러한 검사를 수행하지 않으며, 잘못된 인덱스를 제공하면 유효하지 않은 메모리에 접근할 수 있다. Rust는 이와 같은 오류를 방지하기 위해 메모리 접근을 허용하고 계속 실행하는 대신 즉시 프로그램을 종료한다. 9장에서는 Rust의 오류 처리에 대해 더 자세히 다루며, 패닉을 발생시키지 않고 유효하지 않은 메모리 접근을 허용하지 않는 읽기 쉽고 안전한 코드를 작성하는 방법을 설명한다.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[twos-complement]: https://en.wikipedia.org/wiki/Two%27s_complement
[control-flow]: ch03-05-control-flow.html#control-flow
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[stack-and-heap]: ch04-01-what-is-ownership.html#the-stack-and-the-heap
[vectors]: ch08-01-vectors.html
[unrecoverable-errors-with-panic]: ch09-01-unrecoverable-errors-with-panic.html
[appendix_b]: appendix-02-operators.md


