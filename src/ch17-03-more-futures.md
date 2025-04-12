## 여러 개의 Future 다루기

이전 섹션에서 두 개의 Future에서 세 개로 바꾸면서 `join` 대신 `join3`을 사용해야 했다. Future의 개수가 바뀔 때마다 다른 함수를 호출해야 한다면 번거로울 것이다. 다행히 `join`의 매크로 형태가 있어서 임의의 개수의 인자를 전달할 수 있다. 또한 Future를 직접 대기할 수도 있다. 따라서 리스트 17-13의 코드를 `join3` 대신 `join!`을 사용하도록 리스트 17-14와 같이 다시 작성할 수 있다.

<리스트 번호="17-14" 캡션="`join!`을 사용해 여러 Future를 대기하기" 파일명="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-14/src/main.rs:here}}
```

</리스트>

이 방법은 `join`, `join3`, `join4` 등을 번갈아 사용하는 것보다 확실히 나아졌다! 하지만 이 매크로 형태도 Future의 개수를 미리 알고 있을 때만 작동한다. 실제 Rust에서는 Future를 컬렉션에 넣고 그 중 일부 또는 전체가 완료될 때까지 기다리는 패턴이 흔히 사용된다.

컬렉션에 있는 모든 Future를 확인하려면 _모든_ Future를 순회하며 대기해야 한다. `trpl::join_all` 함수는 `Iterator` 트레잇을 구현한 모든 타입을 받는다. 이 트레잇은 [The Iterator Trait and the `next` Method][iterator-trait]<!-- ignore --> 챕터 13에서 다뤘다. 따라서 이 함수가 적합해 보인다. Future를 벡터에 넣고 `join!` 대신 `join_all`을 사용해보자. 리스트 17-15와 같이 작성할 수 있다.

<리스트 번호="17-15" 캡션="익명 Future를 벡터에 저장하고 `join_all` 호출하기">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-15/src/main.rs:here}}
```

</리스트>

안타깝게도 이 코드는 컴파일되지 않는다. 대신 다음과 같은 에러가 발생한다:

```text
error[E0308]: mismatched types
  --> src/main.rs:45:37
   |
10 |         let tx1_fut = async move {
   |                       ---------- the expected `async` block
...
24 |         let rx_fut = async {
   |                      ----- the found `async` block
...
45 |         let futures = vec![tx1_fut, rx_fut, tx_fut];
   |                                     ^^^^^^ expected `async` block, found a different `async` block
   |
   = note: expected `async` block `{async block@src/main.rs:10:23: 10:33}`
              found `async` block `{async block@src/main.rs:24:22: 24:27}`
   = note: no two async blocks, even if identical, have the same type
   = help: consider pinning your async block and casting it to a trait object
```

이 결과는 놀라울 수 있다. 결국 모든 async 블록은 아무것도 반환하지 않으므로 각각 `Future<Output = ()>`를 생성한다. 하지만 `Future`는 트레잇이며, 컴파일러는 각 async 블록에 대해 고유한 enum을 생성한다. 두 개의 서로 다른 구조체를 `Vec`에 넣을 수 없는 것처럼, 컴파일러가 생성한 서로 다른 enum도 같은 규칙이 적용된다.

이 문제를 해결하려면 _트레잇 객체_를 사용해야 한다. [“Returning Errors from the run function”][dyn]<!-- ignore --> 챕터 12에서와 마찬가지로 트레잇 객체를 사용하면 각 익명 Future를 같은 타입으로 취급할 수 있다. 이는 모두 `Future` 트레잇을 구현하기 때문이다.

> 참고: [Using an Enum to Store Multiple Values][enum-alt]<!-- ignore --> 챕터 8에서 `Vec`에 여러 타입을 포함하는 또 다른 방법을 논의했다. enum을 사용해 벡터에 나타날 수 있는 각 타입을 표현하는 방법이다. 하지만 여기서는 이 방법을 사용할 수 없다. 첫째, 익명 타입이므로 서로 다른 타입에 이름을 붙일 방법이 없다. 둘째, 벡터와 `join_all`을 사용한 이유는 동적으로 Future 컬렉션을 다루기 위함이었고, 출력 타입이 같기만 하면 된다.

