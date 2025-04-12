## 테스트 작성 방법

테스트는 러스트 함수로, 테스트 대상 코드가 예상대로 동작하는지 검증한다. 테스트 함수의 본문은 일반적으로 다음 세 가지 작업을 수행한다:

- 필요한 데이터나 상태를 설정한다.
- 테스트할 코드를 실행한다.
- 결과가 예상과 일치하는지 확인한다.

이제 러스트가 제공하는 테스트 작성 기능을 살펴보자. `test` 속성, 몇 가지 매크로, 그리고 `should_panic` 속성을 활용해 위의 작업을 수행할 수 있다.


### 테스트 함수의 구조

Rust에서 테스트는 `test` 속성(attribute)으로 주석 처리된 함수다. 속성은 Rust 코드에 대한 메타데이터이며, 예를 들어 5장에서 구조체와 함께 사용한 `derive` 속성이 그 예다. 함수를 테스트 함수로 바꾸려면 `fn` 앞에 `#[test]`를 추가한다. `cargo test` 명령어로 테스트를 실행하면, Rust는 테스트 러너 바이너리를 빌드하고, 주석 처리된 함수를 실행한 뒤 각 테스트 함수의 성공 여부를 보고한다.

Cargo로 새로운 라이브러리 프로젝트를 만들 때마다, 테스트 모듈과 그 안에 테스트 함수가 자동으로 생성된다. 이 모듈은 테스트 작성을 위한 템플릿을 제공하므로, 새로운 프로젝트를 시작할 때마다 정확한 구조와 문법을 찾아볼 필요가 없다. 원하는 만큼 추가 테스트 함수와 테스트 모듈을 추가할 수 있다.

실제 코드를 테스트하기 전에, 템플릿 테스트를 실험하면서 테스트가 어떻게 동작하는지 몇 가지 측면을 살펴본다. 그런 다음, 작성한 코드를 호출하고 그 동작이 올바른지 확인하는 실제 테스트를 작성한다.

두 숫자를 더하는 `adder`라는 새로운 라이브러리 프로젝트를 만들어보자:

```console
$ cargo new adder --lib
     Created library `adder` project
$ cd adder
```

`adder` 라이브러리의 _src/lib.rs_ 파일 내용은 다음과 같다.

<Listing number="11-1" file-name="src/lib.rs" caption="`cargo new`로 자동 생성된 코드">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

</Listing>

파일은 예시 `add` 함수로 시작하므로, 테스트할 무언가가 있다.

일단 `it_works` 함수에 집중해보자. `#[test]` 주석에 주목한다. 이 속성은 이 함수가 테스트 함수임을 나타내므로, 테스트 러너가 이 함수를 테스트로 취급한다. 테스트 모듈에는 공통 시나리오 설정이나 일반적인 작업 수행을 돕는 비테스트 함수도 있을 수 있으므로, 항상 어떤 함수가 테스트인지 표시해야 한다.

예시 함수 본문은 `assert_eq!` 매크로를 사용해 `result`가 2와 2를 더한 결과인 4와 같은지 확인한다. 이 단언은 일반적인 테스트의 형식을 보여주는 예시다. 이 테스트가 통과하는지 확인하기 위해 실행해보자.

`cargo test` 명령어는 프로젝트의 모든 테스트를 실행하며, 그 결과는 다음과 같다.

