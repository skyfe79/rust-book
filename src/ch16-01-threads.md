## 스레드를 사용해 코드를 동시에 실행하기

현대 운영체제에서 실행되는 프로그램의 코드는 프로세스 내에서 동작하며, 운영체제는 여러 프로세스를 동시에 관리한다. 프로그램 내부에서도 독립적으로 동시에 실행되는 부분을 만들 수 있다. 이런 독립적인 부분을 실행하는 기능을 스레드라고 한다. 예를 들어, 웹 서버는 여러 스레드를 사용해 동시에 여러 요청에 응답할 수 있다.

프로그램의 계산 작업을 여러 스레드로 나누어 동시에 실행하면 성능을 향상시킬 수 있지만, 복잡성도 증가한다. 스레드가 동시에 실행되기 때문에, 서로 다른 스레드에서 코드가 어떤 순서로 실행될지 보장할 수 없다. 이로 인해 다음과 같은 문제가 발생할 수 있다:

- **경쟁 상태(Race conditions)**: 스레드가 데이터나 리소스에 일관성 없는 순서로 접근하는 경우
- **데드락(Deadlocks)**: 두 스레드가 서로를 기다리며 더 이상 진행되지 못하는 경우
- **특정 상황에서만 발생하는 버그**: 재현하기 어렵고 안정적으로 수정하기 힘든 버그

Rust는 스레드 사용으로 인한 부정적인 영향을 줄이려고 노력하지만, 멀티스레드 환경에서 프로그래밍하려면 신중하게 생각해야 하며, 단일 스레드 프로그램과는 다른 코드 구조가 필요하다.

프로그래밍 언어는 다양한 방식으로 스레드를 구현하며, 많은 운영체제는 새로운 스레드를 생성하기 위한 API를 제공한다. Rust 표준 라이브러리는 **1:1** 스레드 구현 모델을 사용한다. 이 모델에서는 하나의 언어 스레드가 하나의 운영체제 스레드를 사용한다. 1:1 모델과는 다른 트레이드오프를 가지는 스레딩 모델을 구현하는 크레이트도 존재한다. (Rust의 비동기 시스템은 다음 장에서 다룰 예정이며, 이는 동시성을 다루는 또 다른 접근 방식을 제공한다.)


### `spawn`을 사용해 새 스레드 생성하기

새 스레드를 생성하려면 `thread::spawn` 함수를 호출하고, 새 스레드에서 실행할 코드를 담은 클로저를 인자로 전달한다. (클로저는 13장에서 다뤘다.) 리스트 16-1의 예제는 메인 스레드와 새로 생성된 스레드에서 각각 다른 텍스트를 출력한다:

<Listing number="16-1" file-name="src/main.rs" caption="메인 스레드와 새 스레드에서 각각 다른 내용을 출력하는 예제">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-01/src/main.rs}}
```

</Listing>

Rust 프로그램의 메인 스레드가 종료되면, 모든 생성된 스레드는 실행이 완료되었는지 여부와 상관없이 강제로 종료된다. 이 프로그램의 출력은 실행할 때마다 조금씩 다를 수 있지만, 대체로 다음과 비슷한 형태가 된다:

<!-- 출력 결과를 추출하지 않은 이유는, 컴파일러의 변화보다는 스레드 실행 순서의 차이로 인해 출력이 달라질 가능성이 높기 때문이다 -->

```text
hi number 1 from the main thread!
hi number 1 from the spawned thread!
hi number 2 from the main thread!
hi number 2 from the spawned thread!
hi number 3 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the main thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
```

`thread::sleep` 호출은 스레드의 실행을 잠시 멈추게 해서 다른 스레드가 실행될 기회를 제공한다. 스레드가 번갈아가며 실행될 가능성이 높지만, 이는 보장된 동작이 아니다. 스레드의 실행 순서는 운영체제의 스케줄링 방식에 따라 달라진다. 이번 실행에서는 코드상에서 생성된 스레드의 출력문이 먼저 위치했음에도 불구하고, 메인 스레드가 먼저 출력을 시작했다. 또한 생성된 스레드는 `i`가 `9`가 될 때까지 출력하도록 설정했지만, 메인 스레드가 종료되기 전에 `5`까지만 출력했다.

이 코드를 실행했을 때 메인 스레드의 출력만 보이거나, 두 스레드의 출력이 겹치지 않는다면, 범위의 숫자를 늘려서 운영체제가 스레드를 전환할 기회를 더 많이 만들어 보자.


### `join` 핸들을 사용해 모든 스레드가 완료될 때까지 기다리기

리스트 16-1의 코드는 대부분의 경우 메인 스레드가 종료되면서 생성된 스레드가 중간에 멈추는 문제가 있다. 또한 스레드가 실행되는 순서가 보장되지 않기 때문에, 생성된 스레드가 실행될지조차 확신할 수 없다.

이 문제를 해결하기 위해 `thread::spawn`의 반환 값을 변수에 저장할 수 있다. `thread::spawn`의 반환 타입은 `JoinHandle<T>`다. `JoinHandle<T>`는 소유된 값으로, 여기에 `join` 메서드를 호출하면 해당 스레드가 완료될 때까지 기다린다. 리스트 16-2는 리스트 16-1에서 생성한 스레드의 `JoinHandle<T>`를 사용하는 방법과 `join`을 호출해 생성된 스레드가 `main`이 종료되기 전에 완료되도록 보장하는 방법을 보여준다.

<Listing number="16-2" file-name="src/main.rs" caption="`thread::spawn`에서 반환된 `JoinHandle<T>`를 저장해 스레드가 완료될 때까지 기다리기">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-02/src/main.rs}}
```

