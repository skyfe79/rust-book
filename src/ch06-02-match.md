<!-- 이전 헤더. 제거하지 마세요. 링크가 깨질 수 있습니다. -->

<a id="the-match-control-flow-operator"></a>


## `match` 제어 흐름 구조

Rust는 `match`라는 매우 강력한 제어 흐름 구조를 제공한다. `match`는 값을 일련의 패턴과 비교한 후, 어떤 패턴이 일치하는지에 따라 코드를 실행한다. 패턴은 리터럴 값, 변수명, 와일드카드 등 다양한 요소로 구성될 수 있다. [19장][ch19-00-patterns]에서는 모든 종류의 패턴과 그 기능에 대해 다룬다. `match`의 강점은 패턴의 표현력과 컴파일러가 모든 가능한 경우를 처리하도록 보장한다는 점이다.

`match` 표현식을 동전 분류기로 생각해보자. 동전은 다양한 크기의 구멍이 있는 트랙을 따라 미끄러지며, 동전이 맞는 첫 번째 구멍으로 떨어진다. 마찬가지로 `match`에서 값은 각 패턴을 거치며, 값이 '맞는' 첫 번째 패턴에 도달하면 해당 코드 블록으로 들어가 실행된다.

동전을 예로 들어 `match`를 사용해보자. 알 수 없는 미국 동전을 받아 동전 분류기와 비슷한 방식으로 동전의 종류를 판별하고 센트 단위로 값을 반환하는 함수를 작성할 수 있다. Listing 6-3에서 이를 확인할 수 있다.

<Listing number="6-3" caption="열거형과 그 열거형의 변형을 패턴으로 사용하는 `match` 표현식">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-03/src/main.rs:here}}
```

</Listing>

`value_in_cents` 함수의 `match`를 자세히 살펴보자. 먼저 `match` 키워드를 작성한 후 표현식을 나열한다. 여기서는 `coin` 값이 해당한다. 이는 `if`와 함께 사용되는 조건문과 매우 유사해 보이지만, 큰 차이가 있다. `if`의 조건은 불리언 값으로 평가되어야 하지만, `match`는 어떤 타입이든 가능하다. 이 예제에서 `coin`의 타입은 첫 줄에서 정의한 `Coin` 열거형이다.

다음은 `match`의 각 가지(arm)이다. 각 가지는 패턴과 코드 두 부분으로 구성된다. 첫 번째 가지는 `Coin::Penny` 값을 패턴으로 사용하며, `=>` 연산자를 통해 패턴과 실행할 코드를 구분한다. 여기서 코드는 단순히 `1` 값이다. 각 가지는 쉼표로 구분된다.

`match` 표현식이 실행되면, 결과 값을 각 가지의 패턴과 순서대로 비교한다. 패턴이 값과 일치하면 해당 패턴과 연결된 코드가 실행된다. 패턴이 값과 일치하지 않으면 다음 가지로 실행이 계속된다. 동전 분류기와 마찬가지로 필요한 만큼 가지를 추가할 수 있다. Listing 6-3에서는 네 개의 가지가 있다.

각 가지의 코드는 표현식이며, 일치하는 가지의 표현식 결과 값이 전체 `match` 표현식의 반환 값이 된다.

일반적으로 짧은 코드의 경우 중괄호를 사용하지 않는다. Listing 6-3에서 각 가지는 단순히 값을 반환한다. 만약 한 가지에서 여러 줄의 코드를 실행하고 싶다면 중괄호를 사용해야 하며, 이 경우 가지 뒤의 쉼표는 선택 사항이다. 예를 들어, 다음 코드는 `Coin::Penny`로 메서드가 호출될 때마다 "Lucky penny!"를 출력하지만, 여전히 블록의 마지막 값인 `1`을 반환한다:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-08-match-arm-multiple-lines/src/main.rs:here}}
```


### 값에 바인딩하는 패턴

매치 갈래의 또 다른 유용한 기능은 패턴과 일치하는 값의 일부에 바인딩할 수 있다는 점이다. 이를 통해 열거형(enum) 변형에서 값을 추출할 수 있다.

