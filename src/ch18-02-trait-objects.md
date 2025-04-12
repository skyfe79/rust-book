## 다양한 타입의 값을 허용하는 트레이트 객체 사용하기

8장에서 벡터의 한계점 중 하나는 단일 타입의 요소만 저장할 수 있다는 것을 언급했다. 리스트 8-9에서 `SpreadsheetCell` 열거형을 정의해 정수, 부동소수점, 텍스트를 저장할 수 있는 방법을 소개했다. 이렇게 하면 각 셀에 다양한 타입의 데이터를 저장할 수 있으면서도, 여전히 셀 행을 나타내는 벡터를 유지할 수 있다. 이 방법은 코드를 컴파일할 때 교체 가능한 항목이 고정된 타입 집합으로 정해져 있는 경우에 완벽한 해결책이다.

그러나 때로는 라이브러리 사용자가 특정 상황에서 유효한 타입 집합을 확장할 수 있도록 하고 싶을 때가 있다. 이를 어떻게 구현할 수 있는지 보여주기 위해, GUI 도구 예제를 만들어본다. 이 도구는 항목 목록을 순회하며 각 항목의 `draw` 메서드를 호출해 화면에 그리는 일반적인 GUI 기법을 사용한다. `gui`라는 이름의 라이브러리 크레이트를 만들어 GUI 라이브러리의 구조를 담을 것이다. 이 크레이트는 `Button`이나 `TextField`와 같은 사용자 정의 타입을 포함할 수 있다. 또한 `gui` 사용자는 화면에 그릴 수 있는 자신만의 타입을 만들고 싶어할 것이다. 예를 들어, 한 프로그래머는 `Image`를 추가하고, 다른 프로그래머는 `SelectBox`를 추가할 수 있다.

이 예제에서는 완전한 GUI 라이브러리를 구현하지는 않지만, 각 부분이 어떻게 조합되는지 보여줄 것이다. 라이브러리를 작성하는 시점에서는 다른 프로그래머가 만들고 싶어할 모든 타입을 알거나 정의할 수 없다. 하지만 `gui`가 다양한 타입의 값을 추적해야 하고, 이렇게 타입이 다른 각 값에 대해 `draw` 메서드를 호출해야 한다는 것은 알고 있다. `draw` 메서드를 호출했을 때 정확히 어떤 일이 일어날지는 알 필요가 없으며, 단지 해당 값이 호출할 수 있는 `draw` 메서드를 가지고 있다는 것만 알면 된다.

상속이 있는 언어라면 `draw` 메서드를 가진 `Component`라는 클래스를 정의할 수 있다. `Button`, `Image`, `SelectBox`와 같은 다른 클래스들은 `Component`를 상속받아 `draw` 메서드를 물려받을 것이다. 각 클래스는 `draw` 메서드를 오버라이드해 자신만의 동작을 정의할 수 있지만, 프레임워크는 모든 타입을 `Component` 인스턴스처럼 취급하고 `draw` 메서드를 호출할 수 있다. 하지만 Rust에는 상속이 없기 때문에, 사용자가 새로운 타입으로 라이브러리를 확장할 수 있도록 `gui` 라이브러리를 구조화하는 다른 방법이 필요하다.


### 공통 동작을 위한 트레이트 정의

`gui`가 가져야 하는 동작을 구현하기 위해 `Draw`라는 이름의 트레이트를 정의한다. 이 트레이트는 `draw`라는 하나의 메서드를 가진다. 그런 다음 트레이트 객체를 받는 벡터를 정의할 수 있다. _트레이트 객체_는 지정한 트레이트를 구현한 타입의 인스턴스와 런타임에 해당 타입의 트레이트 메서드를 조회하기 위한 테이블을 모두 가리킨다. 트레이트 객체를 생성하려면 `&` 참조나 `Box<T>` 스마트 포인터 같은 포인터를 지정한 다음 `dyn` 키워드를 사용하고 관련 트레이트를 지정한다. (트레이트 객체가 반드시 포인터를 사용해야 하는 이유는 20장의 ["동적 크기 타입과 `Sized` 트레이트"][dynamically-sized]<!-- ignore -->에서 다룬다.) 트레이트 객체는 제네릭이나 구체적인 타입 대신 사용할 수 있다. 트레이트 객체를 사용하는 곳에서는 Rust의 타입 시스템이 컴파일 시점에 해당 컨텍스트에서 사용되는 모든 값이 트레이트 객체의 트레이트를 구현하도록 보장한다. 따라서 컴파일 시점에 모든 가능한 타입을 알 필요가 없다.

