## 객체 지향 디자인 패턴 구현

**상태 패턴**은 객체 지향 디자인 패턴 중 하나다. 이 패턴의 핵심은 값이 내부적으로 가질 수 있는 상태 집합을 정의하는 것이다. 상태는 **상태 객체** 집합으로 표현되며, 값의 동작은 현재 상태에 따라 달라진다. 이 예제에서는 블로그 포스트를 다루며, 포스트는 내부 상태를 나타내는 필드를 가진다. 상태는 "초안", "검토 중", "게시됨" 중 하나가 된다.

상태 객체는 기능을 공유한다. Rust에서는 객체와 상속 대신 구조체와 트레이트를 사용한다. 각 상태 객체는 자신의 동작과 상태 전환 시기를 관리한다. 상태 객체를 포함하는 값은 상태 간의 다른 동작이나 상태 전환 시기에 대해 알지 못한다.

상태 패턴을 사용하면 프로그램의 비즈니스 요구사항이 변경되었을 때, 상태를 포함하는 값이나 값을 사용하는 코드를 변경할 필요가 없다. 단지 상태 객체 중 하나의 코드를 업데이트하여 규칙을 변경하거나 새로운 상태 객체를 추가하면 된다.

먼저 전통적인 객체 지향 방식으로 상태 패턴을 구현한 다음, Rust에 더 적합한 방식으로 접근한다. 상태 패턴을 사용해 블로그 포스트 워크플로우를 점진적으로 구현해보자.

최종 기능은 다음과 같다:

1. 블로그 포스트는 빈 초안 상태로 시작한다.
2. 초안이 완료되면 포스트 검토를 요청한다.
3. 포스트가 승인되면 게시된다.
4. 게시된 블로그 포스트만 콘텐츠를 반환하므로, 승인되지 않은 포스트가 실수로 게시되는 것을 방지한다.

그 외의 변경 시도는 아무런 효과가 없어야 한다. 예를 들어, 검토를 요청하기 전에 초안 블로그 포스트를 승인하려고 하면 포스트는 게시되지 않은 초안 상태로 유지된다.

리스트 18-11은 이 워크플로우를 코드로 보여준다. 이 코드는 `blog`라는 라이브러리 크레이트에서 구현할 API의 사용 예시다. 아직 `blog` 크레이트를 구현하지 않았기 때문에 이 코드는 컴파일되지 않는다.

<Listing number="18-11" file-name="src/main.rs" caption="우리가 `blog` 크레이트에 구현하고자 하는 동작을 보여주는 코드">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:all}}
```

</Listing>

사용자가 `Post::new`를 통해 새로운 초안 블로그 포스트를 생성할 수 있도록 한다. 블로그 포스트에 텍스트를 추가할 수 있어야 한다. 승인 전에 포스트의 콘텐츠를 바로 가져오려고 하면, 포스트가 여전히 초안 상태이므로 텍스트를 얻지 못해야 한다. 코드에는 설명을 위해 `assert_eq!`를 추가했다. 이에 대한 훌륭한 단위 테스트는 초안 블로그 포스트가 `content` 메서드에서 빈 문자열을 반환하는지 확인하는 것이다. 하지만 이 예제에서는 테스트를 작성하지 않는다.

다음으로, 포스트 검토를 요청할 수 있도록 하고, 검토를 기다리는 동안 `content`가 빈 문자열을 반환하도록 한다. 포스트가 승인되면 게시되어, `content`가 호출될 때 포스트의 텍스트가 반환된다.

크레이트에서 상호작용하는 유일한 타입은 `Post` 타입이다. 이 타입은 상태 패턴을 사용하며, 포스트가 가질 수 있는 다양한 상태(초안, 검토 중, 게시됨)를 나타내는 세 가지 상태 객체 중 하나를 값으로 가진다. 한 상태에서 다른 상태로의 전환은 `Post` 타입 내부에서 관리된다. 상태는 `Post` 인스턴스에 대해 라이브러리 사용자가 호출한 메서드에 따라 변경되지만, 사용자가 직접 상태 변경을 관리할 필요는 없다. 또한 사용자는 검토 전에 포스트를 게시하는 등의 실수를 할 수 없다.


### `Post` 정의와 초기 상태로 인스턴스 생성하기

라이브러리 구현을 시작해 보자. 우선 `Post` 구조체가 필요하며, 이 구조체는 일부 콘텐츠를 보관한다. 따라서 `Post` 구조체를 정의하고, `Post` 인스턴스를 생성하는 `new` 함수를 함께 구현한다. 또한 `Post`의 모든 상태 객체가 갖춰야 할 동작을 정의하는 `State` 트레이트를 비공개로 만든다.

`Post`는 `state`라는 비공개 필드에 `Box<dyn State>` 타입의 트레이트 객체를 `Option<T>`로 보관한다. 이렇게 `Option<T>`를 사용하는 이유는 조금 뒤에 설명한다.

<Listing number="18-12" file-name="src/lib.rs" caption="`Post` 구조체와 `new` 함수 정의, `State` 트레이트, `Draft` 구조체">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-12/src/lib.rs}}
```

