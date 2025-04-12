## 고급 함수와 클로저

이 섹션에서는 함수 포인터와 클로저 반환을 포함해 함수와 클로저와 관련된 몇 가지 고급 기능을 살펴본다.


### 함수 포인터

클로저를 함수에 전달하는 방법에 대해 알아봤다면, 일반 함수도 함수에 전달할 수 있다! 이 기법은 새로운 클로저를 정의하지 않고 이미 정의된 함수를 전달하고 싶을 때 유용하다. 함수는 `Fn` 클로저 트레잇과 혼동하지 않도록 `fn` (소문자 _f_) 타입으로 강제 변환된다. 이 `fn` 타입을 _함수 포인터_ 라고 부른다. 함수 포인터를 사용해 함수를 전달하면, 함수를 다른 함수의 인자로 사용할 수 있다.

함수 포인터를 매개변수로 지정하는 문법은 클로저와 유사하다. 아래 예제 20-28에서 `add_one` 함수는 매개변수에 1을 더한다. `do_twice` 함수는 두 개의 매개변수를 받는다: 하나는 `i32` 타입의 매개변수를 받고 `i32`를 반환하는 함수 포인터, 다른 하나는 `i32` 값이다. `do_twice` 함수는 함수 `f`를 두 번 호출하며 `arg` 값을 전달한 후, 두 함수 호출 결과를 더한다. `main` 함수는 `add_one`과 `5`를 인자로 `do_twice`를 호출한다.

<Listing number="20-28" file-name="src/main.rs" caption="함수 포인터를 인자로 받기 위해 `fn` 타입 사용">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-28/src/main.rs}}
```

</Listing>

이 코드는 `The answer is: 12`를 출력한다. `do_twice`의 매개변수 `f`는 `i32` 타입의 매개변수를 하나 받고 `i32`를 반환하는 `fn` 타입으로 지정한다. 그런 다음 `do_twice` 본문에서 `f`를 호출할 수 있다. `main`에서는 `add_one` 함수 이름을 `do_twice`의 첫 번째 인자로 전달한다.

클로저와 달리 `fn`은 트레잇이 아닌 타입이므로, `Fn` 트레잇 중 하나를 트레잇 바운드로 사용해 제네릭 타입 매개변수를 선언하는 대신 `fn`을 직접 매개변수 타입으로 지정한다.

함수 포인터는 세 가지 클로저 트레잇(`Fn`, `FnMut`, `FnOnce`)을 모두 구현한다. 즉, 클로저를 기대하는 함수에 항상 함수 포인터를 인자로 전달할 수 있다. 함수나 클로저를 모두 받을 수 있도록 제네릭 타입과 클로저 트레잇 중 하나를 사용해 함수를 작성하는 것이 가장 좋다.

그러나 클로저가 없는 외부 코드와 인터페이스할 때는 `fn`만 받고 싶을 수 있다. C 함수는 함수를 인자로 받을 수 있지만, C에는 클로저가 없다.

인라인으로 정의된 클로저나 이름이 있는 함수를 사용할 수 있는 예시로, 표준 라이브러리의 `Iterator` 트레잇이 제공하는 `map` 메서드를 살펴보자. `map` 메서드를 사용해 숫자 벡터를 문자열 벡터로 변환하려면, 아래 예제 20-29처럼 클로저를 사용할 수 있다.

<Listing number="20-29" caption="`map` 메서드와 클로저를 사용해 숫자를 문자열로 변환">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-29/src/main.rs:here}}
```

</Listing>

또는 클로저 대신 함수 이름을 `map`의 인자로 사용할 수 있다. 예제 20-30은 이를 보여준다.

<Listing number="20-30" caption="`String::to_string` 메서드를 사용해 숫자를 문자열로 변환">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-30/src/main.rs:here}}
```

</Listing>

여기서는 ["고급 트레잇"][advanced-traits]<!-- ignore -->에서 설명한 완전한 문법을 사용해야 한다. 왜냐하면 `to_string`이라는 이름의 함수가 여러 개 있기 때문이다.

여기서는 표준 라이브러리가 `Display`를 구현한 모든 타입에 대해 구현한 `ToString` 트레잇에 정의된 `to_string` 함수를 사용한다.

6장의 ["열거형 값"][enum-values]<!-- ignore -->에서 정의한 각 열거형 변형의 이름이 초기화 함수가 된다는 것을 기억할 것이다. 이 초기화 함수를 클로저 트레잇을 구현한 함수 포인터로 사용할 수 있다. 즉, 클로저를 받는 메서드에 초기화 함수를 인자로 지정할 수 있다. 예제 20-31에서 이를 확인할 수 있다.

<Listing number="20-31" caption="`map` 메서드와 열거형 초기화 함수를 사용해 숫자로부터 `Status` 인스턴스 생성">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-31/src/main.rs:here}}
```

