## `Deref`를 사용해 스마트 포인터를 일반 참조처럼 다루기

`Deref` 트레잇을 구현하면 *역참조 연산자* `*`의 동작을 커스터마이징할 수 있다. (이 연산자는 곱셈이나 전역 연산자와 혼동하지 말아야 한다.) 스마트 포인터가 일반 참조처럼 동작하도록 `Deref`를 구현하면, 참조를 다루는 코드를 작성하고 그 코드를 스마트 포인터와 함께 사용할 수 있다.

먼저 역참조 연산자가 일반 참조와 어떻게 동작하는지 살펴보자. 그런 다음 `Box<T>`처럼 동작하는 커스텀 타입을 정의하고, 역참조 연산자가 새로 정의한 타입에서 참조처럼 동작하지 않는 이유를 알아볼 것이다. `Deref` 트레잇을 구현함으로써 스마트 포인터가 참조와 유사한 방식으로 동작할 수 있게 되는 과정을 탐구할 것이다. 마지막으로 Rust의 *역참조 강제 변환(deref coercion)* 기능과 이를 통해 참조나 스마트 포인터를 다루는 방법을 살펴볼 것이다.

> 참고: 우리가 만들 `MyBox<T>` 타입과 실제 `Box<T>` 사이에는 한 가지 큰 차이가 있다. 우리 버전은 데이터를 힙에 저장하지 않는다. 이 예제는 `Deref`에 초점을 맞추고 있으므로, 데이터가 실제로 어디에 저장되는지는 포인터와 같은 동작보다 덜 중요하다.


### 포인터를 따라가서 값에 접근하기

일반적인 참조는 일종의 포인터로, 포인터를 값이 저장된 위치를 가리키는 화살표로 생각할 수 있다. 리스트 15-6에서는 `i32` 값에 대한 참조를 생성한 후, 역참조 연산자를 사용해 참조를 따라가서 값에 접근한다.

<Listing number="15-6" file-name="src/main.rs" caption="역참조 연산자를 사용해 `i32` 값에 대한 참조를 따라가기">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-06/src/main.rs}}
```

</Listing>

변수 `x`는 `i32` 값 `5`를 가지고 있다. `y`를 `x`에 대한 참조로 설정한다. `x`가 `5`와 같다는 것을 확인할 수 있다. 하지만 `y`에 있는 값을 확인하려면 `*y`를 사용해 참조가 가리키는 값을 따라가야 한다(이를 _역참조_라고 한다). 이렇게 해야 컴파일러가 실제 값을 비교할 수 있다. `y`를 역참조하면 `y`가 가리키는 정수 값에 접근할 수 있고, 이를 `5`와 비교할 수 있다.

만약 `assert_eq!(5, y);`와 같이 작성하려고 했다면, 다음과 같은 컴파일 오류가 발생한다:

```console
{{#include ../listings/ch15-smart-pointers/output-only-01-comparing-to-reference/output.txt}}
```

숫자와 숫자에 대한 참조를 비교하는 것은 허용되지 않는다. 두 값은 서로 다른 타입이기 때문이다. 참조가 가리키는 값을 따라가기 위해 역참조 연산자를 사용해야 한다.


### `Box<T>`를 참조처럼 사용하기

Listing 15-6의 코드를 참조 대신 `Box<T>`를 사용하도록 다시 작성할 수 있다. Listing 15-7에서 `Box<T>`에 사용한 역참조 연산자는 Listing 15-6에서 참조에 사용한 역참조 연산자와 동일하게 작동한다.

<Listing number="15-7" file-name="src/main.rs" caption="`Box<i32>`에 역참조 연산자 사용하기">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-07/src/main.rs}}
```

</Listing>

Listing 15-7과 Listing 15-6의 주요 차이점은 여기서 `y`를 `x`의 값을 가리키는 참조 대신 `x`의 복사된 값을 가리키는 박스의 인스턴스로 설정한다는 것이다. 마지막 단언문에서 박스의 포인터를 따라가기 위해 역참조 연산자를 사용할 수 있으며, 이는 `y`가 참조였을 때와 동일한 방식이다. 다음으로, 역참조 연산자를 사용할 수 있게 해주는 `Box<T>`의 특별한 점을 우리만의 타입을 정의하며 알아볼 것이다.


### 커스텀 스마트 포인터 정의하기

표준 라이브러리에서 제공하는 `Box<T>` 타입과 유사한 스마트 포인터를 직접 만들어 보자. 이를 통해 스마트 포인터가 기본적으로 참조와 어떻게 다른 동작을 하는지 경험할 수 있다. 이후에는 역참조 연산자를 사용할 수 있도록 기능을 추가하는 방법을 알아볼 것이다.

`Box<T>` 타입은 결국 하나의 요소를 가진 튜플 구조체로 정의된다. 따라서 Listing 15-8에서도 동일한 방식으로 `MyBox<T>` 타입을 정의한다. 또한 `Box<T>`에 정의된 `new` 함수와 일치하도록 `new` 함수를 정의한다.

<Listing number="15-8" file-name="src/main.rs" caption="`MyBox<T>` 타입 정의">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-08/src/main.rs:here}}
```

</Listing>

`MyBox`라는 구조체를 정의하고, 어떤 타입의 값도 담을 수 있도록 제네릭 매개변수 `T`를 선언한다. `MyBox` 타입은 `T` 타입의 요소 하나를 가진 튜플 구조체다. `MyBox::new` 함수는 `T` 타입의 매개변수 하나를 받아, 전달된 값을 담은 `MyBox` 인스턴스를 반환한다.

Listing 15-7의 `main` 함수를 Listing 15-8에 추가하고, `Box<T>` 대신 우리가 정의한 `MyBox<T>` 타입을 사용하도록 수정해 보자. Listing 15-9의 코드는 Rust가 `MyBox`를 어떻게 역참조해야 할지 모르기 때문에 컴파일되지 않는다.

<Listing number="15-9" file-name="src/main.rs" caption="참조와 `Box<T>`를 사용한 것과 동일한 방식으로 `MyBox<T>` 사용 시도">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-09/src/main.rs:here}}
```

