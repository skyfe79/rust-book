## 변수와 가변성

[“변수로 값 저장하기”][storing-values-with-variables]<!-- ignore --> 섹션에서 언급했듯이, 기본적으로 변수는 불변(immutable)이다. 이는 Rust가 제공하는 안전성과 쉬운 동시성(concurrency)을 활용해 코드를 작성하도록 유도하는 여러 방법 중 하나다. 그러나 여전히 변수를 가변(mutable)으로 만들 수 있는 옵션이 있다. Rust가 왜 불변성을 장려하는지, 그리고 어떤 경우에 가변성을 선택해야 하는지 알아보자.

변수가 불변일 때, 값이 이름에 바인딩되면 그 값을 변경할 수 없다. 이를 설명하기 위해 `cargo new variables` 명령을 사용해 _projects_ 디렉터리에 _variables_라는 새 프로젝트를 생성한다.

그런 다음, 새로 생성된 _variables_ 디렉터리에서 _src/main.rs_ 파일을 열고 다음 코드로 바꾼다. 이 코드는 아직 컴파일되지 않는다:

<span class="filename">파일명: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/src/main.rs}}
```

코드를 저장하고 `cargo run` 명령으로 프로그램을 실행한다. 다음과 같이 불변성 오류와 관련된 에러 메시지를 확인할 수 있다:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/output.txt}}
```

이 예제는 컴파일러가 프로그램에서 오류를 찾는 데 어떻게 도움을 주는지 보여준다. 컴파일러 오류는 실망스러울 수 있지만, 이는 단지 프로그램이 아직 안전하게 동작하지 않는다는 의미일 뿐, 여러분이 나쁜 프로그래머라는 뜻은 아니다! 경험 많은 Rust 개발자도 여전히 컴파일러 오류를 마주한다.

`cannot assign twice to immutable variable `x``라는 오류 메시지는 불변 변수 `x`에 두 번째 값을 할당하려 했기 때문에 발생한다.

불변으로 지정된 값을 변경하려고 할 때 컴파일 타임에 오류가 발생하는 것은 중요하다. 이는 버그로 이어질 수 있는 상황이기 때문이다. 코드의 한 부분이 값이 절대 변경되지 않는다는 가정 하에 동작하고, 다른 부분에서 그 값을 변경하면, 첫 번째 부분이 의도한 대로 동작하지 않을 가능성이 있다. 특히 두 번째 코드가 가끔씩만 값을 변경하는 경우, 이런 종류의 버그의 원인을 추적하기는 더 어려울 수 있다. Rust 컴파일러는 값이 변경되지 않는다고 선언하면 실제로 변경되지 않음을 보장하므로, 이를 직접 추적할 필요가 없다. 따라서 코드를 더 쉽게 이해할 수 있다.

하지만 가변성은 매우 유용할 수 있으며, 코드를 더 편리하게 작성할 수 있게 해준다. 변수는 기본적으로 불변이지만, [2장][storing-values-with-variables]<!-- ignore -->에서 했던 것처럼 변수 이름 앞에 `mut`을 추가해 가변으로 만들 수 있다. `mut`을 추가하면 코드의 다른 부분에서 이 변수의 값을 변경할 것임을 미래의 코드 독자에게 알려줄 수 있다.

예를 들어, _src/main.rs_ 파일을 다음과 같이 변경한다:

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/src/main.rs}}
```

이제 프로그램을 실행하면 다음과 같은 결과를 얻는다:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/output.txt}}
```

`mut`을 사용하면 `x`에 바인딩된 값을 `5`에서 `6`으로 변경할 수 있다. 최종적으로 가변성을 사용할지 여부는 여러분의 선택에 달려 있으며, 특정 상황에서 무엇이 가장 명확한지에 따라 결정하면 된다.


### 상수

불변 변수와 마찬가지로, _상수_는 이름에 바인딩된 값이며 변경할 수 없다. 하지만 상수와 변수 사이에는 몇 가지 차이점이 있다.

첫째, 상수에는 `mut` 키워드를 사용할 수 없다. 상수는 기본적으로 불변일 뿐만 아니라 항상 불변이다. 상수는 `let` 키워드 대신 `const` 키워드를 사용해 선언하며, 값의 타입을 반드시 명시해야 한다. 타입과 타입 명시에 대해서는 다음 섹션인 [“데이터 타입”][data-types]<!-- ignore -->에서 자세히 다룰 예정이므로, 지금은 세부 사항에 대해 걱정하지 않아도 된다. 단, 타입을 항상 명시해야 한다는 점만 기억하면 된다.

상수는 전역 스코프를 포함한 모든 스코프에서 선언할 수 있다. 이는 코드의 여러 부분에서 알아야 할 값에 대해 상수를 사용할 때 유용하다.

마지막 차이점은 상수는 상수 표현식으로만 설정할 수 있으며, 런타임에 계산되는 값의 결과로 설정할 수 없다는 것이다.

다음은 상수 선언의 예시다:

```rust
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```