예를 들어, 열거형의 변형 중 하나를 내부에 데이터를 포함하도록 변경해보자. 1999년부터 2008년까지 미국에서는 각 주마다 다른 디자인을 가진 쿼터 동전을 발행했다. 다른 동전에는 주 디자인이 없기 때문에, 쿼터만이 이 추가 값을 가진다. `Quarter` 변형을 `UsState` 값을 포함하도록 변경하면 이 정보를 열거형에 추가할 수 있다. 이를 [Listing 6-4](#listing-6-4)에서 구현했다.

<Listing number="6-4" caption="`Quarter` 변형이 `UsState` 값을 포함하는 `Coin` 열거형">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-04/src/main.rs:here}}
```

</Listing>

친구가 50개 주의 쿼터를 모두 수집하려 한다고 상상해보자. 동전 종류별로 잔돈을 정리하면서, 각 쿼터와 관련된 주의 이름도 함께 알려주면 친구가 아직 가지고 있지 않은 쿼터를 수집할 수 있다.

이 코드의 매치 표현식에서, `Coin::Quarter` 변형과 일치하는 패턴에 `state`라는 변수를 추가한다. `Coin::Quarter`가 매치되면, `state` 변수는 해당 쿼터의 주 값에 바인딩된다. 그런 다음 이 갈래의 코드에서 `state`를 사용할 수 있다.

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-09-variable-in-pattern/src/main.rs:here}}
```

`value_in_cents(Coin::Quarter(UsState::Alaska))`를 호출하면, `coin`은 `Coin::Quarter(UsState::Alaska)`가 된다. 이 값을 각 매치 갈래와 비교할 때, `Coin::Quarter(state)`에 도달할 때까지 아무것도 일치하지 않는다. 그 시점에서 `state`의 바인딩은 `UsState::Alaska` 값이 된다. 이 바인딩을 `println!` 표현식에서 사용하여, `Quarter` 열거형 변형에서 내부의 주 값을 추출할 수 있다.


### `Option<T>`와 매칭하기

이전 섹션에서 `Option<T>`를 사용할 때 `Some` 케이스 안에 있는 `T` 값을 꺼내고 싶었다. `Coin` 열거형에서 했던 것처럼 `match`를 사용해 `Option<T>`를 처리할 수도 있다. 동전을 비교하는 대신 `Option<T>`의 변형을 비교하지만, `match` 표현식의 동작 방식은 동일하다.

예를 들어, `Option<i32>`를 받아서 안에 값이 있으면 그 값에 1을 더하는 함수를 작성하고 싶다고 해보자. 만약 값이 없다면, 함수는 `None`을 반환하고 어떤 연산도 시도하지 않아야 한다.

이 함수는 `match` 덕분에 매우 쉽게 작성할 수 있으며, Listing 6-5와 같다.

<Listing number="6-5" caption="`Option<i32>`에 `match` 표현식을 사용하는 함수">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:here}}
```

</Listing>

`plus_one` 함수의 첫 번째 실행을 자세히 살펴보자. `plus_one(five)`를 호출하면, `plus_one` 함수 본문의 변수 `x`는 `Some(5)` 값을 갖게 된다. 그런 다음 이 값을 각 `match` 갈래와 비교한다:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

`Some(5)` 값은 `None` 패턴과 일치하지 않으므로 다음 갈래로 넘어간다:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:second_arm}}
```

`Some(5)`가 `Some(i)`와 일치하는가? 일치한다! 동일한 변형이다. `i`는 `Some` 안에 있는 값에 바인딩되므로, `i`는 값 `5`를 갖는다. 그런 다음 `match` 갈래의 코드가 실행되어, `i` 값에 1을 더하고 결과값 `6`을 포함한 새로운 `Some` 값을 생성한다.

이제 Listing 6-5에서 `plus_one`의 두 번째 호출을 고려해보자. 여기서 `x`는 `None`이다. `match`에 들어가서 첫 번째 갈래와 비교한다:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

일치한다! 더할 값이 없으므로, 프로그램은 멈추고 `=>` 오른쪽의 `None` 값을 반환한다. 첫 번째 갈래가 일치했기 때문에 다른 갈래는 비교하지 않는다.

`match`와 열거형을 결합하는 것은 다양한 상황에서 유용하다. Rust 코드에서 이 패턴을 자주 보게 될 것이다: 열거형에 대해 `match`를 수행하고, 안에 있는 데이터에 변수를 바인딩한 다음, 이를 기반으로 코드를 실행한다. 처음에는 약간 까다로울 수 있지만, 익숙해지면 모든 언어에서 이 기능을 갖고 싶어질 것이다. 이는 꾸준히 사용자들이 좋아하는 기능 중 하나다.


### 모든 경우를 다뤄야 하는 `match`의 특징

`match`에 대해 다뤄야 할 또 다른 특징이 있다. 바로 모든 가능한 경우를 다뤄야 한다는 점이다. 아래는 버그가 있고 컴파일되지 않는 `plus_one` 함수의 예제다:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/src/main.rs:here}}
```

이 코드는 `None` 케이스를 처리하지 않았기 때문에 버그를 일으킨다. 다행히도, 러스트는 이런 버그를 잡아낼 수 있다. 이 코드를 컴파일하려고 하면 다음과 같은 에러가 발생한다:

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/output.txt}}
```