</Listing>

핸들에 `join`을 호출하면 현재 실행 중인 스레드는 해당 핸들이 나타내는 스레드가 종료될 때까지 블로킹된다. 스레드를 블로킹한다는 것은 해당 스레드가 작업을 수행하거나 종료하지 못하게 하는 것을 의미한다. `join` 호출을 메인 스레드의 `for` 루프 뒤에 배치했기 때문에, 리스트 16-2를 실행하면 다음과 비슷한 출력을 볼 수 있다:

<!-- 출력을 추출하지 않음. 출력 변경은 컴파일러의 변화보다는 스레드 실행 방식의 차이 때문일 가능성이 높음 -->

```text
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 1 from the spawned thread!
hi number 3 from the main thread!
hi number 2 from the spawned thread!
hi number 4 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
```

두 스레드는 계속 번갈아가며 실행되지만, `handle.join()` 호출로 인해 메인 스레드는 생성된 스레드가 완료될 때까지 기다린 후 종료된다.

이제 `handle.join()`을 `main`의 `for` 루프 앞으로 옮기면 어떤 일이 발생하는지 살펴보자:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/no-listing-01-join-too-early/src/main.rs}}
```

</Listing>

메인 스레드는 생성된 스레드가 완료될 때까지 기다린 후 `for` 루프를 실행하므로, 출력은 더 이상 섞이지 않는다:

<!-- 출력을 추출하지 않음. 출력 변경은 컴파일러의 변화보다는 스레드 실행 방식의 차이 때문일 가능성이 높음 -->

```text
hi number 1 from the spawned thread!
hi number 2 from the spawned thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 3 from the main thread!
hi number 4 from the main thread!
```

`join`을 어디서 호출하는지와 같은 작은 세부 사항도 스레드가 동시에 실행되는지 여부에 영향을 미칠 수 있다.


### `move` 클로저와 스레드 함께 사용하기

`thread::spawn`에 전달하는 클로저와 함께 `move` 키워드를 자주 사용한다. 이는 클로저가 환경에서 사용하는 값의 소유권을 가져가기 때문이다. 따라서 해당 값의 소유권이 한 스레드에서 다른 스레드로 이전된다. 13장의 ["클로저로 환경 캡처하기"][capture]에서 클로저의 맥락에서 `move`에 대해 논의했다. 이제는 `move`와 `thread::spawn` 간의 상호작용에 더 집중할 것이다.

목록 16-1에서 `thread::spawn`에 전달하는 클로저는 인수를 받지 않는다. 생성된 스레드의 코드에서 메인 스레드의 데이터를 사용하지 않기 때문이다. 생성된 스레드에서 메인 스레드의 데이터를 사용하려면, 해당 스레드의 클로저가 필요한 값을 캡처해야 한다. 목록 16-3은 메인 스레드에서 벡터를 생성하고 이를 생성된 스레드에서 사용하려는 시도를 보여준다. 그러나 이 코드는 아직 작동하지 않는다.

<Listing number="16-3" file-name="src/main.rs" caption="메인 스레드에서 생성한 벡터를 다른 스레드에서 사용하려는 시도">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-03/src/main.rs}}
```

