<!-- Old heading. Do not remove or links may break. -->

<a id="closures-anonymous-functions-that-can-capture-their-environment"></a>


## 클로저: 환경을 캡처하는 익명 함수

Rust의 클로저는 변수에 저장하거나 다른 함수에 인자로 전달할 수 있는 익명 함수다. 한 곳에서 클로저를 생성한 후, 다른 컨텍스트에서 이를 호출해 실행할 수 있다. 일반 함수와 달리 클로저는 정의된 스코프의 값을 캡처할 수 있다. 이번 장에서는 클로저의 이러한 특징이 어떻게 코드 재사용과 동작 커스터마이징을 가능하게 하는지 살펴본다.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-an-abstraction-of-behavior-with-closures"></a>
<a id="refactoring-using-functions"></a>
<a id="refactoring-with-closures-to-store-code"></a>


### 클로저로 환경 캡처하기

먼저 클로저를 사용해 정의된 환경의 값을 나중에 사용할 수 있도록 캡처하는 방법을 살펴본다. 다음 시나리오를 생각해 보자: 티셔츠 회사는 가끔씩 프로모션으로 메일링 리스트에 있는 사람들에게 한정판 티셔츠를 무료로 제공한다. 메일링 리스트에 있는 사람들은 프로필에 좋아하는 색상을 선택적으로 추가할 수 있다. 무료 티셔츠를 받을 사람이 좋아하는 색상을 설정했다면, 그 색상의 티셔츠를 받는다. 만약 좋아하는 색상을 지정하지 않았다면, 회사에 현재 가장 많이 남아 있는 색상의 티셔츠를 받게 된다.

이를 구현하는 방법은 다양하다. 이 예제에서는 간단히 하기 위해 `ShirtColor`라는 열거형을 사용하며, `Red`와 `Blue` 두 가지 색상만 사용한다. 회사의 재고를 나타내기 위해 `Inventory`라는 구조체를 정의한다. 이 구조체에는 현재 재고 상태를 나타내는 `shirts` 필드가 있으며, 이 필드는 `Vec<ShirtColor>` 타입으로 티셔츠 색상을 저장한다. `Inventory`에 정의된 `giveaway` 메서드는 무료 티셔츠 수령자의 선호 색상 정보를 받아, 그 사람이 받을 티셔츠 색상을 반환한다. 이 설정은 리스트 13-1에 나와 있다:

<Listing number="13-1" file-name="src/main.rs" caption="티셔츠 회사의 프로모션 상황">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-01/src/main.rs}}
```

</Listing>

`main` 함수에서 정의된 `store`는 이 한정판 프로모션을 위해 남아 있는 두 개의 파란색 티셔츠와 하나의 빨간색 티셔츠를 가지고 있다. 빨간색 티셔츠를 선호하는 사용자와 선호 색상이 없는 사용자에 대해 `giveaway` 메서드를 호출한다.

이 코드는 다양한 방식으로 구현할 수 있지만, 여기서는 클로저에 초점을 맞추기 위해 이미 배운 개념만을 사용한다. 단, `giveaway` 메서드의 본문은 클로저를 사용한다. `giveaway` 메서드에서는 사용자 선호 색상을 `Option<ShirtColor>` 타입의 매개변수로 받고, `user_preference`에 대해 `unwrap_or_else` 메서드를 호출한다. 표준 라이브러리에 정의된 [`Option<T>`의 `unwrap_or_else` 메서드][unwrap-or-else]<!-- ignore -->는 하나의 인수를 받는다: 이 인수는 아무런 인수를 받지 않고 `T` 타입의 값을 반환하는 클로저이다. (여기서 `T`는 `Option<T>`의 `Some` 변형에 저장된 타입과 동일한 `ShirtColor`이다.) `Option<T>`가 `Some` 변형이라면, `unwrap_or_else`는 `Some` 내부의 값을 반환한다. `Option<T>`가 `None` 변형이라면, `unwrap_or_else`는 클로저를 호출하고 클로저가 반환한 값을 반환한다.

`unwrap_or_else`의 인수로 클로저 표현식 `|| self.most_stocked()`를 지정한다. 이 클로저는 매개변수를 받지 않는다. (만약 클로저가 매개변수를 받는다면, 두 개의 수직 막대 사이에 나타난다.) 클로저의 본문은 `self.most_stocked()`를 호출한다. 여기서 클로저를 정의하고, `unwrap_or_else`의 구현은 필요할 때 클로저를 평가한다.

이 코드를 실행하면 다음과 같은 결과가 출력된다:

```console
{{#include ../listings/ch13-functional-features/listing-13-01/output.txt}}
```

여기서 흥미로운 점은 현재 `Inventory` 인스턴스에서 `self.most_stocked()`를 호출하는 클로저를 전달했다는 것이다. 표준 라이브러리는 우리가 정의한 `Inventory`나 `ShirtColor` 타입, 또는 이 시나리오에서 사용하려는 로직에 대해 아무것도 알 필요가 없다. 클로저는 `self` `Inventory` 인스턴스에 대한 불변 참조를 캡처하고, 우리가 지정한 코드와 함께 `unwrap_or_else` 메서드에 전달한다. 반면, 함수는 이런 방식으로 환경을 캡처할 수 없다.


### 클로저 타입 추론과 타입 명시

함수와 클로저 사이에는 몇 가지 차이점이 더 있다. 클로저는 일반적으로 `fn` 함수처럼 매개변수나 반환 값의 타입을 명시할 필요가 없다. 함수의 경우 타입 명시가 필수인데, 이는 타입이 사용자에게 노출되는 명시적 인터페이스의 일부이기 때문이다. 이러한 인터페이스를 엄격하게 정의하는 것은 함수가 어떤 타입의 값을 사용하고 반환하는지에 대해 모두가 동의할 수 있도록 보장하는 데 중요하다. 반면 클로저는 이렇게 노출된 인터페이스에서 사용되지 않는다. 클로저는 변수에 저장되며, 이름을 붙이지 않고 라이브러리 사용자에게 노출하지 않은 채로 사용된다.

클로저는 일반적으로 짧고 특정한 맥락에서만 관련이 있으며, 임의의 시나리오에서 사용되지 않는다. 이러한 제한된 맥락에서 컴파일러는 매개변수와 반환 타입을 추론할 수 있다. 이는 컴파일러가 대부분의 변수 타입을 추론할 수 있는 것과 유사하다(드물게 클로저 타입 명시가 필요한 경우도 있긴 하다).

변수와 마찬가지로, 명시성과 명확성을 높이기 위해 타입을 명시할 수도 있다. 다만 이 경우 불필요하게 장황해질 수 있다. 클로저의 타입을 명시하는 방법은 Listing 13-2에서 볼 수 있다. 이 예제에서는 클로저를 정의하고 변수에 저장한다. Listing 13-1에서처럼 클로저를 인자로 전달하는 즉시 정의하지 않는다.

<Listing number="13-2" file-name="src/main.rs" caption="클로저의 매개변수와 반환 값 타입을 선택적으로 명시">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-02/src/main.rs:here}}
```

</Listing>

타입 명시를 추가하면 클로저의 문법이 함수 문법과 더 유사해진다. 여기서는 매개변수에 1을 더하는 함수와 동일한 동작을 하는 클로저를 정의하여 비교한다. 관련 부분을 정렬하기 위해 공백을 추가했다. 이 예제는 클로저 문법이 파이프(|)를 사용하고 선택적 문법이 많다는 점을 제외하면 함수 문법과 유사하다는 것을 보여준다:

```rust,ignore
fn  add_one_v1   (x: u32) -> u32 { x + 1 }
let add_one_v2 = |x: u32| -> u32 { x + 1 };
let add_one_v3 = |x|             { x + 1 };
let add_one_v4 = |x|               x + 1  ;
```

첫 번째 줄은 함수 정의를 보여주고, 두 번째 줄은 타입이 완전히 명시된 클로저 정의를 보여준다. 세 번째 줄에서는 클로저 정의에서 타입 명시를 제거했다. 네 번째 줄에서는 클로저 본문이 단일 표현식이므로 선택적인 중괄호를 제거했다. 이 모든 정의는 호출 시 동일한 동작을 생성하는 유효한 정의들이다. `add_one_v3`와 `add_one_v4` 줄은 클로저가 평가되어야 컴파일할 수 있는데, 이는 타입이 사용법에서 추론되기 때문이다. 이는 `let v = Vec::new();`가 타입 명시나 특정 타입의 값을 `Vec`에 삽입해야 Rust가 타입을 추론할 수 있는 것과 유사하다.

클로저 정의의 경우 컴파일러는 각 매개변수와 반환 값에 대해 하나의 구체적인 타입을 추론한다. 예를 들어, Listing 13-3은 매개변수로 받은 값을 그대로 반환하는 짧은 클로저의 정의를 보여준다. 이 클로저는 예제를 위한 목적 외에는 그다지 유용하지 않다. 정의에 어떤 타입 명시도 추가하지 않았음을 주목하라. 타입 명시가 없기 때문에 클로저를 어떤 타입으로도 호출할 수 있다. 여기서는 처음에 `String`으로 호출했다. 그런 다음 `example_closure`를 정수로 호출하려고 하면 오류가 발생한다.

<Listing number="13-3" file-name="src/main.rs" caption="추론된 타입의 클로저를 두 가지 다른 타입으로 호출하려고 시도">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-03/src/main.rs:here}}
```

</Listing>

컴파일러는 다음과 같은 오류를 발생시킨다:

```console
{{#include ../listings/ch13-functional-features/listing-13-03/output.txt}}
```

`String` 값으로 `example_closure`를 처음 호출할 때 컴파일러는 `x`의 타입과 클로저의 반환 타입을 `String`으로 추론한다. 이 타입은 `example_closure`의 클로저에 고정되며, 이후 동일한 클로저를 다른 타입으로 사용하려고 하면 타입 오류가 발생한다.


### 참조 캡처와 소유권 이동

클로저는 환경에서 값을 캡처하는 세 가지 방법을 사용할 수 있다. 이는 함수가 매개변수를 받는 세 가지 방식과 직접적으로 대응한다: 불변 참조, 가변 참조, 그리고 소유권 가져오기. 클로저는 캡처한 값을 함수 본문에서 어떻게 사용하는지에 따라 이 중 어떤 방식을 사용할지 결정한다.

리스트 13-4에서는 `list`라는 벡터에 대한 불변 참조를 캡처하는 클로저를 정의한다. 이는 단순히 값을 출력하기 위해 불변 참조만 필요하기 때문이다.

<Listing number="13-4" file-name="src/main.rs" caption="불변 참조를 캡처하는 클로저 정의 및 호출">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-04/src/main.rs}}
```

</Listing>

이 예제는 변수가 클로저 정의에 바인딩될 수 있고, 나중에 변수 이름과 괄호를 사용해 함수 이름처럼 클로저를 호출할 수 있음을 보여준다.

`list`에 대한 불변 참조를 동시에 여러 개 가질 수 있기 때문에, 클로저 정의 전, 클로저 정의 후 호출 전, 그리고 클로저 호출 후에도 `list`는 여전히 접근 가능하다. 이 코드는 컴파일되고 실행되며 다음과 같이 출력된다.

```console
{{#include ../listings/ch13-functional-features/listing-13-04/output.txt}}
```

다음으로, 리스트 13-5에서는 클로저 본문을 변경해 `list` 벡터에 요소를 추가한다. 이제 클로저는 가변 참조를 캡처한다.

<Listing number="13-5" file-name="src/main.rs" caption="가변 참조를 캡처하는 클로저 정의 및 호출">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-05/src/main.rs}}
```

</Listing>

이 코드는 컴파일되고 실행되며 다음과 같이 출력된다.

```console
{{#include ../listings/ch13-functional-features/listing-13-05/output.txt}}
```

`borrows_mutably` 클로저의 정의와 호출 사이에 더 이상 `println!`이 없음을 주목하라. `borrows_mutably`가 정의될 때, `list`에 대한 가변 참조를 캡처한다. 클로저를 호출한 후에는 다시 사용하지 않으므로 가변 참조는 종료된다. 클로저 정의와 호출 사이에 불변 참조를 사용해 출력하는 것은 허용되지 않는다. 가변 참조가 있는 동안에는 다른 참조가 허용되지 않기 때문이다. 여기에 `println!`을 추가해 어떤 에러 메시지가 나오는지 확인해 보라!

클로저 본문이 엄밀히 소유권을 필요로 하지 않더라도, 클로저가 환경에서 사용하는 값의 소유권을 강제로 가져오게 하려면 매개변수 목록 앞에 `move` 키워드를 사용할 수 있다.

이 기법은 주로 클로저를 새로운 스레드에 전달해 데이터를 이동시켜 새로운 스레드가 소유하도록 할 때 유용하다. 스레드와 이를 사용해야 하는 이유에 대해서는 16장에서 동시성을 다룰 때 자세히 설명하겠지만, 지금은 `move` 키워드가 필요한 클로저를 사용해 새로운 스레드를 생성하는 방법을 간단히 살펴보자. 리스트 13-6은 리스트 13-4를 수정해 벡터를 메인 스레드가 아닌 새로운 스레드에서 출력하도록 한 예제다.

<Listing number="13-6" file-name="src/main.rs" caption="`move`를 사용해 스레드의 클로저가 `list`의 소유권을 가져오도록 강제">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-06/src/main.rs}}
```

</Listing>

새로운 스레드를 생성하고, 스레드에 실행할 클로저를 인자로 전달한다. 클로저 본문은 리스트를 출력한다. 리스트 13-4에서는 클로저가 `list`를 불변 참조로만 캡처했다. 이는 `list`를 출력하는 데 필요한 최소한의 접근이기 때문이다. 이 예제에서는 클로저 본문이 여전히 불변 참조만 필요하지만, `list`가 클로저로 이동되어야 함을 나타내기 위해 클로저 정의 시작 부분에 `move` 키워드를 추가했다. 새로운 스레드는 메인 스레드의 나머지 부분이 완료되기 전에 끝날 수도 있고, 메인 스레드가 먼저 끝날 수도 있다. 만약 메인 스레드가 `list`의 소유권을 유지한 채로 새로운 스레드보다 먼저 종료되어 `list`를 드롭한다면, 스레드의 불변 참조는 무효가 된다. 따라서 컴파일러는 `list`가 새로운 스레드에 전달된 클로저로 이동되어야 함을 요구한다. `move` 키워드를 제거하거나 클로저 정의 후 메인 스레드에서 `list`를 사용해 어떤 컴파일러 에러가 발생하는지 확인해 보라!

<!-- Old headings. Do not remove or links may break. -->

<a id="storing-closures-using-generic-parameters-and-the-fn-traits"></a>
<a id="limitations-of-the-cacher-implementation"></a>
<a id="moving-captured-values-out-of-the-closure-and-the-fn-traits"></a>


### 클로저에서 캡처한 값을 이동시키기와 `Fn` 트레이트

클로저가 정의된 환경에서 값을 참조로 캡처하거나 소유권을 캡처하면, 클로저가 평가될 때 이 참조나 값에 어떤 일이 발생할지는 클로저 본문의 코드가 결정한다. 클로저 본문은 캡처한 값을 클로저 밖으로 이동시키거나, 캡처한 값을 변경하거나, 값을 이동시키거나 변경하지 않거나, 아무것도 캡처하지 않을 수 있다.

클로저가 환경에서 값을 캡처하고 처리하는 방식은 클로저가 구현하는 트레이트에 영향을 미친다. 트레이트는 함수와 구조체가 어떤 종류의 클로저를 사용할 수 있는지 지정하는 방법이다. 클로저는 본문이 값을 어떻게 처리하는지에 따라 `Fn` 트레이트 중 하나, 둘, 혹은 모두를 자동으로 구현한다.

1. `FnOnce`는 한 번만 호출할 수 있는 클로저에 적용된다. 모든 클로저는 최소한 이 트레이트를 구현한다. 캡처한 값을 본문 밖으로 이동시키는 클로저는 `FnOnce`만 구현하고 다른 `Fn` 트레이트는 구현하지 않는다. 이 클로저는 한 번만 호출할 수 있다.
2. `FnMut`는 캡처한 값을 본문 밖으로 이동시키지는 않지만, 캡처한 값을 변경할 수 있는 클로저에 적용된다. 이 클로저는 여러 번 호출할 수 있다.
3. `Fn`은 캡처한 값을 본문 밖으로 이동시키지 않고, 캡처한 값을 변경하지 않으며, 환경에서 아무것도 캡처하지 않는 클로저에 적용된다. 이 클로저는 환경을 변경하지 않고 여러 번 호출할 수 있다. 이는 클로저를 동시에 여러 번 호출하는 경우에 중요하다.

`Option<T>`의 `unwrap_or_else` 메서드 정의를 살펴보자:

```rust,ignore
impl<T> Option<T> {
    pub fn unwrap_or_else<F>(self, f: F) -> T
    where
        F: FnOnce() -> T
    {
        match self {
            Some(x) => x,
            None => f(),
        }
    }
}
```

`T`는 `Option`의 `Some` 변형에 있는 값의 타입을 나타내는 제네릭 타입이다. 이 타입 `T`는 `unwrap_or_else` 함수의 반환 타입이기도 하다. 예를 들어, `Option<String>`에서 `unwrap_or_else`를 호출하면 `String`을 얻는다.

`unwrap_or_else` 함수에는 추가적인 제네릭 타입 매개변수 `F`가 있다. `F` 타입은 `f`라는 이름의 매개변수 타입으로, `unwrap_or_else`를 호출할 때 제공하는 클로저이다.

제네릭 타입 `F`에 지정된 트레이트 바운드는 `FnOnce() -> T`이다. 이는 `F`가 한 번 호출될 수 있고, 인수를 받지 않으며, `T`를 반환해야 함을 의미한다. `FnOnce`를 트레이트 바운드로 사용하면 `unwrap_or_else`가 `f`를 최대 한 번만 호출한다는 제약을 표현한다. `unwrap_or_else`의 본문에서 볼 수 있듯이, `Option`이 `Some`이면 `f`가 호출되지 않는다. `Option`이 `None`이면 `f`가 한 번 호출된다. 모든 클로저가 `FnOnce`를 구현하므로, `unwrap_or_else`는 세 가지 종류의 클로저를 모두 허용하고 가능한 한 유연하다.

> 참고: 환경에서 값을 캡처할 필요가 없는 경우, 클로저 대신 함수 이름을 사용할 수 있다. 예를 들어, `Option<Vec<T>>` 값에서 `unwrap_or_else(Vec::new)`를 호출하면 값이 `None`일 때 새로운 빈 벡터를 얻을 수 있다. 컴파일러는 함수 정의에 적용 가능한 `Fn` 트레이트를 자동으로 구현한다.

이제 슬라이스에 정의된 표준 라이브러리 메서드 `sort_by_key`를 살펴보자. 이 메서드가 `unwrap_or_else`와 어떻게 다른지, 그리고 왜 `FnOnce` 대신 `FnMut`를 트레이트 바운드로 사용하는지 알아보자. 클로저는 슬라이스의 현재 항목에 대한 참조 형태로 하나의 인수를 받고, 정렬할 수 있는 타입 `K`의 값을 반환한다. 이 함수는 슬라이스를 각 항목의 특정 속성으로 정렬하고 싶을 때 유용하다. 예제 13-7에서는 `Rectangle` 인스턴스 목록을 `width` 속성으로 낮은 순서부터 높은 순서로 정렬하기 위해 `sort_by_key`를 사용한다:

<Listing number="13-7" file-name="src/main.rs" caption="`sort_by_key`를 사용해 사각형을 너비로 정렬">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-07/src/main.rs}}
```

</Listing>

이 코드는 다음과 같이 출력한다:

```console
{{#include ../listings/ch13-functional-features/listing-13-07/output.txt}}
```

`sort_by_key`가 `FnMut` 클로저를 받도록 정의된 이유는 클로저를 여러 번 호출하기 때문이다: 슬라이스의 각 항목에 대해 한 번씩 호출한다. 클로저 `|r| r.width`는 환경에서 아무것도 캡처하거나 변경하거나 이동시키지 않으므로 트레이트 바운드 요구 사항을 충족한다.

반면, 예제 13-8은 환경에서 값을 이동시키므로 `FnOnce` 트레이트만 구현하는 클로저를 보여준다. 컴파일러는 이 클로저를 `sort_by_key`와 함께 사용할 수 없게 한다:

<Listing number="13-8" file-name="src/main.rs" caption="`sort_by_key`와 함께 `FnOnce` 클로저 사용 시도">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-08/src/main.rs}}
```

</Listing>

이 코드는 `list`를 정렬할 때 `sort_by_key`가 클로저를 몇 번 호출하는지 세려고 하는 복잡하고 인위적인 방법(작동하지 않는)을 보여준다. 이 코드는 클로저의 환경에서 `String`인 `value`를 `sort_operations` 벡터로 푸시하여 이 카운팅을 시도한다. 클로저는 `value`를 캡처한 후 `value`의 소유권을 `sort_operations` 벡터로 이전하여 `value`를 클로저 밖으로 이동시킨다. 이 클로저는 한 번만 호출할 수 있다; 두 번째로 호출하려고 하면 `value`가 더 이상 환경에 없으므로 `sort_operations`에 다시 푸시할 수 없다! 따라서 이 클로저는 `FnOnce`만 구현한다. 이 코드를 컴파일하려고 하면 클로저가 `FnMut`를 구현해야 하므로 `value`를 클로저 밖으로 이동시킬 수 없다는 오류가 발생한다:

```console
{{#include ../listings/ch13-functional-features/listing-13-08/output.txt}}
```

오류는 `value`를 환경 밖으로 이동시키는 클로저 본문의 라인을 가리킨다. 이 문제를 해결하려면 클로저 본문을 변경하여 값을 환경 밖으로 이동시키지 않아야 한다. 환경에 카운터를 유지하고 클로저 본문에서 그 값을 증가시키는 것이 클로저가 호출된 횟수를 세는 더 직관적인 방법이다. 예제 13-9의 클로저는 `num_sort_operations` 카운터에 대한 가변 참조만 캡처하므로 `sort_by_key`와 함께 작동한다:

<Listing number="13-9" file-name="src/main.rs" caption="`sort_by_key`와 함께 `FnMut` 클로저 사용">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-09/src/main.rs}}
```

</Listing>

`Fn` 트레이트는 클로저를 사용하는 함수나 타입을 정의하거나 사용할 때 중요하다. 다음 섹션에서는 이터레이터를 다룰 것이다. 많은 이터레이터 메서드가 클로저 인수를 받으므로, 계속 진행하면서 이 클로저 세부 사항을 기억하자!

[unwrap-or-else]: ../std/option/enum.Option.html#method.unwrap_or_else


