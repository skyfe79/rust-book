## 고급 트레이트

트레이트에 대해 처음 다룬 것은 [10장 "트레이트: 공유 동작 정의하기"][traits-defining-shared-behavior]<!-- ignore -->에서였다. 하지만 더 깊이 있는 세부 사항은 논의하지 않았다. 이제 여러분이 러스트에 대해 더 많이 알게 되었으니, 본격적으로 자세히 살펴볼 차례다.

<!-- Old link, do not remove -->

<a id="specifying-placeholder-types-in-trait-definitions-with-associated-types"></a>


### 연관 타입

_연관 타입_은 타입 플레이스홀더를 트레이트와 연결하여 트레이트 메서드 정의에서 이 플레이스홀더 타입을 시그니처에 사용할 수 있게 한다. 트레이트를 구현하는 쪽에서 플레이스홀더 타입 대신 구체적인 타입을 지정한다. 이렇게 하면, 트레이트를 구현할 때까지 정확히 어떤 타입인지 알 필요 없이, 트레이트에서 사용할 타입을 정의할 수 있다.

이 장에서 다룬 대부분의 고급 기능은 거의 필요하지 않다고 설명했다. 연관 타입은 중간 정도의 위치를 차지한다: 이 책의 다른 부분에서 설명한 기능보다는 덜 사용되지만, 이 장에서 다룬 다른 기능들보다는 더 자주 사용된다.

연관 타입이 있는 트레이트의 예로는 표준 라이브러리가 제공하는 `Iterator` 트레이트가 있다. 이 트레이트의 연관 타입은 `Item`이라는 이름을 가지며, `Iterator` 트레이트를 구현하는 타입이 순회하는 값의 타입을 나타낸다. `Iterator` 트레이트의 정의는 아래 목록 20-13과 같다.

<Listing number="20-13" caption="연관 타입 `Item`을 가진 `Iterator` 트레이트의 정의">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-13/src/lib.rs}}
```

</Listing>

`Item` 타입은 플레이스홀더이며, `next` 메서드의 정의는 `Option<Self::Item>` 타입의 값을 반환할 것임을 보여준다. `Iterator` 트레이트를 구현하는 쪽에서 `Item`에 대한 구체적인 타입을 지정하면, `next` 메서드는 그 타입의 값을 포함한 `Option`을 반환한다.

연관 타입은 제네릭과 비슷한 개념으로 보일 수 있다. 제네릭은 함수를 정의할 때 처리할 타입을 지정하지 않아도 되게 한다. 두 개념의 차이를 이해하기 위해, `Item` 타입을 `u32`로 지정한 `Counter` 타입에 `Iterator` 트레이트를 구현한 예제를 살펴보자.

<Listing file-name="src/lib.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-22-iterator-on-counter/src/lib.rs:ch19}}
```

</Listing>

이 문법은 제네릭과 유사해 보인다. 그렇다면 왜 `Iterator` 트레이트를 제네릭으로 정의하지 않았을까? 아래 목록 20-14는 제네릭을 사용한 `Iterator` 트레이트의 가상 정의를 보여준다.