</Listing>

클로저는 `v`를 사용하므로 `v`를 캡처해 클로저 환경의 일부로 만든다. `thread::spawn`은 이 클로저를 새로운 스레드에서 실행하므로, 새로운 스레드 내부에서 `v`에 접근할 수 있어야 한다. 그러나 이 예제를 컴파일하면 다음과 같은 에러가 발생한다.

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-03/output.txt}}
```

Rust는 `v`를 어떻게 캡처할지 추론하며, `println!`이 `v`에 대한 참조만 필요로 하기 때문에 클로저는 `v`를 빌리려고 시도한다. 그러나 문제가 있다. Rust는 생성된 스레드가 얼마나 오래 실행될지 알 수 없기 때문에 `v`에 대한 참조가 항상 유효한지 알 수 없다.

목록 16-4는 `v`에 대한 참조가 유효하지 않을 가능성이 더 높은 시나리오를 보여준다.

<Listing number="16-4" file-name="src/main.rs" caption="메인 스레드에서 `v`를 드롭한 후 `v`에 대한 참조를 캡처하려는 클로저가 있는 스레드">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-04/src/main.rs}}
```

</Listing>

Rust가 이 코드를 실행하도록 허용한다면, 생성된 스레드가 백그라운드로 즉시 이동되어 전혀 실행되지 않을 가능성이 있다. 생성된 스레드는 내부에 `v`에 대한 참조를 가지고 있지만, 메인 스레드는 15장에서 논의한 `drop` 함수를 사용해 즉시 `v`를 드롭한다. 그러면 생성된 스레드가 실행을 시작할 때 `v`는 더 이상 유효하지 않으므로, 그 참조도 무효가 된다. 큰 문제다!

목록 16-3의 컴파일 에러를 수정하기 위해 에러 메시지의 조언을 따를 수 있다.

```text
help: to force the closure to take ownership of `v` (and any other referenced variables), use the `move` keyword
  |
6 |     let handle = thread::spawn(move || {
  |                                ++++
```

클로저 앞에 `move` 키워드를 추가함으로써, 클로저가 사용하는 값의 소유권을 가져가도록 강제한다. Rust가 값을 빌리도록 추론하는 대신, 값을 소유하도록 만든다. 목록 16-5는 목록 16-3을 수정한 것으로, 의도한 대로 컴파일되고 실행된다.

<Listing number="16-5" file-name="src/main.rs" caption="`move` 키워드를 사용해 클로저가 사용하는 값의 소유권을 강제로 가져가도록 함">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-05/src/main.rs}}
```

</Listing>

목록 16-4의 코드를 수정하기 위해 `move` 클로저를 사용해 같은 방법을 시도하고 싶을 수 있다. 그러나 이 수정은 작동하지 않는다. 목록 16-4가 시도하는 작업은 다른 이유로 허용되지 않기 때문이다. 클로저에 `move`를 추가하면 `v`를 클로저의 환경으로 이동시키고, 메인 스레드에서 더 이상 `drop`을 호출할 수 없게 된다. 대신 다음과 같은 컴파일 에러가 발생한다.

```console
{{#include ../listings/ch16-fearless-concurrency/output-only-01-move-drop/output.txt}}
```

Rust의 소유권 규칙이 다시 한번 우리를 구했다! 목록 16-3의 코드에서 에러가 발생한 이유는 Rust가 보수적으로 접근해 스레드에 대해 `v`를 빌려주기만 했기 때문이다. 이는 메인 스레드가 이론적으로 생성된 스레드의 참조를 무효화할 수 있다는 의미였다. Rust에게 `v`의 소유권을 생성된 스레드로 이동하라고 알림으로써, 메인 스레드가 더 이상 `v`를 사용하지 않을 것임을 보장한다. 목록 16-4를 같은 방식으로 변경하면, 메인 스레드에서 `v`를 사용하려고 할 때 소유권 규칙을 위반하게 된다. `move` 키워드는 Rust의 보수적인 기본값인 빌리기를 재정의한다. 하지만 소유권 규칙을 위반하도록 허용하지는 않는다.

이제 스레드가 무엇인지와 스레드 API가 제공하는 메서드를 살펴봤으니, 스레드를 사용할 수 있는 몇 가지 상황을 알아보자.

[capture]: ch13-01-closures.html#capturing-the-environment-with-closures


