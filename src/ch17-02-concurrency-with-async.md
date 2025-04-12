## 동시성 처리와 Async의 활용

<!-- Old headings. Do not remove or links may break. -->

<a id="concurrency-with-async"></a>

이번 섹션에서는 16장에서 스레드를 사용해 해결했던 동시성 문제를 async를 활용해 다시 접근한다. 이미 핵심 개념은 충분히 다뤘으므로, 이번에는 스레드와 future의 차이점에 집중한다.

대부분의 경우, async를 활용한 동시성 처리 API는 스레드를 사용할 때와 매우 유사하다. 하지만 다른 경우에는 상당히 다르게 동작한다. 스레드와 async의 API가 비슷해 보이더라도 실제 동작은 다르며, 성능 특성도 거의 항상 차이가 있다.

<!-- Old headings. Do not remove or links may break. -->

<a id="counting"></a>


### `spawn_task`를 사용해 새 작업 생성하기

[새 스레드 생성하기][thread-spawn]<!-- ignore -->에서 다룬 첫 번째 작업은 두 개의 별도 스레드에서 카운트를 세는 것이었다. 이번에는 async를 사용해 동일한 작업을 해보자. `trpl` 크레이트는 `thread::spawn` API와 매우 유사한 `spawn_task` 함수와 `thread::sleep` API의 async 버전인 `sleep` 함수를 제공한다. 이 두 함수를 함께 사용해 카운팅 예제를 구현할 수 있으며, 그 예는 리스트 17-6에서 확인할 수 있다.

<Listing number="17-6" caption="주 작업이 다른 내용을 출력하는 동안 새 작업을 생성해 한 가지를 출력하기" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-06/src/main.rs:all}}
```

</Listing>

시작점으로, `main` 함수를 `trpl::run`으로 설정해 최상위 함수가 async가 되도록 한다.

> 참고: 이 장의 나머지 부분에서 모든 예제는 `main` 함수에 `trpl::run`을 포함한 동일한 래핑 코드를 사용할 것이다. 따라서 `main` 함수를 생략할 때도 이 코드를 포함해야 한다는 점을 잊지 말자!

그런 다음 해당 블록 안에 두 개의 루프를 작성한다. 각 루프에는 `trpl::sleep` 호출이 포함되어 있으며, 이는 다음 메시지를 보내기 전에 0.5초(500밀리초) 동안 기다린다. 하나의 루프는 `trpl::spawn_task`의 본문에 넣고, 다른 하나는 최상위 `for` 루프에 넣는다. 또한 `sleep` 호출 뒤에 `await`를 추가한다.

이 코드는 스레드 기반 구현과 유사하게 동작한다. 단, 실행 시 터미널에서 메시지가 다른 순서로 나타날 수 있다는 점도 포함된다:

<!-- 출력을 추출하지 않음. 이 출력의 변경은 컴파일러의 변경보다는 스레드가 다르게 실행되기 때문일 가능성이 높음 -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
```

이 버전은 주 async 블록의 `for` 루프가 끝나자마자 종료된다. `spawn_task`로 생성된 작업은 `main` 함수가 끝나면 종료되기 때문이다. 작업이 완료될 때까지 실행되게 하려면, 첫 번째 작업이 완료될 때까지 기다리기 위해 조인 핸들을 사용해야 한다. 스레드에서는 `join` 메서드를 사용해 스레드가 실행을 마칠 때까지 "블로킹"했다. 리스트 17-7에서는 `await`를 사용해 동일한 작업을 수행할 수 있다. 작업 핸들 자체가 future이기 때문이다. `Output` 타입은 `Result`이므로, `await` 후에 이를 언래핑한다.

