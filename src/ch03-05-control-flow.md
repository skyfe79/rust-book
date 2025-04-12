## 제어 흐름

조건이 `true`인지에 따라 특정 코드를 실행하거나, 조건이 `true`인 동안 코드를 반복적으로 실행하는 기능은 대부분의 프로그래밍 언어에서 기본적인 구성 요소이다. Rust 코드의 실행 흐름을 제어하는 가장 일반적인 구조는 `if` 표현식과 반복문(loop)이다.


### `if` 표현식

`if` 표현식을 사용하면 조건에 따라 코드를 분기할 수 있다. 조건을 지정하고 "이 조건이 충족되면 이 코드 블록을 실행하고, 조건이 충족되지 않으면 이 코드 블록을 실행하지 않는다"고 명시한다.

`if` 표현식을 살펴보기 위해 _projects_ 디렉토리에 _branches_라는 새 프로젝트를 생성한다. _src/main.rs_ 파일에 다음 코드를 입력한다:

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/src/main.rs}}
```

모든 `if` 표현식은 `if` 키워드로 시작하며, 그 뒤에 조건이 온다. 이 경우 조건은 변수 `number`의 값이 5보다 작은지 확인한다. 조건이 `true`일 때 실행할 코드 블록은 조건 바로 뒤에 중괄호로 감싸서 작성한다. `if` 표현식에서 조건과 관련된 코드 블록은 때때로 _arms_(가지)라고 부르며, 이는 2장의 [“추측한 값과 비밀번호 비교하기”][comparing-the-guess-to-the-secret-number]<!-- ignore --> 섹션에서 다룬 `match` 표현식의 가지와 유사하다.

선택적으로 `else` 표현식을 포함할 수 있으며, 여기서는 조건이 `false`일 때 실행할 대체 코드 블록을 제공하기 위해 `else`를 사용했다. `else` 표현식을 제공하지 않고 조건이 `false`인 경우, 프로그램은 `if` 블록을 건너뛰고 다음 코드로 이동한다.

이 코드를 실행하면 다음과 같은 출력을 확인할 수 있다:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/output.txt}}
```

이제 `number`의 값을 변경하여 조건이 `false`가 되도록 해보자:

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/src/main.rs:here}}
```

프로그램을 다시 실행하고 출력을 확인한다:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/output.txt}}
```

또한 이 코드에서 조건은 반드시 `bool` 타입이어야 한다. 조건이 `bool` 타입이 아닌 경우 오류가 발생한다. 예를 들어, 다음 코드를 실행해보자:

<span class="filename">파일명: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/src/main.rs}}
```

이번에는 `if` 조건이 `3`으로 평가되며, Rust는 오류를 발생시킨다:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/output.txt}}
```

오류는 Rust가 `bool` 타입을 기대했지만 정수를 받았다는 것을 나타낸다. Ruby나 JavaScript와 같은 언어와 달리 Rust는 비불리언 타입을 자동으로 불리언으로 변환하지 않는다. 명시적으로 `if` 조건에 불리언 값을 제공해야 한다. 예를 들어, `if` 코드 블록이 숫자가 `0`이 아닐 때만 실행되도록 하려면 `if` 표현식을 다음과 같이 변경할 수 있다:

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-29-if-not-equal-0/src/main.rs}}
```

이 코드를 실행하면 `number was something other than zero`가 출력된다.


#### 여러 조건을 `else if`로 처리하기

`if`와 `else`를 조합하여 `else if` 표현식으로 여러 조건을 처리할 수 있다. 예를 들어:

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/src/main.rs}}
```

이 프로그램은 네 가지 가능한 경로를 가진다. 실행한 후 다음과 같은 출력을 확인할 수 있다:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/output.txt}}
```

이 프로그램이 실행되면, 각 `if` 표현식을 순서대로 확인하고 조건이 `true`로 평가되는 첫 번째 본문을 실행한다. 6은 2로 나누어 떨어지지만, `number is divisible by 2`라는 출력이 나타나지 않는다. 또한 `else` 블록의 `number is not divisible by 4, 3, or 2`라는 텍스트도 보이지 않는다. 이는 Rust가 첫 번째 `true` 조건에 해당하는 블록만 실행하고, 한 번 조건을 찾으면 나머지는 확인하지 않기 때문이다.

너무 많은 `else if` 표현식을 사용하면 코드가 복잡해질 수 있다. 따라서 `else if`가 여러 개 있다면 코드를 리팩토링하는 것이 좋다. 6장에서는 이러한 경우에 유용한 Rust의 강력한 분기 구조인 `match`를 소개한다.


#### `let` 문에서 `if` 사용하기

`if`는 표현식이므로, `let` 문의 오른쪽에 사용하여 결과를 변수에 할당할 수 있다. Listing 3-2에서 이를 확인할 수 있다.

<Listing number="3-2" file-name="src/main.rs" caption="`if` 표현식의 결과를 변수에 할당하기">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-02/src/main.rs}}
```

