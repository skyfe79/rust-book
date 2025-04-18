## 아이템 시퀀스 처리와 이터레이터

이터레이터 패턴을 사용하면 아이템 시퀀스에 대해 순차적으로 작업을 수행할 수 있다. 이터레이터는 각 아이템을 순회하고 시퀀스가 끝났는지 판단하는 로직을 담당한다. 이터레이터를 사용하면 이러한 로직을 직접 구현할 필요가 없다.

Rust에서 이터레이터는 **게으른(lazy)** 특성을 가진다. 이는 이터레이터를 소모하는 메서드를 호출하기 전까지는 아무런 효과가 없다는 의미다. 예를 들어, 리스트 13-10은 `Vec<T>`에 정의된 `iter` 메서드를 호출해 벡터 `v1`의 아이템에 대한 이터레이터를 생성한다. 이 코드 자체로는 유용한 작업을 수행하지 않는다.

<Listing number="13-10" file-name="src/main.rs" caption="이터레이터 생성">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-10/src/main.rs:here}}
```

</Listing>

이터레이터는 `v1_iter` 변수에 저장된다. 이터레이터를 생성한 후에는 다양한 방식으로 사용할 수 있다. 3장의 리스트 3-5에서는 `for` 루프를 사용해 배열을 순회하며 각 아이템에 대해 코드를 실행했다. 이때 내부적으로 이터레이터가 암시적으로 생성되고 소모되었지만, 지금까지는 그 동작 원리를 자세히 다루지 않았다.

리스트 13-11의 예제에서는 이터레이터 생성과 `for` 루프에서의 사용을 분리했다. `v1_iter`에 있는 이터레이터를 사용해 `for` 루프가 호출되면, 이터레이터의 각 엘리먼트가 루프의 한 번의 반복에서 사용되며, 각 값을 출력한다.

<Listing number="13-11" file-name="src/main.rs" caption="`for` 루프에서 이터레이터 사용">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-11/src/main.rs:here}}
```

</Listing>

표준 라이브러리에서 이터레이터를 제공하지 않는 언어에서는, 인덱스 0부터 시작하는 변수를 사용해 벡터에서 값을 가져오고, 루프에서 변수 값을 증가시키며 벡터의 전체 아이템 수에 도달할 때까지 반복하는 방식으로 동일한 기능을 구현할 가능성이 높다.

이터레이터는 이러한 모든 로직을 대신 처리해주며, 잠재적으로 실수할 수 있는 반복 코드를 줄여준다. 이터레이터는 벡터처럼 인덱스로 접근할 수 있는 데이터 구조뿐만 아니라 다양한 종류의 시퀀스에 동일한 로직을 사용할 수 있는 유연성을 제공한다. 이터레이터가 어떻게 이를 가능하게 하는지 살펴보자.


### `Iterator` 트레이트와 `next` 메서드

모든 이터레이터는 표준 라이브러리에 정의된 `Iterator`라는 트레이트를 구현한다. 이 트레이트의 정의는 다음과 같다:

```rust
pub trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;

    // 기본 구현이 있는 메서드들은 생략됨
}
```

이 정의에서 새로운 구문인 `type Item`과 `Self::Item`이 사용되었음을 알 수 있다. 이는 이 트레이트와 연관된 타입을 정의하는 것이다. 연관 타입에 대해서는 20장에서 자세히 다룰 예정이다. 지금은 `Iterator` 트레이트를 구현하려면 `Item` 타입도 정의해야 하며, 이 `Item` 타입이 `next` 메서드의 반환 타입으로 사용된다는 점만 알아두면 된다. 즉, `Item` 타입은 이터레이터가 반환할 타입이 된다.

`Iterator` 트레이트는 구현자가 오직 하나의 메서드만 정의하도록 요구한다: 바로 `next` 메서드다. 이 메서드는 이터레이터에서 한 번에 하나의 아이템을 반환하며, `Some`으로 감싸져 있다. 이터레이션이 끝나면 `None`을 반환한다.

