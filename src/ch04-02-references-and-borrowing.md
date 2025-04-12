## 참조와 빌림

리스트 4-5의 튜플 코드에서 문제는 `calculate_length` 함수를 호출한 후에도 `String`을 계속 사용할 수 있도록 `String`을 호출 함수로 반환해야 한다는 것이다. 왜냐하면 `String`이 `calculate_length`로 이동했기 때문이다. 대신, `String` 값에 대한 참조를 제공할 수 있다. 참조는 포인터와 유사하며, 해당 주소에 저장된 데이터에 접근할 수 있는 주소를 의미한다. 그 데이터는 다른 변수가 소유하고 있다. 포인터와 달리, 참조는 해당 참조의 수명 동안 유효한 특정 타입의 값을 가리키도록 보장된다.

다음은 값을 소유하지 않고 객체에 대한 참조를 매개변수로 사용하는 `calculate_length` 함수를 정의하고 사용하는 방법이다:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-07-reference/src/main.rs:all}}
```

</Listing>

먼저, 변수 선언과 함수 반환 값에 있는 모든 튜플 코드가 사라졌다는 점을 확인한다. 두 번째로, `&s1`을 `calculate_length`에 전달하고, 함수 정의에서 `String` 대신 `&String`을 사용한다. 이 앰퍼샌드(&)는 참조를 나타내며, 값을 소유하지 않고도 값을 참조할 수 있게 한다. 그림 4-6은 이 개념을 보여준다.

<img alt="세 개의 테이블: s 테이블은 s1 테이블에 대한 포인터만 포함한다. s1 테이블은 s1의 스택 데이터를 포함하고 힙에 있는 문자열 데이터를 가리킨다." src="img/trpl04-06.svg" class="center" />

<span class="caption">그림 4-6: `&String s`가 `String s1`을 가리키는 다이어그램</span>

> 참고: `&`를 사용한 참조의 반대는 역참조(dereferencing)이며, 역참조 연산자 `*`를 사용해 수행한다. 역참조 연산자의 사용은 8장에서, 역참조의 세부 사항은 15장에서 다룬다.

이제 함수 호출을 자세히 살펴보자:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-07-reference/src/main.rs:here}}
```

`&s1` 구문은 `s1`의 값을 참조하지만 소유하지 않는 참조를 생성한다. 참조가 값을 소유하지 않기 때문에, 참조가 사용을 멈춰도 가리키는 값은 삭제되지 않는다.

마찬가지로, 함수 시그니처는 매개변수 `s`의 타입이 참조임을 나타내기 위해 `&`를 사용한다. 설명을 추가해 보자:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-08-reference-with-annotations/src/main.rs:here}}
```

변수 `s`가 유효한 범위는 다른 함수 매개변수의 범위와 동일하지만, 참조가 가리키는 값은 `s`가 사용을 멈춰도 삭제되지 않는다. 왜냐하면 `s`는 값을 소유하지 않기 때문이다. 함수가 실제 값 대신 참조를 매개변수로 사용할 때, 값을 반환하여 소유권을 돌려줄 필요가 없다. 왜냐하면 처음부터 소유권을 가지지 않았기 때문이다.

참조를 생성하는 행위를 빌림(borrowing)이라고 한다. 실제 생활에서 누군가가 무언가를 소유하고 있다면, 당신은 그것을 빌릴 수 있다. 사용을 마치면 반환해야 한다. 당신은 그것을 소유하지 않는다.

그렇다면, 빌린 것을 수정하려고 하면 어떻게 될까? 리스트 4-6의 코드를 시도해보자. 스포일러 경고: 작동하지 않는다!

<Listing number="4-6" file-name="src/main.rs" caption="빌린 값을 수정하려는 시도">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-06/src/main.rs}}
```

</Listing>

다음은 오류 메시지다:

```console
{{#include ../listings/ch04-understanding-ownership/listing-04-06/output.txt}}
```

변수가 기본적으로 불변인 것처럼, 참조도 기본적으로 불변이다. 참조한 것을 수정하는 것은 허용되지 않는다.


### 가변 참조

리스트 4-6의 코드를 약간 수정하면 가변 참조(_mutable reference_)를 사용해 빌린 값을 수정할 수 있다.

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-09-fixes-listing-04-06/src/main.rs}}
```

</Listing>

먼저 `s`를 `mut`로 변경한다. 그런 다음 `change` 함수를 호출할 때 `&mut s`로 가변 참조를 생성하고, 함수 시그니처를 `some_string: &mut String`으로 업데이트해 가변 참조를 받도록 한다. 이렇게 하면 `change` 함수가 빌린 값을 변경한다는 사실을 명확히 알 수 있다.

가변 참조에는 큰 제약이 하나 있다. 어떤 값에 대한 가변 참조가 존재한다면, 그 값에 대한 다른 참조를 가질 수 없다. 다음 코드는 `s`에 대한 두 개의 가변 참조를 생성하려고 시도하지만 실패한다:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-10-multiple-mut-not-allowed/src/main.rs:here}}
```

</Listing>