</Listing>

컴파일 결과는 다음과 같다:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-09/output.txt}}
```

`MyBox<T>` 타입은 역참조 기능을 구현하지 않았기 때문에 역참조할 수 없다. `*` 연산자를 사용해 역참조를 가능하게 하려면 `Deref` 트레잇을 구현해야 한다.

<!-- Old link, do not remove -->

<a id="treating-a-type-like-a-reference-by-implementing-the-deref-trait"></a>


### `Deref` 트레잇 구현하기

[10장 "타입에 트레잇 구현하기"][impl-trait]에서 다뤘듯이, 트레잇을 구현하려면 트레잇의 필수 메서드에 대한 구현을 제공해야 한다. 표준 라이브러리에서 제공하는 `Deref` 트레잇은 `self`를 빌려서 내부 데이터에 대한 참조를 반환하는 `deref` 메서드 하나를 구현하도록 요구한다. 리스트 15-10은 `MyBox<T>` 정의에 추가할 `Deref` 구현을 보여준다.

<Listing number="15-10" file-name="src/main.rs" caption="`MyBox<T>`에 `Deref` 구현하기">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-10/src/main.rs:here}}
```

</Listing>

`type Target = T;` 구문은 `Deref` 트레잇이 사용할 연관 타입을 정의한다. 연관 타입은 제네릭 매개변수를 선언하는 약간 다른 방식이지만, 지금은 걱정하지 않아도 된다. 20장에서 더 자세히 다룰 예정이다.

`deref` 메서드의 본문을 `&self.0`으로 채워서 `deref`가 `*` 연산자로 접근하려는 값에 대한 참조를 반환하도록 한다. [5장 "이름 없는 필드로 튜플 구조체를 사용해 다른 타입 만들기"][tuple-structs]에서 `.0`이 튜플 구조체의 첫 번째 값에 접근한다는 것을 떠올려보자. 리스트 15-9의 `main` 함수에서 `MyBox<T>` 값에 `*`를 호출하면 이제 컴파일이 되고, 단언문도 통과한다!

`Deref` 트레잇이 없으면 컴파일러는 `&` 참조만 역참조할 수 있다. `deref` 메서드는 컴파일러에게 `Deref`를 구현한 어떤 타입의 값을 가져와서 `deref` 메서드를 호출해 역참조 방법을 알고 있는 `&` 참조를 얻을 수 있는 능력을 제공한다.