</Listing>

`State` 트레이트는 다양한 포스트 상태가 공유하는 동작을 정의한다. 상태 객체는 `Draft`, `PendingReview`, `Published`이며, 이들은 모두 `State` 트레이트를 구현한다. 현재는 트레이트에 메서드가 없으며, 포스트가 시작하는 상태인 `Draft` 상태부터 정의한다.

새로운 `Post`를 생성할 때, `state` 필드를 `Box`를 담은 `Some` 값으로 설정한다. 이 `Box`는 `Draft` 구조체의 새 인스턴스를 가리킨다. 이렇게 하면 `Post`의 새 인스턴스를 생성할 때마다 초기 상태가 `Draft`가 된다. `Post`의 `state` 필드는 비공개이므로, 다른 상태로 `Post`를 생성할 방법은 없다! `Post::new` 함수에서 `content` 필드는 새로운 빈 `String`으로 설정한다.


### 게시물 콘텐츠 텍스트 저장하기

리스트 18-11에서 `add_text`라는 메서드를 호출하고, `&str` 타입의 값을 전달하여 블로그 게시물의 텍스트 콘텐츠로 추가할 수 있도록 하려는 것을 확인했다. 이 기능을 `content` 필드를 `pub`으로 공개하는 대신 메서드로 구현한 이유는 나중에 `content` 필드의 데이터를 읽는 방식을 제어할 수 있는 메서드를 구현하기 위함이다. `add_text` 메서드는 매우 직관적이므로, 리스트 18-13의 구현을 `impl Post` 블록에 추가해 보자.

<Listing number="18-13" file-name="src/lib.rs" caption="게시물의 `content`에 텍스트를 추가하는 `add_text` 메서드 구현">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-13/src/lib.rs:here}}
```

</Listing>

`add_text` 메서드는 `self`에 대한 가변 참조를 받는다. 이는 `add_text`를 호출하는 `Post` 인스턴스를 변경하기 때문이다. 그런 다음 `content`에 있는 `String`에 `push_str`을 호출하고, `text` 인자를 전달하여 저장된 `content`에 추가한다. 이 동작은 게시물의 상태에 의존하지 않으므로 상태 패턴의 일부가 아니다. `add_text` 메서드는 `state` 필드와 전혀 상호작용하지 않지만, 우리가 지원하고자 하는 동작의 일부이다.


### 초안 게시물의 내용이 비어 있는지 확인하기

`add_text`를 호출하고 게시물에 일부 내용을 추가한 후에도, 게시물이 아직 초안 상태이기 때문에 `content` 메서드는 빈 문자열 슬라이스를 반환해야 한다. 이는 목록 18-11의 7번째 줄에서 확인할 수 있다. 현재로서는 이 요구 사항을 충족시키기 위해 가장 간단한 방법으로 `content` 메서드를 구현한다. 즉, 항상 빈 문자열 슬라이스를 반환하는 것이다. 나중에 게시물 상태를 변경하여 게시할 수 있는 기능을 구현하면 이 부분을 수정할 예정이다. 지금은 게시물이 초안 상태에만 있을 수 있으므로, 게시물 내용은 항상 비어 있어야 한다. 목록 18-14는 이 플레이스홀더 구현을 보여준다.

<Listing number="18-14" file-name="src/lib.rs" caption="`Post`에 대한 `content` 메서드의 플레이스홀더 구현 추가. 항상 빈 문자열 슬라이스를 반환한다.">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-14/src/lib.rs:here}}
```

</Listing>

이렇게 추가된 `content` 메서드로 인해, 목록 18-11의 7번째 줄까지 모든 내용이 의도한 대로 작동한다.