<Listing number="11-2" caption="자동 생성된 테스트 실행 결과">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-01/output.txt}}
```

</Listing>

Cargo가 테스트를 컴파일하고 실행했다. `running 1 test` 줄을 볼 수 있다. 다음 줄은 생성된 테스트 함수 이름인 `tests::it_works`를 보여주고, 그 테스트 실행 결과가 `ok`임을 나타낸다. 전체 요약인 `test result: ok.`는 모든 테스트가 통과했음을 의미하며, `1 passed; 0 failed` 부분은 통과하거나 실패한 테스트의 수를 나타낸다.

특정 인스턴스에서 실행되지 않도록 테스트를 무시(ignore)할 수도 있다. 이에 대해서는 이 장의 뒷부분에서 다룬다. 여기서는 그렇게 하지 않았으므로, 요약에 `0 ignored`가 표시된다. 또한 `cargo test` 명령어에 인자를 전달해 이름이 특정 문자열과 일치하는 테스트만 실행할 수도 있다. 이를 _필터링_이라고 하며, 이에 대해서도 나중에 다룬다. 여기서는 테스트를 필터링하지 않았으므로, 요약 끝에 `0 filtered out`이 표시된다.

`0 measured` 통계는 성능을 측정하는 벤치마크 테스트를 위한 것이다. 이 글을 쓰는 시점에서 벤치마크 테스트는 nightly Rust에서만 사용할 수 있다. 벤치마크 테스트에 대한 자세한 내용은 [문서][bench]를 참고한다.

테스트 출력의 다음 부분인 `Doc-tests adder`는 문서 테스트의 결과를 나타낸다. 아직 문서 테스트는 없지만, Rust는 API 문서에 나타나는 모든 코드 예제를 컴파일할 수 있다. 이 기능은 문서와 코드를 동기화하는 데 도움이 된다! 문서 테스트 작성 방법은 14장의 [“테스트로서의 문서 주석”][doc-comments]<!-- ignore --> 섹션에서 다룬다. 지금은 `Doc-tests` 출력을 무시한다.

이제 테스트를 우리의 필요에 맞게 커스터마이징해보자. 먼저 `it_works` 함수의 이름을 `exploration`과 같이 다른 이름으로 바꾼다:

<span class="filename">Filename: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/src/lib.rs}}
```

그런 다음 `cargo test`를 다시 실행한다. 이제 출력에 `it_works` 대신 `exploration`이 표시된다:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/output.txt}}
```

이제 다른 테스트를 추가하지만, 이번에는 실패하는 테스트를 만들어보자! 테스트 함수 내에서 무언가 패닉(panic)이 발생하면 테스트가 실패한다. 각 테스트는 새로운 스레드에서 실행되며, 메인 스레드가 테스트 스레드가 죽은 것을 발견하면 테스트는 실패한 것으로 표시된다. 9장에서 패닉을 발생시키는 가장 간단한 방법은 `panic!` 매크로를 호출하는 것이라고 했다. `another`라는 이름의 함수로 새 테스트를 추가하면 _src/lib.rs_ 파일은 다음과 같다.

<Listing number="11-3" file-name="src/lib.rs" caption="`panic!` 매크로를 호출하여 실패하도록 만든 두 번째 테스트 추가">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-03/src/lib.rs}}
```

</Listing>

`cargo test`로 테스트를 다시 실행한다. 출력은 다음과 같으며, `exploration` 테스트는 통과하고 `another` 테스트는 실패했다.

<Listing number="11-4" caption="하나의 테스트는 통과하고 다른 하나는 실패한 테스트 결과">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-03/output.txt}}
```

</Listing>

`ok` 대신 `test tests::another` 줄에 `FAILED`가 표시된다. 개별 결과와 요약 사이에 두 개의 새로운 섹션이 나타난다. 첫 번째 섹션은 각 테스트 실패의 상세한 이유를 보여준다. 이 경우, `another` 테스트가 _src/lib.rs_ 파일의 17번째 줄에서 `panicked at 'Make this test fail'`로 인해 실패했다는 상세 정보를 얻을 수 있다. 다음 섹션은 실패한 모든 테스트의 이름만 나열한다. 이는 많은 테스트와 상세한 실패 테스트 출력이 있을 때 유용하다. 실패한 테스트의 이름을 사용해 해당 테스트만 실행하면 디버깅이 더 쉬워진다. 테스트 실행 방법에 대해서는 [“테스트 실행 방법 제어”][controlling-how-tests-are-run]<!-- ignore --> 섹션에서 더 자세히 다룬다.

요약 줄은 끝에 표시된다. 전체적으로 테스트 결과는 `FAILED`다. 하나의 테스트는 통과했고, 다른 하나는 실패했다.

이제 다양한 시나리오에서 테스트 결과가 어떻게 보이는지 확인했으니, `panic!` 이외의 테스트에 유용한 다른 매크로를 살펴보자.


### `assert!` 매크로로 결과 확인하기

표준 라이브러리에서 제공하는 `assert!` 매크로는 테스트에서 특정 조건이 `true`로 평가되는지 확인할 때 유용하다. `assert!` 매크로에 부울 값으로 평가되는 인자를 전달한다. 값이 `true`이면 아무 일도 일어나지 않고 테스트가 통과한다. 값이 `false`이면 `assert!` 매크로가 `panic!`을 호출해 테스트를 실패시킨다. `assert!` 매크로를 사용하면 코드가 의도한 대로 동작하는지 확인할 수 있다.

5장의 리스팅 5-15에서 `Rectangle` 구조체와 `can_hold` 메서드를 사용했는데, 이를 리스팅 11-5에서 다시 보여준다. 이 코드를 _src/lib.rs_ 파일에 넣고, `assert!` 매크로를 사용해 테스트를 작성해보자.

<Listing number="11-5" file-name="src/lib.rs" caption="5장의 `Rectangle` 구조체와 `can_hold` 메서드">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-05/src/lib.rs}}
```