Rust에서는 구조체와 열거형을 다른 언어의 객체와 구분하기 위해 "객체"라고 부르지 않는다. 구조체나 열거형에서는 구조체 필드의 데이터와 `impl` 블록의 동작이 분리되어 있지만, 다른 언어에서는 데이터와 동작이 하나의 개념으로 결합된 것을 종종 객체라고 부른다. 그러나 트레이트 객체는 데이터와 동작을 결합한다는 점에서 다른 언어의 객체와 더 비슷하다. 하지만 트레이트 객체는 데이터를 추가할 수 없다는 점에서 전통적인 객체와 다르다. 트레이트 객체는 다른 언어의 객체만큼 일반적으로 유용하지는 않다. 트레이트 객체의 특정 목적은 공통 동작을 통해 추상화를 가능하게 하는 것이다.

리스트 18-3은 `draw`라는 하나의 메서드를 가진 `Draw` 트레이트를 정의하는 방법을 보여준다.

<Listing number="18-3" file-name="src/lib.rs" caption="`Draw` 트레이트 정의">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-03/src/lib.rs}}
```

</Listing>

이 구문은 10장에서 트레이트를 정의하는 방법에 대해 논의할 때 익숙해졌을 것이다. 다음은 새로운 구문이다: 리스트 18-4는 `components`라는 벡터를 가진 `Screen` 구조체를 정의한다. 이 벡터는 `Box<dyn Draw>` 타입으로, 트레이트 객체이다. 이는 `Box` 내부에 `Draw` 트레이트를 구현한 모든 타입을 대표한다.

<Listing number="18-4" file-name="src/lib.rs" caption="`Draw` 트레이트를 구현한 트레이트 객체의 벡터를 가진 `components` 필드를 가진 `Screen` 구조체 정의">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-04/src/lib.rs:here}}
```

</Listing>

`Screen` 구조체에는 `run`이라는 메서드를 정의한다. 이 메서드는 `components`의 각 요소에 대해 `draw` 메서드를 호출한다. 리스트 18-5에서 이를 확인할 수 있다.

<Listing number="18-5" file-name="src/lib.rs" caption="`Screen`의 `run` 메서드: 각 컴포넌트에 대해 `draw` 메서드 호출">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-05/src/lib.rs:here}}
```

</Listing>

이 방식은 트레이트 바운드를 사용한 제네릭 타입 매개변수를 가진 구조체를 정의하는 것과 다르게 동작한다. 제네릭 타입 매개변수는 한 번에 하나의 구체적인 타입으로만 대체될 수 있지만, 트레이트 객체는 런타임에 여러 구체적인 타입이 트레이트 객체를 대체할 수 있도록 허용한다. 예를 들어, 리스트 18-6과 같이 제네릭 타입과 트레이트 바운드를 사용해 `Screen` 구조체를 정의할 수도 있다:

<Listing number="18-6" file-name="src/lib.rs" caption="제네릭과 트레이트 바운드를 사용한 `Screen` 구조체 및 `run` 메서드의 대체 구현">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-06/src/lib.rs:here}}
```

</Listing>

이 방식은 `Screen` 인스턴스가 모든 컴포넌트가 `Button` 타입이거나 모두 `TextField` 타입인 리스트를 가지도록 제한한다. 동일한 타입의 컬렉션만 사용한다면, 제네릭과 트레이트 바운드를 사용하는 것이 더 나은데, 정의가 컴파일 시점에 구체적인 타입을 사용하도록 단일화되기 때문이다.