</Listing>

`number` 변수는 `if` 표현식의 결과에 따라 값이 결정된다. 이 코드를 실행하면 다음과 같은 결과를 볼 수 있다:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-02/output.txt}}
```

코드 블록은 마지막 표현식의 값으로 평가되며, 숫자 자체도 표현식이다. 이 경우, 전체 `if` 표현식의 값은 실행되는 코드 블록에 따라 달라진다. 이는 `if`의 각 분기에서 반환될 수 있는 값의 타입이 동일해야 한다는 것을 의미한다. Listing 3-2에서는 `if` 분기와 `else` 분기의 결과가 모두 `i32` 정수였다. 만약 타입이 일치하지 않으면, 다음과 같은 예제에서 볼 수 있듯이 오류가 발생한다:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/src/main.rs}}
```

이 코드를 컴파일하려고 하면 오류가 발생한다. `if` 분기와 `else` 분기의 값 타입이 호환되지 않으며, Rust는 프로그램 내에서 문제가 발생한 정확한 위치를 알려준다:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/output.txt}}
```

`if` 블록의 표현식은 정수로 평가되고, `else` 블록의 표현식은 문자열로 평가된다. 이는 변수가 단일 타입을 가져야 하며, Rust는 컴파일 시점에 `number` 변수의 타입을 명확히 알아야 하기 때문에 작동하지 않는다. `number`의 타입을 알면 컴파일러는 `number`를 사용하는 모든 곳에서 타입이 유효한지 검증할 수 있다. 만약 `number`의 타입이 런타임에 결정된다면 Rust는 이를 수행할 수 없을 것이다. 컴파일러는 더 복잡해지고, 변수에 대해 여러 가상의 타입을 추적해야 하기 때문에 코드에 대한 보장이 줄어들 것이다.


### 반복문 활용하기

특정 코드 블록을 여러 번 실행해야 할 때가 있다. 이를 위해 Rust는 여러 종류의 **반복문**을 제공한다. 반복문은 코드 블록을 처음부터 끝까지 실행한 후, 다시 처음으로 돌아가 반복한다. 반복문을 실험해보기 위해 _loops_라는 새로운 프로젝트를 만들어보자.

Rust는 세 가지 종류의 반복문을 지원한다: `loop`, `while`, `for`. 각각의 반복문을 하나씩 살펴보자.


#### `loop`로 코드 반복하기

`loop` 키워드는 코드 블록을 무한히 반복하거나 명시적으로 중단할 때까지 계속 실행하도록 지시한다.

예를 들어, _loops_ 디렉토리의 _src/main.rs_ 파일을 다음과 같이 수정해본다:

<span class="filename">파일명: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-loop/src/main.rs}}
```

이 프로그램을 실행하면 `again!`이 계속 출력되며, 수동으로 프로그램을 중단할 때까지 반복된다. 대부분의 터미널에서는 <kbd>ctrl</kbd>-<kbd>c</kbd> 단축키를 사용해 무한 루프에 빠진 프로그램을 중단할 수 있다. 직접 시도해보자:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-32-loop
cargo run
CTRL-C
-->

```console
$ cargo run
   Compiling loops v0.1.0 (file:///projects/loops)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.08s
     Running `target/debug/loops`
again!
again!
again!
again!
^Cagain!
```

`^C` 기호는 <kbd>ctrl</kbd>-<kbd>c</kbd>를 누른 위치를 나타낸다. `^C` 이후에 `again!`이 출력될 수도 있고 그렇지 않을 수도 있는데, 이는 인터럽트 시그널을 받았을 때 코드가 루프의 어느 위치에 있었는지에 따라 달라진다.