리스트 15-9에서 `*y`를 입력했을 때, 러스트는 실제로 다음과 같은 코드를 실행한다:

```rust,ignore
*(y.deref())
```

러스트는 `*` 연산자를 `deref` 메서드 호출로 대체한 다음 일반 역참조를 수행한다. 따라서 우리는 `deref` 메서드를 호출해야 하는지 여부를 고민할 필요가 없다. 이 러스트 기능 덕분에 일반 참조를 사용하든 `Deref`를 구현한 타입을 사용하든 동일하게 작동하는 코드를 작성할 수 있다.

`deref` 메서드가 값에 대한 참조를 반환하고, `*(y.deref())`에서 괄호 밖의 일반 역참조가 여전히 필요한 이유는 소유권 시스템과 관련이 있다. `deref` 메서드가 값에 대한 참조 대신 값을 직접 반환하면 값이 `self`에서 이동된다. 이 경우나 대부분의 역참조 연산자 사용 사례에서 `MyBox<T>` 내부 값의 소유권을 가져오고 싶지는 않다.

`*` 연산자는 `deref` 메서드 호출로 대체된 다음 `*` 연산자 호출이 한 번만 이루어진다는 점에 유의하자. `*` 연산자의 대체가 무한히 재귀하지 않기 때문에 `i32` 타입의 데이터로 끝나며, 이는 리스트 15-9의 `assert_eq!`에서 `5`와 일치한다.


### 함수와 메서드에서의 암시적 Deref 강제 변환

_Deref 강제 변환_은 `Deref` 트레잇을 구현한 타입의 참조를 다른 타입의 참조로 변환한다. 예를 들어, `Deref` 강제 변환은 `&String`을 `&str`로 변환할 수 있다. 이는 `String`이 `Deref` 트레잇을 구현해 `&str`을 반환하기 때문이다. Deref 강제 변환은 함수와 메서드의 인자에 대해 Rust가 편의를 위해 수행하는 기능이며, `Deref` 트레잇을 구현한 타입에서만 동작한다. 이 변환은 함수나 메서드 정의에서 매개변수 타입과 일치하지 않는 특정 타입의 값에 대한 참조를 인자로 전달할 때 자동으로 발생한다. `deref` 메서드를 연속적으로 호출해 제공한 타입을 매개변수가 필요한 타입으로 변환한다.

Rust에 Deref 강제 변환이 추가된 이유는 함수와 메서드 호출을 작성할 때 프로그래머가 `&`와 `*`를 사용해 명시적으로 참조와 역참조를 추가하는 작업을 줄이기 위해서다. 또한 Deref 강제 변환 기능은 참조나 스마트 포인터 모두에 동작하는 코드를 더 많이 작성할 수 있게 해준다.

Deref 강제 변환이 실제로 어떻게 동작하는지 확인하기 위해, Listing 15-8에서 정의한 `MyBox<T>` 타입과 Listing 15-10에서 추가한 `Deref` 구현을 사용해 보자. Listing 15-11은 문자열 슬라이스 타입의 매개변수를 가진 함수의 정의를 보여준다.

<Listing number="15-11" file-name="src/main.rs" caption="`&str` 타입의 `name` 매개변수를 가진 `hello` 함수 정의">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-11/src/main.rs:here}}
```

</Listing>

예를 들어, `hello("Rust");`와 같이 문자열 슬라이스를 인자로 `hello` 함수를 호출할 수 있다. Deref 강제 변환 덕분에 `MyBox<String>` 타입의 값에 대한 참조를 사용해 `hello`를 호출할 수도 있다. 이는 Listing 15-12에서 확인할 수 있다.

<Listing number="15-12" file-name="src/main.rs" caption="Deref 강제 변환 덕분에 `MyBox<String>` 값에 대한 참조로 `hello` 호출하기">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-12/src/main.rs:here}}
```

</Listing>

