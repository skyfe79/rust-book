## 스트림: 순차적 Future

<!-- Old headings. Do not remove or links may break. -->

<a id="streams"></a>

이번 장에서는 주로 개별 Future에 대해 다뤘다. 한 가지 큰 예외는 이전에 사용했던 비동기 채널이다. [“메시지 전달”][17-02-messages]<!-- ignore --> 섹션에서 비동기 채널의 리시버를 어떻게 사용했는지 기억할 것이다. 비동기 `recv` 메서드는 시간에 따라 일련의 아이템을 생성한다. 이는 _스트림_ 이라는 더 일반적인 패턴의 한 예시다.

13장에서 `Iterator` 트레이트를 다룰 때 일련의 아이템을 본 적이 있다. 하지만 이터레이터와 비동기 채널 리시버 사이에는 두 가지 차이점이 있다. 첫 번째 차이점은 시간이다. 이터레이터는 동기적이지만, 채널 리시버는 비동기적이다. 두 번째 차이점은 API다. `Iterator`를 직접 사용할 때는 동기적인 `next` 메서드를 호출한다. 반면 `trpl::Receiver` 스트림에서는 비동기적인 `recv` 메서드를 대신 호출한다. 그 외에는 이 두 API가 매우 유사하며, 이 유사성은 우연이 아니다. 스트림은 비동기적인 형태의 이터레이션과 같다. `trpl::Receiver`가 특정 메시지를 수신하기 위해 대기하는 반면, 일반적인 스트림 API는 훨씬 더 넓은 범위를 제공한다. 이 API는 `Iterator`와 같은 방식으로 다음 아이템을 제공하지만, 비동기적으로 작동한다.

Rust에서 이터레이터와 스트림의 유사성은 실제로 어떤 이터레이터든 스트림으로 변환할 수 있다는 것을 의미한다. 이터레이터와 마찬가지로, 스트림의 `next` 메서드를 호출하고 출력을 기다리는 방식으로 작업할 수 있다. 이는 아래 예제 17-30에서 확인할 수 있다.

<예제 번호="17-30" 설명="이터레이터로부터 스트림을 생성하고 값을 출력하는 예제" 파일 이름="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-30/src/main.rs:stream}}
```

</예제>

숫자 배열로 시작해 이터레이터로 변환한 후, `map`을 호출해 모든 값을 두 배로 만든다. 그런 다음 `trpl::stream_from_iter` 함수를 사용해 이터레이터를 스트림으로 변환한다. 다음으로, `while let` 루프를 사용해 스트림의 아이템이 도착할 때마다 반복한다.

안타깝게도 이 코드를 실행하려고 하면 컴파일되지 않고, `next` 메서드가 없다는 오류가 발생한다.

```console
error[E0599]: no method named `next` found for struct `Iter` in the current scope
  --> src/main.rs:10:40
   |