먼저 `vec!` 안의 각 Future를 `Box::new`로 감싼다. 리스트 17-16과 같이 작성할 수 있다.

<리스트 번호="17-16" 캡션="`Box::new`를 사용해 `Vec` 안의 Future 타입을 맞추기" 파일명="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-16/src/main.rs:here}}
```

</리스트>

안타깝게도 이 코드도 여전히 컴파일되지 않는다. 사실 두 번째와 세 번째 `Box::new` 호출에서 이전과 같은 기본 에러가 발생하며, `Unpin` 트레잇과 관련된 새로운 에러도 나타난다. 잠시 후 `Unpin` 에러로 돌아올 것이다. 먼저 `Box::new` 호출에서 발생한 타입 에러를 해결하기 위해 `futures` 변수의 타입을 명시적으로 지정한다. 리스트 17-17과 같이 작성할 수 있다.

<리스트 번호="17-17" 캡션="명시적 타입 선언을 사용해 나머지 타입 불일치 에러 해결하기" 파일명="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-17/src/main.rs:here}}
```

</리스트>

이 타입 선언은 조금 복잡하므로 단계별로 살펴보자:

1. 가장 안쪽 타입은 Future 자체다. Future의 출력이 단위 타입 `()`임을 `Future<Output = ()>`로 명시한다.
2. 그런 다음 트레잇을 `dyn`으로 표시해 동적임을 나타낸다.
3. 전체 트레잇 참조를 `Box`로 감싼다.
4. 마지막으로 `futures`가 이러한 항목을 포함하는 `Vec`임을 명시한다.

이렇게 하면 큰 차이가 생긴다. 이제 컴파일러를 실행하면 `Unpin`과 관련된 에러만 나타난다. 세 개의 에러가 있지만 내용은 매우 비슷하다.


# 오류만 복사

# 경로 수정

-->

```text
error[E0277]: `dyn Future<Output = ()>` cannot be unpinned
   --> src/main.rs:49:24
    |
49  |         trpl::join_all(futures).await;
    |         -------------- ^^^^^^^ the trait `Unpin` is not implemented for `dyn Future<Output = ()>`
    |         |
    |         required by a bound introduced by this call
    |
    = note: consider using the `pin!` macro
            consider using `Box::pin` if you need to access the pinned value outside of the current scope
    = note: required for `Box<dyn Future<Output = ()>>` to implement `Future`
note: required by a bound in `join_all`
   --> file:///home/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/futures-util-0.3.30/src/future/join_all.rs:105:14
    |
102 | pub fn join_all<I>(iter: I) -> JoinAll<I::Item>
    |        -------- required by a bound in this function
...
105 |     I::Item: Future,
    |              ^^^^^^ required by this bound in `join_all`

error[E0277]: `dyn Future<Output = ()>` cannot be unpinned
  --> src/main.rs:49:9
   |
49 |         trpl::join_all(futures).await;
   |         ^^^^^^^^^^^^^^^^^^^^^^^ the trait `Unpin` is not implemented for `dyn Future<Output = ()>`
   |
   = note: consider using the `pin!` macro
           consider using `Box::pin` if you need to access the pinned value outside of the current scope
   = note: required for `Box<dyn Future<Output = ()>>` to implement `Future`
note: required by a bound in `futures_util::future::join_all::JoinAll`
  --> file:///home/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/futures-util-0.3.30/src/future/join_all.rs:29:8
   |
27 | pub struct JoinAll<F>
   |            ------- required by a bound in this struct
28 | where
29 |     F: Future,
   |        ^^^^^^ required by this bound in `JoinAll`

error[E0277]: `dyn Future<Output = ()>` cannot be unpinned
  --> src/main.rs:49:33
   |
49 |         trpl::join_all(futures).await;
   |                                 ^^^^^ the trait `Unpin` is not implemented for `dyn Future<Output = ()>`
   |
   = note: consider using the `pin!` macro
           consider using `Box::pin` if you need to access the pinned value outside of the current scope
   = note: required for `Box<dyn Future<Output = ()>>` to implement `Future`
note: required by a bound in `futures_util::future::join_all::JoinAll`
  --> file:///home/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/futures-util-0.3.30/src/future/join_all.rs:29:8
   |
27 | pub struct JoinAll<F>
   |            ------- required by a bound in this struct
28 | where
29 |     F: Future,
   |        ^^^^^^ required by this bound in `JoinAll`

For more information about this error, try `rustc --explain E0277`.
error: could not compile `async_await` (bin "async_await") due to 3 previous errors
```


