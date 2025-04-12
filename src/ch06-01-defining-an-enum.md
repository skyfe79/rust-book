## 열거형 정의하기

구조체는 `width`와 `height` 같은 관련 필드와 데이터를 그룹화하는 방법을 제공한다. 반면, 열거형은 값이 가능한 집합 중 하나임을 표현하는 방법을 제공한다. 예를 들어, `Rectangle`이 `Circle`과 `Triangle`도 포함하는 가능한 도형 집합 중 하나라고 말하고 싶을 수 있다. 이를 위해 Rust는 이러한 가능성을 열거형으로 인코딩할 수 있게 한다.

코드로 표현하고 싶은 상황을 살펴보고, 이 경우에 왜 열거형이 유용하고 구조체보다 더 적합한지 알아보자. IP 주소를 다루어야 한다고 가정해보자. 현재 IP 주소에는 두 가지 주요 표준이 사용된다: 버전 4와 버전 6이다. 우리 프로그램이 만날 수 있는 IP 주소의 가능성이 이 두 가지뿐이므로, 모든 가능한 변형을 *열거*할 수 있다. 이것이 열거형이라는 이름의 유래이다.

어떤 IP 주소도 버전 4나 버전 6 중 하나일 수 있지만, 동시에 둘 다일 수는 없다. IP 주소의 이러한 특성은 열거형 데이터 구조를 적합하게 만든다. 왜냐하면 열거형 값은 오직 하나의 변형만 될 수 있기 때문이다. 버전 4와 버전 6 주소는 근본적으로 여전히 IP 주소이므로, 코드가 어떤 종류의 IP 주소에도 적용되는 상황을 처리할 때 동일한 타입으로 취급되어야 한다.

이 개념을 코드로 표현하기 위해 `IpAddrKind` 열거형을 정의하고, IP 주소가 될 수 있는 가능한 종류인 `V4`와 `V6`를 나열할 수 있다. 이들은 열거형의 변형이다:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:def}}
```

`IpAddrKind`는 이제 우리 코드의 다른 곳에서 사용할 수 있는 커스텀 데이터 타입이 된다.


### 열거형 값

`IpAddrKind`의 두 가지 변형을 다음과 같이 인스턴스화할 수 있다:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:instance}}
```

열거형의 변형은 해당 식별자 아래에 네임스페이스로 구분되며, 두 개의 콜론(`::`)을 사용해 구분한다. 이는 `IpAddrKind::V4`와 `IpAddrKind::V6`가 모두 동일한 타입인 `IpAddrKind`로 간주되기 때문에 유용하다. 예를 들어, `IpAddrKind` 타입을 인자로 받는 함수를 정의할 수 있다:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn}}
```

그리고 이 함수를 두 변형 중 어느 것으로도 호출할 수 있다:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn_call}}
```

열거형을 사용하면 더 많은 장점이 있다. IP 주소 타입에 대해 더 깊이 생각해보면, 현재는 실제 IP 주소 데이터를 저장할 방법이 없다. 단지 어떤 종류인지만 알고 있을 뿐이다. 5장에서 구조체를 배웠기 때문에, 이를 구조체로 해결하려는 생각이 들 수 있다. 리스팅 6-1은 이를 보여준다.

<Listing number="6-1" caption="구조체를 사용해 IP 주소의 데이터와 `IpAddrKind` 변형 저장">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-01/src/main.rs:here}}
```

</Listing>

여기서 `IpAddr` 구조체를 정의했으며, 두 개의 필드를 가지고 있다: `IpAddrKind` 타입의 `kind` 필드와 `String` 타입의 `address` 필드. 이 구조체의 두 인스턴스가 있다. 첫 번째는 `home`이며, `kind` 값으로 `IpAddrKind::V4`를 가지고 있고, 관련 주소 데이터는 `127.0.0.1`이다. 두 번째 인스턴스는 `loopback`이며, `kind` 값으로 `IpAddrKind::V6`를 가지고 있고, 관련 주소 데이터는 `::1`이다. 이렇게 구조체를 사용해 `kind`와 `address` 값을 함께 묶었기 때문에, 이제 변형이 값과 연결된다.

그러나 열거형만 사용해 동일한 개념을 표현하는 것이 더 간결하다: 구조체 안에 열거형을 넣는 대신, 데이터를 각 열거형 변형에 직접 넣을 수 있다. 이 새로운 `IpAddr` 열거형 정의는 `V4`와 `V6` 변형이 모두 `String` 값을 가질 것이라고 명시한다:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-02-enum-with-data/src/main.rs:here}}
```

각 열거형 변형에 데이터를 직접 첨부했기 때문에, 추가적인 구조체가 필요 없다. 여기서 열거형이 어떻게 동작하는지 또 다른 세부 사항을 더 쉽게 확인할 수 있다: 정의한 각 열거형 변형의 이름은 해당 열거형의 인스턴스를 생성하는 함수가 된다. 즉, `IpAddr::V4()`는 `String` 인자를 받아 `IpAddr` 타입의 인스턴스를 반환하는 함수 호출이다. 열거형을 정의함으로써 자동으로 이 생성자 함수가 정의된다.

열거형을 사용하는 또 다른 장점은 각 변형이 서로 다른 타입과 양의 데이터를 가질 수 있다는 점이다. 버전 4 IP 주소는 항상 0에서 255 사이의 값을 가진 네 개의 숫자 구성 요소를 가진다. 만약 `V4` 주소를 네 개의 `u8` 값으로 저장하고 싶지만, `V6` 주소는 하나의 `String` 값으로 표현하고 싶다면, 구조체로는 이를 할 수 없다. 열거형은 이러한 경우를 쉽게 처리한다:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-03-variants-with-different-data/src/main.rs:here}}
```

버전 4와 버전 6 IP 주소를 저장하기 위한 데이터 구조를 정의하는 여러 가지 방법을 보여줬다. 그러나 IP 주소를 저장하고 어떤 종류인지 인코딩하는 것은 매우 일반적인 요구 사항이기 때문에, [표준 라이브러리에서 사용할 수 있는 정의가 있다!][IpAddr]<!-- ignore --> 표준 라이브러리가 `IpAddr`를 어떻게 정의하는지 살펴보자: 우리가 정의하고 사용한 것과 동일한 열거형과 변형을 가지고 있지만, 주소 데이터를 두 개의 다른 구조체 형태로 변형 안에 포함시킨다. 각 변형에 대해 다르게 정의된 구조체이다:

```rust
struct Ipv4Addr {
    // --snip--
}

struct Ipv6Addr {
    // --snip--
}

enum IpAddr {
    V4(Ipv4Addr),
    V6(Ipv6Addr),
}
```

이 코드는 열거형 변형 안에 어떤 종류의 데이터든 넣을 수 있음을 보여준다: 문자열, 숫자 타입, 또는 구조체 등. 심지어 다른 열거형도 포함할 수 있다! 또한 표준 라이브러리 타입은 종종 여러분이 생각해낸 것보다 훨씬 복잡하지 않다.

표준 라이브러리에 `IpAddr` 정의가 포함되어 있더라도, 표준 라이브러리의 정의를 우리의 스코프로 가져오지 않았기 때문에 여전히 우리만의 정의를 생성하고 사용할 수 있다. 7장에서 타입을 스코프로 가져오는 방법에 대해 더 자세히 다룰 것이다.

리스팅 6-2에서 또 다른 열거형 예제를 살펴보자: 이 열거형은 다양한 타입의 값을 변형 안에 포함한다.

<Listing number="6-2" caption="각 변형이 서로 다른 양과 타입의 값을 저장하는 `Message` 열거형">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-02/src/main.rs:here}}
```

</Listing>

이 열거형은 네 가지 변형을 가지고 있으며, 각 변형은 서로 다른 타입을 가진다:

- `Quit`은 어떤 데이터도 가지고 있지 않다.
- `Move`는 구조체처럼 이름이 있는 필드를 가진다.
- `Write`는 단일 `String`을 포함한다.
- `ChangeColor`는 세 개의 `i32` 값을 포함한다.

리스팅 6-2와 같은 변형을 가진 열거형을 정의하는 것은 다양한 종류의 구조체 정의를 만드는 것과 유사하지만, 열거형은 `struct` 키워드를 사용하지 않고 모든 변형이 `Message` 타입 아래에 그룹화된다. 다음 구조체들은 앞서 열거형 변형이 가지고 있는 것과 동일한 데이터를 보유할 수 있다:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-04-structs-similar-to-message-enum/src/main.rs:here}}
```

그러나 각각의 구조체가 자신만의 타입을 가지고 있다면, 리스팅 6-2에서 정의한 `Message` 열거형처럼 단일 타입으로 이러한 종류의 메시지를 받는 함수를 쉽게 정의할 수 없다.

열거형과 구조체 사이에는 또 다른 유사점이 있다: 구조체에 `impl`을 사용해 메서드를 정의할 수 있는 것처럼, 열거형에도 메서드를 정의할 수 있다. 다음은 `Message` 열거형에 정의할 수 있는 `call`이라는 메서드의 예시이다:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-05-methods-on-enums/src/main.rs:here}}
```

메서드의 본문은 `self`를 사용해 메서드를 호출한 값을 가져온다. 이 예제에서 `m`이라는 변수를 생성했으며, 이 변수는 `Message::Write(String::from("hello"))` 값을 가진다. 따라서 `m.call()`을 실행할 때 `call` 메서드의 본문에서 `self`는 이 값이 된다.

표준 라이브러리에서 매우 일반적이고 유용한 또 다른 열거형인 `Option`을 살펴보자.


### `Option` 열거형과 Null 값 대비 장점

이 섹션에서는 표준 라이브러리에 정의된 또 다른 열거형인 `Option`에 대한 사례를 살펴본다. `Option` 타입은 값이 존재할 수도 있고 없을 수도 있는 매우 일반적인 시나리오를 인코딩한다.

예를 들어, 비어 있지 않은 리스트에서 첫 번째 항목을 요청하면 값을 얻을 수 있다. 하지만 빈 리스트에서 첫 번째 항목을 요청하면 아무것도 얻지 못한다. 이 개념을 타입 시스템으로 표현하면 컴파일러가 모든 경우를 처리했는지 확인할 수 있다. 이 기능은 다른 프로그래밍 언어에서 매우 흔히 발생하는 버그를 방지할 수 있다.

프로그래밍 언어 설계는 어떤 기능을 포함할지에 대해 고민하는 경우가 많지만, 어떤 기능을 제외할지도 중요하다. Rust는 다른 많은 언어가 가지고 있는 null 기능을 제공하지 않는다. _Null_은 값이 없음을 의미하는 값이다. null을 지원하는 언어에서는 변수가 항상 두 가지 상태 중 하나일 수 있다: null이거나 null이 아니거나.

2009년 발표에서 null의 발명가인 Tony Hoare는 이렇게 말했다:

> 나는 이것을 10억 달러짜리 실수라고 부른다. 당시 나는 객체 지향 언어에서 참조를 위한 첫 번째 포괄적인 타입 시스템을 설계하고 있었다. 내 목표는 모든 참조 사용이 절대적으로 안전하도록 하고, 컴파일러가 자동으로 검사하도록 하는 것이었다. 하지만 null 참조를 추가하는 유혹을 이기지 못했고, 단순히 구현하기 쉬웠기 때문이었다. 이것은 셀 수 없이 많은 오류, 취약점, 시스템 충돌을 초래했고, 지난 40년 동안 10억 달러의 고통과 손실을 초래했다.

null 값의 문제는 null 값을 null이 아닌 값처럼 사용하려고 하면 어떤 종류의 오류가 발생한다는 점이다. null 또는 null이 아닌 속성이 광범위하게 적용되기 때문에 이런 종류의 오류를 범하기가 매우 쉽다.

하지만 null이 표현하려는 개념은 여전히 유용하다: null은 어떤 이유로 현재 유효하지 않거나 존재하지 않는 값을 의미한다.

문제는 개념 자체가 아니라 특정 구현에 있다. 따라서 Rust는 null을 제공하지 않지만, 값이 존재하거나 존재하지 않음을 인코딩할 수 있는 열거형을 제공한다. 이 열거형이 바로 `Option<T>`이며, 표준 라이브러리에 다음과 같이 정의되어 있다:

```rust
enum Option<T> {
    None,
    Some(T),
}
```

`Option<T>` 열거형은 매우 유용하기 때문에 프리루드에 포함되어 있다. 따라서 명시적으로 스코프로 가져올 필요가 없다. 또한 `Some`과 `None` 변형도 프리루드에 포함되어 있어 `Option::` 접두사 없이 바로 사용할 수 있다. `Option<T>` 열거형은 여전히 일반적인 열거형이며, `Some(T)`와 `None`은 `Option<T>` 타입의 변형이다.

`<T>` 문법은 아직 다루지 않은 Rust의 기능이다. 이것은 제네릭 타입 매개변수이며, 제네릭에 대해서는 10장에서 더 자세히 다룰 것이다. 지금은 `<T>`가 `Option` 열거형의 `Some` 변형이 어떤 타입의 데이터도 하나씩 보유할 수 있음을 의미한다는 점만 알면 된다. 그리고 `T` 대신 사용되는 각 구체적인 타입은 전체 `Option<T>` 타입을 다른 타입으로 만든다. 다음은 숫자 타입과 문자 타입을 보유하기 위해 `Option` 값을 사용하는 예제이다:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-06-option-examples/src/main.rs:here}}
```

`some_number`의 타입은 `Option<i32>`이다. `some_char`의 타입은 `Option<char>`로, 다른 타입이다. Rust는 `Some` 변형 안에 값을 지정했기 때문에 이 타입들을 추론할 수 있다. `absent_number`의 경우 Rust는 전체 `Option` 타입을 명시하도록 요구한다: 컴파일러는 `None` 값만 보고 해당 `Some` 변형이 보유할 타입을 추론할 수 없다. 여기서 우리는 `absent_number`가 `Option<i32>` 타입이 되도록 명시한다.

`Some` 값을 가지고 있다면 값이 존재하며 그 값이 `Some` 안에 보관되어 있음을 알 수 있다. `None` 값을 가지고 있다면 어떤 의미에서는 null과 동일하다: 유효한 값이 없다. 그렇다면 `Option<T>`를 사용하는 것이 null을 사용하는 것보다 왜 더 나을까?

간단히 말하면, `Option<T>`와 `T`(여기서 `T`는 어떤 타입이든 될 수 있음)는 다른 타입이기 때문에, 컴파일러는 `Option<T>` 값을 마치 확실히 유효한 값인 것처럼 사용하지 못하게 한다. 예를 들어, 이 코드는 `i8`을 `Option<i8>`에 더하려고 하기 때문에 컴파일되지 않는다:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/src/main.rs:here}}
```

이 코드를 실행하면 다음과 같은 오류 메시지가 나타난다:

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/output.txt}}
```

이 오류 메시지는 Rust가 `i8`과 `Option<i8>`을 더하는 방법을 이해하지 못한다는 것을 의미한다. 왜냐하면 이들은 다른 타입이기 때문이다. Rust에서 `i8`과 같은 타입의 값을 가지고 있다면, 컴파일러는 우리가 항상 유효한 값을 가지고 있음을 보장한다. 따라서 그 값을 사용하기 전에 null을 확인할 필요 없이 안심하고 진행할 수 있다. `Option<i8>`(또는 우리가 작업 중인 어떤 타입의 값)을 가지고 있을 때만 값이 없을 가능성을 고려해야 하며, 컴파일러는 그 값을 사용하기 전에 그 경우를 처리하도록 강제한다.

다시 말해, `Option<T>`를 `T`로 변환해야만 `T` 연산을 수행할 수 있다. 일반적으로 이는 null과 관련된 가장 흔한 문제 중 하나인, 실제로는 null인데 null이 아니라고 가정하는 경우를 잡아내는 데 도움이 된다.

null이 아니라고 잘못 가정하는 위험을 제거하면 코드에 더 확신을 가질 수 있다. null일 가능성이 있는 값을 가지려면, 그 값의 타입을 `Option<T>`로 명시적으로 선택해야 한다. 그리고 그 값을 사용할 때는 값이 null인 경우를 명시적으로 처리해야 한다. `Option<T>`가 아닌 타입의 값은 어디에서나 안전하게 null이 아니라고 가정할 수 있다. 이는 Rust가 null의 광범위한 사용을 제한하고 Rust 코드의 안전성을 높이기 위해 의도적으로 설계한 결정이다.

그렇다면 `Option<T>` 타입의 값에서 `Some` 변형 안의 `T` 값을 어떻게 꺼내서 사용할 수 있을까? `Option<T>` 열거형에는 다양한 상황에서 유용한 많은 메서드가 있다; [문서][docs]에서 확인할 수 있다. `Option<T>`의 메서드를 익히는 것은 Rust를 사용하는 데 있어 매우 유용할 것이다.

일반적으로 `Option<T>` 값을 사용하려면 각 변형을 처리할 코드가 필요하다. `Some(T)` 값을 가지고 있을 때만 실행될 코드가 필요하며, 이 코드는 내부의 `T`를 사용할 수 있다. `None` 값을 가지고 있을 때만 실행될 다른 코드도 필요하며, 이 코드는 `T` 값을 사용할 수 없다. `match` 표현식은 열거형과 함께 사용할 때 이 작업을 수행하는 제어 흐름 구조이다: 열거형의 어떤 변형을 가지고 있는지에 따라 다른 코드를 실행하며, 해당 코드는 매칭된 값 안의 데이터를 사용할 수 있다.

[IpAddr]: ../std/net/enum.IpAddr.html
[option]: ../std/option/enum.Option.html
[docs]: ../std/option/enum.Option.html