10 |         while let Some(value) = stream.next().await {
   |                                        ^^^^
   |
   = note: the full type name has been written to 'file:///projects/async-await/target/debug/deps/async_await-575db3dd3197d257.long-type-14490787947592691573.txt'
   = note: consider using `--verbose` to print the full type name to the console
   = help: items from traits can only be used if the trait is in scope
help: the following traits which provide `next` are implemented but not in scope; perhaps you want to import one of them
   |
1  + use crate::trpl::StreamExt;
   |
1  + use futures_util::stream::stream::StreamExt;
   |
1  + use std::iter::Iterator;
   |
1  + use std::str::pattern::Searcher;
   |
help: there is a method `try_next` with a similar name
   |
10 |         while let Some(value) = stream.try_next().await {
   |                                        ~~~~~~~~
```

이 출력에서 설명하듯, 컴파일러 오류의 원인은 `next` 메서드를 사용하려면 적절한 트레이트가 스코프 내에 있어야 한다는 것이다. 지금까지의 논의를 고려하면, 이 트레이트가 `Stream`일 것이라고 예상할 수 있지만, 실제로는 `StreamExt`다. _extension_ 의 약자인 `Ext`는 Rust 커뮤니티에서 한 트레이트를 다른 트레이트로 확장하는 일반적인 패턴이다.

`Stream`과 `StreamExt` 트레이트에 대해서는 이 장의 끝에서 좀 더 자세히 설명할 것이다. 지금은 `Stream` 트레이트가 `Iterator`와 `Future` 트레이트를 효과적으로 결합한 저수준 인터페이스를 정의한다는 것만 알면 된다. `StreamExt`는 `Stream` 위에 `next` 메서드와 `Iterator` 트레이트에서 제공하는 유틸리티 메서드와 유사한 고수준 API 세트를 제공한다. `Stream`과 `StreamExt`는 아직 Rust의 표준 라이브러리에 포함되지 않았지만, 대부분의 생태계 크레이트가 동일한 정의를 사용한다.

컴파일러 오류를 수정하려면 `trpl::StreamExt`에 대한 `use` 문을 추가해야 한다. 이는 아래 예제 17-31에서 확인할 수 있다.

<예제 번호="17-31" 설명="이터레이터를 스트림의 기반으로 성공적으로 사용하는 예제" 파일 이름="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-31/src/main.rs:all}}
```

</예제>

이 모든 조각을 합치면, 이 코드는 원하는 대로 작동한다! 더 나아가, 이제 `StreamExt`가 스코프 내에 있으므로, 이터레이터와 마찬가지로 모든 유틸리티 메서드를 사용할 수 있다. 예를 들어, 예제 17-32에서는 `filter` 메서드를 사용해 3과 5의 배수만 남기도록 필터링한다.

<예제 번호="17-32" 설명="`StreamExt::filter` 메서드로 스트림 필터링하기" 파일 이름="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-32/src/main.rs:all}}
```

</예제>

물론, 이는 일반 이터레이터로도 할 수 있고, 비동기와는 전혀 무관하므로 그다지 흥미롭지 않다. 이제 스트림만의 고유한 기능을 살펴보자.


### 스트림 합성하기

많은 개념은 자연스럽게 스트림으로 표현할 수 있다. 큐에서 아이템이 사용 가능해지는 경우, 전체 데이터가 컴퓨터 메모리보다 클 때 파일 시스템에서 데이터를 점진적으로 가져오는 경우, 네트워크를 통해 시간이 지남에 따라 데이터가 도착하는 경우 등이 그 예이다. 스트림은 Future이기 때문에 다른 종류의 Future와 함께 사용할 수 있고, 흥미로운 방식으로 조합할 수 있다. 예를 들어, 너무 많은 네트워크 호출을 방지하기 위해 이벤트를 일괄 처리하거나, 장기 실행 작업 시퀀스에 타임아웃을 설정하거나, 불필요한 작업을 피하기 위해 사용자 인터페이스 이벤트를 조절할 수 있다.

먼저 WebSocket이나 다른 실시간 통신 프로토콜에서 볼 수 있는 데이터 스트림을 대체할 메시지 스트림을 만들어 보자. 이는 리스팅 17-33에 나와 있다.

<Listing number="17-33" caption="`rx` 수신기를 `ReceiverStream`으로 사용하기" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-33/src/main.rs:all}}
```

</Listing>

먼저 `get_messages`라는 함수를 만들고, 이 함수는 `impl Stream<Item = String>`을 반환한다. 구현에서는 비동기 채널을 생성하고, 영어 알파벳의 첫 10글자를 반복하며 채널을 통해 전송한다.

또한 `ReceiverStream`이라는 새로운 타입을 사용한다. 이 타입은 `trpl::channel`의 `rx` 수신기를 `next` 메서드가 있는 `Stream`으로 변환한다. `main` 함수에서는 `while let` 루프를 사용해 스트림에서 모든 메시지를 출력한다.

이 코드를 실행하면 예상한 결과를 얻을 수 있다:

<!-- 출력을 추출하지 않음. 이 출력의 변경은 중요하지 않으며, 컴파일러의 변경보다는 스레드가 다르게 실행되었기 때문일 가능성이 높음 -->

```text
Message: 'a'
Message: 'b'
Message: 'c'
Message: 'd'
Message: 'e'
Message: 'f'
Message: 'g'
Message: 'h'
Message: 'i'
Message: 'j'
```

하지만 이 작업은 일반 `Receiver` API나 심지어 일반 `Iterator` API로도 할 수 있다. 따라서 스트림이 필요한 기능을 추가해 보자: 스트림의 각 아이템에 타임아웃을 적용하고, 전송하는 아이템에 지연을 추가한다. 이는 리스팅 17-34에 나와 있다.

<Listing number="17-34" caption="스트림의 아이템에 시간 제한을 설정하기 위해 `StreamExt::timeout` 메서드 사용하기" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-34/src/main.rs:timeout}}
```

</Listing>

먼저 `StreamExt` 트레이트의 `timeout` 메서드를 사용해 스트림에 타임아웃을 추가한다. 그런 다음 `while let` 루프의 본문을 업데이트한다. 이제 스트림은 `Result`를 반환한다. `Ok` 변형은 메시지가 시간 내에 도착했음을 나타내고, `Err` 변형은 타임아웃이 지나기 전에 메시지가 도착하지 않았음을 나타낸다. 이 결과를 `match`로 처리하고, 메시지를 성공적으로 받으면 출력하고, 타임아웃이 발생하면 알림을 출력한다. 마지막으로, 타임아웃을 적용한 후 메시지를 고정한다. 타임아웃 헬퍼는 폴링되기 위해 고정이 필요한 스트림을 생성하기 때문이다.

하지만 메시지 사이에 지연이 없기 때문에 이 타임아웃은 프로그램의 동작을 변경하지 않는다. 이제 전송하는 메시지에 변수 지연을 추가해 보자. 이는 리스팅 17-35에 나와 있다.

<Listing number="17-35" caption="`get_messages`를 비동기 함수로 만들지 않고 `tx`를 통해 메시지를 비동기 지연과 함께 전송하기" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-35/src/main.rs:messages}}
```