<Listing number="17-7" caption="조인 핸들에 `await`를 사용해 작업을 완료까지 실행하기" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-07/src/main.rs:handle}}
```

</Listing>

이 업데이트된 버전은 _두_ 루프가 모두 끝날 때까지 실행된다.

<!-- 출력을 추출하지 않음. 이 출력의 변경은 컴파일러의 변경보다는 스레드가 다르게 실행되기 때문일 가능성이 높음 -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

지금까지 async와 스레드는 기본적으로 동일한 결과를 제공하지만, 구문만 다르다는 것을 알 수 있다: 조인 핸들에 `join`을 호출하는 대신 `await`를 사용하고, `sleep` 호출에 `await`를 사용한다.

더 큰 차이점은 이 작업을 위해 또 다른 운영체제 스레드를 생성할 필요가 없다는 점이다. 사실 여기서는 작업을 생성할 필요조차 없다. async 블록은 익명 future로 컴파일되기 때문에, 각 루프를 async 블록에 넣고 `trpl::join` 함수를 사용해 런타임이 두 루프를 모두 완료할 때까지 실행하도록 할 수 있다.

[모든 스레드가 완료될 때까지 기다리기][join-handles]<!-- ignore --> 섹션에서는 `std::thread::spawn`을 호출할 때 반환되는 `JoinHandle` 타입에 `join` 메서드를 사용하는 방법을 보여줬다. `trpl::join` 함수는 이와 유사하지만 future를 대상으로 한다. 두 future를 주면, 이들이 _모두_ 완료된 후 각 future의 출력을 포함하는 튜플을 출력하는 단일 새로운 future를 생성한다. 따라서 리스트 17-8에서는 `trpl::join`을 사용해 `fut1`과 `fut2`가 모두 끝날 때까지 기다린다. `fut1`과 `fut2`를 `await`하는 대신, `trpl::join`이 생성한 새로운 future를 `await`한다. 출력은 두 단위 값을 포함하는 튜플이므로 이를 무시한다.

<Listing number="17-8" caption="`trpl::join`을 사용해 두 익명 future를 await하기" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-08/src/main.rs:join}}
```

</Listing>

이 코드를 실행하면 두 future가 모두 완료될 때까지 실행되는 것을 볼 수 있다:

<!-- 출력을 추출하지 않음. 이 출력의 변경은 컴파일러의 변경보다는 스레드가 다르게 실행되기 때문일 가능성이 높음 -->

```text
hi number 1 from the first task!
hi number 1 from the second task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

이제 매번 동일한 순서로 출력되는 것을 볼 수 있다. 이는 스레드에서 본 것과 매우 다르다. `trpl::join` 함수는 _공정_하기 때문이다. 즉, 각 future를 동일한 빈도로 확인하고 번갈아가며 실행하며, 한 future가 준비되어 있으면 다른 future가 앞서 나가지 않도록 한다. 스레드의 경우 운영체제가 어떤 스레드를 확인할지와 얼마나 오래 실행할지를 결정한다. async Rust에서는 런타임이 어떤 작업을 확인할지 결정한다. (실제로는 async 런타임이 내부적으로 운영체제 스레드를 사용해 동시성을 관리할 수 있으므로 공정성을 보장하는 것이 더 많은 작업이 될 수 있지만, 여전히 가능하다!) 런타임은 특정 작업에 대해 공정성을 보장할 필요는 없으며, 종종 공정성을 원하는지 여부를 선택할 수 있도록 다양한 API를 제공한다.

future를 await하는 이러한 변형을 시도해보고 어떤 결과가 나오는지 확인해보자:

- 하나 또는 두 루프 주변의 async 블록을 제거한다.
- async 블록을 정의한 직후에 바로 await한다.
- 첫 번째 루프만 async 블록으로 감싸고, 두 번째 루프의 본문 이후에 결과 future를 await한다.

추가 도전으로, 코드를 실행하기 전에 각 경우의 출력이 어떻게 될지 예측해보자!

<!-- 오래된 헤딩. 제거하지 말 것. 링크가 깨질 수 있음. -->

<a id="message-passing"></a>


### 두 작업에서 메시지 전달을 사용해 카운팅하기

퓨처 간에 데이터를 공유하는 방법은 이미 익숙할 것이다. 이번에도 메시지 전달 방식을 사용하지만, 비동기 버전의 타입과 함수를 활용한다. [스레드 간 데이터 전달을 위한 메시지 전달][message-passing-threads]<!-- ignore -->에서 다룬 방식과는 약간 다른 접근법을 통해 스레드 기반 동시성과 퓨처 기반 동시성의 주요 차이점을 살펴본다. 리스트 17-9에서는 단일 async 블록으로 시작한다. 별도의 스레드를 생성하지 않고, 별도의 작업도 생성하지 않는다.

<Listing number="17-9" caption="비동기 채널을 생성하고 `tx`와 `rx`에 할당하기" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-09/src/main.rs:channel}}
```

