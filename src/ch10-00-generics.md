# 제네릭 타입, 트레이트, 그리고 라이프타임

모든 프로그래밍 언어는 개념의 중복을 효과적으로 처리하기 위한 도구를 제공한다. Rust에서는 _제네릭_이 그런 도구 중 하나다. 제네릭은 구체적인 타입이나 속성의 추상적인 대체물이다. 코드를 컴파일하고 실행할 때 어떤 값이 들어갈지 알지 못해도, 제네릭의 동작이나 다른 제네릭과의 관계를 표현할 수 있다.

함수는 `i32`나 `String` 같은 구체적인 타입 대신 제네릭 타입의 매개변수를 받을 수 있다. 이는 여러 구체적인 값에 대해 동일한 코드를 실행하기 위해 알려지지 않은 값을 매개변수로 받는 방식과 유사하다. 사실, 우리는 이미 제네릭을 사용해 왔다. 6장의 `Option<T>`, 8장의 `Vec<T>`와 `HashMap<K, V>`, 그리고 9장의 `Result<T, E>`가 그 예시다. 이 장에서는 제네릭을 사용해 자신만의 타입, 함수, 메서드를 정의하는 방법을 알아볼 것이다.

먼저, 코드 중복을 줄이기 위해 함수를 추출하는 방법을 복습한다. 그런 다음, 매개변수의 타입만 다른 두 함수에서 제네릭 함수를 만드는 동일한 기법을 사용한다. 또한 구조체와 열거형 정의에서 제네릭 타입을 사용하는 방법도 설명한다.

그 다음, _트레이트_를 사용해 동작을 제네릭 방식으로 정의하는 방법을 배운다. 트레이트와 제네릭 타입을 결합하면, 모든 타입이 아닌 특정 동작을 가진 타입만 허용하도록 제네릭 타입을 제한할 수 있다.

마지막으로, _라이프타임_에 대해 논의한다. 라이프타임은 참조가 서로 어떻게 관련되는지 컴파일러에게 알려주는 일종의 제네릭이다. 라이프타임을 통해 빌린 값에 대한 충분한 정보를 컴파일러에게 제공하면, 우리의 도움 없이도 더 많은 상황에서 참조가 유효할 수 있도록 보장할 수 있다.


## 중복 코드 제거를 위한 함수 추출

제네릭은 특정 타입을 여러 타입을 대표하는 플레이스홀더로 대체해 코드 중복을 제거할 수 있게 해준다. 제네릭 문법을 살펴보기 전에, 먼저 제네릭 타입을 사용하지 않고 중복 코드를 제거하는 방법을 알아보자. 특정 값을 여러 값을 대표하는 플레이스홀더로 대체하는 함수를 추출하는 방식이다. 그런 다음 동일한 기법을 적용해 제네릭 함수를 추출할 것이다. 함수로 추출할 수 있는 중복 코드를 어떻게 인식하는지 살펴보면, 제네릭을 사용할 수 있는 중복 코드도 자연스럽게 인식할 수 있게 될 것이다.

먼저 리스트에서 가장 큰 숫자를 찾는 짧은 프로그램부터 시작해보자. 아래는 리스트에서 가장 큰 숫자를 찾는 코드이다.

<Listing number="10-1" file-name="src/main.rs" caption="숫자 리스트에서 가장 큰 숫자 찾기">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-01/src/main.rs:here}}
```

</Listing>

`number_list` 변수에 정수 리스트를 저장하고, `largest` 변수에는 리스트의 첫 번째 숫자를 참조로 저장한다. 그런 다음 리스트의 모든 숫자를 순회하며, 현재 숫자가 `largest`에 저장된 숫자보다 크면 해당 변수의 참조를 교체한다. 현재 숫자가 지금까지 본 가장 큰 숫자보다 작거나 같으면 변수는 변경되지 않고 코드는 리스트의 다음 숫자로 이동한다. 리스트의 모든 숫자를 확인한 후, `largest`는 가장 큰 숫자를 참조하게 되며, 이 경우에는 100이 된다.

이제 두 개의 다른 숫자 리스트에서 가장 큰 숫자를 찾는 작업을 해야 한다. 이를 위해 Listing 10-1의 코드를 복제하고 프로그램의 두 곳에서 동일한 로직을 사용할 수 있다. 아래는 두 리스트에서 가장 큰 숫자를 찾는 코드이다.

<Listing number="10-2" file-name="src/main.rs" caption="*두* 리스트에서 가장 큰 숫자를 찾는 코드">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-02/src/main.rs}}
```

</Listing>

이 코드는 동작하지만, 코드를 복제하는 것은 번거롭고 오류가 발생하기 쉽다. 또한 코드를 변경할 때 여러 곳에서 동시에 업데이트해야 한다는 점도 잊지 말아야 한다.

이 중복을 제거하기 위해, 정수 리스트를 매개변수로 받아 처리하는 함수를 정의해 추상화를 만들어보자. 이 방법은 코드를 더 명확하게 만들고, 리스트에서 가장 큰 숫자를 찾는 개념을 추상적으로 표현할 수 있게 해준다.

Listing 10-3에서는 가장 큰 숫자를 찾는 코드를 `largest`라는 함수로 추출한다. 그런 다음 Listing 10-2의 두 리스트에서 가장 큰 숫자를 찾기 위해 이 함수를 호출한다. 이 함수는 앞으로 사용할 수 있는 다른 `i32` 값 리스트에도 사용할 수 있다.

<Listing number="10-3" file-name="src/main.rs" caption="두 리스트에서 가장 큰 숫자를 찾기 위한 추상화된 코드">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-03/src/main.rs:here}}
```

</Listing>

`largest` 함수는 `list`라는 매개변수를 가지며, 이는 함수에 전달할 수 있는 `i32` 값의 구체적인 슬라이스를 나타낸다. 결과적으로 함수를 호출할 때, 코드는 전달한 특정 값에 대해 실행된다.

요약하면, Listing 10-2의 코드를 Listing 10-3으로 변경하기 위해 다음과 같은 단계를 거쳤다:

1. 중복 코드를 식별한다.
1. 중복 코드를 함수 본문으로 추출하고, 함수 시그니처에서 해당 코드의 입력과 반환 값을 명시한다.
1. 중복 코드의 두 인스턴스를 함수 호출로 업데이트한다.

다음으로, 이와 동일한 단계를 제네릭에 적용해 코드 중복을 줄여보자. 함수 본문이 특정 값 대신 추상적인 `list`에서 동작할 수 있는 것처럼, 제네릭은 코드가 추상적인 타입에서 동작할 수 있게 해준다.

예를 들어, `i32` 값 슬라이스에서 가장 큰 항목을 찾는 함수와 `char` 값 슬라이스에서 가장 큰 항목을 찾는 함수가 있다고 가정해보자. 이 중복을 어떻게 제거할 수 있을까? 함께 알아보자!


