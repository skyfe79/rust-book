## 고급 타입

Rust의 타입 시스템에는 지금까지 언급만 하고 자세히 다루지 않은 몇 가지 기능이 있다. 먼저 뉴타입(newtype)의 일반적인 개념을 살펴보고, 왜 뉴타입이 유용한 타입인지 알아본다. 그런 다음 뉴타입과 유사하지만 약간 다른 의미를 가진 타입 별칭(type alias)에 대해 설명한다. 마지막으로 `!` 타입과 동적 크기 타입(dynamically sized types)에 대해 논의한다.


### 타입 안전성과 추상화를 위한 뉴타입 패턴 사용

이 섹션을 읽기 전에 이전 섹션인 [“외부 타입에 외부 트레이트를 구현하기 위해 뉴타입 패턴 사용”][using-the-newtype-pattern]<!-- ignore -->을 먼저 읽었다고 가정한다. 뉴타입 패턴은 지금까지 논의한 내용 외에도, 값이 혼동되지 않도록 정적으로 강제하거나 값의 단위를 나타내는 데 유용하다. 리스트 20-16에서 뉴타입을 사용해 단위를 나타내는 예제를 살펴보았다: `Millimeters`와 `Meters` 구조체가 `u32` 값을 뉴타입으로 감싸는 것을 기억할 것이다. 만약 `Millimeters` 타입의 매개변수를 받는 함수를 작성했다면, 실수로 `Meters` 타입이나 일반 `u32` 값으로 이 함수를 호출하려는 프로그램은 컴파일되지 않는다.

또한 뉴타입 패턴을 사용해 타입의 구현 세부 사항을 추상화할 수도 있다: 새로운 타입은 내부 타입의 API와 다른 공개 API를 노출할 수 있다.

뉴타입은 내부 구현을 숨기는 데에도 사용할 수 있다. 예를 들어, `People` 타입을 제공해 `HashMap<i32, String>`을 감싸고, 여기서 사람의 ID와 이름을 연결하여 저장할 수 있다. `People`을 사용하는 코드는 우리가 제공하는 공개 API와만 상호작용할 것이다. 예를 들어, `People` 컬렉션에 이름 문자열을 추가하는 메서드가 있을 수 있다. 이 코드는 내부적으로 이름에 `i32` ID를 할당한다는 사실을 알 필요가 없다. 뉴타입 패턴은 구현 세부 사항을 숨기기 위한 가벼운 캡슐화 방법이다. 이는 18장의 [“구현 세부 사항을 숨기는 캡슐화”][encapsulation-that-hides-implementation-details]<!-- ignore -->에서 논의한 내용과 일맥상통한다.


### 타입 별칭을 사용해 타입 동의어 만들기

Rust는 기존 타입에 다른 이름을 붙일 수 있는 _타입 별칭_을 선언할 수 있는 기능을 제공한다. 이를 위해 `type` 키워드를 사용한다. 예를 들어, `i32` 타입에 `Kilometers`라는 별칭을 다음과 같이 만들 수 있다:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:here}}
```

이제 `Kilometers`는 `i32`의 _동의어_가 된다. Listing 20-16에서 만든 `Millimeters`와 `Meters` 타입과 달리, `Kilometers`는 별도의 새로운 타입이 아니다. `Kilometers` 타입의 값은 `i32` 타입의 값과 동일하게 처리된다:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:there}}
```

`Kilometers`와 `i32`는 동일한 타입이므로, 두 타입의 값을 더할 수 있고, `i32` 타입의 매개변수를 받는 함수에 `Kilometers` 값을 전달할 수도 있다. 그러나 이 방법을 사용하면 앞서 설명한 newtype 패턴에서 얻을 수 있는 타입 검사 이점을 얻을 수 없다. 즉, `Kilometers`와 `i32` 값을 혼용하더라도 컴파일러는 에러를 발생시키지 않는다.

타입 별칭의 주요 사용 사례는 반복을 줄이는 것이다. 예를 들어, 다음과 같이 길고 복잡한 타입이 있을 수 있다:

```rust,ignore
Box<dyn Fn() + Send + 'static>
```