</Listing>

여기서는 `trpl::channel`을 사용한다. 이는 16장에서 스레드와 함께 사용한 다중 생산자, 단일 소비자 채널 API의 비동기 버전이다. 비동기 버전 API는 스레드 기반 버전과 크게 다르지 않다. 불변 수신자 `rx` 대신 가변 수신자를 사용하며, `recv` 메서드는 값을 직접 반환하는 대신 퓨처를 생성해 await해야 한다. 이제 송신자에서 수신자로 메시지를 보낼 수 있다. 별도의 스레드나 작업을 생성할 필요 없이, 단순히 `rx.recv` 호출을 await하면 된다.

`std::mpsc::channel`의 동기식 `Receiver::recv` 메서드는 메시지를 받을 때까지 블로킹된다. 반면 `trpl::Receiver::recv` 메서드는 비동기식이므로 블로킹되지 않는다. 대신, 메시지를 받거나 채널의 송신 측이 닫힐 때까지 런타임에 제어권을 넘긴다. 반면 `send` 호출은 블로킹되지 않으므로 await하지 않는다. 우리가 사용하는 채널은 무제한이므로 블로킹할 필요가 없다.

> 참고: 이 모든 비동기 코드는 `trpl::run` 호출 내의 async 블록에서 실행되므로, 내부에서는 블로킹을 피할 수 있다. 그러나 외부 코드는 `run` 함수가 반환될 때까지 블로킹된다. 이것이 `trpl::run` 함수의 핵심이다. 이 함수를 사용하면 비동기 코드 세트에서 블로킹할 위치를 선택할 수 있으며, 동기 코드와 비동기 코드 간 전환 지점을 결정할 수 있다. 대부분의 비동기 런타임에서 `run`은 정확히 이 이유로 `block_on`이라고 불린다.

이 예제에서 두 가지를 주목하자. 첫째, 메시지는 즉시 도착한다. 둘째, 여기서 퓨처를 사용하지만 아직 동시성이 없다. 리스트의 모든 작업은 퓨처가 없을 때와 마찬가지로 순차적으로 실행된다.

첫 번째 부분을 해결하기 위해 일련의 메시지를 보내고 그 사이에 잠시 대기하는 방법을 알아보자. 리스트 17-10에서 이를 확인할 수 있다.

<!-- 이 예제는 테스트할 수 없으며, 종료되지 않는다! -->

