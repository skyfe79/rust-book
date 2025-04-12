## 간결한 제어 흐름: `if let`과 `let else`

`if let` 구문은 `if`와 `let`을 결합하여 더 간결하게 패턴 매칭을 처리할 수 있게 해준다. 특정 패턴에만 관심이 있고 나머지는 무시하려는 경우 유용하다. 예를 들어, `Option<u8>` 타입의 `config_max` 변수를 매칭할 때, 값이 `Some`인 경우에만 코드를 실행하고 싶다면 다음과 같이 작성할 수 있다.

<Listing number="6-6" caption="값이 `Some`인 경우에만 코드를 실행하는 `match` 예제">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-06/src/main.rs:here}}
```

</Listing>

값이 `Some`인 경우, 패턴에서 `max` 변수에 값을 바인딩하여 `Some` 내부의 값을 출력한다. `None` 값에 대해서는 아무런 동작도 수행하지 않는다. `match` 표현식을 완성하기 위해 `_ => ()`를 추가해야 하는데, 이는 불필요한 보일러플레이트 코드다.

이를 더 간단하게 `if let`을 사용해 작성할 수 있다. 다음 코드는 Listing 6-6의 `match`와 동일한 동작을 한다:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-12-if-let/src/main.rs:here}}
```

`if let` 구문은 패턴과 표현식을 등호로 구분하여 사용한다. 이는 `match`와 동일하게 동작하며, 표현식은 `match`에 전달되고 패턴은 첫 번째 매치 갈래가 된다. 여기서 패턴은 `Some(max)`이며, `max`는 `Some` 내부의 값에 바인딩된다. 그런 다음 `if let` 블록 내에서 `max`를 사용할 수 있으며, 이는 `match` 갈래에서 `max`를 사용하는 것과 동일하다. `if let` 블록의 코드는 값이 패턴과 일치할 때만 실행된다.

`if let`을 사용하면 타이핑이 줄어들고, 들여쓰기가 감소하며, 보일러플레이트 코드가 사라진다. 하지만 `match`가 제공하는 철저한 검사 기능을 잃게 된다. `match`와 `if let` 중 어떤 것을 선택할지는 특정 상황에서 무엇을 하느냐에 달려 있으며, 간결함을 얻는 대신 철저한 검사를 포기하는 것이 적절한지 판단해야 한다.

즉, `if let`은 특정 패턴과 일치할 때만 코드를 실행하고 나머지 값은 무시하는 `match`의 축약형이라고 생각할 수 있다.

`if let`과 함께 `else`를 사용할 수도 있다. `else` 블록의 코드는 `if let`과 동등한 `match` 표현식에서 `_` 케이스에 해당하는 블록과 동일하다. Listing 6-4의 `Coin` 열거형 정의를 떠올려보자. `Quarter` 변형은 `UsState` 값을 포함하고 있다. 만약 쿼터가 아닌 동전의 수를 세면서 동시에 쿼터의 주를 알리고 싶다면, 다음과 같이 `match` 표현식을 사용할 수 있다:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-13-count-and-announce-match/src/main.rs:here}}
```

또는 `if let`과 `else` 표현식을 사용해 다음과 같이 작성할 수도 있다:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-14-count-and-announce-if-let-else/src/main.rs:here}}
```


## `let...else`로 "해피 패스" 유지하기

값이 존재할 때는 특정 계산을 수행하고, 그렇지 않으면 기본값을 반환하는 패턴은 자주 사용된다. `UsState` 값을 가진 동전 예제를 계속 이어가 보자. 쿼터에 새겨진 주의 연령에 따라 재미있는 말을 하고 싶다면, `UsState`에 주의 연령을 확인하는 메서드를 추가할 수 있다.

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:state}}
```

그런 다음 `if let`을 사용해 동전 타입을 매칭하고, 조건문 내부에 `state` 변수를 도입할 수 있다. 이는 Listing 6-7과 같다.

<Listing number="6-7" caption="`if let` 내부에 조건문을 중첩해 1900년에 존재했던 주를 확인하기." file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:describe}}
```

</Listing>

이 방법은 작업을 `if let` 문의 본문으로 밀어넣어 처리하기 때문에, 작업이 복잡해지면 최상위 분기와의 관계를 파악하기 어려워질 수 있다. 또한 표현식이 값을 생성한다는 사실을 활용해 `if let`에서 `state`를 생성하거나 조기에 반환할 수도 있다. 이는 Listing 6-8과 같다. (`match`를 사용해 비슷한 작업을 수행할 수도 있다.)

<Listing number="6-8" caption="값을 생성하거나 조기에 반환하기 위해 `if let` 사용하기." file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-08/src/main.rs:describe}}
```

</Listing>

하지만 이 방법도 따르기에는 조금 번거롭다! `if let`의 한 분기는 값을 생성하고, 다른 분기는 함수 전체에서 반환한다.

이런 일반적인 패턴을 더 깔끔하게 표현하기 위해 Rust는 `let...else`를 제공한다. `let...else` 구문은 `if let`과 매우 유사하게 왼쪽에 패턴을, 오른쪽에 표현식을 받지만, `if` 분기는 없고 `else` 분기만 있다. 패턴이 매칭되면 패턴에서 값을 외부 스코프에 바인딩한다. 패턴이 매칭되지 않으면 프로그램은 `else` 분기로 흐르며, 이 분기에서는 반드시 함수에서 반환해야 한다.

Listing 6-9에서는 `if let` 대신 `let...else`를 사용해 Listing 6-8을 어떻게 표현하는지 확인할 수 있다. 이 방식은 함수의 주요 본문에서 "해피 패스"를 유지하며, `if let`처럼 두 분기 간에 크게 다른 제어 흐름을 만들지 않는다.

<Listing number="6-9" caption="함수의 흐름을 명확히 하기 위해 `let...else` 사용하기." file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-09/src/main.rs:describe}}
```

</Listing>

만약 `match`로 표현하기에는 너무 장황한 로직이 있다면, `if let`과 `let...else`가 Rust 도구 상자에 있다는 것을 기억하라.


## 요약

지금까지 열거형(enum)을 사용해 특정 값들 중 하나를 선택할 수 있는 커스텀 타입을 만드는 방법을 알아보았다. 또한 표준 라이브러리의 `Option<T>` 타입이 어떻게 타입 시스템을 활용해 에러를 방지하는지 살펴보았다. 열거형 값 안에 데이터가 포함된 경우, `match`나 `if let`을 사용해 해당 값을 추출하고 활용할 수 있다. 이때 처리해야 하는 케이스의 수에 따라 적절한 방법을 선택하면 된다.

이제 여러분의 Rust 프로그램은 구조체(struct)와 열거형을 통해 도메인 개념을 표현할 수 있다. API에서 사용할 커스텀 타입을 만들면 타입 안전성을 보장할 수 있다. 컴파일러가 각 함수가 기대하는 타입의 값만 전달되도록 확인해 주기 때문이다.

사용자에게 잘 정리된 API를 제공하고, 사용하기 간편하며, 사용자가 필요한 기능만 정확히 노출하려면 이제 Rust의 모듈 시스템을 살펴볼 차례다.