러스트는 모든 가능한 케이스를 다루지 않았다는 것을 알고 있으며, 심지어 어떤 패턴을 빠뜨렸는지도 정확히 알고 있다! 러스트의 `match`는 **모든 경우를 다뤄야 한다(exhaustive)**. 즉, 코드가 유효하려면 모든 가능성을 다뤄야 한다. 특히 `Option<T>`의 경우, 러스트는 `None` 케이스를 명시적으로 처리하지 않으면 이를 막아준다. 이는 우리가 값이 있을 것이라고 가정했을 때 실제로는 `null`이 있을 수 있는 상황을 방지해주며, 이전에 언급했던 '10억 달러짜리 실수'를 불가능하게 만든다.


### 모든 경우를 포괄하는 패턴과 `_` 플레이스홀더

열거형을 사용하면 특정 값에 대해 특별한 동작을 정의하고, 나머지 모든 값에 대해 기본 동작을 지정할 수 있다. 예를 들어, 주사위를 굴려 3이 나오면 플레이어가 움직이지 않고 멋진 모자를 얻는 게임을 구현한다고 가정해보자. 7이 나오면 플레이어가 모자를 잃는다. 나머지 숫자가 나오면 플레이어는 해당 숫자만큼 게임 보드에서 이동한다. 다음은 이 로직을 구현한 `match` 표현식이다. 주사위 결과는 랜덤 값이 아닌 하드코딩되었고, 나머지 로직은 실제 구현을 생략한 함수로 표현했다:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-15-binding-catchall/src/main.rs:here}}
```

처음 두 가지 `arm`은 리터럴 값 `3`과 `7`에 해당한다. 나머지 모든 가능한 값을 포괄하는 마지막 `arm`은 `other`라는 변수로 패턴을 정의한다. `other` `arm`에 해당하는 코드는 이 변수를 `move_player` 함수에 전달하여 사용한다.

이 코드는 `u8` 타입이 가질 수 있는 모든 값을 나열하지 않았음에도 컴파일된다. 마지막 패턴이 명시적으로 나열되지 않은 모든 값을 매칭하기 때문이다. 이 모든 경우를 포괄하는 패턴은 `match`가 모든 가능성을 다뤄야 한다는 요구 사항을 충족한다. 모든 경우를 포괄하는 `arm`은 반드시 마지막에 위치해야 한다는 점에 주의하자. 패턴은 순서대로 평가되기 때문에, 모든 경우를 포괄하는 `arm`을 앞에 두면 다른 `arm`은 절대 실행되지 않는다. 따라서 Rust는 모든 경우를 포괄하는 `arm` 뒤에 다른 `arm`을 추가하면 경고를 표시한다.

Rust는 모든 경우를 포괄하지만 해당 값을 사용하지 않을 때 사용할 수 있는 특별한 패턴도 제공한다. `_`는 어떤 값이든 매칭하지만 그 값에 바인딩하지 않는 패턴이다. 이 패턴은 해당 값을 사용하지 않을 것임을 Rust에게 알려주므로, 사용하지 않는 변수에 대한 경고를 피할 수 있다.

이제 게임 규칙을 변경해보자. 이제 3이나 7이 아닌 값이 나오면 다시 주사위를 굴려야 한다. 모든 경우를 포괄하는 값을 사용할 필요가 없으므로, `other` 변수 대신 `_`를 사용하도록 코드를 수정할 수 있다:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-16-underscore-catchall/src/main.rs:here}}
```

이 예제도 마지막 `arm`에서 나머지 모든 값을 명시적으로 무시하므로, 모든 가능성을 다뤘다는 요구 사항을 충족한다.

마지막으로 게임 규칙을 한 번 더 변경해보자. 이제 3이나 7이 아닌 값이 나오면 아무 일도 일어나지 않는다. 이를 표현하기 위해 `_` `arm`에 단위 값(빈 튜플 타입)을 사용할 수 있다:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-17-underscore-unit/src/main.rs:here}}
```

여기서는 이전 `arm`에서 매칭되지 않은 다른 값을 사용하지 않을 것이며, 이 경우 어떤 코드도 실행하지 않을 것임을 Rust에게 명시적으로 알린다.

패턴과 매칭에 대해 더 자세한 내용은 [19장][ch19-00-patterns]에서 다룬다. 지금은 `match` 표현식이 다소 장황할 때 유용한 `if let` 문법으로 넘어가보자.

[tuples]: ch03-02-data-types.html#the-tuple-type
[ch19-00-patterns]: ch19-00-patterns.html