<Listing number="17-10" caption="비동기 채널을 통해 여러 메시지를 보내고 받으며 각 메시지 사이에 `await`로 대기하기" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-10/src/main.rs:many-messages}}
```

</Listing>

메시지를 보내는 것 외에도, 이를 받아야 한다. 이 경우에는 몇 개의 메시지가 오는지 알고 있으므로 `rx.recv().await`를 네 번 호출해 수동으로 처리할 수 있다. 그러나 실제 상황에서는 대개 알 수 없는 수의 메시지를 기다리므로, 더 이상 메시지가 없을 때까지 계속 대기해야 한다.

리스트 16-10에서는 동기 채널에서 받은 모든 항목을 처리하기 위해 `for` 루프를 사용했다. 그러나 Rust는 아직 비동기 항목 시퀀스에 대해 `for` 루프를 작성할 수 있는 방법을 제공하지 않으므로, 새로운 루프인 `while let` 조건 루프를 사용해야 한다. 이는 [간결한 제어 흐름: `if let`과 `let else`][if-let]<!-- ignore -->에서 본 `if let` 구문의 루프 버전이다. 이 루프는 지정된 패턴이 값과 계속 일치하는 한 실행을 계속한다.

`rx.recv` 호출은 퓨처를 생성하며, 이를 await한다. 런타임은 퓨처가 준비될 때까지 일시 중지한다. 메시지가 도착하면 퓨처는 `Some(message)`로 해결된다. 채널이 닫히면, 메시지가 도착했는지 여부와 상관없이 퓨처는 `None`으로 해결되어 더 이상 값이 없으므로 폴링(즉, await)을 중지해야 함을 나타낸다.

`while let` 루프는 이 모든 것을 하나로 묶는다. `rx.recv().await` 호출 결과가 `Some(message)`라면, 루프 본문에서 메시지에 접근해 사용할 수 있다. `if let`과 마찬가지로, 결과가 `None`이면 루프가 종료된다. 루프가 완료될 때마다 다시 await 지점에 도달하므로, 런타임은 다른 메시지가 도착할 때까지 다시 일시 중지한다.

이제 코드는 모든 메시지를 성공적으로 보내고 받는다. 그러나 아직 몇 가지 문제가 남아 있다. 첫째, 메시지가 0.5초 간격으로 도착하지 않는다. 프로그램 시작 후 2초(2,000밀리초)가 지나면 한꺼번에 도착한다. 둘째, 이 프로그램은 종료되지 않는다! 대신, 새로운 메시지를 영원히 기다린다. <span class="keystroke">ctrl-c</span>를 눌러 강제로 종료해야 한다.

먼저, 메시지가 각각의 지연 시간 사이에 도착하는 대신 전체 지연 시간 후에 한꺼번에 도착하는 이유를 살펴보자. 주어진 async 블록 내에서 `await` 키워드가 코드에 나타나는 순서는 프로그램 실행 시 실행 순서와 동일하다.

리스트 17-10에는 하나의 async 블록만 있으므로, 내부의 모든 작업은 선형적으로 실행된다. 여전히 동시성이 없다. 모든 `tx.send` 호출이 발생하고, 그 사이에 `trpl::sleep` 호출과 관련된 await 지점이 있다. 그런 후에야 `while let` 루프가 `recv` 호출의 await 지점을 처리할 수 있다.

각 메시지 사이에 지연 시간이 발생하는 동작을 얻으려면, `tx`와 `rx` 작업을 각각의 async 블록에 배치해야 한다. 리스트 17-11에서 이를 확인할 수 있다. 이렇게 하면 런타임이 `trpl::join`을 사용해 각 블록을 별도로 실행할 수 있다. 다시 한번, `trpl::join` 호출 결과를 await하며, 개별 퓨처를 await하지 않는다. 개별 퓨처를 순차적으로 await하면, 우리가 피하려고 했던 순차적 흐름으로 돌아가게 된다.

<!-- 이 예제는 테스트할 수 없으며, 종료되지 않는다! -->

<Listing number="17-11" caption="`send`와 `recv`를 각각의 `async` 블록으로 분리하고 이 블록의 퓨처를 await하기" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-11/src/main.rs:futures}}
```

</Listing>

리스트 17-11의 업데이트된 코드를 통해 메시지는 2초 후에 한꺼번에 도착하는 대신 500밀리초 간격으로 출력된다.

그러나 프로그램은 여전히 종료되지 않는다. 이는 `while let` 루프와 `trpl::join`의 상호작용 방식 때문이다:

- `trpl::join`에서 반환된 퓨처는 전달된 두 퓨처가 모두 완료된 후에야 완료된다.
- `tx` 퓨처는 `vals`의 마지막 메시지를 보낸 후 잠시 대기한 후 완료된다.
- `rx` 퓨처는 `while let` 루프가 종료될 때까지 완료되지 않는다.
- `while let` 루프는 `rx.recv`를 await한 결과가 `None`이 될 때까지 종료되지 않는다.
- `rx.recv`를 await한 결과가 `None`을 반환하려면 채널의 다른 쪽이 닫혀야 한다.
- 채널은 `rx.close`를 호출하거나 송신 측인 `tx`가 삭제될 때만 닫힌다.
- 우리는 어디에서도 `rx.close`를 호출하지 않으며, `tx`는 `trpl::run`에 전달된 가장 바깥쪽 async 블록이 종료될 때까지 삭제되지 않는다.
- 이 블록은 `trpl::join`이 완료될 때까지 블로킹되므로 종료할 수 없다.