### 퓨처 경주

`join` 계열의 함수와 매크로를 사용해 퓨처를 "조인"할 때는 모든 퓨처가 완료될 때까지 기다린다. 하지만 때로는 여러 퓨처 중 하나만 완료되면 진행할 수 있는 상황이 있다. 이는 마치 퓨처끼리 경주를 시키는 것과 비슷하다.

리스트 17-21에서는 다시 `trpl::race`를 사용해 `slow`와 `fast` 두 퓨처를 서로 경주시킨다.

<Listing number="17-21" caption="`race`를 사용해 먼저 완료된 퓨처의 결과를 얻기" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-21/src/main.rs:here}}
```

</Listing>

각 퓨처는 실행을 시작할 때 메시지를 출력하고, `sleep`을 호출하고 기다린 후, 완료되면 또 다른 메시지를 출력한다. 그런 다음 `slow`와 `fast`를 `trpl::race`에 전달하고 둘 중 하나가 완료될 때까지 기다린다. (결과는 당연히 `fast`가 이긴다.) [첫 번째 비동기 프로그램][async-program]에서 `race`를 사용했을 때와 달리, 여기서는 반환된 `Either` 인스턴스를 무시한다. 왜냐하면 모든 흥미로운 동작이 async 블록 내부에서 일어나기 때문이다.

`race`의 인자 순서를 바꾸면 "시작됨" 메시지의 순서가 바뀌지만, `fast` 퓨처는 항상 먼저 완료된다. 이는 이 특정 `race` 함수의 구현이 공정하지 않기 때문이다. 이 구현은 항상 전달된 순서대로 퓨처를 실행한다. 다른 구현들은 공정하며, 어떤 퓨처를 먼저 폴링할지 무작위로 선택한다. 하지만 우리가 사용하는 `race` 구현이 공정하든 아니든, 한 퓨처는 다른 태스크가 시작되기 전에 본문의 첫 번째 `await`까지 실행된다.

[첫 번째 비동기 프로그램][async-program]에서 기억할 수 있듯이, 각 await 지점에서 러스트는 런타임에게 태스크를 일시 중지하고, 기다리는 퓨처가 준비되지 않았다면 다른 태스크로 전환할 기회를 준다. 반대의 경우도 마찬가지다: 러스트는 async 블록을 일시 중지하고 await 지점에서만 런타임에 제어권을 넘긴다. await 지점 사이의 모든 작업은 동기적으로 실행된다.

즉, async 블록 내에서 await 지점 없이 많은 작업을 수행하면, 그 퓨처는 다른 퓨처가 진행하는 것을 막을 수 있다. 이를 종종 한 퓨처가 다른 퓨처를 **굶주리게** 만든다고 표현한다. 어떤 경우에는 이게 큰 문제가 되지 않을 수도 있다. 하지만 비용이 많이 드는 초기 설정이나 오래 실행되는 작업을 수행하거나, 특정 작업을 무한히 반복하는 퓨처가 있다면, 언제 어디서 런타임에 제어권을 넘길지 고민해야 한다.

마찬가지로, 오래 실행되는 블로킹 작업이 있다면, async는 프로그램의 다른 부분이 서로 관련을 맺을 수 있는 유용한 도구가 될 수 있다.

그렇다면 이런 경우에 어떻게 런타임에 제어권을 넘길 수 있을까?

<!-- Old headings. Do not remove or links may break. -->

<a id="yielding"></a>


### 런타임에 제어권 양보하기

긴 작업을 시뮬레이션해 보자. Listing 17-22는 `slow` 함수를 소개한다.

<Listing number="17-22" caption="`thread::sleep`을 사용해 느린 작업 시뮬레이션하기" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-22/src/main.rs:slow}}
```