</Listing>

여기서 `map`이 호출된 범위의 각 `u32` 값을 사용해 `Status::Value` 인스턴스를 생성한다. 이때 `Status::Value`의 초기화 함수를 사용한다. 어떤 사람은 이 스타일을 선호하고, 어떤 사람은 클로저를 선호한다. 둘 다 같은 코드로 컴파일되므로, 더 명확한 스타일을 사용하면 된다.


### 클로저 반환하기

클로저는 트레잇으로 표현되기 때문에 직접 반환할 수 없다. 대부분의 경우 트레잇을 반환하려면 해당 트레잇을 구현한 구체적인 타입을 함수의 반환 값으로 사용할 수 있다. 하지만 클로저는 반환 가능한 구체적인 타입이 없기 때문에 일반적으로 이 방법을 사용할 수 없다. 예를 들어, 클로저가 스코프에서 값을 캡처하면 함수 포인터 `fn`을 반환 타입으로 사용할 수 없다.

대신, 일반적으로 10장에서 배운 `impl Trait` 문법을 사용한다. `Fn`, `FnOnce`, `FnMut`를 사용해 어떤 함수 타입이든 반환할 수 있다. 예를 들어, 아래 예제 코드는 정상적으로 동작한다.

<Listing number="20-32" caption="`impl Trait` 문법을 사용해 함수에서 클로저 반환하기">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-32/src/lib.rs}}
```

</Listing>

하지만 13장의 ["클로저 타입 추론과 명시적 타입 지정"][closure-types]에서 언급했듯이, 각 클로저는 고유한 타입을 가진다. 동일한 시그니처를 가지지만 구현이 다른 여러 함수를 다뤄야 한다면 트레잇 객체를 사용해야 한다. 아래 예제 코드에서 어떤 일이 발생하는지 살펴보자.

<Listing file-name="src/main.rs" number="20-33" caption="`impl Fn`을 반환하는 함수로 정의된 클로저의 `Vec<T>` 생성하기">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-33/src/main.rs}}
```

</Listing>

여기서 `returns_closure`와 `returns_initialized_closure` 두 함수는 모두 `impl Fn(i32) -> i32`를 반환한다. 두 함수가 반환하는 클로저는 동일한 타입을 구현하지만 서로 다르다. 이 코드를 컴파일하려고 하면 Rust는 다음과 같은 오류를 발생시킨다:

```text
{{#include ../listings/ch20-advanced-features/listing-20-33/output.txt}}
```

오류 메시지는 `impl Trait`를 반환할 때마다 Rust가 고유한 _불투명 타입(opaque type)_ 을 생성한다는 것을 알려준다. 이 타입은 Rust가 우리를 위해 생성한 세부 사항을 볼 수 없는 타입이다. 따라서 이 두 함수가 동일한 트레잇 `Fn(i32) -> i32`를 구현하는 클로저를 반환하더라도, Rust가 생성한 불투명 타입은 서로 다르다. (이는 17장의 ["여러 Future 다루기"][any-number-of-futures]에서 본 것처럼, 동일한 출력 타입을 가지는 다른 async 블록에 대해 Rust가 서로 다른 구체적인 타입을 생성하는 것과 유사하다.) 이 문제에 대한 해결책은 이미 여러 번 살펴봤듯이, 트레잇 객체를 사용하는 것이다. 아래 예제 코드를 참고하자.

<Listing number="20-34" caption="`Box<dyn Fn>`을 반환하는 함수로 정의된 클로저의 `Vec<T>` 생성하기">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-34/src/main.rs:here}}
```

</Listing>

이 코드는 정상적으로 컴파일된다. 트레잇 객체에 대한 더 자세한 내용은 18장의 ["다양한 타입의 값을 허용하는 트레잇 객체 사용하기"][using-trait-objects-that-allow-for-values-of-different-types] 섹션을 참고하자.

다음으로, 매크로에 대해 알아보자!

[advanced-traits]: ch20-02-advanced-traits.html#advanced-traits
[enum-values]: ch06-01-defining-an-enum.html#enum-values
[closure-types]: ch13-01-closures.html#closure-type-inference-and-annotation
[any-number-of-futures]: ch17-03-more-futures.html
[using-trait-objects-that-allow-for-values-of-different-types]: ch18-02-trait-objects.html#using-trait-objects-that-allow-for-values-of-different-types


