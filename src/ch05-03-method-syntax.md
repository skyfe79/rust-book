## 메서드 문법

메서드는 함수와 유사하다. `fn` 키워드와 이름을 사용해 선언하고, 매개변수와 반환 값을 가질 수 있으며, 다른 곳에서 호출될 때 실행될 코드를 포함한다. 함수와 달리 메서드는 구조체의 컨텍스트 내에서 정의된다(또는 열거형이나 트레잇 객체 내에서 정의될 수 있으며, 이에 대해서는 각각 [6장][enums]<!-- ignore -->과 [18장][trait-objects]<!-- ignore -->에서 다룬다). 그리고 메서드의 첫 번째 매개변수는 항상 `self`이며, 이는 메서드가 호출된 구조체의 인스턴스를 나타낸다.


### 메서드 정의하기

`Rectangle` 인스턴스를 매개변수로 받는 `area` 함수를 변경해 `Rectangle` 구조체에 정의된 `area` 메서드로 만들어 보자. 이 내용은 리스트 5-13에 나와 있다.

<Listing number="5-13" file-name="src/main.rs" caption="`Rectangle` 구조체에 `area` 메서드 정의하기">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-13/src/main.rs}}
```

</Listing>

`Rectangle`의 컨텍스트 내에서 함수를 정의하려면 `Rectangle`에 대한 `impl`(구현) 블록을 시작한다. 이 `impl` 블록 내의 모든 것은 `Rectangle` 타입과 연관된다. 그런 다음 `area` 함수를 `impl`의 중괄호 안으로 이동시키고, 시그니처와 본문 내의 첫 번째(이 경우 유일한) 매개변수를 `self`로 변경한다. `main` 함수에서는 `area` 함수를 호출하고 `rect1`을 인자로 전달했던 부분을, 이제는 _메서드 문법_ 을 사용해 `Rectangle` 인스턴스의 `area` 메서드를 호출하도록 변경할 수 있다. 메서드 문법은 인스턴스 뒤에 온다: 점(.)을 추가한 후 메서드 이름, 괄호, 그리고 필요한 인자를 적는다.

`area`의 시그니처에서 `rectangle: &Rectangle` 대신 `&self`를 사용한다. `&self`는 실제로 `self: &Self`의 축약형이다. `impl` 블록 내에서 `Self` 타입은 `impl` 블록이 적용되는 타입의 별칭이다. 메서드는 첫 번째 매개변수로 `Self` 타입의 `self`를 가져야 하므로, Rust는 첫 번째 매개변수 위치에 단순히 `self`만 적어도 되도록 허용한다. 여전히 `self` 앞에 `&`를 사용해 이 메서드가 `Self` 인스턴스를 빌린다는 것을 나타내야 한다. 이는 `rectangle: &Rectangle`에서와 동일하다. 메서드는 `self`의 소유권을 가져갈 수도 있고, 여기서처럼 불변으로 빌릴 수도 있으며, 가변으로 빌릴 수도 있다. 이는 다른 매개변수와 동일하다.

여기서 `&self`를 선택한 이유는 함수 버전에서 `&Rectangle`을 사용한 이유와 동일하다: 소유권을 가져가고 싶지 않으며, 구조체의 데이터를 읽기만 하고 쓰지는 않기 때문이다. 만약 메서드가 호출된 인스턴스를 변경하고 싶다면 첫 번째 매개변수로 `&mut self`를 사용한다. 단순히 `self`를 첫 번째 매개변수로 사용해 인스턴스의 소유권을 가져가는 메서드는 드물다; 이 기법은 보통 메서드가 `self`를 다른 것으로 변환하고, 변환 후에 원본 인스턴스를 사용하지 못하게 하려는 경우에 사용된다.

메서드를 함수 대신 사용하는 주요 이유는 메서드 문법을 제공하고, 모든 메서드의 시그니처에서 `self`의 타입을 반복하지 않아도 되기 때문이다. 또한, 코드를 조직화하는 데에도 도움이 된다. 우리는 타입의 인스턴스로 할 수 있는 모든 작업을 하나의 `impl` 블록에 넣어, 나중에 우리가 제공한 라이브러리에서 `Rectangle`의 기능을 찾기 위해 여러 곳을 헤매지 않도록 했다.

메서드 이름을 구조체 필드와 동일하게 지을 수도 있다. 예를 들어, `Rectangle`에 `width`라는 메서드를 정의할 수 있다:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-06-method-field-interaction/src/main.rs:here}}
```

</Listing>

