## 함수

Rust 코드에서 함수는 매우 흔하게 사용된다. 여러분은 이미 언어에서 가장 중요한 함수 중 하나인 `main` 함수를 보았다. 이 함수는 많은 프로그램의 진입점이다. 또한 새로운 함수를 선언할 수 있는 `fn` 키워드도 보았다.

Rust 코드는 함수와 변수 이름에 관례적으로 _스네이크 케이스_를 사용한다. 스네이크 케이스는 모든 글자를 소문자로 쓰고 단어 사이에 밑줄을 넣는 방식이다. 다음은 함수 정의 예제가 포함된 프로그램이다:

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-16-functions/src/main.rs}}
```

Rust에서 함수를 정의하려면 `fn` 키워드 뒤에 함수 이름과 괄호를 붙인다. 중괄호는 함수의 시작과 끝을 컴파일러에게 알려준다.

정의한 함수는 이름 뒤에 괄호를 붙여 호출할 수 있다. `another_function`은 프로그램 내에 정의되어 있으므로 `main` 함수 안에서 호출할 수 있다. 소스 코드에서 `another_function`을 `main` 함수 _뒤에_ 정의했지만, 앞에 정의해도 상관없다. Rust는 함수가 어디에 정의되었는지 신경 쓰지 않는다. 단지 호출자가 볼 수 있는 스코프 안에 정의되어 있기만 하면 된다.

함수를 더 자세히 알아보기 위해 _functions_라는 이름의 새 바이너리 프로젝트를 시작해 보자. `another_function` 예제를 _src/main.rs_에 넣고 실행한다. 다음과 같은 출력을 볼 수 있다:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-16-functions/output.txt}}
```

`main` 함수에 나타나는 순서대로 코드가 실행된다. 먼저 "Hello, world!" 메시지가 출력되고, 그 다음 `another_function`이 호출되어 메시지가 출력된다.


### 매개변수

함수는 _매개변수_를 가질 수 있다. 매개변수는 함수 시그니처의 일부인 특별한 변수다. 함수가 매개변수를 가지면, 해당 매개변수에 구체적인 값을 전달할 수 있다. 엄밀히 말하면, 이 구체적인 값은 _인자_라고 부르지만, 일상적인 대화에서는 _매개변수_와 _인자_라는 용어를 혼용해서 사용하기도 한다. 이 용어들은 함수 정의에서의 변수를 가리키거나, 함수를 호출할 때 전달하는 구체적인 값을 의미할 수 있다.

이번 버전의 `another_function`에서는 매개변수를 추가했다:

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/src/main.rs}}
```

이 프로그램을 실행해 보면 다음과 같은 출력을 확인할 수 있다:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/output.txt}}
```

`another_function`의 선언에는 `x`라는 이름의 매개변수가 하나 있다. `x`의 타입은 `i32`로 지정되어 있다. `another_function`에 `5`를 전달하면, `println!` 매크로는 형식 문자열에서 `x`를 포함한 중괄호 쌍을 `5`로 대체한다.

함수 시그니처에서는 각 매개변수의 타입을 반드시 선언해야 한다. 이는 Rust 설계에서 의도적으로 결정된 부분이다. 함수 정의에서 타입 주석을 요구함으로써, 컴파일러는 코드의 다른 부분에서 타입을 추론하기 위해 주석을 사용할 필요가 거의 없어진다. 또한 컴파일러는 함수가 기대하는 타입을 알고 있기 때문에 더 유용한 에러 메시지를 제공할 수 있다.

여러 매개변수를 정의할 때는 쉼표로 구분하여 매개변수 선언을 나열한다:

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/src/main.rs}}
```

이 예제는 `print_labeled_measurement`라는 이름의 함수를 만들고, 두 개의 매개변수를 정의한다. 첫 번째 매개변수는 `value`라는 이름의 `i32` 타입이고, 두 번째 매개변수는 `unit_label`이라는 이름의 `char` 타입이다. 이 함수는 `value`와 `unit_label`을 모두 포함한 텍스트를 출력한다.

이 코드를 실행해 보자. 현재 _functions_ 프로젝트의 _src/main.rs_ 파일에 있는 프로그램을 앞의 예제로 교체하고 `cargo run`을 사용해 실행한다:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/output.txt}}
```

`value`에 `5`를, `unit_label`에 `'h'`를 전달했기 때문에, 프로그램의 출력에는 이 값들이 포함된다.


### 구문과 표현식

함수의 본문은 일련의 구문으로 구성되며, 선택적으로 표현식으로 끝난다. 지금까지 다룬 함수들은 마지막에 표현식을 포함하지 않았지만, 구문의 일부로 표현식을 본 적이 있다. Rust는 표현식 기반 언어이기 때문에 이 차이를 이해하는 것이 중요하다. 다른 언어들은 동일한 구분을 가지고 있지 않으므로, 구문과 표현식이 무엇인지 그리고 그 차이가 함수 본문에 어떤 영향을 미치는지 살펴보자.

- **구문**은 어떤 동작을 수행하지만 값을 반환하지 않는 명령이다.
- **표현식**은 결과 값을 평가한다. 몇 가지 예를 살펴보자.