이렇게 긴 타입을 함수 시그니처나 타입 어노테이션에 반복적으로 작성하는 것은 지루하고 오류가 발생하기 쉽다. Listing 20-25와 같은 코드가 프로젝트 전체에 걸쳐 있다고 상상해 보자.

<Listing number="20-25" caption="긴 타입을 여러 곳에서 사용하는 예">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-25/src/main.rs:here}}
```

</Listing>

타입 별칭을 사용하면 반복을 줄여 코드를 더 관리하기 쉽게 만들 수 있다. Listing 20-26에서는 `Thunk`라는 별칭을 도입하여 긴 타입을 더 짧은 별칭 `Thunk`로 대체했다.

<Listing number="20-26" caption="타입 별칭 `Thunk`를 도입해 반복을 줄이는 예">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-26/src/main.rs:here}}
```

</Listing>

이 코드는 훨씬 읽고 쓰기 쉬워졌다! 타입 별칭에 의미 있는 이름을 선택하면 의도를 더 명확히 전달할 수도 있다 (_thunk_는 나중에 평가될 코드를 의미하는 단어이므로, 저장된 클로저에 적합한 이름이다).

타입 별칭은 `Result<T, E>` 타입과 함께 사용되어 반복을 줄이는 데에도 흔히 사용된다. 표준 라이브러리의 `std::io` 모듈을 생각해 보자. I/O 작업은 종종 작업이 실패할 경우를 처리하기 위해 `Result<T, E>`를 반환한다. 이 라이브러리에는 모든 가능한 I/O 오류를 나타내는 `std::io::Error` 구조체가 있다. `std::io`의 많은 함수들은 `E`가 `std::io::Error`인 `Result<T, E>`를 반환한다. 예를 들어, `Write` 트레이트의 함수들은 다음과 같다:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-05-write-trait/src/lib.rs}}
```

`Result<..., Error>`가 반복적으로 사용된다. 따라서 `std::io`는 다음과 같은 타입 별칭을 선언한다:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:here}}
```

이 선언이 `std::io` 모듈에 있으므로, `std::io::Result<T>`라는 완전한 별칭을 사용할 수 있다. 즉, `E`가 `std::io::Error`로 채워진 `Result<T, E>`이다. `Write` 트레이트의 함수 시그니처는 다음과 같이 된다:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:there}}
```

타입 별칭은 두 가지 방식으로 도움을 준다: 코드를 더 쉽게 작성할 수 있게 하고, `std::io` 전체에 걸쳐 일관된 인터페이스를 제공한다. 별칭이기 때문에 여전히 `Result<T, E>`이며, 따라서 `Result<T, E>`에서 동작하는 모든 메서드와 `?` 연산자와 같은 특별한 문법을 사용할 수 있다.


### 값을 반환하지 않는 Never 타입

Rust에는 `!`라는 특별한 타입이 있다. 타입 이론에서는 이를 _빈 타입(empty type)_이라고 부르는데, 이 타입은 어떤 값도 가질 수 없기 때문이다. 하지만 우리는 이 타입을 _never 타입_이라고 부르는 것을 선호한다. 이 타입은 함수가 값을 반환하지 않을 때 반환 타입 자리에 위치하기 때문이다. 다음은 그 예시이다:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-07-never-type/src/lib.rs:here}}
```

이 코드는 "함수 `bar`는 never를 반환한다"고 읽을 수 있다. never를 반환하는 함수는 _발산 함수(diverging functions)_라고 불린다. `!` 타입의 값을 생성할 수 없기 때문에 `bar`는 절대 값을 반환할 수 없다.

그렇다면 값을 생성할 수 없는 타입은 왜 필요할까? 2장에서 다룬 숫자 맞추기 게임의 코드를 떠올려보자. 여기서는 그 중 일부를 다시 살펴본다.

<Listing number="20-27" caption="`continue`로 끝나는 `match` 구문">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:ch19}}
```

</Listing>

당시 이 코드의 몇 가지 세부 사항을 건너뛰었다. 6장의 ["`match` 제어 흐름 연산자"][the-match-control-flow-operator]<!-- ignore -->에서 `match` 구문의 모든 패턴은 동일한 타입을 반환해야 한다고 설명했다. 예를 들어, 다음 코드는 동작하지 않는다:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-08-match-arms-different-types/src/main.rs:here}}
```