여기서는 `width` 메서드가 인스턴스의 `width` 필드 값이 `0`보다 크면 `true`를 반환하고, `0`이면 `false`를 반환하도록 했다: 동일한 이름의 필드를 메서드 내에서 어떤 목적으로든 사용할 수 있다. `main` 함수에서 `rect1.width` 뒤에 괄호를 붙이면 Rust는 `width` 메서드를 의미한다고 이해한다. 괄호를 사용하지 않으면 Rust는 `width` 필드를 의미한다고 이해한다.

종종, 항상은 아니지만, 메서드 이름을 필드와 동일하게 지을 때는 필드의 값을 반환만 하고 다른 작업을 하지 않도록 하는 경우가 많다. 이런 메서드를 _getter_ 라고 부르며, Rust는 다른 언어와 달리 구조체 필드에 대해 자동으로 getter를 구현하지 않는다. Getter는 필드를 private로 만들고 메서드를 public으로 만들어, 타입의 public API의 일부로 해당 필드에 대한 읽기 전용 접근을 허용할 때 유용하다. public과 private이 무엇인지, 그리고 필드나 메서드를 public 또는 private으로 지정하는 방법은 [7장][public]<!-- ignore -->에서 다룬다.

> ### `->` 연산자는 어디에 있나요?
>
> C와 C++에서는 메서드를 호출할 때 두 가지 다른 연산자를 사용한다: 객체에 직접 메서드를 호출할 때는 `.`를 사용하고, 객체에 대한 포인터에서 메서드를 호출할 때는 `->`를 사용해 포인터를 먼저 역참조한다. 즉, `object`가 포인터라면 `object->something()`은 `(*object).something()`과 유사하다.
>
> Rust는 `->` 연산자에 해당하는 것이 없다; 대신 Rust에는 _자동 참조 및 역참조_ 라는 기능이 있다. 메서드 호출은 Rust에서 이 동작이 적용되는 몇 안 되는 경우 중 하나다.
>
> 이 기능은 다음과 같이 동작한다: `object.something()`으로 메서드를 호출할 때, Rust는 자동으로 `&`, `&mut`, 또는 `*`를 추가해 `object`가 메서드의 시그니처와 일치하도록 한다. 즉, 다음 두 코드는 동일하다:
>
> <!-- CAN'T EXTRACT SEE BUG https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust
> # #[derive(Debug,Copy,Clone)]
> # struct Point {
> #     x: f64,
> #     y: f64,
> # }
> #
> # impl Point {
> #    fn distance(&self, other: &Point) -> f64 {
> #        let x_squared = f64::powi(other.x - self.x, 2);
> #        let y_squared = f64::powi(other.y - self.y, 2);
> #
> #        f64::sqrt(x_squared + y_squared)
> #    }
> # }
> # let p1 = Point { x: 0.0, y: 0.0 };
> # let p2 = Point { x: 5.0, y: 6.5 };
> p1.distance(&p2);
> (&p1).distance(&p2);
> ```
>
> 첫 번째 코드가 훨씬 깔끔해 보인다. 이 자동 참조 동작은 메서드가 명확한 수신자(`self`의 타입)를 가지고 있기 때문에 가능하다. 수신자와 메서드 이름이 주어지면 Rust는 메서드가 읽기(`&self`), 변경(`&mut self`), 또는 소비(`self`) 중 어떤 작업을 하는지 명확히 파악할 수 있다. Rust가 메서드 수신자에 대한 빌림을 암묵적으로 처리하는 것은 소유권을 실용적으로 만드는 데 큰 역할을 한다.


### 추가 매개변수를 가진 메서드

`Rectangle` 구조체에 두 번째 메서드를 구현하며 메서드 사용법을 연습해 보자. 이번에는 `Rectangle` 인스턴스가 다른 `Rectangle` 인스턴스를 받아서 두 번째 `Rectangle`이 `self`(첫 번째 `Rectangle`) 안에 완전히 들어갈 수 있으면 `true`를 반환하고, 그렇지 않으면 `false`를 반환하도록 한다. 즉, `can_hold` 메서드를 정의한 후에는 아래 예제와 같은 프로그램을 작성할 수 있어야 한다.

<Listing number="5-14" file-name="src/main.rs" caption="아직 작성되지 않은 `can_hold` 메서드 사용 예제">

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-14/src/main.rs}}
```

</Listing>

`rect2`의 두 차원 모두 `rect1`보다 작지만, `rect3`은 `rect1`보다 넓기 때문에 예상 출력은 다음과 같다:

```text
Can rect1 hold rect2? true
Can rect1 hold rect3? false
```