<Listing number="20-14" caption="제네릭을 사용한 `Iterator` 트레이트의 가상 정의">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-14/src/lib.rs}}
```

</Listing>

차이점은 제네릭을 사용할 때, 목록 20-14와 같이 각 구현에서 타입을 명시해야 한다는 것이다. `Iterator<String> for Counter`를 구현하거나 다른 타입을 구현할 수 있기 때문에, `Counter`에 대해 `Iterator`를 여러 번 구현할 수 있다. 즉, 트레이트에 제네릭 파라미터가 있으면, 한 타입에 대해 여러 번 구현할 수 있고, 매번 제네릭 타입 파라미터의 구체적인 타입을 바꿀 수 있다. `Counter`에서 `next` 메서드를 사용할 때, 어떤 `Iterator` 구현을 사용할지 타입 어노테이션을 제공해야 한다.

연관 타입을 사용하면, 타입을 명시할 필요가 없다. 왜냐하면 한 타입에 대해 트레이트를 여러 번 구현할 수 없기 때문이다. 목록 20-13에서 연관 타입을 사용한 정의를 보면, `Item` 타입을 한 번만 선택할 수 있다. 왜냐하면 `impl Iterator for Counter`는 하나만 존재할 수 있기 때문이다. `Counter`에서 `next`를 호출할 때마다 `u32` 값의 반복자를 원한다고 명시할 필요가 없다.

연관 타입은 또한 트레이트의 계약의 일부가 된다: 트레이트를 구현하는 쪽은 연관 타입 플레이스홀더를 대체할 타입을 제공해야 한다. 연관 타입은 종종 그 타입이 어떻게 사용될지 설명하는 이름을 가지며, API 문서에서 연관 타입을 문서화하는 것이 좋은 관행이다.


### 기본 제네릭 타입 매개변수와 연산자 오버로딩

제네릭 타입 매개변수를 사용할 때, 제네릭 타입에 대한 기본 구체 타입을 지정할 수 있다. 이렇게 하면 기본 타입이 적합한 경우, 트레이트를 구현하는 개발자가 구체 타입을 지정할 필요가 없어진다. 기본 타입은 `<PlaceholderType=ConcreteType>` 구문을 사용해 제네릭 타입을 선언할 때 지정한다.

이 기법이 유용한 대표적인 예는 **연산자 오버로딩**이다. 연산자 오버로딩은 특정 상황에서 연산자(예: `+`)의 동작을 커스텀하는 것을 의미한다.

Rust에서는 새로운 연산자를 만들거나 임의의 연산자를 오버로드할 수 없다. 하지만 `std::ops`에 나열된 연산과 해당 트레이트를 구현함으로써 연산자를 오버로드할 수 있다. 예를 들어, 리스트 20-15에서는 `Point` 인스턴스 두 개를 더하기 위해 `+` 연산자를 오버로드한다. 이를 위해 `Point` 구조체에 `Add` 트레이트를 구현한다.

<Listing number="20-15" file-name="src/main.rs" caption="`Point` 인스턴스에 `+` 연산자를 오버로드하기 위해 `Add` 트레이트 구현">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-15/src/main.rs}}
```

</Listing>

`add` 메서드는 두 `Point` 인스턴스의 `x` 값과 `y` 값을 더해 새로운 `Point`를 생성한다. `Add` 트레이트에는 `Output`이라는 연관 타입이 있으며, 이 타입은 `add` 메서드가 반환하는 타입을 결정한다.

이 코드에서 기본 제네릭 타입은 `Add` 트레이트 내에 있다. 다음은 그 정의이다:

```rust
trait Add<Rhs=Self> {
    type Output;

    fn add(self, rhs: Rhs) -> Self::Output;
}
```

이 코드는 일반적으로 익숙할 것이다: 하나의 메서드와 연관 타입을 가진 트레이트이다. 새로운 부분은 `Rhs=Self`이다: 이 구문을 **기본 타입 매개변수**라고 한다. `Rhs` 제네릭 타입 매개변수("right-hand side"의 약어)는 `add` 메서드의 `rhs` 매개변수 타입을 정의한다. `Add` 트레이트를 구현할 때 `Rhs`에 대한 구체 타입을 지정하지 않으면, `Rhs`의 타입은 기본적으로 `Self`가 되며, 이는 `Add`를 구현 중인 타입이 된다.

`Point`에 대해 `Add`를 구현할 때, 두 `Point` 인스턴스를 더하고 싶었기 때문에 `Rhs`의 기본값을 사용했다. 이제 기본값을 사용하지 않고 `Rhs` 타입을 커스텀하는 `Add` 트레이트 구현 예제를 살펴보자.

`Millimeters`와 `Meters`라는 두 구조체가 있으며, 각각 다른 단위로 값을 보관한다. 기존 타입을 다른 구조체로 감싸는 이 방식을 **뉴타입 패턴**이라고 하며, 이에 대해서는 ["뉴타입 패턴을 사용해 외부 타입에 외부 트레이트 구현하기"][newtype]<!-- ignore --> 섹션에서 자세히 설명한다. 밀리미터 단위의 값과 미터 단위의 값을 더하고, `Add` 구현이 올바르게 변환하도록 하고 싶다. 리스트 20-16과 같이 `Millimeters`에 대해 `Meters`를 `Rhs`로 지정해 `Add`를 구현할 수 있다.