</Listing>

`can_hold` 메서드는 부울 값을 반환하므로 `assert!` 매크로를 사용하기에 적합하다. 리스팅 11-6에서는 `can_hold` 메서드를 테스트하기 위해 너비가 8이고 높이가 7인 `Rectangle` 인스턴스를 생성하고, 너비가 5이고 높이가 1인 다른 `Rectangle` 인스턴스를 담을 수 있는지 확인하는 테스트를 작성한다.

<Listing number="11-6" file-name="src/lib.rs" caption="더 큰 직사각형이 더 작은 직사각형을 담을 수 있는지 확인하는 `can_hold` 테스트">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-06/src/lib.rs:here}}
```

</Listing>

`tests` 모듈 안의 `use super::*;` 줄을 주목하자. `tests` 모듈은 7장의 ["모듈 트리에서 항목을 참조하는 경로"][paths-for-referring-to-an-item-in-the-module-tree]<!-- ignore --> 섹션에서 다룬 일반적인 가시성 규칙을 따른다. `tests` 모듈은 내부 모듈이므로, 외부 모듈의 테스트 대상 코드를 내부 모듈의 스코프로 가져와야 한다. 여기서는 glob을 사용해 외부 모듈에 정의된 모든 항목을 `tests` 모듈에서 사용할 수 있도록 한다.

테스트 이름을 `larger_can_hold_smaller`로 지정하고, 필요한 두 `Rectangle` 인스턴스를 생성했다. 그런 다음 `assert!` 매크로를 호출하고 `larger.can_hold(&smaller)`의 결과를 전달했다. 이 표현식은 `true`를 반환할 것이므로 테스트가 통과할 것이다. 결과를 확인해보자!

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-06/output.txt}}
```

테스트가 통과했다! 이번에는 더 작은 직사각형이 더 큰 직사각형을 담을 수 없는지 확인하는 테스트를 추가해보자:

<span class="filename">Filename: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/src/lib.rs:here}}
```

이 경우 `can_hold` 함수의 올바른 결과는 `false`이므로, `assert!` 매크로에 전달하기 전에 결과를 부정해야 한다. 결과적으로 `can_hold`가 `false`를 반환하면 테스트가 통과한다:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/output.txt}}
```

두 테스트가 모두 통과했다! 이제 코드에 버그를 도입했을 때 테스트 결과가 어떻게 되는지 살펴보자. `can_hold` 메서드의 구현을 변경해 너비를 비교할 때 '보다 큼' 기호를 '보다 작음' 기호로 바꿔보자:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/src/lib.rs:here}}
```

이제 테스트를 실행하면 다음과 같은 결과가 나온다:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/output.txt}}
```

테스트가 버그를 잡았다! `larger.width`는 `8`이고 `smaller.width`는 `5`이므로, `can_hold`에서 너비를 비교할 때 `false`를 반환한다: 8은 5보다 작지 않다.


### `assert_eq!`와 `assert_ne!` 매크로를 사용한 동등성 테스트

코드의 기능을 검증하는 일반적인 방법은 테스트 중인 코드의 결과와 예상 값을 비교하는 것이다. 이를 위해 `assert!` 매크로를 사용하고 `==` 연산자를 포함한 표현식을 전달할 수 있다. 하지만 이는 매우 일반적인 테스트이기 때문에, 표준 라이브러리는 이를 더 편리하게 수행할 수 있는 두 가지 매크로인 `assert_eq!`와 `assert_ne!`를 제공한다. 이 매크로는 각각 두 인자의 동등성 또는 비동등성을 비교한다. 또한, 테스트가 실패할 경우 두 값을 출력하므로, 테스트가 실패한 이유를 쉽게 파악할 수 있다. 반면, `assert!` 매크로는 `==` 표현식이 `false` 값을 반환했음을 알려줄 뿐, 어떤 값 때문에 `false`가 발생했는지는 출력하지 않는다.