</Listing>

이 코드는 `trpl::sleep` 대신 `std::thread::sleep`을 사용해 `slow` 함수를 호출하면 현재 스레드를 몇 밀리초 동안 블로킹한다. `slow` 함수는 실제로 오래 걸리고 블로킹되는 작업을 대신하는 역할을 한다.

Listing 17-23에서는 `slow` 함수를 사용해 두 개의 Future에서 CPU 집약적인 작업을 에뮬레이트한다.

<Listing number="17-23" caption="`thread::sleep`을 사용해 느린 작업 시뮬레이션하기" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-23/src/main.rs:slow-futures}}
```

</Listing>

처음에 각 Future는 여러 번의 느린 작업을 수행한 후에야 런타임에 제어권을 넘긴다. 이 코드를 실행하면 다음과 같은 출력을 볼 수 있다:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-23/
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'a' ran for 10ms
'a' ran for 20ms
'b' started.
'b' ran for 75ms
'b' ran for 10ms
'b' ran for 15ms
'b' ran for 350ms
'a' finished.
```

이전 예제와 마찬가지로 `a`가 완료되면 `race`도 즉시 종료된다. 하지만 두 Future 간에 작업이 교차하지는 않는다. `a` Future는 `trpl::sleep` 호출을 기다릴 때까지 모든 작업을 수행한 후, `b` Future가 자신의 `trpl::sleep` 호출을 기다릴 때까지 모든 작업을 수행하고, 마지막으로 `a` Future가 완료된다. 두 Future가 느린 작업 사이에 진행 상태를 유지하려면 런타임에 제어권을 넘길 수 있는 await 포인트가 필요하다. 즉, await할 수 있는 무언가가 필요하다!

Listing 17-23에서도 이런 제어권 전환이 일어나는 것을 볼 수 있다. `a` Future의 마지막에 있는 `trpl::sleep`을 제거하면 `b` Future가 전혀 실행되지 않고 `a` Future가 완료된다. Listing 17-24와 같이 `sleep` 함수를 사용해 작업이 번갈아가며 진행되도록 해보자.

<Listing number="17-24" caption="`sleep`을 사용해 작업이 번갈아가며 진행되도록 하기" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-24/src/main.rs:here}}
```

</Listing>

Listing 17-24에서는 각 `slow` 호출 사이에 await 포인트와 함께 `trpl::sleep` 호출을 추가한다. 이제 두 Future의 작업이 교차해서 진행된다:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-24
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'b' started.
'b' ran for 75ms
'a' ran for 10ms
'b' ran for 10ms
'a' ran for 20ms
'b' ran for 15ms
'a' finished.
```

`a` Future는 `trpl::sleep`을 호출하기 전에 `slow`를 호출하므로 `b`에 제어권을 넘기기 전에 조금 실행되지만, 그 이후에는 각 Future가 await 포인트에 도달할 때마다 번갈아가며 실행된다. 이 경우에는 모든 `slow` 호출 후에 await 포인트를 추가했지만, 작업을 어떻게 나누는지는 상황에 따라 달라질 수 있다.

하지만 여기서 우리가 원하는 것은 _sleep_이 아니라 가능한 한 빨리 작업을 진행하는 것이다. 단지 런타임에 제어권을 넘기기만 하면 된다. 이를 직접적으로 수행하기 위해 `yield_now` 함수를 사용할 수 있다. Listing 17-25에서는 모든 `sleep` 호출을 `yield_now`로 대체한다.