<Listing number="20-16" file-name="src/lib.rs" caption="`Millimeters`에 `Add` 트레이트를 구현해 `Millimeters`와 `Meters`를 더하기">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-16/src/lib.rs}}
```

</Listing>

`Millimeters`와 `Meters`를 더하기 위해, `impl Add<Meters>`를 지정해 `Rhs` 타입 매개변수의 값을 설정한다. 이렇게 하면 `Self`의 기본값을 사용하지 않는다.

기본 타입 매개변수는 주로 두 가지 방식으로 사용된다:

1. 기존 코드를 손상시키지 않고 타입을 확장하기 위해
2. 대부분의 사용자가 필요로 하지 않는 특정 경우에 커스텀을 허용하기 위해

표준 라이브러리의 `Add` 트레이트는 두 번째 목적의 예이다: 일반적으로 동일한 타입 두 개를 더하지만, `Add` 트레이트는 그 이상의 커스텀을 허용한다. `Add` 트레이트 정의에서 기본 타입 매개변수를 사용하면 대부분의 경우 추가 매개변수를 지정할 필요가 없다. 즉, 구현 상의 보일러플레이트가 필요 없어져 트레이트를 더 쉽게 사용할 수 있다.

첫 번째 목적은 두 번째와 비슷하지만 반대 방향이다: 기존 트레이트에 타입 매개변수를 추가하려면, 기본값을 지정해 트레이트의 기능을 확장할 수 있으며, 기존 구현 코드를 손상시키지 않는다.

<!-- Old link, do not remove -->

<a id="fully-qualified-syntax-for-disambiguation-calling-methods-with-the-same-name"></a>


### 동일한 이름의 메서드 구분하기

Rust에서는 서로 다른 트레이트가 동일한 이름의 메서드를 가질 수 있다. 또한 하나의 타입에 여러 트레이트를 구현할 수도 있다. 심지어 타입 자체에 트레이트의 메서드와 동일한 이름의 메서드를 직접 구현할 수도 있다.

동일한 이름의 메서드를 호출할 때는 Rust에게 어떤 메서드를 사용할지 명확히 알려줘야 한다. 예를 들어, `Pilot`와 `Wizard`라는 두 트레이트가 있고, 둘 다 `fly`라는 메서드를 가지고 있다고 가정하자. 이 두 트레이트를 `Human` 타입에 구현하고, `Human` 타입 자체에도 `fly` 메서드를 직접 구현했다. 각 `fly` 메서드는 서로 다른 동작을 수행한다.

<Listing number="20-17" file-name="src/main.rs" caption="두 트레이트가 `fly` 메서드를 가지고 있으며, `Human` 타입에 구현되었고, `Human` 타입에 직접 `fly` 메서드가 구현됨">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-17/src/main.rs:here}}
```

</Listing>

`Human` 인스턴스에서 `fly`를 호출하면, 컴파일러는 타입에 직접 구현된 메서드를 기본적으로 호출한다. 이는 Listing 20-18에서 확인할 수 있다.

<Listing number="20-18" file-name="src/main.rs" caption="`Human` 인스턴스에서 `fly` 호출">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-18/src/main.rs:here}}
```

</Listing>

이 코드를 실행하면 `*waving arms furiously*`가 출력된다. 이는 Rust가 `Human`에 직접 구현된 `fly` 메서드를 호출했음을 보여준다.

`Pilot` 트레이트나 `Wizard` 트레이트의 `fly` 메서드를 호출하려면, 더 명시적인 문법을 사용해 어떤 `fly` 메서드를 호출할지 지정해야 한다. Listing 20-19는 이 문법을 보여준다.

<Listing number="20-19" file-name="src/main.rs" caption="호출할 트레이트의 `fly` 메서드 지정">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-19/src/main.rs:here}}
```

</Listing>

메서드 이름 앞에 트레이트 이름을 지정하면 Rust가 어떤 `fly` 구현을 호출할지 명확히 알 수 있다. `Human::fly(&person)`과 같이 작성할 수도 있지만, 이는 `person.fly()`와 동일하며, 구분이 필요하지 않다면 더 길게 작성할 필요는 없다.

