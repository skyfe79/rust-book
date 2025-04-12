## Async 트레이트 심층 분석

<!-- Old headings. Do not remove or links may break. -->

<a id="digging-into-the-traits-for-async"></a>

이번 장에서는 `Future`, `Pin`, `Unpin`, `Stream`, `StreamExt` 트레이트를 다양한 방식으로 사용했다. 지금까지는 이들이 어떻게 작동하고 서로 어떻게 연결되는지에 대한 세부 사항을 깊이 다루지 않았는데, 대부분의 경우 일상적인 Rust 작업에는 이 정도로 충분하다. 하지만 때로는 이러한 세부 사항을 더 깊이 이해해야 하는 상황이 발생한다. 이번 섹션에서는 그러한 시나리오에 도움이 될 만큼만 자세히 살펴보고, _진짜_ 깊이 있는 내용은 다른 문서에 맡긴다.

<!-- Old headings. Do not remove or links may break. -->

<a id="future"></a>


### `Future` 트레이트

먼저 `Future` 트레이트가 어떻게 동작하는지 자세히 살펴보자. Rust에서 `Future`는 다음과 같이 정의한다:

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Future {
    type Output;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

이 트레이트 정의에는 새로운 타입과 이전에 보지 못한 구문이 포함되어 있다. 따라서 정의를 하나씩 살펴보자.

먼저, `Future`의 연관 타입인 `Output`은 future가 최종적으로 어떤 값을 반환할지 지정한다. 이는 `Iterator` 트레이트의 `Item` 연관 타입과 유사하다. 두 번째로, `Future`는 `poll` 메서드를 가지고 있다. 이 메서드는 `self` 매개변수로 특별한 `Pin` 참조를 받고, `Context` 타입의 가변 참조를 받으며, `Poll<Self::Output>`을 반환한다. `Pin`과 `Context`에 대해서는 잠시 후에 더 자세히 알아볼 것이다. 지금은 메서드가 반환하는 `Poll` 타입에 집중해 보자:

```rust
enum Poll<T> {
    Ready(T),
    Pending,
}
```

이 `Poll` 타입은 `Option`과 비슷하다. 값을 가지는 `Ready(T)`와 값을 가지지 않는 `Pending`이라는 두 가지 변형이 있다. 하지만 `Poll`은 `Option`과는 상당히 다른 의미를 가진다! `Pending` 변형은 future가 아직 작업을 완료하지 않았음을 나타내므로, 호출자는 나중에 다시 확인해야 한다. `Ready` 변형은 future가 작업을 완료했고 `T` 값이 사용 가능함을 나타낸다.

> 참고: 대부분의 future는 `Ready`를 반환한 후에 다시 `poll`을 호출하면 안 된다. 많은 future는 준비 상태가 된 후에 다시 `poll`을 호출하면 패닉을 일으킨다. 다시 `poll`을 호출해도 안전한 future는 해당 문서에 명시적으로 설명한다. 이는 `Iterator::next`의 동작과 유사하다.

`await`를 사용하는 코드를 보면, Rust는 내부적으로 `poll`을 호출하는 코드로 컴파일한다. 이전에 단일 URL의 페이지 제목을 출력했던 코드를 다시 살펴보면, Rust는 이를 다음과 비슷한 코드로 컴파일한다:

```rust,ignore
match page_title(url).poll() {
    Ready(page_title) => match page_title {
        Some(title) => println!("The title for {url} was {title}"),
        None => println!("{url} had no title"),
    }
    Pending => {
        // 여기서는 어떻게 해야 할까?
    }
}
```

future가 여전히 `Pending` 상태라면 어떻게 해야 할까? future가 준비될 때까지 계속 시도할 방법이 필요하다. 다시 말해, 루프가 필요하다:

```rust,ignore
let mut page_title_fut = page_title(url);
loop {
    match page_title_fut.poll() {
        Ready(value) => match page_title {
            Some(title) => println!("The title for {url} was {title}"),
            None => println!("{url} had no title"),
        }
        Pending => {
            // 계속 진행
        }
    }
}
```

하지만 Rust가 정확히 이 코드로 컴파일한다면, 모든 `await`가 블로킹될 것이다. 이는 우리가 원하는 것과 정반대다! 대신 Rust는 이 루프가 다른 future를 처리하고 나중에 다시 확인할 수 있도록 제어를 넘길 수 있게 한다. 앞서 본 것처럼, 이는 async 런타임이 담당하며, 이 스케줄링과 조정 작업이 런타임의 주요 역할 중 하나다.

이 장의 앞부분에서 `rx.recv`를 기다리는 것에 대해 설명했다. `recv` 호출은 future를 반환하고, future를 기다리면 `poll`을 호출한다. 런타임은 future가 `Some(message)` 또는 채널이 닫힌 경우 `None`을 반환할 때까지 future를 일시 중지한다. `Future` 트레이트, 특히 `Future::poll`에 대한 깊은 이해를 바탕으로 이를 어떻게 작동하는지 알 수 있다. 런타임은 future가 `Poll::Pending`을 반환하면 아직 준비되지 않았다는 것을 안다. 반대로, 런타임은 `poll`이 `Poll::Ready(Some(message))` 또는 `Poll::Ready(None)`를 반환하면 future가 준비되었음을 알고 이를 진행시킨다.

런타임이 이를 어떻게 수행하는지에 대한 정확한 세부 사항은 이 책의 범위를 벗어나지만, 중요한 점은 future의 기본 메커니즘을 이해하는 것이다: 런타임은 자신이 담당하는 각 future를 _폴링_하고, future가 아직 준비되지 않았다면 다시 잠재운다.

<!-- Old headings. Do not remove or links may break. -->

<a id="pinning-and-the-pin-and-unpin-traits"></a>


### `Pin`과 `Unpin` 트레이트

리스트 17-16에서 고정(pinning) 개념을 소개하며 복잡한 에러 메시지를 마주했다. 여기서 그 에러 메시지의 관련 부분을 다시 살펴보자:

```text
error[E0277]: `{async block@src/main.rs:10:23: 10:33}` cannot be unpinned
  --> src/main.rs:48:33
   |
48 |         trpl::join_all(futures).await;
   |                                 ^^^^^ the trait `Unpin` is not implemented for `{async block@src/main.rs:10:23: 10:33}`
   |
   = note: consider using the `pin!` macro
           consider using `Box::pin` if you need to access the pinned value outside of the current scope
   = note: required for `Box<{async block@src/main.rs:10:23: 10:33}>` to implement `Future`
note: required by a bound in `futures_util::future::join_all::JoinAll`
  --> file:///home/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/futures-util-0.3.30/src/future/join_all.rs:29:8
   |
27 | pub struct JoinAll<F>
   |            ------- required by a bound in this struct
28 | where
29 |     F: Future,
   |        ^^^^^^ required by this bound in `JoinAll`
```

이 에러 메시지는 값들을 고정해야 한다는 것뿐만 아니라 왜 고정이 필요한지도 알려준다. `trpl::join_all` 함수는 `JoinAll`이라는 구조체를 반환한다. 이 구조체는 `F` 타입에 대해 제네릭하며, `F`는 `Future` 트레이트를 구현해야 한다. `await`를 사용해 퓨처를 직접 기다리면 암묵적으로 퓨처가 고정된다. 그래서 퓨처를 기다릴 때마다 `pin!`을 사용할 필요가 없다.

하지만 여기서는 퓨처를 직접 기다리지 않는다. 대신 `join_all` 함수에 퓨처 컬렉션을 전달해 새로운 퓨처인 `JoinAll`을 생성한다. `join_all`의 시그니처는 컬렉션의 아이템 타입이 모두 `Future` 트레이트를 구현해야 한다는 것을 요구하며, `Box<T>`는 `T`가 `Unpin` 트레이트를 구현한 퓨처일 때만 `Future`를 구현한다.

이 내용을 완전히 이해하려면 _고정_과 관련해 `Future` 트레이트가 실제로 어떻게 동작하는지 더 깊이 파헤쳐야 한다.

`Future` 트레이트의 정의를 다시 살펴보자:

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Future {
    type Output;

    // Required method
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

`cx` 매개변수와 그 `Context` 타입은 런타임이 퓨처를 언제 확인해야 하는지 알 수 있게 하는 핵심이다. 이 동작의 세부 사항은 이 장의 범위를 벗어나며, 일반적으로 커스텀 `Future` 구현을 작성할 때만 이 부분을 고려하면 된다. 대신 `self`의 타입에 집중하자. 이는 `self`에 타입 주석이 붙은 메서드를 처음 보는 것이다. `self`의 타입 주석은 다른 함수 매개변수의 타입 주석과 비슷하지만 두 가지 중요한 차이점이 있다:

- 이 주석은 메서드가 호출되기 위해 `self`가 어떤 타입이어야 하는지 Rust에게 알려준다.

- 이 타입은 아무 타입이나 될 수 없다. 메서드가 구현된 타입, 그 타입에 대한 참조 또는 스마트 포인터, 또는 그 타입에 대한 참조를 감싼 `Pin`으로 제한된다.

이 문법에 대해선 [18장][ch-18]에서 더 자세히 다룬다. 지금은 퓨처가 `Pending`인지 `Ready(Output)`인지 확인하기 위해 퓨처를 폴링하려면 해당 타입에 대한 `Pin`으로 감싼 가변 참조가 필요하다는 것만 알면 된다.

`Pin`은 `&`, `&mut`, `Box`, `Rc` 같은 포인터형 타입을 위한 래퍼다. (기술적으로 `Pin`은 `Deref` 또는 `DerefMut` 트레이트를 구현한 타입과 함께 동작하지만, 이는 실질적으로 포인터와만 동작하는 것과 같다.) `Pin`은 포인터 자체가 아니며 `Rc`나 `Arc`처럼 참조 카운팅과 같은 자체 동작을 하지 않는다. 이는 컴파일러가 포인터 사용에 대한 제약을 강제하는 순수한 도구다.

`await`가 `poll` 호출로 구현된다는 것을 떠올리면 앞서 본 에러 메시지를 설명할 수 있지만, 그 메시지는 `Unpin`이 아니라 `Pin`에 관한 것이었다. 그렇다면 `Pin`은 `Unpin`과 어떻게 관련되며, 왜 `Future`는 `poll`을 호출하기 위해 `self`가 `Pin` 타입이어야 할까?

이 장 앞부분에서 퓨처 내의 일련의 await 지점이 상태 머신으로 컴파일되며, 컴파일러는 이 상태 머신이 Rust의 일반적인 안전 규칙(소유권 및 참조 규칙 포함)을 모두 따르도록 보장한다는 것을 기억하자. 이를 위해 Rust는 하나의 await 지점과 다음 await 지점 또는 async 블록의 끝 사이에 어떤 데이터가 필요한지 확인한다. 그런 다음 컴파일된 상태 머신에 해당하는 변형을 생성한다. 각 변형은 소스 코드의 해당 섹션에서 사용될 데이터에 필요한 접근 권한을 얻는다. 이는 해당 데이터의 소유권을 가져오거나, 가변 또는 불변 참조를 얻는 방식으로 이루어진다.

지금까지는 문제가 없다: 주어진 async 블록에서 소유권이나 참조에 대해 잘못된 부분이 있으면 빌림 검사기가 알려준다. 하지만 해당 블록에 해당하는 퓨처를 이동하려 할 때—예를 들어 `join_all`에 전달하기 위해 `Vec`에 넣으려 할 때—문제가 복잡해진다.

퓨처를 이동할 때—`join_all`과 함께 이터레이터로 사용하기 위해 데이터 구조에 푸시하거나 함수에서 반환할 때—이는 실제로 Rust가 생성한 상태 머신을 이동하는 것을 의미한다. 그리고 Rust의 대부분의 다른 타입과 달리, async 블록을 위해 Rust가 생성한 퓨처는 특정 변형의 필드에 자기 자신에 대한 참조를 가질 수 있다. 이는 그림 17-4의 단순화된 예시에서 볼 수 있다.

<figure>

<img alt="A single-column, three-row table representing a future, fut1, which has data values 0 and 1 in the first two rows and an arrow pointing from the third row back to the second row, representing an internal reference within the future." src="img/trpl17-04.svg" class="center" />

<figcaption>그림 17-4: 자기 참조 데이터 타입.</figcaption>

</figure>

하지만 기본적으로 자기 자신에 대한 참조를 가진 객체는 이동하기에 안전하지 않다. 참조는 항상 참조 대상의 실제 메모리 주소를 가리키기 때문이다(그림 17-5 참조). 데이터 구조 자체를 이동하면 그 내부 참조는 이전 위치를 가리키게 된다. 그러나 이 메모리 위치는 이제 유효하지 않다. 한 가지는 데이터 구조를 변경할 때 그 값이 업데이트되지 않는다는 점이다. 더 중요한 점은 컴퓨터가 이제 그 메모리를 다른 목적으로 재사용할 수 있다는 것이다! 나중에 완전히 관련 없는 데이터를 읽게 될 수 있다.

<figure>

<img alt="Two tables, depicting two futures, fut1 and fut2, each of which has one column and three rows, representing the result of having moved a future out of fut1 into fut2. The first, fut1, is grayed out, with a question mark in each index, representing unknown memory. The second, fut2, has 0 and 1 in the first and second rows and an arrow pointing from its third row back to the second row of fut1, representing a pointer that is referencing the old location in memory of the future before it was moved." src="img/trpl17-05.svg" class="center" />

<figcaption>그림 17-5: 자기 참조 데이터 타입을 이동한 결과의 안전하지 않은 상황</figcaption>

</figure>

이론적으로 Rust 컴파일러는 객체가 이동할 때마다 모든 참조를 업데이트하려고 시도할 수 있지만, 이는 특히 참조의 전체 네트워크를 업데이트해야 할 때 많은 성능 오버헤드를 추가할 수 있다. 대신 해당 데이터 구조가 메모리에서 _이동하지 않는다_는 것을 보장할 수 있다면, 어떤 참조도 업데이트할 필요가 없다. 이는 Rust의 빌림 검사기가 요구하는 것과 정확히 일치한다: 안전한 코드에서는 활성 참조가 있는 항목을 이동하는 것을 방지한다.

`Pin`은 이를 기반으로 우리가 필요한 정확한 보장을 제공한다. `Pin`으로 값을 감싸면 그 값은 더 이상 이동할 수 없다. 따라서 `Pin<Box<SomeType>>`이 있다면 실제로 `SomeType` 값을 고정하는 것이지 `Box` 포인터를 고정하는 것이 아니다. 그림 17-6은 이 과정을 보여준다.

<figure>

<img alt="Three boxes laid out side by side. The first is labeled “Pin”, the second “b1”, and the third “pinned”. Within “pinned” is a table labeled “fut”, with a single column; it represents a future with cells for each part of the data structure. Its first cell has the value “0”, its second cell has an arrow coming out of it and pointing to the fourth and final cell, which has the value “1” in it, and the third cell has dashed lines and an ellipsis to indicate there may be other parts to the data structure. All together, the “fut” table represents a future which is self-referential. An arrow leaves the box labeled “Pin”, goes through the box labeled “b1” and has terminates inside the “pinned” box at the “fut” table." src="img/trpl17-06.svg" class="center" />

<figcaption>그림 17-6: 자기 참조 퓨처 타입을 가리키는 `Box`를 고정하기.</figcaption>

</figure>

사실 `Box` 포인터는 여전히 자유롭게 이동할 수 있다. 기억하자: 우리가 신경 쓰는 것은 궁극적으로 참조되는 데이터가 제자리에 있는지 확인하는 것이다. 포인터가 이동하더라도 _그 포인터가 가리키는 데이터가 같은 위치에 있다면_ (그림 17-7에서와 같이) 잠재적인 문제가 없다. 독립적인 연습으로, 타입과 `std::pin` 모듈의 문서를 살펴보고 `Box`를 감싼 `Pin`으로 이를 어떻게 할지 생각해보자.) 핵심은 자기 참조 타입 자체가 이동할 수 없다는 것이다. 왜냐하면 여전히 고정되어 있기 때문이다.

<figure>

<img alt="Four boxes laid out in three rough columns, identical to the previous diagram with a change to the second column. Now there are two boxes in the second column, labeled “b1” and “b2”, “b1” is grayed out, and the arrow from “Pin” goes through “b2” instead of “b1”, indicating that the pointer has moved from “b1” to “b2”, but the data in “pinned” has not moved." src="img/trpl17-07.svg" class="center" />

<figcaption>그림 17-7: 자기 참조 퓨처 타입을 가리키는 `Box`를 이동하기.</figcaption>

</figure>

하지만 대부분의 타입은 `Pin` 래퍼 뒤에 있더라도 완벽하게 안전하게 이동할 수 있다. 내부 참조가 있는 항목에 대해서만 고정을 고려하면 된다. 숫자나 불리언 같은 기본 값은 내부 참조가 없으므로 안전하다. Rust에서 일반적으로 작업하는 대부분의 타입도 마찬가지다. 예를 들어 `Vec`을 이동할 때 걱정할 필요가 없다. 지금까지 본 내용만으로는 `Pin<Vec<String>>`이 있다면 `Pin`이 제공하는 안전하지만 제한적인 API를 통해 모든 작업을 해야 하지만, `Vec<String>`은 다른 참조가 없다면 항상 안전하게 이동할 수 있다. 이와 같은 경우에 항목을 이동해도 괜찮다는 것을 컴파일러에게 알려줄 방법이 필요하다—그리고 바로 여기서 `Unpin`이 등장한다.

`Unpin`은 16장에서 본 `Send`와 `Sync` 트레이트와 유사한 마커 트레이트이며, 따라서 자체 기능은 없다. 마커 트레이트는 특정 컨텍스트에서 주어진 트레이트를 구현한 타입을 안전하게 사용할 수 있다는 것을 컴파일러에게 알리는 역할만 한다. `Unpin`은 주어진 타입이 값이 안전하게 이동할 수 있는지에 대한 보장을 유지할 필요가 없다는 것을 컴파일러에게 알린다.

`Send`와 `Sync`와 마찬가지로, 컴파일러는 안전하다고 판단될 경우 모든 타입에 대해 `Unpin`을 자동으로 구현한다. 특수한 경우로, `Send`와 `Sync`와 유사하게, `Unpin`이 타입에 대해 구현되지 않는 경우가 있다. 이를 나타내는 표기법은 <code>impl !Unpin for <em>SomeType</em></code>이며, 여기서 <code><em>SomeType</em></code>은 `Pin`으로 감싼 포인터를 사용할 때 안전을 위해 해당 보장을 유지해야 하는 타입의 이름이다.

다시 말해, `Pin`과 `Unpin`의 관계에 대해 두 가지를 기억해야 한다. 첫째, `Unpin`은 "일반적인" 경우이고 `!Unpin`은 특수한 경우다. 둘째, 타입이 `Unpin`을 구현하는지 `!Unpin`을 구현하는지는 <code>Pin<&mut <em>SomeType</em>></code>과 같은 고정된 포인터를 사용할 때만 중요하다.

이를 구체적으로 이해하기 위해 `String`을 생각해보자: 길이와 이를 구성하는 유니코드 문자를 가지고 있다. 그림 17-8에서 볼 수 있듯이 `String`을 `Pin`으로 감쌀 수 있다. 그러나 `String`은 Rust의 대부분의 다른 타입과 마찬가지로 자동으로 `Unpin`을 구현한다.

<figure>

<img alt="Concurrent work flow" src="img/trpl17-08.svg" class="center" />

<figcaption>그림 17-8: `String` 고정하기; 점선은 `String`이 `Unpin` 트레이트를 구현하므로 고정되지 않음을 나타낸다.</figcaption>

</figure>

결과적으로 `String`이 `!Unpin`을 구현했다면 불법이었을 행동을 할 수 있다. 예를 들어 그림 17-9에서와 같이 메모리의 정확히 같은 위치에서 한 문자열을 다른 문자열로 교체할 수 있다. 이는 `Pin` 계약을 위반하지 않는다. 왜냐하면 `String`은 이동해도 안전하지 않게 만드는 내부 참조가 없기 때문이다! 이것이 바로 `String`이 `!Unpin`이 아니라 `Unpin`을 구현하는 이유다.

<figure>

<img alt="Concurrent work flow" src="img/trpl17-09.svg" class="center" />

<figcaption>그림 17-9: 메모리에서 `String`을 완전히 다른 `String`으로 교체하기.</figcaption>

</figure>

이제 리스트 17-17의 `join_all` 호출에서 보고된 에러를 이해할 수 있다. 원래 async 블록에 의해 생성된 퓨처를 `Vec<Box<dyn Future<Output = ()>>>`로 이동하려고 시도했지만, 앞서 본 것처럼 이 퓨처는 내부 참조를 가질 수 있으므로 `Unpin`을 구현하지 않는다. 이들은 고정되어야 하며, 그런 다음 `Pin` 타입을 `Vec`에 전달할 수 있다. 이렇게 하면 퓨처의 기본 데이터가 이동되지 않는다는 확신을 가질 수 있다.

`Pin`과 `Unpin`은 주로 하위 수준 라이브러리를 구축하거나 런타임 자체를 구축할 때 중요하며, 일상적인 Rust 코드에서는 그다지 중요하지 않다. 하지만 이 트레이트가 에러 메시지에 나타날 때, 이제는 코드를 어떻게 수정해야 할지 더 잘 이해할 수 있을 것이다!

> 참고: `Pin`과 `Unpin`의 조합은 Rust에서 자기 참조 때문에 구현하기 어려운 복잡한 타입의 전체 클래스를 안전하게 구현할 수 있게 한다. `Pin`이 필요한 타입은 오늘날 async Rust에서 가장 흔하게 나타나지만, 가끔 다른 컨텍스트에서도 볼 수 있다.
>
> `Pin`과 `Unpin`이 어떻게 동작하며, 이들이 유지해야 할 규칙에 대한 세부 사항은 `std::pin`의 API 문서에서 광범위하게 다루므로, 더 알고 싶다면 이 문서가 좋은 시작점이다.
>
> 내부적으로 어떻게 동작하는지 더 자세히 알고 싶다면 [_Asynchronous Programming in Rust_][async-book]의 [2장][under-the-hood]과 [4장][pinning]을 참고하라.


### `Stream` 트레이트

이제 `Future`, `Pin`, 그리고 `Unpin` 트레이트에 대해 깊이 이해했으니, `Stream` 트레이트에 대해 알아보자. 앞서 배웠듯이, 스트림은 비동기 이터레이터와 유사하다. 하지만 `Iterator`와 `Future`와 달리, `Stream`은 현재 표준 라이브러리에 정의되어 있지 않다. 대신, `futures` 크레이트에서 제공하는 정의가 생태계 전반에서 널리 사용되고 있다.

`Stream` 트레이트를 살펴보기 전에, `Iterator`와 `Future` 트레이트의 정의를 다시 짚어보자. `Iterator`는 시퀀스의 개념을 제공한다. `next` 메서드는 `Option<Self::Item>`을 반환한다. `Future`는 시간에 따른 준비 상태의 개념을 제공한다. `poll` 메서드는 `Poll<Self::Output>`을 반환한다. 시간에 따라 준비되는 아이템의 시퀀스를 표현하기 위해, 이 두 기능을 결합한 `Stream` 트레이트를 정의할 수 있다:

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

trait Stream {
    type Item;

    fn poll_next(
        self: Pin<&mut Self>,
        cx: &mut Context<'_>
    ) -> Poll<Option<Self::Item>>;
}
```

`Stream` 트레이트는 스트림이 생성하는 아이템의 타입을 나타내는 `Item`이라는 연관 타입을 정의한다. 이는 `Iterator`와 유사하며, 아이템이 없거나 여러 개일 수 있다. 반면 `Future`는 항상 단일 `Output`을 가지며, 심지어 단위 타입 `()`일 수도 있다.

`Stream`은 또한 이러한 아이템을 가져오는 메서드를 정의한다. 이 메서드를 `poll_next`라고 부르는데, 이는 `Future::poll`과 같은 방식으로 동작하며, `Iterator::next`와 같은 방식으로 아이템 시퀀스를 생성한다. 반환 타입은 `Poll`과 `Option`을 결합한 형태다. 외부 타입은 `Poll`인데, 이는 `Future`와 마찬가지로 준비 상태를 확인해야 하기 때문이다. 내부 타입은 `Option`인데, 이는 `Iterator`와 마찬가지로 더 이상 메시지가 있는지 여부를 알려주기 때문이다.

이와 매우 유사한 정의가 Rust의 표준 라이브러리에 추가될 가능성이 크다. 그때까지는 대부분의 런타임에서 이 트레이트를 사용할 수 있으므로, 안심하고 사용할 수 있다. 또한 이어지는 내용은 일반적으로 적용 가능하다.

스트리밍 섹션에서 본 예제에서는 `poll_next`나 `Stream`을 직접 사용하지 않고, `next`와 `StreamExt`를 사용했다. 물론, `poll_next` API를 직접 사용하여 `Stream` 상태 머신을 직접 작성할 수도 있다. 이는 `poll` 메서드를 통해 `Future`를 직접 다루는 것과 유사하다. 하지만 `await`를 사용하는 것이 훨씬 편리하며, `StreamExt` 트레이트는 `next` 메서드를 제공하여 이를 가능하게 한다:

```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-stream-ext/src/lib.rs:here}}
```

> 참고: 이 장의 앞부분에서 사용한 실제 정의는 이와 조금 다르다. 이는 Rust가 트레이트 내에서 async 함수를 아직 지원하지 않았던 버전을 지원하기 때문이다. 따라서 다음과 같이 보인다:
>
> ```rust,ignore
> fn next(&mut self) -> Next<'_, Self> where Self: Unpin;
> ```
>
> `Next` 타입은 `Future`를 구현한 `struct`이며, `Next<'_, Self>`를 통해 `self`에 대한 참조의 라이프타임을 명시할 수 있다. 이를 통해 `await`가 이 메서드와 함께 동작할 수 있다.