다행히 Rust는 코드를 통해 루프를 탈출할 수 있는 방법도 제공한다. 루프 내부에 `break` 키워드를 사용하면 프로그램이 언제 루프 실행을 멈출지 지정할 수 있다. 이전에 2장의 [“정답을 맞힌 후 종료하기”][quitting-after-a-correct-guess]<!-- ignore --> 섹션에서 사용자가 정답을 맞혀 게임에서 승리했을 때 프로그램을 종료하기 위해 이 방법을 사용했던 것을 떠올려보자.

또한, 추측 게임에서 `continue`를 사용했는데, 이는 루프 내에서 남은 코드를 건너뛰고 다음 반복으로 넘어가도록 지시한다.


#### 루프에서 값 반환하기

`loop`의 주요 용도 중 하나는 실패할 가능성이 있는 작업을 반복적으로 시도하는 것이다. 예를 들어 스레드가 작업을 완료했는지 확인하는 경우가 이에 해당한다. 이때 작업의 결과를 루프 밖의 코드로 전달해야 할 수도 있다. 이를 위해 루프를 멈추는 `break` 표현식 뒤에 반환할 값을 추가하면 된다. 이 값은 루프 밖으로 반환되어 코드에서 사용할 수 있다. 다음 예제를 보자:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-33-return-value-from-loop/src/main.rs}}
```

루프를 시작하기 전에 `counter`라는 변수를 선언하고 `0`으로 초기화한다. 그다음 루프에서 반환된 값을 저장할 `result` 변수를 선언한다. 루프가 반복될 때마다 `counter` 변수에 `1`을 더하고, `counter`가 `10`인지 확인한다. `counter`가 `10`이 되면 `break` 키워드와 함께 `counter * 2` 값을 반환한다. 루프가 끝난 후 `result`에 값을 할당하는 문장을 세미콜론으로 마친다. 마지막으로 `result`의 값을 출력하는데, 이 경우 `20`이 출력된다.

또한 루프 내부에서 `return`을 사용할 수도 있다. `break`는 현재 루프만 종료하지만, `return`은 현재 함수를 완전히 종료한다.


#### 여러 루프를 구분하기 위한 루프 라벨

루프 안에 또 다른 루프가 중첩된 경우, `break`와 `continue`는 해당 위치에서 가장 안쪽에 있는 루프에 적용된다. 선택적으로 루프에 _루프 라벨_을 지정할 수 있으며, 이 라벨을 `break`나 `continue`와 함께 사용하면 해당 키워드가 가장 안쪽 루프가 아닌 라벨이 지정된 루프에 적용된다. 루프 라벨은 작은따옴표(`'`)로 시작해야 한다. 다음은 두 개의 중첩된 루프를 사용한 예제다:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/src/main.rs}}
```

바깥쪽 루프는 `'counting_up`이라는 라벨을 가지며, 0부터 2까지 카운트업한다. 라벨이 없는 안쪽 루프는 10부터 9까지 카운트다운한다. 라벨을 지정하지 않은 첫 번째 `break`는 안쪽 루프만 종료한다. `break 'counting_up;` 문은 바깥쪽 루프를 종료한다. 이 코드는 다음과 같이 출력된다:

```console
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/output.txt}}
```


#### `while`을 활용한 조건부 반복

프로그램은 종종 반복문 안에서 조건을 평가해야 한다. 조건이 `true`인 동안 반복문이 실행된다. 조건이 더 이상 `true`가 아니면 프로그램은 `break`를 호출해 반복문을 멈춘다. `loop`, `if`, `else`, `break`를 조합해 이런 동작을 구현할 수 있다. 원한다면 지금 바로 프로그램에서 시도해 볼 수 있다. 하지만 이 패턴은 너무 흔해서 Rust는 이를 위해 `while` 루프라는 내장 언어 구문을 제공한다. 예제 3-3에서 `while`을 사용해 프로그램을 세 번 반복하며 매번 카운트다운을 하고, 반복문이 끝난 후 메시지를 출력하고 종료한다.

<Listing number="3-3" file-name="src/main.rs" caption="조건이 `true`인 동안 코드를 실행하기 위해 `while` 루프 사용">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-03/src/main.rs}}
```

</Listing>