메서드를 정의할 것이므로 `impl Rectangle` 블록 안에 작성한다. 메서드 이름은 `can_hold`로 정하고, 다른 `Rectangle` 인스턴스를 불변 참조로 받을 것이다. 메서드를 호출하는 코드를 보면 매개변수의 타입을 알 수 있다: `rect1.can_hold(&rect2)`에서 `&rect2`를 전달하며, 이는 `Rectangle` 인스턴스인 `rect2`의 불변 참조다. 이는 `rect2`를 읽기만 하면 되고(쓰기는 필요하지 않으므로 가변 참조가 필요하지 않음), `can_hold` 메서드 호출 후에도 `main` 함수가 `rect2`의 소유권을 유지할 수 있도록 하기 때문이다. `can_hold`의 반환 값은 불리언 타입이며, 구현에서는 `self`의 너비와 높이가 다른 `Rectangle`의 너비와 높이보다 각각 큰지 확인한다. 이제 `can_hold` 메서드를 `impl` 블록에 추가해 보자.

<Listing number="5-15" file-name="src/main.rs" caption="`Rectangle`에 `can_hold` 메서드 구현">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-15/src/main.rs:here}}
```

</Listing>

Listing 5-14의 `main` 함수와 함께 이 코드를 실행하면 원하는 출력을 얻을 수 있다. 메서드는 `self` 매개변수 뒤에 추가 매개변수를 받을 수 있으며, 이 매개변수들은 함수의 매개변수와 동일하게 동작한다.


### 연관 함수

`impl` 블록 내에 정의된 모든 함수는 _연관 함수_라고 한다. 이 함수들은 `impl` 뒤에 명시된 타입과 연관되어 있기 때문이다. `self`를 첫 번째 매개변수로 가지지 않는 연관 함수도 정의할 수 있다. 이런 함수는 메서드가 아니며, 타입의 인스턴스가 필요하지 않다. 이미 이런 함수를 사용한 적이 있다. 바로 `String` 타입에 정의된 `String::from` 함수가 그 예시다.

메서드가 아닌 연관 함수는 주로 새로운 구조체 인스턴스를 반환하는 생성자로 사용된다. 이런 함수는 보통 `new`라고 이름 짓지만, `new`는 특별한 이름이 아니며 언어에 내장된 기능도 아니다. 예를 들어, `square`라는 연관 함수를 정의할 수 있다. 이 함수는 하나의 차원 매개변수를 받아 너비와 높이로 사용하며, 정사각형 `Rectangle`을 쉽게 생성할 수 있게 해준다. 이렇게 하면 같은 값을 두 번 지정할 필요가 없다:

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-03-associated-functions/src/main.rs:here}}
```

함수의 반환 타입과 본문에서 사용된 `Self` 키워드는 `impl` 뒤에 오는 타입의 별칭이다. 이 경우에는 `Rectangle`이다.

이 연관 함수를 호출하려면 구조체 이름과 `::` 문법을 사용한다. 예를 들어 `let sq = Rectangle::square(3);`와 같이 호출할 수 있다. 이 함수는 구조체에 의해 네임스페이스가 지정된다. `::` 문법은 연관 함수와 모듈에 의해 생성된 네임스페이스에 모두 사용된다. 모듈에 대해서는 [7장][modules]<!-- ignore -->에서 자세히 다룬다.


### 여러 개의 `impl` 블록

각 구조체는 여러 개의 `impl` 블록을 가질 수 있다. 예를 들어, 리스트 5-15는 각 메서드를 별도의 `impl` 블록에 나눈 리스트 5-16과 동일한 코드다.

<Listing number="5-16" caption="여러 개의 `impl` 블록을 사용해 리스트 5-15를 다시 작성">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-16/src/main.rs:here}}
```

</Listing>

여기서는 이 메서드들을 여러 `impl` 블록으로 나눌 필요가 없지만, 문법적으로 유효한 방식이다. 제네릭 타입과 트레이트를 다루는 10장에서 여러 `impl` 블록이 유용한 경우를 살펴볼 것이다.


## 요약

구조체를 사용하면 특정 도메인에 의미 있는 커스텀 타입을 만들 수 있다. 구조체를 통해 서로 연관된 데이터를 하나로 묶고, 각 데이터에 이름을 붙여 코드의 가독성을 높일 수 있다. `impl` 블록에서는 해당 타입과 연관된 함수를 정의할 수 있으며, 메서드는 구조체의 인스턴스가 가질 동작을 지정하는 연관 함수의 한 종류이다.

하지만 구조체만이 커스텀 타입을 만드는 유일한 방법은 아니다. 이제 Rust의 열거형(enum) 기능을 살펴보며 도구 상자에 또 하나의 유용한 도구를 추가해 보자.

[enums]: ch06-00-enums.html
[trait-objects]: ch18-02-trait-objects.md
[public]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html