에러 메시지는 다음과 같다:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-10-multiple-mut-not-allowed/output.txt}}
```

이 에러는 `s`를 동시에 여러 번 가변으로 빌릴 수 없기 때문에 코드가 유효하지 않다는 것을 알려준다. 첫 번째 가변 빌림은 `r1`에서 발생하며, `println!`에서 사용될 때까지 유효하다. 하지만 이 가변 참조가 생성된 후 사용되기 전에, `r2`에서 같은 데이터를 빌리는 또 다른 가변 참조를 생성하려고 시도했다.

동일한 데이터에 대한 여러 가변 참조를 동시에 허용하지 않는 제약은 변이를 허용하지만 매우 제어된 방식으로만 허용한다. 대부분의 언어에서는 원할 때마다 변이를 허용하기 때문에, 새로운 Rust 개발자들은 이 제약에 어려움을 겪는다. 이 제약의 장점은 Rust가 컴파일 타임에 데이터 경쟁(_data race_)을 방지할 수 있다는 것이다. _데이터 경쟁_은 경쟁 조건과 유사하며, 다음과 같은 세 가지 동작이 발생할 때 일어난다:

- 두 개 이상의 포인터가 동시에 같은 데이터에 접근한다.
- 최소 하나의 포인터가 데이터를 쓰기 위해 사용된다.
- 데이터 접근을 동기화하는 메커니즘이 없다.

데이터 경쟁은 정의되지 않은 동작을 유발하며, 런타임에 이를 추적하고 수정하는 것은 어려울 수 있다. Rust는 데이터 경쟁이 있는 코드를 컴파일하지 않음으로써 이 문제를 방지한다!

언제나 중괄호를 사용해 새로운 스코프를 생성할 수 있으며, 이를 통해 여러 가변 참조를 허용할 수 있다. 단, 동시에 사용할 수는 없다:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-11-muts-in-separate-scopes/src/main.rs:here}}
```

Rust는 가변 참조와 불변 참조를 결합하는 경우에도 비슷한 규칙을 적용한다. 다음 코드는 에러를 발생시킨다:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-12-immutable-and-mutable-not-allowed/src/main.rs:here}}
```

에러 메시지는 다음과 같다:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-12-immutable-and-mutable-not-allowed/output.txt}}
```

휴! 같은 값에 대한 불변 참조가 존재하는 동안에는 가변 참조를 가질 수 없다.

불변 참조를 사용하는 사용자는 값이 갑자기 변경될 것을 예상하지 않는다! 그러나 여러 불변 참조는 허용된다. 데이터를 읽기만 하는 사용자는 다른 사용자의 데이터 읽기에 영향을 미칠 수 없기 때문이다.

참조의 스코프는 참조가 도입된 지점부터 시작해 마지막으로 사용된 지점까지 계속된다. 예를 들어, 다음 코드는 불변 참조의 마지막 사용이 `println!`에서 이루어진 후 가변 참조가 도입되기 때문에 컴파일된다:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-13-reference-scope-ends/src/main.rs:here}}
```

불변 참조 `r1`과 `r2`의 스코프는 마지막으로 사용된 `println!` 이후에 끝나며, 이는 가변 참조 `r3`가 생성되기 전이다. 이 스코프들은 겹치지 않으므로 이 코드는 허용된다. 컴파일러는 스코프가 끝나기 전에 참조가 더 이상 사용되지 않는다는 것을 알 수 있다.

빌림 에러가 때로는 답답할 수 있지만, Rust 컴파일러가 잠재적인 버그를 조기에(런타임이 아닌 컴파일 타임에) 지적하고 문제가 있는 정확한 위치를 보여준다는 점을 기억하자. 그러면 데이터가 예상과 다를 때 그 이유를 추적할 필요가 없다.


### 댕글링 참조

포인터를 사용하는 언어에서는, 메모리를 해제한 후에도 그 메모리에 대한 포인터를 유지하는 실수를 통해 _댕글링 포인터_를 쉽게 만들 수 있다. 댕글링 포인터는 이미 다른 곳에 할당된 메모리 위치를 참조하는 포인터를 의미한다. 반면에 Rust에서는 컴파일러가 참조가 절대 댕글링 참조가 되지 않도록 보장한다. 즉, 어떤 데이터에 대한 참조가 있다면, 컴파일러는 그 데이터가 참조보다 먼저 스코프를 벗어나지 않도록 한다.

Rust가 어떻게 컴파일 타임 오류를 통해 댕글링 참조를 방지하는지 확인해보자:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-14-dangling-reference/src/main.rs}}
```

</Listing>

발생한 오류는 다음과 같다:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-14-dangling-reference/output.txt}}
```

이 오류 메시지는 아직 다루지 않은 기능인 '라이프타임'을 언급한다. 라이프타임에 대해서는 10장에서 자세히 설명할 것이다. 하지만 라이프타임에 대한 부분을 무시하더라도, 이 메시지는 왜 이 코드가 문제가 되는지에 대한 핵심을 담고 있다:

```text
이 함수의 반환 타입은 빌린 값을 포함하지만, 빌릴 값이 존재하지 않습니다.
```

이제 `dangle` 코드의 각 단계에서 정확히 어떤 일이 일어나는지 자세히 살펴보자:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-15-dangling-reference-annotated/src/main.rs:here}}
```

</Listing>

`s`는 `dangle` 함수 내부에서 생성되므로, `dangle`의 코드가 실행을 마치면 `s`는 해제된다. 하지만 우리는 `s`에 대한 참조를 반환하려고 했다. 이는 이 참조가 유효하지 않은 `String`을 가리키게 된다는 것을 의미한다. 이는 좋지 않은 상황이다! Rust는 이런 상황을 허용하지 않는다.

여기서 해결책은 `String`을 직접 반환하는 것이다:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-16-no-dangle/src/main.rs:here}}
```

이 코드는 아무런 문제 없이 동작한다. 소유권이 이동되고, 아무것도 해제되지 않는다.


### 참조의 규칙


지금까지 다룬 참조에 대한 내용을 다시 정리해 보자:

- 특정 시점에 **하나의 가변 참조**를 가질 수 있거나, **여러 개의 불변 참조**를 가질 수 있다.
- 모든 참조는 항상 유효해야 한다.

다음으로, 다른 종류의 참조인 슬라이스에 대해 알아보자.