이 구문은 `loop`, `if`, `else`, `break`를 사용할 때 필요한 많은 중첩을 제거하고 코드를 더 명확하게 만든다. 조건이 `true`인 동안 코드가 실행되고, 그렇지 않으면 반복문을 빠져나온다.


#### `for` 루프를 사용해 컬렉션 순회하기

컬렉션의 요소를 순회할 때 `while` 구문을 사용할 수도 있다. 예를 들어, 아래 코드는 배열 `a`의 각 요소를 출력한다.

<Listing number="3-4" file-name="src/main.rs" caption="`while` 루프를 사용해 컬렉션의 각 요소 순회하기">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-04/src/main.rs}}
```

</Listing>

이 코드는 배열의 요소를 처음부터 끝까지 순회한다. 인덱스 `0`에서 시작해 배열의 마지막 인덱스에 도달할 때까지(`index < 5`가 `true`인 동안) 반복한다. 이 코드를 실행하면 배열의 모든 요소가 출력된다:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-04/output.txt}}
```

예상대로 배열의 다섯 값이 모두 터미널에 출력된다. `index` 값이 `5`에 도달할 수는 있지만, 배열에서 여섯 번째 값을 가져오려고 시도하기 전에 루프가 종료된다.

하지만 이 방식은 오류가 발생하기 쉽다. 인덱스 값이나 조건이 잘못되면 프로그램이 패닉 상태에 빠질 수 있다. 예를 들어, 배열 `a`를 네 개의 요소로 변경했는데 조건을 `while index < 4`로 업데이트하지 않으면 코드가 패닉 상태에 빠진다. 또한 이 방식은 느린데, 컴파일러가 매 반복마다 인덱스가 배열의 범위 내에 있는지 조건을 확인하는 런타임 코드를 추가하기 때문이다.

더 간결한 대안으로 `for` 루프를 사용해 컬렉션의 각 항목에 대해 코드를 실행할 수 있다. `for` 루프는 아래 코드와 같다.

<Listing number="3-5" file-name="src/main.rs" caption="`for` 루프를 사용해 컬렉션의 각 요소 순회하기">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-05/src/main.rs}}
```

</Listing>

이 코드를 실행하면 Listing 3-4와 동일한 결과가 출력된다. 더 중요한 점은 코드의 안전성이 높아졌고, 배열의 끝을 벗어나거나 일부 항목을 놓치는 버그가 발생할 가능성이 사라졌다는 것이다.

`for` 루프를 사용하면 배열의 값 개수를 변경할 때 다른 코드를 수정할 필요가 없다. Listing 3-4에서 사용한 방식과 달리 `for` 루프는 이러한 문제를 자동으로 처리한다.

`for` 루프의 안전성과 간결성 덕분에 Rust에서 가장 흔히 사용되는 루프 구문이다. Listing 3-3에서 `while` 루프를 사용한 카운트다운 예제처럼 특정 횟수만큼 코드를 실행해야 하는 경우에도 대부분의 Rust 개발자는 `for` 루프를 사용한다. 이를 위해 표준 라이브러리에서 제공하는 `Range`를 사용할 수 있다. `Range`는 시작 숫자부터 다른 숫자 직전까지의 모든 숫자를 순서대로 생성한다.

`for` 루프와 아직 다루지 않은 `rev` 메서드를 사용해 범위를 역순으로 바꾸면 카운트다운 코드는 아래와 같다:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-34-for-range/src/main.rs}}
```

이 코드가 더 깔끔하지 않은가?


## 요약

여러분은 이 장을 끝까지 완료했다! 이번 장에서는 변수, 스칼라와 복합 데이터 타입, 함수, 주석, `if` 표현식, 그리고 반복문에 대해 배웠다. 이 장에서 다룬 개념을 연습하기 위해 다음 프로그램을 만들어 보자:

- 화씨와 섭씨 온도를 변환한다.
- *n*번째 피보나치 수를 생성한다.
- 크리스마스 캐롤 "The Twelve Days of Christmas"의 가사를 출력한다. 이때 노래의 반복 구조를 활용한다.

이제 다음 단계로 넘어갈 준비가 되었다면, Rust에서 다른 프로그래밍 언어에서는 흔히 볼 수 없는 개념인 '소유권'에 대해 이야기할 것이다.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[quitting-after-a-correct-guess]: ch02-00-guessing-game-tutorial.html#quitting-after-a-correct-guess