이미 구문과 표현식을 사용해본 적이 있다. `let` 키워드를 사용해 변수를 생성하고 값을 할당하는 것은 구문이다. 예제 3-1에서 `let y = 6;`은 구문이다.

<Listing number="3-1" file-name="src/main.rs" caption="하나의 구문을 포함한 `main` 함수 선언">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-01/src/main.rs}}
```

</Listing>

함수 정의도 구문이다. 앞의 예제 전체가 하나의 구문이다. (아래에서 보게 될 것처럼, 함수를 _호출_하는 것은 구문이 아니다.)

구문은 값을 반환하지 않는다. 따라서 `let` 구문을 다른 변수에 할당하려고 하면 오류가 발생한다. 다음 코드는 이를 시도했을 때 발생하는 오류를 보여준다:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/src/main.rs}}
```

이 프로그램을 실행하면 다음과 같은 오류가 발생한다:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/output.txt}}
```

`let y = 6` 구문은 값을 반환하지 않기 때문에 `x`가 바인딩할 값이 없다. 이는 C나 Ruby와 같은 다른 언어와 다르다. 그런 언어에서는 할당이 할당된 값을 반환하기 때문에 `x = y = 6`과 같이 작성하면 `x`와 `y` 모두 값 `6`을 가진다. Rust에서는 그렇지 않다.

표현식은 값을 평가하며, Rust에서 작성할 코드의 대부분을 차지한다. 예를 들어 `5 + 6`과 같은 수학 연산은 값 `11`로 평가되는 표현식이다. 표현식은 구문의 일부가 될 수 있다. 예제 3-1에서 `let y = 6;` 구문의 `6`은 값 `6`으로 평가되는 표현식이다. 함수 호출은 표현식이다. 매크로 호출도 표현식이다. 중괄호로 생성된 새로운 스코프 블록도 표현식이다. 예를 들어:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-20-blocks-are-expressions/src/main.rs}}
```

이 표현식:

```rust,ignore
{
    let x = 3;
    x + 1
}
```

은 이 경우 `4`로 평가되는 블록이다. 이 값은 `let` 구문의 일부로 `y`에 바인딩된다. `x + 1` 줄 끝에 세미콜론이 없다는 점에 주목하자. 지금까지 본 대부분의 줄과 다르다. 표현식은 끝에 세미콜론을 포함하지 않는다. 표현식 끝에 세미콜론을 추가하면 구문으로 바뀌며 더 이상 값을 반환하지 않는다. 다음에 함수 반환 값과 표현식을 탐구할 때 이 점을 기억하자.


### 값을 반환하는 함수

함수는 호출한 코드에 값을 반환할 수 있다. 반환 값에 이름을 붙이지는 않지만, 화살표(`->`) 뒤에 반환 값의 타입을 명시해야 한다. Rust에서 함수의 반환 값은 함수 본문의 마지막 표현식의 값과 동일하다. `return` 키워드를 사용해 함수를 조기에 종료하고 값을 반환할 수도 있지만, 대부분의 함수는 마지막 표현식을 암묵적으로 반환한다. 다음은 값을 반환하는 함수의 예시다:

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/src/main.rs}}
```

`five` 함수에는 함수 호출, 매크로, 심지어 `let` 문도 없다. 단순히 숫자 `5`만 존재한다. 이는 Rust에서 완벽하게 유효한 함수다. 함수의 반환 타입이 `-> i32`로 지정된 것에 주목하라. 이 코드를 실행해 보면 다음과 같은 출력이 나온다:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/output.txt}}
```

`five` 함수의 `5`는 함수의 반환 값이며, 반환 타입이 `i32`인 이유다. 이를 더 자세히 살펴보자. 두 가지 중요한 점이 있다: 첫째, `let x = five();` 라인은 함수의 반환 값을 사용해 변수를 초기화하는 것을 보여준다. `five` 함수가 `5`를 반환하기 때문에, 이 라인은 다음과 동일하다:

```rust
let x = 5;
```

둘째, `five` 함수는 매개변수가 없고 반환 값의 타입을 정의하지만, 함수 본문은 세미콜론이 없는 단순한 `5`다. 이는 반환하고자 하는 값의 표현식이기 때문이다.

다른 예시를 살펴보자:

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-22-function-parameter-and-return/src/main.rs}}
```

이 코드를 실행하면 `The value of x is: 6`이 출력된다. 하지만 `x + 1`이 포함된 라인 끝에 세미콜론을 추가해 표현식에서 문장으로 변경하면 오류가 발생한다:

<span class="filename">파일명: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/src/main.rs}}
```

이 코드를 컴파일하면 다음과 같은 오류가 발생한다:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/output.txt}}
```

주요 오류 메시지인 `mismatched types`는 이 코드의 핵심 문제를 나타낸다. `plus_one` 함수의 정의는 `i32`를 반환한다고 명시하지만, 문장은 값으로 평가되지 않으며, 이는 `()`(유닛 타입)로 표현된다. 따라서 아무것도 반환되지 않아 함수 정의와 모순되고 오류가 발생한다. 이 출력에서 Rust는 이 문제를 해결하기 위해 세미콜론을 제거하라는 메시지를 제공한다. 이렇게 하면 오류가 수정된다.