`StreamExt` 트레이트는 스트림과 함께 사용할 수 있는 모든 흥미로운 메서드의 집합이기도 하다. `StreamExt`는 `Stream`을 구현하는 모든 타입에 대해 자동으로 구현되지만, 이 트레이트는 기본 트레이트에 영향을 주지 않고 편의 API를 반복적으로 개선할 수 있도록 별도로 정의된다.

`trpl` 크레이트에서 사용된 `StreamExt` 버전에서는, `next` 메서드를 정의할 뿐만 아니라 `Stream::poll_next`를 호출하는 세부 사항을 올바르게 처리하는 `next` 메서드의 기본 구현도 제공한다. 이는 스트리밍 데이터 타입을 직접 작성해야 할 때도 `Stream`만 구현하면 되며, 이를 사용하는 모든 사람이 `StreamExt`와 그 메서드를 자동으로 사용할 수 있음을 의미한다.

이 트레이트에 대한 저수준의 세부 사항은 여기까지 다룬다. 마지막으로, `Future`(스트림 포함), `Task`, 그리고 `Thread`가 어떻게 함께 작동하는지 살펴보자!

[ch-18]: ch18-00-oop.html
[async-book]: https://rust-lang.github.io/async-book/
[under-the-hood]: https://rust-lang.github.io/async-book/02_execution/01_chapter.html
[pinning]: https://rust-lang.github.io/async-book/04_pinning/01_chapter.html
[first-async]: ch17-01-futures-and-syntax.html#our-first-async-program
[any-number-futures]: ch17-03-more-futures.html#working-with-any-number-of-futures