</Listing>

`get_messages` 함수에서 `messages` 배열과 함께 `enumerate` 이터레이터 메서드를 사용해 전송하는 각 아이템의 인덱스와 아이템 자체를 얻는다. 그런 다음 짝수 인덱스 아이템에는 100밀리초 지연을, 홀수 인덱스 아이템에는 300밀리초 지연을 적용해 실제 세계의 메시지 스트림에서 볼 수 있는 다양한 지연을 시뮬레이트한다. 타임아웃이 200밀리초이기 때문에 이는 메시지의 절반에 영향을 미칠 것이다.

`get_messages` 함수에서 메시지 사이에 블로킹 없이 지연을 추가하려면 비동기를 사용해야 한다. 하지만 `get_messages` 자체를 비동기 함수로 만들 수는 없다. 그렇게 하면 `Future<Output = Stream<Item = String>>`을 반환하게 되고, 스트림 자체가 아니라 스트림에 접근하려면 `get_messages`를 기다려야 하기 때문이다. 하지만 기억하자: 주어진 Future 내의 모든 작업은 선형적으로 발생한다. 동시성은 Future _사이_에서 발생한다. `get_messages`를 기다리면 모든 메시지와 각 메시지 사이의 지연을 전송한 후에야 수신 스트림을 반환하게 된다. 결과적으로 타임아웃은 쓸모 없게 된다. 스트림 자체에는 지연이 없을 것이다. 모든 지연은 스트림이 사용 가능해지기 전에 발생할 것이다.

대신, `get_messages`를 스트림을 반환하는 일반 함수로 두고, 비동기 `sleep` 호출을 처리하는 작업을 생성한다.

> 참고: 이 방식으로 `spawn_task`를 호출하는 것은 런타임을 이미 설정했기 때문에 가능하다. 그렇지 않으면 패닉이 발생할 것이다. 다른 구현은 다른 트레이드오프를 선택한다: 새로운 런타임을 생성하고 패닉을 피하지만 약간의 추가 오버헤드를 발생시키거나, 런타임에 대한 참조 없이 작업을 생성할 수 있는 독립적인 방법을 제공하지 않을 수도 있다. 사용하는 런타임이 어떤 트레이드오프를 선택했는지 알고 그에 맞게 코드를 작성해야 한다!

이제 코드의 결과가 훨씬 더 흥미로워진다. 매번 다른 메시지 쌍 사이에 `Problem: Elapsed(())` 오류가 발생한다.

<!-- 출력을 추출하지 않음. 이 출력의 변경은 중요하지 않으며, 컴파일러의 변경보다는 스레드가 다르게 실행되었기 때문일 가능성이 높음 -->

```text
Message: 'a'
Problem: Elapsed(())
Message: 'b'
Message: 'c'
Problem: Elapsed(())
Message: 'd'
Message: 'e'
Problem: Elapsed(())
Message: 'f'
Message: 'g'
Problem: Elapsed(())
Message: 'h'
Message: 'i'
Problem: Elapsed(())
Message: 'j'
```