<Listing number="17-25" caption="`yield_now`를 사용해 작업이 번갈아가며 진행되도록 하기" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-25/src/main.rs:yields}}
```

</Listing>

이 코드는 실제 의도를 더 명확히 표현할 뿐만 아니라 `sleep`을 사용하는 것보다 훨씬 빠를 수 있다. 왜냐하면 `sleep`이 사용하는 타이머는 종종 최소 단위에 제한이 있기 때문이다. 예를 들어, 우리가 사용하는 `sleep` 버전은 1나노초의 `Duration`을 전달하더라도 항상 최소 1밀리초 동안 sleep한다. 다시 말하지만, 현대 컴퓨터는 _매우 빠르다_: 1밀리초 동안 많은 작업을 수행할 수 있다!

Listing 17-26과 같은 간단한 벤치마크를 설정해 이를 직접 확인할 수 있다. (이 방법은 성능 테스트를 수행하는 데 특히 엄격한 방법은 아니지만, 여기서 차이를 보여주기에는 충분하다.)

<Listing number="17-26" caption="`sleep`과 `yield_now`의 성능 비교" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-26/src/main.rs:here}}
```

</Listing>

여기서는 모든 상태 출력을 생략하고, `trpl::sleep`에 1나노초의 `Duration`을 전달한 후, 각 Future를 별도로 실행한다. 그리고 1,000번 반복 실행해 `trpl::sleep`을 사용한 Future와 `trpl::yield_now`를 사용한 Future의 실행 시간을 비교한다.

`yield_now`를 사용한 버전이 _훨씬_ 빠르다!

이는 async가 컴퓨팅 집약적인 작업에서도 유용할 수 있음을 보여준다. 프로그램의 다른 부분과의 관계를 구조화하는 데 유용한 도구를 제공하기 때문이다. 이는 _협력적 멀티태스킹(cooperative multitasking)_의 한 형태로, 각 Future가 await 포인트를 통해 제어권을 넘길 시점을 결정할 수 있다. 따라서 각 Future는 너무 오래 블로킹하지 않도록 주의해야 한다. 일부 Rust 기반 임베디드 운영체제에서는 이 방식이 _유일한_ 멀티태스킹 방식이다!

실제 코드에서는 보통 모든 줄마다 함수 호출과 await 포인트를 번갈아가며 사용하지는 않는다. 이렇게 제어권을 양보하는 것은 상대적으로 비용이 적지만, 무료는 아니다. 많은 경우, 컴퓨팅 집약적인 작업을 나누려고 하면 오히려 전체 성능이 크게 저하될 수 있으므로, 때로는 작업이 잠시 블로킹되는 것이 _전체_ 성능에 더 나을 수 있다. 항상 실제 성능 병목 현상을 측정해 보아야 한다. 하지만 만약 예상한 동시성이 아닌 직렬로 많은 작업이 수행되고 있다면, 이 기본 동작을 염두에 두는 것이 중요하다!


### 우리만의 비동기 추상화 만들기

우리는 이미 갖고 있는 비동기 빌딩 블록을 조합해 새로운 패턴을 만들 수 있다. 예를 들어, `timeout` 함수를 만들 수 있다. 이 작업이 끝나면, 결과적으로 우리가 사용할 수 있는 또 다른 빌딩 블록이 생긴다. 이를 통해 더 많은 비동기 추상화를 만들 수 있다.

Listing 17-27은 우리가 상상한 `timeout` 함수가 느린 future와 함께 어떻게 동작할지 보여준다.

<Listing number="17-27" caption="상상한 `timeout`을 사용해 시간 제한 내에 느린 작업 실행하기" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-27/src/main.rs:here}}
```

</Listing>

이제 이를 구현해보자. 먼저 `timeout`의 API를 생각해보자:

- 비동기 함수여야 한다. 그래서 `await`를 사용할 수 있다.
- 첫 번째 매개변수로 실행할 future를 받아야 한다. 모든 future와 호환되도록 제네릭으로 만들 수 있다.
- 두 번째 매개변수는 최대 대기 시간이다. `Duration`을 사용하면 `trpl::sleep`에 쉽게 전달할 수 있다.
- `Result`를 반환해야 한다. future가 성공적으로 완료되면 `Result`는 `Ok`와 함께 future가 생성한 값을 반환한다. 만약 타임아웃이 먼저 발생하면 `Result`는 `Err`와 함께 타임아웃이 대기한 시간을 반환한다.

Listing 17-28은 이 선언을 보여준다.

<!-- 이 코드는 의도적으로 컴파일되지 않으므로 테스트하지 않는다. -->

<Listing number="17-28" caption="`timeout`의 시그니처 정의" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-28/src/main.rs:declaration}}
```