반면, 트레이트 객체를 사용하는 방법에서는 하나의 `Screen` 인스턴스가 `Box<Button>`과 `Box<TextField>`를 모두 포함하는 `Vec<T>`를 가질 수 있다. 이 방식이 어떻게 동작하는지 살펴보고, 런타임 성능에 미치는 영향에 대해 논의해 보자.


### 트레이트 구현하기

이제 `Draw` 트레이트를 구현하는 타입들을 추가해 보자. `Button` 타입을 구현할 것이다. 실제 GUI 라이브러리를 구현하는 것은 이 책의 범위를 벗어나므로, `draw` 메서드의 본문에는 유용한 구현이 포함되지 않을 것이다. 구현이 어떻게 보일지 상상해 보자면, `Button` 구조체는 `width`, `height`, `label` 필드를 가질 수 있다. 다음은 리스트 18-7에 나온 예제다:

<Listing number="18-7" file-name="src/lib.rs" caption="`Draw` 트레이트를 구현한 `Button` 구조체">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-07/src/lib.rs:here}}
```

</Listing>

`Button`의 `width`, `height`, `label` 필드는 다른 컴포넌트와 다를 수 있다. 예를 들어, `TextField` 타입은 동일한 필드에 더해 `placeholder` 필드를 가질 수 있다. 화면에 그릴 각 타입은 `Draw` 트레이트를 구현하지만, `draw` 메서드에서 해당 타입을 어떻게 그릴지 정의하는 코드는 다를 것이다. `Button`의 경우, 사용자가 버튼을 클릭할 때 발생하는 동작과 관련된 메서드를 포함하는 추가 `impl` 블록을 가질 수 있다. 이러한 메서드는 `TextField`와 같은 타입에는 적용되지 않는다.

우리 라이브러리를 사용하는 누군가가 `width`, `height`, `options` 필드를 가진 `SelectBox` 구조체를 구현하기로 결정했다면, `SelectBox` 타입에서도 `Draw` 트레이트를 구현할 수 있다. 다음은 리스트 18-8에 나온 예제다:

<Listing number="18-8" file-name="src/main.rs" caption="`gui`를 사용하고 `SelectBox` 구조체에 `Draw` 트레이트를 구현한 다른 크레이트">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-08/src/main.rs:here}}
```

</Listing>

이제 라이브러리 사용자는 `main` 함수를 작성해 `Screen` 인스턴스를 생성할 수 있다. `Screen` 인스턴스에 `SelectBox`와 `Button`을 추가할 수 있는데, 각각을 `Box<T>`에 넣어 트레이트 객체로 만든다. 그런 다음 `Screen` 인스턴스에서 `run` 메서드를 호출할 수 있으며, 이 메서드는 각 컴포넌트에서 `draw` 메서드를 호출한다. 다음은 리스트 18-9에 나온 구현 예제다:

<Listing number="18-9" file-name="src/main.rs" caption="동일한 트레이트를 구현하는 다양한 타입의 값을 저장하기 위해 트레이트 객체 사용">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-09/src/main.rs:here}}
```

</Listing>

우리가 라이브러리를 작성할 때는 누군가가 `SelectBox` 타입을 추가할지 알지 못했지만, `Screen` 구현은 새로운 타입에서 동작하고 이를 그릴 수 있었다. 이는 `SelectBox`가 `Draw` 트레이트를 구현했기 때문이다. 즉, `draw` 메서드를 구현했다는 의미다.

이 개념은 값의 구체적인 타입보다는 값이 응답하는 메시지에만 관심을 갖는 것으로, 동적 타입 언어에서의 _덕 타이핑(duck typing)_ 개념과 유사하다: 만약 어떤 것이 오리처럼 걷고 오리처럼 꽥꽥거린다면, 그것은 오리일 것이다! 리스트 18-5에서 `Screen`의 `run` 구현에서 `run`은 각 컴포넌트의 구체적인 타입이 무엇인지 알 필요가 없다. 컴포넌트가 `Button`의 인스턴스인지 `SelectBox`의 인스턴스인지 확인하지 않고, 단순히 컴포넌트에서 `draw` 메서드를 호출한다. `components` 벡터의 값 타입으로 `Box<dyn Draw>`를 지정함으로써, `Screen`이 `draw` 메서드를 호출할 수 있는 값이 필요하다고 정의했다.

트레이트 객체와 Rust의 타입 시스템을 사용해 덕 타이핑과 유사한 코드를 작성할 때의 장점은, 런타임에 값이 특정 메서드를 구현했는지 확인하거나, 값이 메서드를 구현하지 않았는데도 호출할 때 발생할 수 있는 오류를 걱정할 필요가 없다는 점이다. Rust는 값이 트레이트 객체가 필요로 하는 트레이트를 구현하지 않았다면 코드를 컴파일하지 않는다.

예를 들어, 리스트 18-10은 `String`을 컴포넌트로 사용해 `Screen`을 생성하려고 할 때 발생하는 상황을 보여준다.

<Listing number="18-10" file-name="src/main.rs" caption="트레이트 객체의 트레이트를 구현하지 않은 타입을 사용하려는 시도">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-10/src/main.rs}}
```