리스트 11-7에서는 `add_two`라는 함수를 작성하고, 이 함수에 `2`를 더한 결과를 `assert_eq!` 매크로를 사용해 테스트한다.

<Listing number="11-7" file-name="src/lib.rs" caption="`assert_eq!` 매크로를 사용해 `add_two` 함수 테스트">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-07/src/lib.rs}}
```

</Listing>

테스트가 통과하는지 확인해보자.

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-07/output.txt}}
```

`result`라는 변수를 생성하고, `add_two(2)`를 호출한 결과를 저장한다. 그런 다음 `result`와 `4`를 `assert_eq!`의 인자로 전달한다. 이 테스트의 출력 줄은 `test tests::it_adds_two ... ok`이며, `ok` 텍스트는 테스트가 통과했음을 나타낸다!

이제 코드에 버그를 추가하여 `assert_eq!`가 실패할 때 어떻게 보이는지 확인해보자. `add_two` 함수의 구현을 변경하여 `3`을 더하도록 한다:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/src/lib.rs:here}}
```

테스트를 다시 실행한다:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/output.txt}}
```

테스트가 버그를 잡았다! `it_adds_two` 테스트가 실패했으며, 실패한 어설션은 ``assertion `left == right` failed``라는 메시지와 함께 `left`와 `right` 값을 보여준다. 이 메시지는 디버깅을 시작하는 데 도움이 된다: `left` 인자는 `add_two(2)`를 호출한 결과인 `5`였고, `right` 인자는 `4`였다. 이는 특히 많은 테스트가 진행 중일 때 매우 유용할 것이다.

일부 언어와 테스트 프레임워크에서는 동등성 어설션 함수의 매개변수를 `expected`와 `actual`로 부르며, 인자를 지정하는 순서가 중요하다. 그러나 Rust에서는 이를 `left`와 `right`로 부르며, 예상 값과 코드가 생성한 값을 지정하는 순서는 중요하지 않다. 이 테스트에서 어설션을 `assert_eq!(add_two(2), result)`로 작성할 수도 있으며, 이는 동일한 실패 메시지를 출력할 것이다.

`assert_ne!` 매크로는 두 값이 같지 않으면 통과하고, 같으면 실패한다. 이 매크로는 값이 무엇인지 확실히 알 수 없지만, 값이 분명히 무엇이 아니어야 하는 경우에 가장 유용하다. 예를 들어, 입력을 어떤 방식으로든 변경하는 함수를 테스트할 때, 입력이 변경되는 방식이 테스트를 실행하는 요일에 따라 달라질 수 있다면, 함수의 출력이 입력과 같지 않음을 어설션하는 것이 최선일 수 있다.

내부적으로 `assert_eq!`와 `assert_ne!` 매크로는 각각 `==`와 `!=` 연산자를 사용한다. 어설션이 실패할 경우, 이 매크로는 디버그 포맷팅을 사용해 인자를 출력하므로, 비교되는 값은 `PartialEq`와 `Debug` 트레이트를 구현해야 한다. 모든 기본 타입과 대부분의 표준 라이브러리 타입은 이 트레이트를 구현한다. 직접 정의한 구조체나 열거형의 경우, 이 타입들의 동등성을 어설션하기 위해 `PartialEq`를 구현해야 한다. 또한 어설션이 실패할 때 값을 출력하기 위해 `Debug`도 구현해야 한다. 두 트레이트는 모두 파생 가능한 트레이트이므로, 구조체나 열거형 정의에 `#[derive(PartialEq, Debug)]` 어노테이션을 추가하는 것만으로도 충분하다. 이와 다른 파생 가능한 트레이트에 대한 자세한 내용은 부록 C, ["파생 가능한 트레이트"][derivable-traits]<!-- ignore -->를 참조하라.


### 커스텀 실패 메시지 추가하기

`assert!`, `assert_eq!`, 그리고 `assert_ne!` 매크로에 선택적 인자로 커스텀 메시지를 추가할 수 있다. 필수 인자 이후에 지정된 모든 인자는 `format!` 매크로로 전달되므로, `{}` 자리 표시자를 포함한 포맷 문자열과 해당 자리 표시자에 들어갈 값을 전달할 수 있다. 커스텀 메시지는 테스트가 실패했을 때 문제를 더 잘 이해할 수 있도록 도와준다.