이 코드를 실행하면 다음과 같이 출력된다:

```console
{{#include ../listings/ch20-advanced-features/listing-20-19/output.txt}}
```

`fly` 메서드가 `self` 파라미터를 가지고 있기 때문에, 두 타입이 하나의 트레이트를 구현하고 있다면 Rust는 `self`의 타입을 기반으로 어떤 트레이트 구현을 사용할지 결정할 수 있다.

그러나 메서드가 아닌 연관 함수는 `self` 파라미터를 가지고 있지 않다. 동일한 함수 이름을 가진 여러 타입이나 트레이트가 있을 때, Rust는 _완전한 정규화 문법(fully qualified syntax)_을 사용하지 않으면 어떤 타입을 의미하는지 알 수 없다. 예를 들어, Listing 20-20에서는 모든 강아지의 이름을 _Spot_으로 짓는 동물 보호소를 위한 트레이트를 만든다. `Animal` 트레이트에는 연관 함수 `baby_name`이 있다. `Animal` 트레이트는 `Dog` 구조체에 구현되며, `Dog`에도 직접 `baby_name` 연관 함수가 제공된다.

<Listing number="20-20" file-name="src/main.rs" caption="연관 함수를 가진 트레이트와 동일한 이름의 연관 함수를 가진 타입이 트레이트를 구현함">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-20/src/main.rs}}
```

</Listing>

`Dog`에 정의된 `baby_name` 연관 함수에서 모든 강아지의 이름을 Spot으로 짓는 코드를 구현했다. `Dog` 타입은 `Animal` 트레이트도 구현하며, 이 트레이트는 모든 동물이 가진 특성을 설명한다. 강아지는 puppy라고 불리며, 이는 `Animal` 트레이트의 `baby_name` 함수에서 표현된다.

`main`에서 `Dog::baby_name` 함수를 호출하면, `Dog`에 직접 정의된 연관 함수가 호출된다. 이 코드는 다음과 같이 출력된다:

```console
{{#include ../listings/ch20-advanced-features/listing-20-20/output.txt}}
```

이 출력은 우리가 원하는 결과가 아니다. 우리는 `Dog`에 구현된 `Animal` 트레이트의 `baby_name` 함수를 호출해 `A baby dog is called a puppy`가 출력되길 원한다. Listing 20-19에서 사용한 트레이트 이름 지정 기법은 여기서 도움이 되지 않는다. `main`을 Listing 20-21의 코드로 변경하면 컴파일 오류가 발생한다.

<Listing number="20-21" file-name="src/main.rs" caption="`Animal` 트레이트의 `baby_name` 함수를 호출하려고 시도했지만, Rust가 어떤 구현을 사용할지 알 수 없음">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-21/src/main.rs:here}}
```

</Listing>

`Animal::baby_name`은 `self` 파라미터를 가지고 있지 않으며, `Animal` 트레이트를 구현하는 다른 타입이 있을 수 있기 때문에 Rust는 어떤 `Animal::baby_name` 구현을 사용할지 결정할 수 없다. 이 경우 다음과 같은 컴파일 오류가 발생한다:

```console
{{#include ../listings/ch20-advanced-features/listing-20-21/output.txt}}
```

Rust에게 다른 타입이 아닌 `Dog`에 구현된 `Animal` 트레이트의 구현을 사용하라고 명확히 알려주기 위해 완전한 정규화 문법을 사용해야 한다. Listing 20-22는 완전한 정규화 문법을 사용하는 방법을 보여준다.

<Listing number="20-22" file-name="src/main.rs" caption="완전한 정규화 문법을 사용해 `Dog`에 구현된 `Animal` 트레이트의 `baby_name` 함수를 호출함">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-22/src/main.rs:here}}
```

</Listing>

각괄호 안에 타입 어노테이션을 제공해 Rust에게 `Dog` 타입을 `Animal`로 취급해 `baby_name` 메서드를 호출하라고 알려준다. 이제 이 코드는 우리가 원하는 대로 출력한다:

```console
{{#include ../listings/ch20-advanced-features/listing-20-22/output.txt}}
```

일반적으로 완전한 정규화 문법은 다음과 같이 정의된다:

```rust,ignore
<Type as Trait>::function(receiver_if_method, next_arg, ...);
```

메서드가 아닌 연관 함수의 경우 `receiver`가 없으며, 다른 인수 목록만 존재한다. 함수나 메서드를 호출할 때 완전한 정규화 문법을 어디서든 사용할 수 있다. 그러나 Rust가 프로그램의 다른 정보를 통해 추론할 수 있는 부분은 생략할 수 있다. 동일한 이름을 가진 여러 구현이 있고 Rust가 어떤 구현을 호출할지 도움이 필요한 경우에만 이 더 장황한 문법을 사용하면 된다.

<!-- Old link, do not remove -->

<a id="using-supertraits-to-require-one-traits-functionality-within-another-trait"></a>


### 슈퍼트레이트 사용하기

때로는 한 트레이트 정의가 다른 트레이트에 의존하도록 작성할 수 있다. 첫 번째 트레이트를 구현하려면 해당 타입이 두 번째 트레이트도 구현해야 한다. 이렇게 하면 트레이트 정의에서 두 번째 트레이트의 연관 아이템을 활용할 수 있다. 이때 의존하는 트레이트를 _슈퍼트레이트_라고 부른다.

예를 들어, `OutlinePrint` 트레이트를 만들고, `outline_print` 메서드를 통해 주어진 값을 별표로 둘러싼 형태로 출력하려 한다고 가정해 보자. 즉, `Point` 구조체가 표준 라이브러리의 `Display` 트레이트를 구현하여 `(x, y)` 형태로 출력된다면, `x`가 `1`이고 `y`가 `3`인 `Point` 인스턴스에서 `outline_print`를 호출하면 다음과 같은 결과가 출력되어야 한다:

```text
**********
*        *
* (1, 3) *
*        *
**********
```

`outline_print` 메서드를 구현할 때 `Display` 트레이트의 기능을 사용하고자 한다. 따라서 `OutlinePrint` 트레이트는 `Display`를 구현한 타입에 대해서만 동작하도록 지정해야 한다. 이를 위해 트레이트 정의에서 `OutlinePrint: Display`를 지정할 수 있다. 이 기법은 트레이트에 트레이트 바운드를 추가하는 것과 유사하다. 아래 예제는 `OutlinePrint` 트레이트의 구현을 보여준다.

<Listing number="20-23" file-name="src/main.rs" caption="`Display`의 기능을 필요로 하는 `OutlinePrint` 트레이트 구현">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-23/src/main.rs:here}}
```

</Listing>

`OutlinePrint`가 `Display` 트레이트를 필요로 한다고 명시했기 때문에, `Display`를 구현한 모든 타입에 대해 자동으로 구현되는 `to_string` 함수를 사용할 수 있다. 만약 `Display` 트레이트를 지정하지 않고 `to_string`을 사용하려고 하면, 현재 스코프에서 `&Self` 타입에 대해 `to_string` 메서드를 찾을 수 없다는 오류가 발생한다.

이제 `Display`를 구현하지 않은 타입(예: `Point` 구조체)에 `OutlinePrint`를 구현하려고 할 때 어떤 일이 발생하는지 살펴보자:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/src/main.rs:here}}
```

</Listing>

이 경우 `Display`가 필요하지만 구현되지 않았다는 오류가 발생한다:

```console
{{#include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/output.txt}}
```

이 문제를 해결하려면 `Point`에 `Display`를 구현하여 `OutlinePrint`가 요구하는 제약 조건을 충족시켜야 한다. 아래와 같이 작성할 수 있다:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-03-impl-display-for-point/src/main.rs:here}}
```

</Listing>

이제 `Point`에 `OutlinePrint` 트레이트를 구현하면 성공적으로 컴파일되며, `Point` 인스턴스에서 `outline_print`를 호출해 별표로 둘러싼 형태로 출력할 수 있다.


### 뉴타입 패턴을 사용해 외부 타입에 외부 트레잇 구현하기

10장의 ["타입에 트레잇 구현하기"][implementing-a-trait-on-a-type]<!-- ignore -->에서, 오펀 규칙(orphan rule)에 대해 언급했다. 이 규칙에 따르면, 트레잇이나 타입 중 하나 또는 둘 다 크레이트 내부에 정의되어 있을 때만 해당 타입에 트레잇을 구현할 수 있다. 이 제약을 우회하기 위해 **뉴타입 패턴(newtype pattern)**을 사용할 수 있다. 이 패턴은 튜플 구조체(tuple struct) 내에 새로운 타입을 만드는 방식이다. (튜플 구조체에 대해서는 5장의 ["이름 없는 필드를 가진 튜플 구조체로 서로 다른 타입 만들기"][tuple-structs]<!-- ignore -->에서 다뤘다.) 튜플 구조체는 하나의 필드를 가지며, 트레잇을 구현하려는 타입을 감싸는 얇은 래퍼 역할을 한다. 이렇게 하면 래퍼 타입이 크레이트 내부에 속하게 되고, 래퍼에 트레잇을 구현할 수 있다. **뉴타입**이라는 용어는 Haskell 프로그래밍 언어에서 유래했다. 이 패턴을 사용해도 런타임 성능에 영향을 미치지 않으며, 컴파일 시 래퍼 타입은 제거된다.

예를 들어, `Vec<T>`에 `Display` 트레잇을 구현하고 싶다고 가정해보자. 오펀 규칙 때문에 `Display` 트레잇과 `Vec<T>` 타입이 모두 크레이트 외부에 정의되어 있으므로 직접 구현할 수 없다. 이 경우 `Vec<T>` 인스턴스를 갖는 `Wrapper` 구조체를 만들 수 있다. 그런 다음 `Wrapper`에 `Display`를 구현하고 `Vec<T>` 값을 사용할 수 있다. 이 내용은 리스트 20-24에 나와 있다.

<Listing number="20-24" file-name="src/main.rs" caption="`Vec<String>`을 감싸는 `Wrapper` 타입을 만들어 `Display` 구현하기">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-24/src/main.rs}}
```

</Listing>

`Display` 구현에서 `self.0`을 사용해 내부의 `Vec<T>`에 접근한다. `Wrapper`는 튜플 구조체이고, `Vec<T>`는 튜플의 0번 인덱스에 위치하기 때문이다. 이제 `Wrapper`에서 `Display` 트레잇의 기능을 사용할 수 있다.

이 기법의 단점은 `Wrapper`가 새로운 타입이기 때문에, 내부에 있는 값의 메서드를 그대로 사용할 수 없다는 점이다. `Vec<T>`의 모든 메서드를 `Wrapper`에 직접 구현해야 한다. 이때 메서드들은 `self.0`에 위임해야 하며, 이렇게 하면 `Wrapper`를 `Vec<T>`처럼 다룰 수 있다. 만약 새로운 타입이 내부 타입의 모든 메서드를 갖게 하려면, `Wrapper`에 `Deref` 트레잇을 구현해 내부 타입을 반환하는 방식으로 해결할 수 있다. (15장의 ["`Deref` 트레잇으로 스마트 포인터를 일반 참조처럼 다루기"][smart-pointer-deref]<!-- ignore -->에서 `Deref` 트레잇 구현에 대해 다뤘다.) 만약 `Wrapper` 타입이 내부 타입의 모든 메서드를 갖지 않게 하려면, 예를 들어 `Wrapper` 타입의 동작을 제한하려면, 원하는 메서드만 수동으로 구현해야 한다.

이 뉴타입 패턴은 트레잇과 관련이 없을 때도 유용하다. 이제 관점을 바꿔 러스트의 타입 시스템과 상호작용하는 몇 가지 고급 방법을 살펴보자.

[newtype]: ch20-02-advanced-traits.html#using-the-newtype-pattern-to-implement-external-traits-on-external-types
[implementing-a-trait-on-a-type]: ch10-02-traits.html#implementing-a-trait-on-a-type
[traits-defining-shared-behavior]: ch10-02-traits.html#traits-defining-shared-behavior
[smart-pointer-deref]: ch15-02-deref.html#treating-smart-pointers-like-regular-references-with-the-deref-trait
[tuple-structs]: ch05-01-defining-structs.html#using-tuple-structs-without-named-fields-to-create-different-types