타임아웃은 메시지가 결국 도착하는 것을 막지 않는다. 여전히 모든 원래 메시지를 받는다. 왜냐하면 채널이 _무제한_이기 때문이다: 메모리에 맞는 한 많은 메시지를 보유할 수 있다. 메시지가 타임아웃 전에 도착하지 않으면 스트림 핸들러는 이를 처리하지만, 스트림을 다시 폴링할 때 메시지가 도착했을 수 있다.

필요한 경우 다른 종류의 채널이나 일반적으로 다른 종류의 스트림을 사용해 다른 동작을 얻을 수 있다. 이제 시간 간격 스트림과 이 메시지 스트림을 결합해 실제로 하나를 살펴보자.


### 스트림 병합하기

먼저, 직접 실행할 경우 매 밀리초마다 아이템을 방출하는 스트림을 생성한다. 간단하게 `sleep` 함수를 사용해 메시지를 지연 전송하고, `get_messages`에서 사용한 채널 기반 스트림 생성 방식을 활용한다. 이번에는 경과한 간격의 카운트를 반환하므로, 반환 타입은 `impl Stream<Item = u32>`가 되고, 이 함수를 `get_intervals`라고 부른다(리스트 17-36 참조).

<Listing number="17-36" caption="매 밀리초마다 카운트를 방출하는 스트림 생성" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-36/src/main.rs:intervals}}
```

</Listing>

먼저 태스크 내부에 `count`를 정의한다. (태스크 외부에서 정의할 수도 있지만, 변수의 범위를 제한하는 것이 더 명확하다.) 그런 다음 무한 루프를 생성한다. 루프의 각 반복은 비동기적으로 1밀리초 동안 대기하고, 카운트를 증가시킨 후 채널을 통해 전송한다. 이 모든 것이 `spawn_task`로 생성된 태스크에 포함되므로, 무한 루프를 포함한 모든 것이 런타임과 함께 정리된다.

이런 종류의 무한 루프는 전체 런타임이 종료될 때까지 계속 실행되며, 비동기 Rust에서 꽤 흔히 볼 수 있다. 많은 프로그램이 무한히 실행되어야 하기 때문이다. 비동기에서는 루프의 각 반복에 최소 하나의 await 포인트가 있으면 다른 작업을 블로킹하지 않는다.

이제 메인 함수의 async 블록으로 돌아가 `messages`와 `intervals` 스트림을 병합해 본다(리스트 17-37 참조).

<Listing number="17-37" caption="`messages`와 `intervals` 스트림 병합 시도" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-37/src/main.rs:main}}
```

</Listing>

먼저 `get_intervals`를 호출한다. 그런 다음 `messages`와 `intervals` 스트림을 `merge` 메서드로 병합한다. 이 메서드는 여러 스트림을 하나로 합치며, 소스 스트림에서 아이템이 사용 가능해지면 순서에 관계없이 즉시 방출한다. 마지막으로 `messages` 대신 병합된 스트림을 루프로 처리한다.

이 시점에서 `messages`와 `intervals`는 고정되거나 변경 가능할 필요가 없다. 두 스트림이 단일 `merged` 스트림으로 결합되기 때문이다. 그러나 이 `merge` 호출은 컴파일되지 않는다! (`while let` 루프의 `next` 호출도 마찬가지지만, 이 문제는 나중에 다시 다룬다.) 이는 두 스트림의 타입이 다르기 때문이다. `messages` 스트림은 `Timeout<impl Stream<Item = String>>` 타입을 가지며, `Timeout`은 `timeout` 호출에 대해 `Stream`을 구현한 타입이다. `intervals` 스트림은 `impl Stream<Item = u32>` 타입을 가진다. 이 두 스트림을 병합하려면 하나의 타입을 다른 타입과 맞춰야 한다. `messages`는 이미 원하는 기본 형식이며 타임아웃 오류를 처리해야 하므로, `intervals` 스트림을 수정한다(리스트 17-38 참조).