어딘가에서 `rx.close`를 호출해 수동으로 닫을 수 있지만, 이는 큰 의미가 없다. 임의의 수의 메시지를 처리한 후 프로그램을 종료하면 메시지를 놓칠 수 있다. 함수가 종료되기 전에 `tx`가 삭제되도록 하는 다른 방법이 필요하다.

현재, 메시지를 보내는 async 블록은 `tx`를 빌려 사용한다. 메시지를 보내는 데 소유권이 필요하지 않기 때문이다. 그러나 `tx`를 이 async 블록으로 이동시킬 수 있다면, 블록이 종료될 때 삭제될 것이다. 13장의 [참조 캡처 또는 소유권 이동][capture-or-move]<!-- ignore -->에서 클로저와 함께 `move` 키워드를 사용하는 방법을 배웠다. 16장의 [스레드와 함께 `move` 클로저 사용하기][move-threads]<!-- ignore -->에서도 스레드 작업 시 데이터를 클로저로 이동해야 하는 경우가 많다는 것을 확인했다. async 블록에도 동일한 기본 원칙이 적용되므로, `move` 키워드는 클로저와 마찬가지로 async 블록에서도 작동한다.

리스트 17-12에서는 메시지를 보내는 블록을 `async`에서 `async move`로 변경한다. 이 버전의 코드를 실행하면 마지막 메시지가 보내지고 받은 후에 정상적으로 종료된다.

<Listing number="17-12" caption="리스트 17-11의 코드를 수정해 완료 시 정상적으로 종료되도록 함" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-12/src/main.rs:with-move}}
```

</Listing>

이 비동기 채널은 다중 생산자 채널이기도 하므로, 여러 퓨처에서 메시지를 보내려면 `tx`를 복제할 수 있다. 리스트 17-13에서 이를 확인할 수 있다.

<Listing number="17-13" caption="여러 생산자와 async 블록 사용하기" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-13/src/main.rs:here}}
```

</Listing>

먼저, `tx`를 복제해 첫 번째 async 블록 외부에서 `tx1`을 생성한다. 이전에 `tx`를 이동시켰던 것처럼 `tx1`을 이 블록으로 이동시킨다. 그런 다음, 원래의 `tx`를 새로운 async 블록으로 이동시켜 약간 더 느린 지연 시간으로 더 많은 메시지를 보낸다. 이 새로운 async 블록은 메시지를 받는 async 블록 뒤에 배치했지만, 앞에 배치해도 상관없다. 핵심은 퓨처가 생성된 순서가 아니라 await된 순서다.

메시지를 보내는 두 async 블록 모두 `async move` 블록이어야 하므로, 두 블록이 완료될 때 `tx`와 `tx1`이 삭제된다. 그렇지 않으면, 처음에 시작했던 무한 루프로 돌아가게 된다. 마지막으로, 추가 퓨처를 처리하기 위해 `trpl::join` 대신 `trpl::join3`으로 전환한다.

이제 두 송신 퓨처의 모든 메시지가 출력되며, 송신 퓨처가 약간 다른 지연 시간을 사용하므로 메시지도 다른 간격으로 받는다.

<!-- 출력을 추출하지 않음. 이 출력의 변경은 컴파일러의 변경보다는 스레드 실행 방식의 차이로 인한 것일 가능성이 높음 -->

```text
received 'hi'
received 'more'
received 'from'
received 'the'
received 'messages'
received 'future'
received 'for'
received 'you'
```

이는 좋은 시작이지만, `join`으로 두 개, `join3`으로 세 개의 퓨처로 제한된다. 더 많은 퓨처를 다루는 방법을 살펴보자.

[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[join-handles]: ch16-01-threads.html#waiting-for-all-threads-to-finish-using-join-handles
[message-passing-threads]: ch16-02-message-passing.html
[if-let]: ch06-03-if-let.html
[capture-or-move]: ch13-01-closures.html#capturing-references-or-moving-ownership
[move-threads]: ch16-01-threads.html#using-move-closures-with-threads