</Listing>

이렇게 하면 타입에 대한 목표를 충족한다. 이제 우리가 필요한 _동작_을 생각해보자: 전달된 future와 duration을 경쟁시키고 싶다. `trpl::sleep`을 사용해 duration으로부터 타이머 future를 만들고, `trpl::race`를 사용해 이 타이머와 호출자가 전달한 future를 함께 실행할 수 있다.

또한 `race`는 공정하지 않으며, 전달된 순서대로 인수를 폴링한다는 것을 알고 있다. 따라서 `future_to_try`를 먼저 `race`에 전달해 `max_time`이 매우 짧은 duration일 때도 완료할 기회를 준다. `future_to_try`가 먼저 완료되면 `race`는 `Left`와 함께 `future_to_try`의 출력을 반환한다. `timer`가 먼저 완료되면 `race`는 `Right`와 함께 타이머의 출력인 `()`를 반환한다.

Listing 17-29에서는 `trpl::race`를 `await`한 결과를 매칭한다.

<Listing number="17-29" caption="`race`와 `sleep`을 사용해 `timeout` 정의하기" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-29/src/main.rs:implementation}}
```

</Listing>

`future_to_try`가 성공하고 `Left(output)`를 얻으면 `Ok(output)`를 반환한다. 대신 `sleep` 타이머가 만료되고 `Right(())`를 얻으면 `()`를 `_`로 무시하고 `Err(max_time)`를 반환한다.

이렇게 하면 두 개의 다른 비동기 헬퍼를 사용해 동작하는 `timeout`을 만들었다. 코드를 실행하면 타임아웃 후 실패 모드를 출력할 것이다:

```text
Failed after 2 seconds
```

future는 다른 future와 조합될 수 있으므로, 작은 비동기 빌딩 블록을 사용해 매우 강력한 도구를 만들 수 있다. 예를 들어, 이와 같은 접근 방식을 사용해 타임아웃과 재시도를 결합하고, 이를 네트워크 호출과 같은 작업에 사용할 수 있다(이 장의 시작 부분에서 다룬 예제 중 하나).

실제로는 주로 `async`와 `await`를 직접 사용하고, `join`, `join_all`, `race`와 같은 함수와 매크로를 보조적으로 사용할 것이다. `pin`은 가끔 이러한 API와 함께 future를 사용할 때만 필요하다.

이제 여러 future를 동시에 작업하는 여러 방법을 살펴보았다. 다음으로는 _스트림_을 사용해 시간에 따라 여러 future를 순차적으로 작업하는 방법을 살펴볼 것이다. 하지만 먼저 고려해볼 몇 가지 사항이 있다:

- `join_all`과 함께 `Vec`를 사용해 특정 그룹의 모든 future가 완료되기를 기다렸다. `Vec`를 사용해 그룹의 future를 순차적으로 처리하려면 어떻게 해야 할까? 그렇게 했을 때의 장단점은 무엇인가?

- `futures` 크레이트의 `futures::stream::FuturesUnordered` 타입을 살펴보자. `Vec`를 사용하는 것과 어떻게 다를까? (이 타입이 크레이트의 `stream` 부분에 있다는 사실은 걱정하지 않아도 된다. future의 어떤 컬렉션과도 잘 동작한다.)

[dyn]: ch12-03-improving-error-handling-and-modularity.html
[enum-alt]: ch08-01-vectors.html#using-an-enum-to-store-multiple-types
[async-program]: ch17-01-futures-and-syntax.html#our-first-async-program
[iterator-trait]: ch13-02-iterators.html#the-iterator-trait-and-the-next-method