이 코드에서 `guess`의 타입은 정수 _이면서_ 문자열이어야 하지만, Rust는 `guess`가 단일 타입을 가져야 한다고 요구한다. 그렇다면 `continue`는 무엇을 반환할까? Listing 20-27에서 한 패턴은 `u32`를 반환하고 다른 패턴은 `continue`로 끝나는데, 어떻게 이 코드가 유효할까?

추측할 수 있듯이, `continue`는 `!` 값을 가진다. 즉, Rust가 `guess`의 타입을 계산할 때, 두 패턴을 모두 살펴보는데, 하나는 `u32` 값을 가지고 다른 하나는 `!` 값을 가진다. `!`는 값을 가질 수 없기 때문에 Rust는 `guess`의 타입을 `u32`로 결정한다.

이 동작을 공식적으로 설명하면, `!` 타입의 표현식은 다른 어떤 타입으로도 강제 변환될 수 있다. `match` 패턴을 `continue`로 끝낼 수 있는 이유는 `continue`가 값을 반환하지 않고, 대신 루프의 시작으로 제어를 이동시키기 때문이다. 따라서 `Err` 경우에는 `guess`에 값을 할당하지 않는다.

never 타입은 `panic!` 매크로와도 유용하게 사용된다. `Option<T>` 값에 대해 `unwrap` 함수를 호출하면 값을 생성하거나 패닉을 일으키는데, 그 정의는 다음과 같다:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-09-unwrap-definition/src/lib.rs:here}}
```

이 코드에서 Listing 20-27의 `match` 구문과 동일한 일이 발생한다: Rust는 `val`이 `T` 타입이고 `panic!`이 `!` 타입임을 확인한 후, 전체 `match` 표현식의 결과를 `T`로 결정한다. 이 코드는 `panic!`이 값을 생성하지 않고 프로그램을 종료하기 때문에 유효하다. `None` 경우에는 `unwrap`에서 값을 반환하지 않으므로 이 코드는 정상적으로 동작한다.

마지막으로 `!` 타입을 가지는 표현식은 `loop`이다:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-10-loop-returns-never/src/main.rs:here}}
```

여기서 루프는 절대 끝나지 않으므로 `!`가 표현식의 값이다. 하지만 `break`를 포함한다면 이는 성립하지 않는다. `break`에 도달하면 루프가 종료되기 때문이다.


### 동적 크기 타입과 `Sized` 트레잇

Rust는 특정 타입의 값에 얼마나 많은 공간을 할당해야 하는지와 같은 세부 사항을 알아야 한다. 이 때문에 타입 시스템의 한 부분이 처음에는 조금 혼란스러울 수 있다: 바로 _동적 크기 타입(Dynamically Sized Types, DST)_의 개념이다. 이 타입은 _DSTs_ 또는 _unsized types_라고도 불리며, 런타임에만 크기를 알 수 있는 값을 사용해 코드를 작성할 수 있게 해준다.