이터레이터에서 직접 `next` 메서드를 호출할 수 있다. 리스트 13-12는 벡터에서 생성된 이터레이터에 `next`를 반복적으로 호출했을 때 어떤 값이 반환되는지 보여준다.

<Listing number="13-12" file-name="src/lib.rs" caption="이터레이터에서 `next` 메서드 호출">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-12/src/lib.rs:here}}
```

</Listing>

`v1_iter`를 가변으로 만들어야 한다는 점에 주목하자: 이터레이터에서 `next` 메서드를 호출하면 이터레이터가 시퀀스 내에서 현재 위치를 추적하기 위해 사용하는 내부 상태가 변경된다. 즉, 이 코드는 이터레이터를 소비하거나 사용한다. `next`를 호출할 때마다 이터레이터의 아이템을 하나씩 소비한다. `for` 루프를 사용할 때는 `v1_iter`를 가변으로 만들 필요가 없었는데, 이는 루프가 `v1_iter`의 소유권을 가져와서 내부적으로 가변으로 만들었기 때문이다.

또한 `next`를 호출하여 얻은 값들은 벡터 내 값에 대한 불변 참조라는 점도 주목하자. `iter` 메서드는 불변 참조에 대한 이터레이터를 생성한다. 만약 `v1`의 소유권을 가져오고 소유한 값을 반환하는 이터레이터를 만들고 싶다면, `iter` 대신 `into_iter`를 호출하면 된다. 마찬가지로, 가변 참조를 순회하고 싶다면 `iter` 대신 `iter_mut`를 호출하면 된다.


### 이터레이터를 소비하는 메서드

`Iterator` 트레이트는 표준 라이브러리에서 제공하는 기본 구현을 가진 여러 메서드를 포함한다. 이 메서드들에 대한 자세한 정보는 표준 라이브러리 API 문서에서 `Iterator` 트레이트를 참조하면 된다. 이 메서드들 중 일부는 정의 내부에서 `next` 메서드를 호출하기 때문에, `Iterator` 트레이트를 구현할 때 `next` 메서드를 반드시 구현해야 한다.

`next`를 호출하는 메서드는 _소비 어댑터(consuming adapters)_ 라고 불린다. 이 메서드들을 호출하면 이터레이터가 소비되기 때문이다. 예를 들어, `sum` 메서드는 이터레이터의 소유권을 가져와 `next`를 반복적으로 호출하며 아이템을 순회한다. 이 과정에서 각 아이템을 누적 합계에 더하고, 순회가 완료되면 총합을 반환한다. 리스트 13-13은 `sum` 메서드를 사용하는 예제를 보여준다.

<Listing number="13-13" file-name="src/lib.rs" caption="`sum` 메서드를 호출하여 이터레이터의 모든 아이템의 총합을 구하기">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-13/src/lib.rs:here}}
```

</Listing>

`sum`을 호출한 후에는 `v1_iter`를 사용할 수 없다. `sum`이 호출된 이터레이터의 소유권을 가져가기 때문이다.


### 다른 이터레이터를 생성하는 메서드

_이터레이터 어댑터_는 `Iterator` 트레이트에 정의된 메서드로, 이터레이터를 소비하지 않는다. 대신, 원래 이터레이터의 일부를 변경하여 새로운 이터레이터를 생성한다.

리스트 13-14는 이터레이터 어댑터 메서드인 `map`을 호출하는 예제를 보여준다. `map`은 각 항목을 순회할 때 호출할 클로저를 인자로 받는다. `map` 메서드는 수정된 항목을 생성하는 새로운 이터레이터를 반환한다. 여기서 클로저는 벡터의 각 항목에 1을 더한 새로운 이터레이터를 생성한다:

<Listing number="13-14" file-name="src/main.rs" caption="새로운 이터레이터를 생성하기 위해 이터레이터 어댑터 `map` 호출">