예를 들어, 이름을 받아 사람들에게 인사하는 함수가 있고, 이 함수에 전달한 이름이 출력에 포함되는지 테스트하고 싶다고 가정해 보자.

<span class="filename">파일명: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-05-greeter/src/lib.rs}}
```

이 프로그램의 요구사항이 아직 확정되지 않았으며, 인사말의 시작 부분에 있는 `Hello` 텍스트가 변경될 가능성이 높다. 요구사항이 변경될 때마다 테스트를 업데이트하지 않기 위해, `greeting` 함수가 반환한 값과 정확히 일치하는지 확인하는 대신, 출력에 입력 매개변수의 텍스트가 포함되어 있는지 확인하기로 결정했다.

이제 `greeting` 함수를 수정하여 `name`을 제외하고 버그를 도입해 보자. 이렇게 하면 기본 테스트 실패 메시지가 어떻게 나타나는지 확인할 수 있다.

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/src/lib.rs:here}}
```

이 테스트를 실행하면 다음과 같은 결과가 나타난다.

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/output.txt}}
```

이 결과는 단순히 테스트가 실패했고, 어느 줄에서 실패했는지 알려준다. 더 유용한 실패 메시지는 `greeting` 함수에서 반환된 값을 출력하는 것이다. `greeting` 함수에서 실제로 얻은 값을 포맷 문자열에 포함시켜 커스텀 실패 메시지를 추가해 보자.

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/src/lib.rs:here}}
```

이제 테스트를 실행하면 더 많은 정보를 담은 에러 메시지를 확인할 수 있다.

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/output.txt}}
```

테스트 출력에서 실제로 얻은 값을 확인할 수 있으므로, 예상과 다른 상황에서 무엇이 잘못되었는지 디버깅하는 데 도움이 된다.


### `should_panic`으로 패닉 상태 확인하기

반환 값을 확인하는 것 외에도, 코드가 예상대로 에러 상황을 처리하는지 확인하는 것도 중요하다. 예를 들어, 9장의 리스팅 9-13에서 생성한 `Guess` 타입을 생각해 보자. `Guess`를 사용하는 다른 코드들은 `Guess` 인스턴스가 1에서 100 사이의 값만 포함한다는 보장에 의존한다. 이 범위를 벗어난 값으로 `Guess` 인스턴스를 생성하려고 할 때 패닉이 발생하는지 확인하는 테스트를 작성할 수 있다.

이를 위해 테스트 함수에 `should_panic` 속성을 추가한다. 함수 내부의 코드가 패닉을 일으키면 테스트는 통과하고, 패닉이 발생하지 않으면 테스트는 실패한다.

리스팅 11-8은 `Guess::new`의 에러 조건이 예상대로 발생하는지 확인하는 테스트를 보여준다.

<Listing number="11-8" file-name="src/lib.rs" caption="`panic!`을 일으키는 조건 테스트">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-08/src/lib.rs}}
```

</Listing>

`#[should_panic]` 속성은 `#[test]` 속성 뒤에, 그리고 적용할 테스트 함수 앞에 위치시킨다. 이 테스트가 통과할 때의 결과를 살펴보자:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-08/output.txt}}
```

잘 동작한다! 이제 `new` 함수가 값이 100보다 클 때 패닉을 일으키는 조건을 제거하여 버그를 만들어 보자:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/src/lib.rs:here}}
```

리스팅 11-8의 테스트를 실행하면 실패한다:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/output.txt}}
```

이 경우에는 도움이 되는 메시지를 얻지 못하지만, 테스트 함수를 보면 `#[should_panic]`으로 주석이 달려 있다. 실패 메시지는 테스트 함수 내의 코드가 패닉을 일으키지 않았다는 것을 의미한다.

`should_panic`을 사용한 테스트는 정확하지 않을 수 있다. 테스트가 예상과 다른 이유로 패닉을 일으켜도 `should_panic` 테스트는 통과할 수 있다. `should_panic` 테스트를 더 정확하게 만들기 위해 `should_panic` 속성에 `expected` 매개변수를 추가할 수 있다. 테스트 도구는 실패 메시지에 제공된 텍스트가 포함되어 있는지 확인한다. 예를 들어, 리스팅 11-9에서 `new` 함수가 값이 너무 작은지 큰지에 따라 다른 메시지로 패닉을 일으키도록 수정된 `Guess` 코드를 살펴보자.