이 책 전반에서 사용해 온 `str` 타입을 예로 들어 동적 크기 타입의 세부 사항을 살펴보자. `&str`이 아니라 `str` 자체가 DST라는 점에 주목하자. 런타임에만 문자열의 길이를 알 수 있기 때문에, `str` 타입의 변수를 만들거나 `str` 타입의 인자를 받을 수 없다. 다음 코드는 동작하지 않는다:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-11-cant-create-str/src/main.rs:here}}
```

Rust는 특정 타입의 값에 얼마나 많은 메모리를 할당해야 하는지 알아야 하며, 동일한 타입의 모든 값은 동일한 양의 메모리를 사용해야 한다. 만약 Rust가 이 코드를 허용한다면, 두 `str` 값은 동일한 크기의 공간을 차지해야 한다. 하지만 이들의 길이는 다르다: `s1`은 12바이트를 필요로 하고, `s2`는 15바이트를 필요로 한다. 이 때문에 동적 크기 타입을 담는 변수를 만들 수 없다.

그렇다면 어떻게 해야 할까? 이 경우 이미 답을 알고 있을 것이다: `s1`과 `s2`의 타입을 `str` 대신 `&str`로 만드는 것이다. [4장의 "문자열 슬라이스"][string-slices]<!-- ignore -->에서 슬라이스 데이터 구조는 단지 시작 위치와 슬라이스의 길이만 저장한다는 것을 기억할 것이다. 따라서 `&T`는 `T`가 위치한 메모리 주소를 저장하는 단일 값이지만, `&str`은 _두_ 값을 저장한다: `str`의 주소와 그 길이. 이 때문에 `&str` 값의 크기를 컴파일 타임에 알 수 있다: `usize` 길이의 두 배다. 즉, `&str`이 참조하는 문자열의 길이가 얼마나 길든 상관없이 `&str`의 크기는 항상 알 수 있다. 일반적으로 Rust에서 동적 크기 타입을 사용하는 방식은 이렇다: 동적 정보의 크기를 저장하는 추가 메타데이터를 가지고 있다. 동적 크기 타입의 황금 법칙은 동적 크기 타입의 값을 항상 어떤 종류의 포인터 뒤에 두어야 한다는 것이다.

`str`을 다양한 포인터와 함께 사용할 수 있다: 예를 들어, `Box<str>`이나 `Rc<str>` 등이 있다. 사실, 이전에 다른 동적 크기 타입으로 이를 본 적이 있다: 트레잇이다. 모든 트레잇은 동적 크기 타입이며, 트레잇의 이름을 사용해 참조할 수 있다. [18장의 "서로 다른 타입의 값을 허용하는 트레잇 객체 사용"][using-trait-objects-that-allow-for-values-of-different-types]<!-- ignore -->에서 트레잇을 트레잇 객체로 사용하려면 `&dyn Trait`이나 `Box<dyn Trait>` (`Rc<dyn Trait>`도 가능)과 같은 포인터 뒤에 두어야 한다고 언급했다.

DST를 다루기 위해 Rust는 `Sized` 트레잇을 제공한다. 이 트레잇은 타입의 크기가 컴파일 타임에 알려져 있는지 여부를 결정한다. 이 트레잇은 크기가 컴파일 타임에 알려진 모든 타입에 대해 자동으로 구현된다. 또한 Rust는 모든 제네릭 함수에 `Sized` 바운드를 암묵적으로 추가한다. 즉, 다음과 같은 제네릭 함수 정의는:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-12-generic-fn-definition/src/lib.rs}}
```

실제로는 다음과 같이 작성된 것처럼 처리된다:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-13-generic-implicit-sized-bound/src/lib.rs}}
```

기본적으로 제네릭 함수는 컴파일 타임에 크기가 알려진 타입에 대해서만 동작한다. 하지만 다음과 같은 특수 문법을 사용해 이 제한을 완화할 수 있다:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-14-generic-maybe-sized/src/lib.rs}}
```

`?Sized` 트레잇 바운드는 "`T`가 `Sized`일 수도 있고 아닐 수도 있다"는 의미이며, 이 표기법은 제네릭 타입이 컴파일 타임에 크기가 알려져야 한다는 기본 설정을 재정의한다. 이 의미의 `?Trait` 문법은 `Sized`에만 사용할 수 있으며, 다른 트레잇에는 사용할 수 없다.

또한 `t` 매개변수의 타입을 `T`에서 `&T`로 변경했다. 타입이 `Sized`가 아닐 수 있기 때문에, 어떤 종류의 포인터 뒤에 두어야 한다. 이 경우 참조를 선택했다.

다음으로 함수와 클로저에 대해 이야기할 것이다!

[encapsulation-that-hides-implementation-details]: ch18-01-what-is-oo.html#encapsulation-that-hides-implementation-details
[string-slices]: ch04-03-slices.html#string-slices
[the-match-control-flow-operator]: ch06-02-match.html#the-match-control-flow-operator
[using-trait-objects-that-allow-for-values-of-different-types]: ch18-02-trait-objects.html#using-trait-objects-that-allow-for-values-of-different-types
[using-the-newtype-pattern]: ch20-02-advanced-traits.html#using-the-newtype-pattern-to-implement-external-traits-on-external-types