<Listing number="17-38" caption="`intervals` 스트림의 타입을 `messages` 스트림과 맞추기" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-38/src/main.rs:main}}
```

</Listing>

먼저 `map` 헬퍼 메서드를 사용해 `intervals`를 문자열로 변환한다. 두 번째로, `messages`의 `Timeout`과 일치시켜야 한다. 그러나 `intervals`에 실제로 타임아웃을 원하지 않으므로, 사용 중인 다른 지속 시간보다 긴 타임아웃을 생성한다. 여기서는 `Duration::from_secs(10)`로 10초 타임아웃을 생성한다. 마지막으로 `while let` 루프의 `next` 호출이 스트림을 반복할 수 있도록 `stream`을 변경 가능하게 만들고, 안전하게 처리할 수 있도록 고정한다. 이렇게 하면 거의 필요한 지점에 도달한다. 모든 것이 타입 검사를 통과한다. 그러나 이 코드를 실행하면 두 가지 문제가 발생한다. 첫째, 절대 멈추지 않는다! <span class="keystroke">ctrl-c</span>로 중지해야 한다. 둘째, 영어 알파벳 메시지가 모든 간격 카운터 메시지 사이에 묻힌다.

```text
--snip--
Interval: 38
Interval: 39
Interval: 40
Message: 'a'
Interval: 41
Interval: 42
Interval: 43
--snip--
```

리스트 17-39는 이 두 문제를 해결하는 한 가지 방법을 보여준다.

<Listing number="17-39" caption="`throttle`과 `take`를 사용해 병합된 스트림 관리" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-39/src/main.rs:throttle}}
```

</Listing>

먼저 `intervals` 스트림에 `throttle` 메서드를 적용해 `messages` 스트림을 압도하지 않도록 한다. _쓰로틀링_은 함수 호출 빈도를 제한하는 방법이다. 이 경우 스트림이 폴링되는 빈도를 제한한다. 메시지가 대략 100밀리초마다 도착하므로, 100밀리초마다 한 번씩 처리하도록 설정한다.

스트림에서 받을 아이템의 수를 제한하기 위해 `merged` 스트림에 `take` 메서드를 적용한다. 최종 출력만 제한하려는 것이지, 하나의 스트림만 제한하려는 것이 아니기 때문이다.

이제 프로그램을 실행하면 스트림에서 20개의 아이템을 가져온 후 멈추고, 간격 메시지가 메시지를 압도하지 않는다. 또한 `Interval: 100`이나 `Interval: 200` 같은 메시지 대신 `Interval: 1`, `Interval: 2` 등이 출력된다. 원본 스트림이 매 밀리초마다 이벤트를 생성할 수 있음에도 불구하고 말이다. 이는 `throttle` 호출이 원본 스트림을 감싸는 새로운 스트림을 생성하기 때문이다. 원본 스트림은 자체 "기본" 속도가 아니라 쓰로틀 속도로만 폴링된다. 처리되지 않은 간격 메시지를 무시하는 것이 아니라, 처음부터 그런 메시지를 생성하지 않는다. 이는 Rust 퓨처의 고유한 "게으름"이 다시 작동하는 것으로, 성능 특성을 선택할 수 있게 해준다.

```text
Interval: 1
Message: 'a'
Interval: 2
Interval: 3
Problem: Elapsed(())
Interval: 4
Message: 'b'
Interval: 5
Message: 'c'
Interval: 6
Interval: 7
Problem: Elapsed(())
Interval: 8
Message: 'd'
Interval: 9
Message: 'e'
Interval: 10
Interval: 11
Problem: Elapsed(())
Interval: 12
```

마지막으로 처리해야 할 것은 오류다! 이 두 채널 기반 스트림에서 `send` 호출은 채널의 반대쪽이 닫히면 실패할 수 있다. 이는 스트림을 구성하는 퓨처가 런타임에서 어떻게 실행되는지에 달려 있다. 지금까지는 `unwrap`을 호출해 이 가능성을 무시했지만, 잘 동작하는 앱에서는 최소한 루프를 종료해 더 이상 메시지를 보내지 않도록 명시적으로 오류를 처리해야 한다. 리스트 17-40은 간단한 오류 처리 전략을 보여준다. 문제를 출력한 후 루프에서 `break`한다.

<Listing number="17-40" caption="오류 처리 및 루프 종료">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-40/src/main.rs:errors}}
```

</Listing>

일반적으로 메시지 전송 오류를 처리하는 올바른 방법은 다양하므로, 반드시 전략을 세워야 한다.

이제 실제로 비동기 코드를 많이 살펴봤으니, 한 걸음 물러나 `Future`, `Stream`, 그리고 Rust가 비동기를 가능하게 하는 다른 주요 트레이트의 세부 사항을 깊이 있게 알아본다.

[17-02-messages]: ch17-02-concurrency-with-async.html#message-passing
[iterator-trait]: ch13-02-iterators.html#the-iterator-trait-and-the-next-method