<Listing number="11-9" file-name="src/lib.rs" caption="지정된 부분 문자열을 포함하는 `panic!` 메시지 테스트">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-09/src/lib.rs:here}}
```

</Listing>

이 테스트는 `should_panic` 속성의 `expected` 매개변수에 넣은 값이 `Guess::new` 함수가 패닉을 일으킬 때의 메시지의 부분 문자열이기 때문에 통과한다. 예상하는 전체 패닉 메시지를 지정할 수도 있는데, 이 경우에는 `Guess value must be less than or equal to 100, got 200`이 될 것이다. 어떤 부분을 지정할지는 패닉 메시지의 고유하거나 동적인 부분이 얼마나 되는지, 그리고 테스트를 얼마나 정확하게 만들고 싶은지에 따라 달라진다. 이 경우에는 패닉 메시지의 부분 문자열만으로도 테스트 함수가 `else if value > 100` 경우를 실행하는지 확인하기에 충분하다.

`expected` 메시지가 있는 `should_panic` 테스트가 실패할 때 어떤 일이 발생하는지 보기 위해, `if value < 1`과 `else if value > 100` 블록의 본문을 바꾸어 버그를 다시 만들어 보자:

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/src/lib.rs:here}}
```

이번에 `should_panic` 테스트를 실행하면 실패한다:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/output.txt}}
```

실패 메시지는 이 테스트가 예상대로 패닉을 일으켰지만, 패닉 메시지에 예상한 문자열 `less than or equal to 100`이 포함되어 있지 않다는 것을 나타낸다. 이 경우에 얻은 패닉 메시지는 `Guess value must be greater than or equal to 1, got 200.`이다. 이제 버그가 어디에 있는지 파악할 수 있다!


### `Result<T, E>`를 테스트에서 사용하기

지금까지 작성한 테스트는 실패할 때 패닉을 일으켰다. `Result<T, E>`를 사용하는 테스트도 작성할 수 있다. 리스트 11-1의 테스트를 `Result<T, E>`를 사용하도록 수정하고, 패닉 대신 `Err`를 반환하도록 바꿔보자:

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-10-result-in-tests/src/lib.rs:here}}
```

`it_works` 함수는 이제 `Result<(), String>` 타입을 반환한다. 함수 본문에서 `assert_eq!` 매크로를 호출하는 대신, 테스트가 성공하면 `Ok(())`를 반환하고 실패하면 `String`이 포함된 `Err`를 반환한다.

테스트가 `Result<T, E>`를 반환하도록 작성하면 테스트 본문에서 물음표 연산자(`?`)를 사용할 수 있다. 이는 테스트 내부의 어떤 연산이 `Err`를 반환할 경우 테스트가 실패하도록 작성하는 편리한 방법이다.

`Result<T, E>`를 사용하는 테스트에서는 `#[should_panic]` 어노테이션을 사용할 수 없다. 연산이 `Err`를 반환하는지 확인하려면 `Result<T, E>` 값에 물음표 연산자를 사용하지 말고, 대신 `assert!(value.is_err())`를 사용한다.

이제 테스트를 작성하는 여러 방법을 알게 되었으니, 테스트를 실행할 때 어떤 일이 일어나는지 살펴보고 `cargo test`와 함께 사용할 수 있는 다양한 옵션을 탐구해보자.

[concatenation-with-the--operator-or-the-format-macro]: ch08-02-strings.html#concatenation-with-the--operator-or-the-format-macro
[bench]: ../unstable-book/library-features/test.html
[ignoring]: ch11-02-running-tests.html#ignoring-some-tests-unless-specifically-requested
[subset]: ch11-02-running-tests.html#running-a-subset-of-tests-by-name
[controlling-how-tests-are-run]: ch11-02-running-tests.html#controlling-how-tests-are-run
[derivable-traits]: appendix-03-derivable-traits.html
[doc-comments]: ch14-02-publishing-to-crates-io.html#documentation-comments-as-tests
[paths-for-referring-to-an-item-in-the-module-tree]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html