```rust,not_desired_behavior
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-14/src/main.rs:here}}
```

</Listing>

하지만 이 코드는 다음과 같은 경고를 발생시킨다:

```console
{{#include ../listings/ch13-functional-features/listing-13-14/output.txt}}
```

리스트 13-14의 코드는 아무런 동작을 하지 않는다. 지정한 클로저가 호출되지 않기 때문이다. 이 경고는 이터레이터 어댑터가 지연 평가(lazy)되며, 이터레이터를 소비해야 한다는 사실을 상기시켜 준다.

이 경고를 해결하고 이터레이터를 소비하기 위해, 12장의 리스트 12-1에서 `env::args`와 함께 사용한 `collect` 메서드를 사용한다. 이 메서드는 이터레이터를 소비하고 결과 값을 컬렉션 데이터 타입으로 모은다.

리스트 13-15에서는 `map` 호출로 반환된 이터레이터를 순회한 결과를 벡터로 모은다. 이 벡터는 원래 벡터의 각 항목에 1을 더한 값을 포함하게 된다.

<Listing number="13-15" file-name="src/main.rs" caption="새로운 이터레이터를 생성하기 위해 `map` 메서드를 호출하고, `collect` 메서드를 호출하여 새로운 이터레이터를 소비하고 벡터를 생성">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-15/src/main.rs:here}}
```

</Listing>

`map`은 클로저를 인자로 받기 때문에, 각 항목에 대해 수행하고 싶은 어떤 연산이든 지정할 수 있다. 이는 클로저가 `Iterator` 트레이트가 제공하는 반복 동작을 재사용하면서도 특정 동작을 커스터마이즈할 수 있는 좋은 예시이다.

여러 이터레이터 어댑터 호출을 연결하여 복잡한 동작을 가독성 있게 수행할 수 있다. 하지만 모든 이터레이터는 지연 평가되기 때문에, 이터레이터 어댑터 호출의 결과를 얻으려면 소비형 어댑터 메서드 중 하나를 호출해야 한다.


### 환경을 캡처하는 클로저 사용하기

많은 이터레이터 어댑터는 클로저를 인자로 받는다. 특히 이터레이터 어댑터에 전달하는 클로저는 주변 환경을 캡처하는 경우가 많다.

이 예제에서는 클로저를 인자로 받는 `filter` 메서드를 사용한다. 이 클로저는 이터레이터에서 아이템을 받아 `bool` 값을 반환한다. 클로저가 `true`를 반환하면, `filter`가 생성한 이터레이션에 해당 값이 포함된다. `false`를 반환하면 포함되지 않는다.

리스트 13-16에서는 `filter`를 사용해 주변 환경에서 `shoe_size` 변수를 캡처하는 클로저를 적용한다. 이를 통해 `Shoe` 구조체 인스턴스 컬렉션을 순회하며 지정된 크기의 신발만 반환한다.

<Listing number="13-16" file-name="src/lib.rs" caption="`shoe_size`를 캡처하는 클로저와 함께 `filter` 메서드 사용하기">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-16/src/lib.rs}}
```

</Listing>

`shoes_in_size` 함수는 신발 벡터와 신발 크기를 매개변수로 받아 해당 크기의 신발만 포함된 벡터를 반환한다.

`shoes_in_size` 함수 본문에서는 `into_iter`를 호출해 벡터의 소유권을 가진 이터레이터를 생성한다. 그런 다음 `filter`를 호출해 클로저가 `true`를 반환하는 요소만 포함된 새로운 이터레이터로 변환한다.

클로저는 환경에서 `shoe_size` 매개변수를 캡처하고, 각 신발의 크기와 비교해 지정된 크기의 신발만 남긴다. 마지막으로 `collect`를 호출해 변환된 이터레이터가 반환한 값을 벡터로 모아 함수에서 반환한다.

테스트를 통해 `shoes_in_size`를 호출하면 지정한 크기와 동일한 신발만 반환되는 것을 확인할 수 있다.