</Listing>

`String`이 `Draw` 트레이트를 구현하지 않았기 때문에 다음과 같은 오류가 발생한다:

```console
{{#include ../listings/ch18-oop/listing-18-10/output.txt}}
```

이 오류는 우리가 `Screen`에 의도하지 않은 타입을 전달했음을 알려주므로, 다른 타입을 전달하거나 `String`에서 `Draw`를 구현해 `Screen`이 `draw`를 호출할 수 있도록 해야 한다.


### 트레이트 객체와 동적 디스패치

[10장 "제네릭 코드의 성능"][performance-of-code-using-generics]<!-- ignore -->에서 컴파일러가 제네릭에 대해 수행하는 단일화(monomorphization) 과정에 대해 논의했다. 컴파일러는 제네릭 타입 파라미터 대신 사용하는 구체적인 타입마다 함수와 메서드의 비제네릭 구현을 생성한다. 단일화를 통해 생성된 코드는 _정적 디스패치(static dispatch)_를 수행한다. 정적 디스패치는 컴파일 시점에 어떤 메서드를 호출할지 컴파일러가 알 수 있는 경우를 말한다. 이와 반대로 _동적 디스패치(dynamic dispatch)_는 컴파일 시점에 어떤 메서드를 호출할지 컴파일러가 알 수 없는 경우를 의미한다. 동적 디스패치에서는 컴파일러가 런타임에 어떤 메서드를 호출할지 결정하는 코드를 생성한다.

트레이트 객체를 사용할 때 Rust는 동적 디스패치를 사용해야 한다. 컴파일러는 트레이트 객체를 사용하는 코드에서 어떤 타입이 사용될지 알 수 없기 때문에, 어떤 타입의 어떤 메서드를 호출해야 할지 결정할 수 없다. 대신 런타임에 Rust는 트레이트 객체 내부의 포인터를 사용해 호출할 메서드를 결정한다. 이 과정에서 런타임 오버헤드가 발생하며, 이는 정적 디스패치에서는 발생하지 않는다. 또한 동적 디스패치는 컴파일러가 메서드의 코드를 인라인화하는 것을 방해해 일부 최적화를 막는다. Rust는 동적 디스패치를 어디서 사용할 수 있고 없는지에 대한 규칙을 가지고 있으며, 이를 _dyn 호환성(dyn compatibility)_이라고 한다. 이 규칙은 이 논의의 범위를 벗어나지만, [레퍼런스][dyn-compatibility]에서 더 자세히 알아볼 수 있다. 그러나 [리스트 18-5][dynamically-sized]와 [리스트 18-9][dyn-compatibility]에서 작성한 코드는 추가적인 유연성을 얻을 수 있었으므로, 이는 고려해야 할 트레이드오프다.

[performance-of-code-using-generics]: ch10-01-syntax.html#performance-of-code-using-generics
[dynamically-sized]: ch20-03-advanced-types.html#dynamically-sized-types-and-the-sized-trait
[dyn-compatibility]: https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility


