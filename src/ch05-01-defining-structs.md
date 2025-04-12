## 구조체 정의와 인스턴스 생성

구조체는 [“튜플 타입”][tuples]<!--
ignore --> 섹션에서 다룬 튜플과 유사하게, 여러 관련 값을 함께 담는다. 튜플과 마찬가지로 구조체의 각 부분은 서로 다른 타입을 가질 수 있다. 하지만 튜플과 달리, 구조체에서는 각 데이터 조각에 이름을 붙여 값의 의미를 명확히 할 수 있다. 이러한 이름 덕분에 구조체는 튜플보다 더 유연하다. 인스턴스의 값을 지정하거나 접근할 때 데이터의 순서에 의존할 필요가 없다.

구조체를 정의하려면 `struct` 키워드를 사용하고 구조체 전체에 이름을 붙인다. 구조체의 이름은 함께 그룹화된 데이터 조각의 의미를 잘 설명해야 한다. 그런 다음 중괄호 안에 데이터 조각의 이름과 타입을 정의하는데, 이를 _필드_라고 부른다. 예를 들어, Listing 5-1은 사용자 계정 정보를 저장하는 구조체를 보여준다.

<Listing number="5-1" file-name="src/main.rs" caption="`User` 구조체 정의">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-01/src/main.rs:here}}
```

</Listing>

구조체를 정의한 후에는 각 필드에 구체적인 값을 지정해 구조체의 _인스턴스_를 생성한다. 구조체의 이름을 명시한 다음 중괄호 안에 _`키: 값`_ 쌍을 추가해 인스턴스를 만든다. 여기서 키는 필드의 이름이고, 값은 해당 필드에 저장할 데이터이다. 필드는 구조체에서 선언한 순서와 동일하게 지정할 필요는 없다. 즉, 구조체 정의는 타입에 대한 일반적인 템플릿 역할을 하고, 인스턴스는 이 템플릿에 특정 데이터를 채워 타입의 값을 생성한다. 예를 들어, Listing 5-2와 같이 특정 사용자를 선언할 수 있다.

<Listing number="5-2" file-name="src/main.rs" caption="`User` 구조체의 인스턴스 생성">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-02/src/main.rs:here}}
```

</Listing>

구조체에서 특정 값을 가져오려면 점 표기법을 사용한다. 예를 들어, 이 사용자의 이메일 주소에 접근하려면 `user1.email`을 사용한다. 인스턴스가 가변적이라면, 점 표기법을 사용해 특정 필드에 값을 할당하여 값을 변경할 수 있다. Listing 5-3은 가변 `User` 인스턴스의 `email` 필드 값을 변경하는 방법을 보여준다.

<Listing number="5-3" file-name="src/main.rs" caption="`User` 인스턴스의 `email` 필드 값 변경">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-03/src/main.rs:here}}
```

</Listing>

전체 인스턴스가 가변적이어야 한다는 점에 유의한다. Rust는 특정 필드만 가변적으로 표시하는 것을 허용하지 않는다. 다른 표현식과 마찬가지로, 함수 본문의 마지막 표현식으로 구조체의 새 인스턴스를 생성해 암묵적으로 새 인스턴스를 반환할 수 있다.

Listing 5-4는 주어진 이메일과 사용자 이름으로 `User` 인스턴스를 반환하는 `build_user` 함수를 보여준다. `active` 필드는 `true` 값을, `sign_in_count` 필드는 `1` 값을 가진다.

<Listing number="5-4" file-name="src/main.rs" caption="이메일과 사용자 이름을 받아 `User` 인스턴스를 반환하는 `build_user` 함수">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-04/src/main.rs:here}}
```

</Listing>

함수 매개변수의 이름을 구조체 필드와 동일하게 짓는 것이 합리적이지만, `email`과 `username` 필드 이름과 변수를 반복해야 하는 것은 다소 지루할 수 있다. 구조체에 더 많은 필드가 있다면, 각 이름을 반복하는 것이 더 번거로울 것이다. 다행히 편리한 단축 문법이 있다!

<!-- Old heading. Do not remove or links may break. -->

<a id="using-the-field-init-shorthand-when-variables-and-fields-have-the-same-name"></a>


### 필드 초기화 축약 문법 사용하기

리스트 5-4에서 매개변수 이름과 구조체 필드 이름이 정확히 동일하기 때문에, _필드 초기화 축약 문법_을 사용해 `build_user` 함수를 다시 작성할 수 있다. 이렇게 하면 동일한 동작을 유지하면서 `username`과 `email`의 반복을 줄일 수 있다. 리스트 5-5에서 이를 확인할 수 있다.

<Listing number="5-5" file-name="src/main.rs" caption="`username`과 `email` 매개변수가 구조체 필드와 동일한 이름을 가지고 있어 필드 초기화 축약 문법을 사용한 `build_user` 함수">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-05/src/main.rs:here}}
```

</Listing>

여기서는 `User` 구조체의 새 인스턴스를 생성한다. 이 구조체에는 `email`이라는 필드가 있다. `build_user` 함수의 `email` 매개변수 값을 `email` 필드에 설정하려고 한다. `email` 필드와 `email` 매개변수의 이름이 동일하기 때문에 `email: email` 대신 단순히 `email`만 작성하면 된다.


### 구조체 업데이트 문법을 사용해 다른 인스턴스로부터 인스턴스 생성하기

기존 구조체 인스턴스의 대부분의 값을 그대로 사용하면서 일부만 변경해 새로운 인스턴스를 생성하는 경우가 많다. 이때 **구조체 업데이트 문법**을 사용할 수 있다.

먼저, 리스팅 5-6에서는 업데이트 문법 없이 `user2`라는 새로운 `User` 인스턴스를 생성하는 일반적인 방법을 보여준다. `email`에 새로운 값을 설정하고, 나머지 필드는 리스팅 5-2에서 생성한 `user1`의 값을 그대로 사용한다.

<Listing number="5-6" file-name="src/main.rs" caption="`user1`의 값 중 하나를 제외하고 새로운 `User` 인스턴스 생성">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-06/src/main.rs:here}}
```

</Listing>

구조체 업데이트 문법을 사용하면 더 적은 코드로 동일한 결과를 얻을 수 있다. 리스팅 5-7에서와 같이 `..` 문법은 명시적으로 설정하지 않은 나머지 필드가 주어진 인스턴스의 필드와 동일한 값을 가지도록 지정한다.

<Listing number="5-7" file-name="src/main.rs" caption="구조체 업데이트 문법을 사용해 `User` 인스턴스의 새로운 `email` 값을 설정하고 나머지 값은 `user1`에서 가져오기">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-07/src/main.rs:here}}
```

</Listing>

리스팅 5-7의 코드도 `user2` 인스턴스를 생성하며, `email` 값은 다르지만 `username`, `active`, `sign_in_count` 필드는 `user1`과 동일한 값을 가진다. `..user1`은 반드시 마지막에 위치해야 하며, 이는 나머지 필드가 `user1`의 해당 필드에서 값을 가져오도록 지정한다. 하지만 원하는 순서대로 원하는 만큼의 필드에 값을 지정할 수 있으며, 이는 구조체 정의에서 필드가 정의된 순서와 무관하다.

구조체 업데이트 문법은 할당처럼 `=`를 사용한다. 이는 데이터를 이동시키기 때문이며, 이전에 [“변수와 데이터 상호작용: 이동”][move]<!-- ignore --> 섹션에서 본 것과 동일하다. 이 예제에서는 `user2`를 생성한 후 `user1`을 더 이상 사용할 수 없다. 왜냐하면 `user1`의 `username` 필드에 있는 `String`이 `user2`로 이동했기 때문이다. 만약 `user2`에 `email`과 `username` 모두 새로운 `String` 값을 주고, `active`와 `sign_in_count` 값만 `user1`에서 가져왔다면, `user2`를 생성한 후에도 `user1`은 여전히 유효할 것이다. `active`와 `sign_in_count`는 `Copy` 트레이트를 구현하는 타입이므로, [“스택 전용 데이터: 복사”][copy]<!-- ignore --> 섹션에서 논의한 동작이 적용된다. 이 예제에서는 `user1.email`을 여전히 사용할 수 있는데, 그 값이 이동되지 않았기 때문이다.


### 이름 없는 필드로 구성된 튜플 구조체 사용하기

Rust는 튜플과 유사한 구조체인 _튜플 구조체_를 지원한다. 튜플 구조체는 구조체 이름이 제공하는 의미를 가지지만, 필드에 이름을 붙이지는 않는다. 대신 필드의 타입만 지정한다. 튜플 구조체는 전체 튜플에 이름을 부여하고, 다른 튜플과 구별되는 타입을 만들고 싶을 때 유용하다. 또한 일반 구조체처럼 각 필드에 이름을 붙이는 것이 번거롭거나 불필요한 경우에도 사용할 수 있다.

튜플 구조체를 정의하려면 `struct` 키워드와 구조체 이름을 쓰고, 그 뒤에 튜플의 타입을 나열한다. 예를 들어, `Color`와 `Point`라는 두 개의 튜플 구조체를 정의하고 사용해 보자:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-01-tuple-structs/src/main.rs}}
```

</Listing>

`black`과 `origin` 값은 서로 다른 튜플 구조체의 인스턴스이기 때문에 다른 타입이다. 각 구조체는 고유한 타입이며, 구조체 내부의 필드가 동일한 타입을 가질지라도 서로 다른 타입으로 간주된다. 예를 들어, `Color` 타입의 매개변수를 받는 함수는 `Point` 타입의 인자를 받을 수 없다. 두 타입 모두 세 개의 `i32` 값으로 구성되어 있더라도 말이다. 그 외에는 튜플 구조체 인스턴스는 튜플과 유사하게 동작한다. 개별 요소로 분해할 수 있고, `.` 뒤에 인덱스를 붙여 개별 값에 접근할 수 있다. 튜플과 달리, 튜플 구조체를 분해할 때는 구조체의 타입을 명시해야 한다. 예를 들어, `let Point(x, y, z) = point`와 같이 작성한다.


### 필드가 없는 유닛 구조체

필드가 없는 구조체도 정의할 수 있다! 이를 **유닛 구조체**라고 부르며, 이는 [“튜플 타입”][tuples]<!-- ignore --> 섹션에서 언급한 `()` 유닛 타입과 유사하게 동작한다. 유닛 구조체는 어떤 타입에 대해 트레이트를 구현해야 하지만, 그 타입 자체에 저장할 데이터가 없을 때 유용하다. 트레이트에 대해서는 10장에서 자세히 다룰 것이다. 다음은 `AlwaysEqual`이라는 유닛 구조체를 선언하고 인스턴스를 생성하는 예제이다:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-04-unit-like-structs/src/main.rs}}
```

</Listing>

`AlwaysEqual`을 정의하려면 `struct` 키워드와 원하는 이름을 사용한 뒤 세미콜론을 붙인다. 중괄호나 괄호는 필요 없다! 그런 다음 `subject` 변수에 `AlwaysEqual`의 인스턴스를 생성할 수 있다. 이때도 중괄호나 괄호 없이 정의한 이름만 사용한다. 나중에 이 타입에 대해 모든 `AlwaysEqual` 인스턴스가 다른 타입의 모든 인스턴스와 항상 동일하도록 동작을 구현할 수 있다. 예를 들어 테스트 목적으로 알려진 결과를 얻기 위해 사용할 수 있다. 이러한 동작을 구현하기 위해 데이터는 필요하지 않다! 10장에서는 트레이트를 정의하고 유닛 구조체를 포함한 모든 타입에 이를 구현하는 방법을 배울 것이다.

> ### 구조체 데이터의 소유권
>
> 5-1 예제의 `User` 구조체 정의에서 `&str` 문자열 슬라이스 타입 대신 소유권을 가진 `String` 타입을 사용했다. 이는 의도적인 선택으로, 이 구조체의 각 인스턴스가 자신의 데이터를 소유하고, 구조체 전체가 유효한 동안 그 데이터도 유효하도록 하기 위함이다.
>
> 구조체가 다른 곳에서 소유한 데이터에 대한 참조를 저장할 수도 있지만, 이를 위해서는 **라이프타임**이라는 Rust 기능을 사용해야 한다. 라이프타임은 구조체가 참조하는 데이터가 구조체가 유효한 동안 유효하도록 보장한다. 라이프타임을 지정하지 않고 구조체에 참조를 저장하려고 하면 다음과 같은 문제가 발생한다:
>
> <Listing file-name="src/main.rs">
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore,does_not_compile
> struct User {
>     active: bool,
>     username: &str,
>     email: &str,
>     sign_in_count: u64,
> }
>
> fn main() {
>     let user1 = User {
>         active: true,
>         username: "someusername123",
>         email: "someone@example.com",
>         sign_in_count: 1,
>     };
> }
> ```
>
> </Listing>
>
> 컴파일러는 라이프타임 지정자가 필요하다고 불평할 것이다:
>
> ```console
> $ cargo run
>    Compiling structs v0.1.0 (file:///projects/structs)
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:3:15
>   |
> 3 |     username: &str,
>   |               ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 ~     username: &'a str,
>   |
>
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:4:12
>   |
> 4 |     email: &str,
>   |            ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 |     username: &str,
> 4 ~     email: &'a str,
>   |
>
> For more information about this error, try `rustc --explain E0106`.
> error: could not compile `structs` (bin "structs") due to 2 previous errors
> ```
>
> 10장에서는 이러한 오류를 수정해 구조체에 참조를 저장하는 방법을 다룰 것이다. 하지만 지금은 `&str` 같은 참조 대신 `String` 같은 소유 타입을 사용해 이러한 오류를 해결할 것이다.

<!-- manual-regeneration
for the error above
after running update-rustc.sh:
pbcopy < listings/ch05-using-structs-to-structure-related-data/no-listing-02-reference-in-struct/output.txt
paste above
add `> ` before every line -->

[tuples]: ch03-02-data-types.html#the-tuple-type
[move]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-move
[copy]: ch04-01-what-is-ownership.html#stack-only-data-copy