이 상수의 이름은 `THREE_HOURS_IN_SECONDS`이며, 값은 60(1분의 초 수)을 60(1시간의 분 수)으로 곱한 후 3(이 프로그램에서 계산하려는 시간 수)을 곱한 결과로 설정된다. Rust에서 상수의 이름은 모든 글자를 대문자로 쓰고 단어 사이에 밑줄을 사용하는 것이 관례다. 컴파일러는 컴파일 시점에 제한된 연산을 평가할 수 있으므로, 상수를 10,800으로 직접 설정하는 대신 이렇게 작성하면 이해하고 검증하기 쉬운 방식으로 값을 표현할 수 있다. 상수 선언 시 사용할 수 있는 연산에 대한 더 자세한 정보는 [Rust Reference의 상수 평가 섹션][const-eval]을 참고하면 된다.

상수는 선언된 스코프 내에서 프로그램이 실행되는 동안 유효하다. 이 특성은 프로그램의 여러 부분에서 알아야 할 애플리케이션 도메인의 값, 예를 들어 게임에서 플레이어가 획득할 수 있는 최대 점수나 빛의 속도와 같은 값을 상수로 정의할 때 유용하다.

프로그램 전체에서 사용되는 하드코딩된 값을 상수로 명명하면, 코드를 유지보수할 사람에게 그 값의 의미를 전달하는 데 도움이 된다. 또한, 나중에 하드코딩된 값을 업데이트해야 할 경우 코드 내에서 단 한 곳만 변경하면 된다는 장점도 있다.


### 쉐도잉(Shadowing)

[2장][comparing-the-guess-to-the-secret-number]<!-- ignore -->에서 다룬 숫자 맞추기 게임 튜토리얼에서 보았듯이, 이전에 선언한 변수와 같은 이름으로 새로운 변수를 선언할 수 있다. 러스트 프로그래머들은 이를 첫 번째 변수가 두 번째 변수에 의해 _쉐도잉(shadowed)_ 되었다고 표현한다. 이는 변수 이름을 사용할 때 컴파일러가 두 번째 변수를 인식한다는 의미이다. 실제로 두 번째 변수는 첫 번째 변수를 가려버리며, 변수 이름을 사용하는 모든 경우에 두 번째 변수가 적용된다. 이 상태는 두 번째 변수 자체가 쉐도잉되거나 스코프가 종료될 때까지 지속된다. `let` 키워드를 다시 사용해 동일한 변수 이름으로 쉐도잉을 수행할 수 있다.

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/src/main.rs}}
```

이 프로그램은 먼저 `x`를 `5`로 바인딩한다. 그런 다음 `let x =`를 다시 사용해 새로운 변수 `x`를 생성하고, 기존 값에 `1`을 더해 `x`의 값을 `6`으로 만든다. 이후 중괄호로 생성된 내부 스코프에서 세 번째 `let` 문이 `x`를 다시 쉐도잉하고, 이전 값에 `2`를 곱해 `x`의 값을 `12`로 만든다. 이 스코프가 끝나면 내부 쉐도잉이 종료되고 `x`는 다시 `6`으로 돌아간다. 이 프로그램을 실행하면 다음과 같은 결과가 출력된다:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/output.txt}}
```

쉐도잉은 변수를 `mut`로 표시하는 것과 다르다. `let` 키워드를 사용하지 않고 변수에 재할당을 시도하면 컴파일 타임 에러가 발생한다. `let`을 사용하면 값에 몇 가지 변환을 수행할 수 있고, 변환이 완료된 후에는 변수를 불변 상태로 유지할 수 있다.

`mut`와 쉐도잉의 또 다른 차이점은 `let` 키워드를 다시 사용해 새로운 변수를 생성할 때 값의 타입을 변경할 수 있다는 점이다. 예를 들어, 프로그램에서 사용자에게 텍스트 사이에 원하는 공백 수를 입력하도록 요청하고, 그 입력을 숫자로 저장하려는 경우를 생각해 보자:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-04-shadowing-can-change-types/src/main.rs:here}}
```

첫 번째 `spaces` 변수는 문자열 타입이고, 두 번째 `spaces` 변수는 숫자 타입이다. 쉐도잉을 사용하면 `spaces_str`이나 `spaces_num`과 같은 다른 이름을 고민할 필요 없이, 단순히 `spaces`라는 이름을 재사용할 수 있다. 그러나 `mut`를 사용해 이를 시도하면 다음과 같이 컴파일 타임 에러가 발생한다:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/src/main.rs:here}}
```

에러 메시지는 변수의 타입을 변경할 수 없다고 알려준다:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/output.txt}}
```

이제 변수가 어떻게 동작하는지 살펴보았으니, 변수가 가질 수 있는 다양한 데이터 타입에 대해 알아보자.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[data-types]: ch03-02-data-types.html#data-types
[storing-values-with-variables]: ch02-00-guessing-game-tutorial.html#storing-values-with-variables
[const-eval]: ../reference/const_eval.html