여기서는 `&m`을 인자로 `hello` 함수를 호출한다. `&m`은 `MyBox<String>` 값에 대한 참조다. Listing 15-10에서 `MyBox<T>`에 `Deref` 트레잇을 구현했기 때문에, Rust는 `deref`를 호출해 `&MyBox<String>`을 `&String`으로 변환할 수 있다. 표준 라이브러리는 `String`에 대한 `Deref` 구현을 제공하며, 이는 문자열 슬라이스를 반환한다. 이 내용은 `Deref`의 API 문서에 나와 있다. Rust는 `deref`를 다시 호출해 `&String`을 `&str`로 변환하며, 이는 `hello` 함수의 정의와 일치한다.

만약 Rust가 Deref 강제 변환을 구현하지 않았다면, `&MyBox<String>` 타입의 값으로 `hello`를 호출하기 위해 Listing 15-13의 코드를 작성해야 했을 것이다.

<Listing number="15-13" file-name="src/main.rs" caption="Rust에 Deref 강제 변환이 없었다면 작성해야 했던 코드">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-13/src/main.rs:here}}
```

</Listing>

`(*m)`은 `MyBox<String>`을 `String`으로 역참조한다. 그런 다음 `&`와 `[..]`는 전체 문자열과 동일한 `String`의 문자열 슬라이스를 가져와 `hello`의 시그니처와 일치시킨다. Deref 강제 변환이 없다면 이 코드는 읽기, 작성하기, 이해하기 모두 더 어려워진다. Deref 강제 변환은 Rust가 이러한 변환을 자동으로 처리할 수 있게 해준다.

관련 타입에 대해 `Deref` 트레잇이 정의되어 있다면, Rust는 타입을 분석하고 `Deref::deref`를 필요한 만큼 호출해 매개변수의 타입과 일치하는 참조를 얻는다. `Deref::deref`를 삽입해야 하는 횟수는 컴파일 타임에 결정되므로, Deref 강제 변환을 활용해도 런타임 성능에 영향을 미치지 않는다!


### Deref 강제 변환과 가변성의 상호작용

불변 참조에서 `*` 연산자를 오버라이드하기 위해 `Deref` 트레잇을 사용하는 것과 유사하게, 가변 참조에서 `*` 연산자를 오버라이드하기 위해 `DerefMut` 트레잇을 사용할 수 있다.

Rust는 세 가지 경우에 타입과 트레잇 구현을 발견할 때 Deref 강제 변환을 수행한다:

1. `&T`에서 `&U`로 변환. 이때 `T: Deref<Target=U>` 조건을 만족한다.
2. `&mut T`에서 `&mut U`로 변환. 이때 `T: DerefMut<Target=U>` 조건을 만족한다.
3. `&mut T`에서 `&U`로 변환. 이때 `T: Deref<Target=U>` 조건을 만족한다.

첫 번째와 두 번째 경우는 가변성 구현 여부만 다르고 나머지는 동일하다. 첫 번째 경우는 `&T`가 있고 `T`가 `Deref`를 구현하여 어떤 타입 `U`로 변환될 수 있다면, `&U`를 투명하게 얻을 수 있다는 것을 의미한다. 두 번째 경우는 가변 참조에 대해 동일한 Deref 강제 변환이 일어난다는 것을 나타낸다.

세 번째 경우는 더 복잡하다: Rust는 가변 참조를 불변 참조로도 강제 변환한다. 하지만 그 반대는 **불가능**하다: 불변 참조는 절대 가변 참조로 강제 변환되지 않는다. 빌림 규칙에 따라, 가변 참조가 있다면 그 가변 참조는 해당 데이터에 대한 유일한 참조여야 한다(그렇지 않으면 프로그램이 컴파일되지 않는다). 하나의 가변 참조를 하나의 불변 참조로 변환하는 것은 빌림 규칙을 절대 위반하지 않는다. 그러나 불변 참조를 가변 참조로 변환하려면 초기 불변 참조가 해당 데이터에 대한 유일한 불변 참조여야 하는데, 빌림 규칙이 이를 보장하지 않는다. 따라서 Rust는 불변 참조를 가변 참조로 변환하는 것이 가능하다고 가정할 수 없다.

[impl-trait]: ch10-02-traits.html#implementing-a-trait-on-a-type
[tuple-structs]: ch05-01-defining-structs.html#using-tuple-structs-without-named-fields-to-create-different-types