<!-- Old link, do not remove -->

<a id="requesting-a-review-of-the-post-changes-its-state"></a>


### 리뷰 요청으로 게시물 상태 변경하기

다음으로 게시물의 리뷰를 요청하는 기능을 추가해야 한다. 이 기능은 게시물의 상태를 `Draft`에서 `PendingReview`로 변경한다. 리스트 18-15는 이 코드를 보여준다.

<Listing number="18-15" file-name="src/lib.rs" caption="`Post`와 `State` 트레잇에 `request_review` 메서드 구현">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-15/src/lib.rs:here}}
```

</Listing>

`Post`에 `request_review`라는 공개 메서드를 추가한다. 이 메서드는 `self`에 대한 가변 참조를 받는다. 그런 다음 `Post`의 현재 상태에 대해 내부 `request_review` 메서드를 호출한다. 이 두 번째 `request_review` 메서드는 현재 상태를 소비하고 새로운 상태를 반환한다.

`State` 트레잇에 `request_review` 메서드를 추가한다. 이제 이 트레잇을 구현하는 모든 타입은 `request_review` 메서드를 구현해야 한다. 메서드의 첫 번째 매개변수로 `self`, `&self`, 또는 `&mut self` 대신 `self: Box<Self>`를 사용한다. 이 구문은 해당 메서드가 `Box`에 담긴 타입에서만 호출될 수 있음을 의미한다. 이 구문은 `Box<Self>`의 소유권을 가져가므로, 이전 상태가 무효화되고 `Post`의 상태 값이 새로운 상태로 변환될 수 있다.

이전 상태를 소비하기 위해 `request_review` 메서드는 상태 값의 소유권을 가져와야 한다. 이때 `Post`의 `state` 필드에 있는 `Option`이 사용된다. `take` 메서드를 호출해 `state` 필드에서 `Some` 값을 꺼내고 그 자리에 `None`을 남긴다. Rust는 구조체에서 비어 있는 필드를 허용하지 않기 때문이다. 이를 통해 `state` 값을 빌리는 대신 `Post`에서 이동시킬 수 있다. 그런 다음 이 작업의 결과를 `post`의 `state` 값으로 설정한다.

`state` 값을 직접 `self.state = self.state.request_review();`와 같은 코드로 설정하는 대신, 일시적으로 `None`으로 설정해야 한다. 이렇게 하면 `state` 값의 소유권을 얻을 수 있다. 이는 `Post`가 상태를 새로운 상태로 변환한 후 이전 `state` 값을 사용할 수 없도록 보장한다.

`Draft`의 `request_review` 메서드는 새로운 `PendingReview` 구조체의 박스 인스턴스를 반환한다. 이 구조체는 게시물이 리뷰를 기다리는 상태를 나타낸다. `PendingReview` 구조체도 `request_review` 메서드를 구현하지만 아무런 변환을 수행하지 않는다. 대신, 이미 `PendingReview` 상태에 있는 게시물에 대해 리뷰를 요청하면 `PendingReview` 상태를 유지해야 하므로 자기 자신을 반환한다.

이제 상태 패턴의 장점을 확인할 수 있다. `Post`의 `request_review` 메서드는 `state` 값에 관계없이 동일하다. 각 상태는 자신의 규칙을 책임진다.

`Post`의 `content` 메서드는 그대로 두고 빈 문자열 슬라이스를 반환한다. 이제 `Post`를 `PendingReview` 상태와 `Draft` 상태로 둘 수 있다. 하지만 `PendingReview` 상태에서도 동일한 동작을 원한다. 리스트 18-11은 이제 10번째 줄까지 작동한다!

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-the-approve-method-that-changes-the-behavior-of-content"></a>


### `content` 동작을 변경하기 위해 `approve` 추가하기

`approve` 메서드는 `request_review` 메서드와 유사하게 동작한다. 현재 상태가 승인되었을 때 설정해야 하는 값으로 `state`를 변경한다. 이 내용은 리스트 18-16에서 확인할 수 있다:

<Listing number="18-16" file-name="src/lib.rs" caption="`Post`와 `State` 트레잇에 `approve` 메서드 구현">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-16/src/lib.rs:here}}
```

</Listing>

`State` 트레잇에 `approve` 메서드를 추가하고, `State`를 구현하는 새로운 구조체인 `Published` 상태를 정의한다.

`PendingReview`에서 `request_review`가 동작하는 방식과 마찬가지로, `Draft`에서 `approve` 메서드를 호출하면 아무런 효과가 없다. `approve`는 `self`를 반환하기 때문이다. `PendingReview`에서 `approve`를 호출하면 `Published` 구조체의 새로운 박스 인스턴스를 반환한다. `Published` 구조체는 `State` 트레잇을 구현하며, `request_review` 메서드와 `approve` 메서드 모두에서 `self`를 반환한다. 이 경우 포스트는 `Published` 상태로 유지되어야 하기 때문이다.

이제 `Post`의 `content` 메서드를 업데이트해야 한다. `content`에서 반환되는 값이 `Post`의 현재 상태에 따라 달라지도록 하기 위해, `Post`가 `state`에 정의된 `content` 메서드에 위임하도록 한다. 이 내용은 리스트 18-17에서 확인할 수 있다:

<Listing number="18-17" file-name="src/lib.rs" caption="`Post`의 `content` 메서드를 `State`의 `content` 메서드에 위임하도록 업데이트">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-17/src/lib.rs:here}}
```

</Listing>

이 규칙들을 `State`를 구현하는 구조체 내부에 유지하기 위해, `state`의 값에 `content` 메서드를 호출하고 `post` 인스턴스(즉, `self`)를 인자로 전달한다. 그런 다음 `state` 값의 `content` 메서드를 사용해 반환된 값을 반환한다.

`Option`에 `as_ref` 메서드를 호출하는 이유는 `Option` 내부 값의 소유권이 아닌 참조를 얻기 위해서다. `state`가 `Option<Box<dyn State>>`이기 때문에, `as_ref`를 호출하면 `Option<&Box<dyn State>>`가 반환된다. `as_ref`를 호출하지 않으면 함수 매개변수의 `&self`에서 `state`를 이동시킬 수 없기 때문에 에러가 발생한다.

그런 다음 `unwrap` 메서드를 호출하는데, 이 메서드는 절대 패닉을 일으키지 않는다. `Post`의 메서드들이 완료될 때 `state`가 항상 `Some` 값을 포함하도록 보장하기 때문이다. 이는 9장의 ["컴파일러보다 더 많은 정보를 가진 경우"][more-info-than-rustc]<!-- ignore -->에서 다룬 경우 중 하나로, 컴파일러가 이해할 수는 없지만 `None` 값이 절대 발생하지 않음을 알고 있는 상황이다.

이 시점에서 `&Box<dyn State>`에 `content`를 호출하면, `&`와 `Box`에 대한 역참조 강제가 적용되어 `State` 트레잇을 구현하는 타입의 `content` 메서드가 최종적으로 호출된다. 이는 `State` 트레잇 정의에 `content`를 추가해야 함을 의미하며, 여기에 현재 상태에 따라 반환할 콘텐츠에 대한 로직을 넣는다. 이 내용은 리스트 18-18에서 확인할 수 있다:

<Listing number="18-18" file-name="src/lib.rs" caption="`State` 트레잇에 `content` 메서드 추가">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-18/src/lib.rs:here}}
```

</Listing>

`content` 메서드에 기본 구현을 추가해 빈 문자열 슬라이스를 반환하도록 한다. 이는 `Draft`와 `PendingReview` 구조체에서 `content`를 구현할 필요가 없음을 의미한다. `Published` 구조체는 `content` 메서드를 오버라이드하고 `post.content`의 값을 반환한다.

10장에서 논의한 것처럼 이 메서드에 라이프타임 주석이 필요하다. `post`에 대한 참조를 인자로 받고 그 `post`의 일부에 대한 참조를 반환하기 때문에, 반환된 참조의 라이프타임은 `post` 인자의 라이프타임과 관련이 있다.

이제 리스트 18-11의 모든 내용이 작동한다! 블로그 포스트 워크플로우의 규칙을 따라 상태 패턴을 구현했다. 규칙과 관련된 로직은 `Post` 전체에 흩어져 있지 않고 상태 객체 내부에 존재한다.

> ### 왜 열거형을 사용하지 않았나요?
>
> 포스트 상태를 나타내는 열거형을 사용하지 않은 이유가 궁금할 수 있다. 이 방법도 가능한 해결책이다. 직접 시도해보고 최종 결과를 비교해보자! 열거형을 사용할 때의 단점은 열거형의 값을 확인하는 모든 곳에서 가능한 모든 변형을 처리하기 위해 `match` 표현식이나 유사한 것이 필요하다는 점이다. 이는 트레잇 객체를 사용한 해결책보다 더 반복적일 수 있다.


### 상태 패턴의 장단점

Rust가 객체 지향의 상태 패턴을 구현할 수 있음을 확인했다. 이 패턴은 각 상태에 따라 포스트가 가져야 하는 다양한 동작을 캡슐화한다. `Post`의 메서드는 다양한 동작에 대해 전혀 알지 못한다. 코드를 이렇게 구성하면, 포스트가 발행 상태일 때 어떤 동작을 하는지 알고 싶을 때 단 한 곳만 확인하면 된다: `Published` 구조체에서 `State` 트레이트를 구현한 부분이다.

만약 상태 패턴을 사용하지 않는 대안적인 구현을 한다면, `Post`의 메서드나 `main` 코드에서 `match` 표현식을 사용해 포스트의 상태를 확인하고 그에 따라 동작을 변경할 수도 있다. 하지만 이렇게 하면 포스트가 발행 상태일 때의 모든 의미를 이해하기 위해 여러 곳을 살펴봐야 한다! 상태가 더 많아질수록 이 문제는 더 심각해진다: 각 `match` 표현식에 새로운 분기(arm)를 추가해야 하기 때문이다.

상태 패턴을 사용하면 `Post` 메서드와 `Post`를 사용하는 곳에서 `match` 표현식이 필요 없으며, 새로운 상태를 추가할 때는 단순히 새로운 구조체를 추가하고 해당 구조체에 트레이트 메서드를 구현하기만 하면 된다.

상태 패턴을 사용한 구현은 기능을 추가하기 쉽다. 상태 패턴을 사용한 코드를 유지보수하는 것이 얼마나 간단한지 확인하기 위해, 다음 제안을 시도해 보자:

- `PendingReview` 상태에서 `Draft` 상태로 변경하는 `reject` 메서드를 추가한다.
- `Published` 상태로 변경하기 전에 `approve` 메서드를 두 번 호출하도록 요구한다.
- 포스트가 `Draft` 상태일 때만 사용자가 텍스트 콘텐츠를 추가할 수 있도록 허용한다. 힌트: 상태 객체가 콘텐츠의 변경 가능성을 책임지되, `Post`를 수정하는 책임은 지지 않도록 한다.

상태 패턴의 단점 중 하나는, 상태 간 전환을 상태 자체가 구현하기 때문에 일부 상태가 서로 결합된다는 점이다. 예를 들어 `PendingReview`와 `Published` 사이에 `Scheduled`와 같은 새로운 상태를 추가한다면, `PendingReview`의 코드를 수정해 `Scheduled`로 전환하도록 변경해야 한다. `PendingReview`가 새로운 상태의 추가에 따라 변경될 필요가 없다면 작업량이 줄어들겠지만, 그렇게 하려면 다른 디자인 패턴으로 전환해야 한다.

또 다른 단점은 일부 로직이 중복된다는 점이다. 이 중복을 줄이기 위해 `State` 트레이트에 `request_review`와 `approve` 메서드의 기본 구현을 추가해 `self`를 반환하도록 할 수도 있다. 하지만 이 방법은 동작하지 않는다: `State`를 트레이트 객체로 사용할 때, 트레이트는 구체적인 `self`가 무엇인지 정확히 알지 못하기 때문에 반환 타입을 컴파일 시점에 알 수 없다. (이는 앞서 언급한 dyn 호환성 규칙 중 하나다.)

다른 중복 사례로는 `Post`의 `request_review`와 `approve` 메서드의 유사한 구현이 있다. 두 메서드 모두 `Post`의 `state` 필드에 `Option::take`를 사용하며, `state`가 `Some`이면 래핑된 값의 동일한 메서드 구현에 위임하고, `state` 필드의 새 값을 결과로 설정한다. 만약 `Post`에 이 패턴을 따르는 메서드가 많다면, 반복을 줄이기 위해 매크로를 정의하는 것을 고려할 수 있다. (20장의 [“매크로”][macros]<!-- ignore --> 참조)

객체 지향 언어를 위해 정의된 상태 패턴을 그대로 구현하면, Rust의 강점을 최대한 활용하지 못하게 된다. `blog` 크레이트를 변경해 유효하지 않은 상태와 전환을 컴파일 타임 오류로 만들 수 있는 몇 가지 방법을 살펴보자.


#### 상태와 동작을 타입으로 인코딩하기

이번에는 상태 패턴을 재고하여 다른 방식의 트레이드오프를 얻는 방법을 알아본다. 상태와 전환을 완전히 캡슐화해 외부 코드가 알 수 없게 하는 대신, 상태를 서로 다른 타입으로 인코딩한다. 이를 통해 Rust의 타입 검사 시스템이 컴파일러 오류를 발생시켜, 게시된 게시물만 허용되는 곳에서 초안 게시물을 사용하려는 시도를 방지한다.

Listing 18-11의 `main` 함수 첫 부분을 살펴보자:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:here}}
```

</Listing>

`Post::new`를 사용해 초안 상태의 새 게시물을 생성하고, 게시물 내용에 텍스트를 추가하는 기능은 여전히 유지한다. 하지만 초안 게시물에서 빈 문자열을 반환하는 `content` 메서드를 제공하는 대신, 초안 게시물에는 `content` 메서드 자체를 없앤다. 이렇게 하면 초안 게시물의 내용을 가져오려고 할 때 메서드가 존재하지 않는다는 컴파일러 오류가 발생한다. 결과적으로, 초안 게시물의 내용을 실수로 프로덕션 환경에서 표시하는 일은 발생하지 않는다. 해당 코드는 컴파일조차 되지 않기 때문이다. Listing 18-19는 `Post` 구조체와 `DraftPost` 구조체의 정의, 그리고 각 구조체의 메서드를 보여준다.

<Listing number="18-19" file-name="src/lib.rs" caption="`content` 메서드가 있는 `Post`와 `content` 메서드가 없는 `DraftPost`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-19/src/lib.rs}}
```

</Listing>

`Post`와 `DraftPost` 구조체 모두 블로그 게시물 텍스트를 저장하는 `content` 필드를 가지고 있다. 이제 구조체에는 `state` 필드가 없다. 상태를 인코딩하는 방식을 구조체의 타입으로 옮겼기 때문이다. `Post` 구조체는 게시된 게시물을 나타내며, `content` 메서드를 통해 `content`를 반환한다.

`Post::new` 함수는 여전히 존재하지만, `Post` 인스턴스 대신 `DraftPost` 인스턴스를 반환한다. `content` 필드는 비공개이며, `Post`를 반환하는 함수가 없기 때문에 현재로서는 `Post` 인스턴스를 생성할 수 없다.

`DraftPost` 구조체에는 `add_text` 메서드가 있어 이전과 마찬가지로 `content`에 텍스트를 추가할 수 있다. 하지만 `DraftPost`에는 `content` 메서드가 정의되어 있지 않다는 점에 주목하자! 이제 프로그램은 모든 게시물이 초안 상태로 시작하고, 초안 게시물의 내용은 표시할 수 없도록 보장한다. 이러한 제약을 우회하려는 모든 시도는 컴파일러 오류를 발생시킬 것이다.


#### 트랜지션을 다른 타입으로 변환하여 구현하기

그렇다면 어떻게 게시물을 발행할 수 있을까? 우리는 초안 상태의 게시물이 반드시 검토와 승인을 거쳐야만 발행될 수 있도록 규칙을 강제하고 싶다. 검토 대기 중인 게시물은 여전히 어떤 내용도 표시하지 않아야 한다. 이 제약 조건을 구현하기 위해 `PendingReviewPost`라는 새로운 구조체를 추가하고, `DraftPost`에 `request_review` 메서드를 정의하여 `PendingReviewPost`를 반환하도록 한다. 또한 `PendingReviewPost`에 `approve` 메서드를 정의하여 `Post`를 반환하도록 한다. 이는 리스팅 18-20에서 확인할 수 있다.

<Listing number="18-20" file-name="src/lib.rs" caption="`DraftPost`에서 `request_review`를 호출해 생성되는 `PendingReviewPost`와 `PendingReviewPost`를 발행된 `Post`로 변환하는 `approve` 메서드">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-20/src/lib.rs:here}}
```

</Listing>

`request_review`와 `approve` 메서드는 `self`의 소유권을 가져가므로, `DraftPost`와 `PendingReviewPost` 인스턴스를 소비하고 각각 `PendingReviewPost`와 발행된 `Post`로 변환한다. 이렇게 하면 `request_review`를 호출한 후에도 `DraftPost` 인스턴스가 남아 있지 않게 된다. `PendingReviewPost` 구조체는 `content` 메서드가 정의되어 있지 않으므로, `DraftPost`와 마찬가지로 내용을 읽으려고 하면 컴파일러 오류가 발생한다. `content` 메서드가 정의된 발행된 `Post` 인스턴스를 얻는 유일한 방법은 `PendingReviewPost`에서 `approve` 메서드를 호출하는 것이고, `PendingReviewPost`를 얻는 유일한 방법은 `DraftPost`에서 `request_review` 메서드를 호출하는 것이다. 이렇게 하여 블로그 게시물의 워크플로우를 타입 시스템에 인코딩했다.

그러나 `main`에도 약간의 변경이 필요하다. `request_review`와 `approve` 메서드는 호출된 구조체를 수정하는 대신 새로운 인스턴스를 반환하므로, 반환된 인스턴스를 저장하기 위해 `let post =` 섀도잉 할당을 추가해야 한다. 또한 초안 및 검토 대기 중인 게시물의 내용이 빈 문자열이라는 단언은 더 이상 필요하지 않다. 이 상태의 게시물 내용을 사용하려는 코드는 컴파일할 수 없기 때문이다. 업데이트된 `main` 코드는 리스팅 18-21에서 확인할 수 있다.

<Listing number="18-21" file-name="src/main.rs" caption="새로운 블로그 게시물 워크플로우 구현을 사용하도록 수정된 `main`">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-21/src/main.rs}}
```

</Listing>

`post`를 재할당하기 위해 `main`에 필요한 변경 사항은 이 구현이 더 이상 객체 지향적인 상태 패턴을 따르지 않음을 의미한다. 상태 간의 변환이 `Post` 구현 내에 완전히 캡슐화되지 않았기 때문이다. 그러나 우리가 얻은 이점은 타입 시스템과 컴파일 타임에 발생하는 타입 검사 덕분에 이제 잘못된 상태가 불가능해졌다는 점이다. 이는 발행되지 않은 게시물의 내용이 표시되는 등의 특정 버그가 프로덕션 환경에 도달하기 전에 발견되도록 보장한다.

리스팅 18-21 이후의 `blog` 크레이트에서 이 섹션의 시작 부분에서 제안된 작업을 시도해보고 이 버전의 코드 설계에 대해 어떻게 생각하는지 확인해보자. 이 설계에서 일부 작업은 이미 완료되었을 수도 있다.

우리는 Rust가 객체 지향적인 디자인 패턴을 구현할 수 있지만, 타입 시스템에 상태를 인코딩하는 것과 같은 다른 패턴도 Rust에서 사용 가능하다는 것을 확인했다. 이러한 패턴은 서로 다른 장단점을 가진다. 객체 지향 패턴에 익숙할지라도, Rust의 기능을 활용하기 위해 문제를 재고하는 것은 컴파일 타임에 일부 버그를 방지하는 등의 이점을 제공할 수 있다. 소유권과 같은 객체 지향 언어에는 없는 특정 기능 때문에 Rust에서 객체 지향 패턴이 항상 최선의 해결책은 아니다.


## 요약

이 장을 읽고 나면 Rust가 객체 지향 언어인지 여부에 대한 의견은 각자 다를 수 있다. 그러나 이제 트레이트 객체를 사용해 Rust에서 객체 지향적 기능을 활용할 수 있다는 점은 분명히 알게 됐다. 동적 디스패치는 런타임 성능을 약간 희생하는 대신 코드에 유연성을 제공한다. 이 유연성을 활용해 코드의 유지보수성을 높이는 객체 지향 패턴을 구현할 수 있다. 또한 Rust는 소유권과 같은 객체 지향 언어에는 없는 고유한 기능도 제공한다. Rust의 강점을 최대한 활용하기 위해 객체 지향 패턴이 항상 최선의 방법은 아니지만, 선택 가능한 옵션 중 하나임은 분명하다.

다음 장에서는 Rust의 또 다른 유연한 기능인 패턴에 대해 알아본다. 이 책 전반에서 간략히 살펴봤지만, 아직 그 모든 잠재력을 확인하진 못했다. 이제 본격적으로 파헤쳐보자!

[more-info-than-rustc]: ch09-03-to-panic-or-not-to-panic.html#cases-in-which-you-have-more-information-than-the-compiler
[macros]: ch20-05-macros.html#macros


