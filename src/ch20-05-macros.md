## 매크로

이 책에서 `println!`과 같은 매크로를 사용해왔지만, 매크로가 무엇이고 어떻게 동작하는지 완전히 설명하지는 않았다. _매크로_라는 용어는 러스트의 여러 기능을 가리킨다. `macro_rules!`를 사용한 _선언적_ 매크로와 세 가지 종류의 _프로시저_ 매크로가 있다:

- 구조체와 열거형에 `derive` 속성을 사용할 때 추가되는 코드를 지정하는 커스텀 `#[derive]` 매크로
- 모든 아이템에 사용 가능한 커스텀 속성을 정의하는 속성 형태의 매크로
- 함수 호출처럼 보이지만 인자로 지정된 토큰을 처리하는 함수 형태의 매크로

이러한 각 매크로에 대해 차례로 설명할 것이다. 하지만 먼저, 함수가 이미 있는데 왜 매크로가 필요한지 살펴보자.


### 매크로와 함수의 차이점

기본적으로 매크로는 코드를 생성하는 코드를 작성하는 방식이다. 이를 _메타프로그래밍_이라고 한다. 부록 C에서는 `derive` 속성을 다루는데, 이는 다양한 트레이트의 구현을 자동으로 생성한다. 또한 이 책 전반에서 `println!`과 `vec!` 매크로를 사용했다. 이 모든 매크로는 직접 작성한 코드보다 더 많은 코드를 생성하도록 _확장_된다.

메타프로그래밍은 작성하고 유지해야 하는 코드의 양을 줄이는 데 유용하며, 이는 함수의 역할 중 하나이기도 하다. 그러나 매크로는 함수가 할 수 없는 몇 가지 추가적인 기능을 제공한다.

함수 시그니처는 함수가 갖는 매개변수의 수와 타입을 명시해야 한다. 반면 매크로는 가변적인 수의 매개변수를 받을 수 있다. 예를 들어 `println!("hello")`처럼 하나의 인자로 호출할 수도 있고, `println!("hello {}", name)`처럼 두 개의 인자로 호출할 수도 있다. 또한 매크로는 컴파일러가 코드의 의미를 해석하기 전에 확장되므로, 특정 타입에 대해 트레이트를 구현하는 등의 작업을 할 수 있다. 함수는 런타임에 호출되기 때문에 컴파일 타임에 구현해야 하는 트레이트를 구현할 수 없다.

함수 대신 매크로를 구현할 때의 단점은 매크로 정의가 함수 정의보다 복잡하다는 점이다. 왜냐하면 Rust 코드를 생성하는 Rust 코드를 작성해야 하기 때문이다. 이러한 간접적인 구조 때문에 매크로 정의는 일반적으로 함수 정의보다 읽기, 이해하기, 유지하기가 더 어렵다.

매크로와 함수의 또 다른 중요한 차이점은 매크로를 파일에서 호출하기 전에 정의하거나 스코프로 가져와야 한다는 점이다. 반면 함수는 어디에서든 정의하고 호출할 수 있다.


### `macro_rules!`를 사용한 선언적 매크로와 일반 메타프로그래밍

러스트에서 가장 널리 사용되는 매크로 형태는 _선언적 매크로_다. 이는 때때로 "예제 매크로", "`macro_rules!` 매크로", 또는 단순히 "매크로"라고도 불린다. 선언적 매크로의 핵심은 러스트의 `match` 표현식과 유사한 것을 작성할 수 있게 해준다는 점이다. 6장에서 논의했듯이, `match` 표현식은 특정 표현식을 평가한 결과를 패턴과 비교한 후, 매칭되는 패턴과 관련된 코드를 실행하는 제어 구조다. 매크로도 마찬가지로 값을 패턴과 비교하는데, 여기서 값은 매크로에 전달된 러스트 소스 코드의 리터럴이다. 패턴은 해당 소스 코드의 구조와 비교되며, 매칭된 패턴과 관련된 코드는 매크로에 전달된 코드를 대체한다. 이 모든 과정은 컴파일 중에 일어난다.

매크로를 정의하려면 `macro_rules!` 구문을 사용한다. `vec!` 매크로가 어떻게 정의되어 있는지 살펴보면서 `macro_rules!`의 사용법을 알아보자. 8장에서는 `vec!` 매크로를 사용해 특정 값을 가진 새로운 벡터를 생성하는 방법을 다뤘다. 예를 들어, 다음 매크로는 세 개의 정수를 포함하는 새로운 벡터를 생성한다:

```rust
let v: Vec<u32> = vec![1, 2, 3];
```

또한 `vec!` 매크로를 사용해 두 개의 정수로 이루어진 벡터나 다섯 개의 문자열 슬라이스로 이루어진 벡터를 만들 수도 있다. 함수를 사용해 동일한 작업을 수행할 수는 없는 이유는, 함수에서는 사전에 값의 개수나 타입을 알 수 없기 때문이다.

리스트 20-35는 `vec!` 매크로의 정의를 약간 단순화한 버전을 보여준다.

<Listing number="20-35" file-name="src/lib.rs" caption="`vec!` 매크로 정의의 단순화된 버전">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-35/src/lib.rs}}
```

</Listing>

> 참고: 표준 라이브러리에서 `vec!` 매크로의 실제 정의에는 사전에 정확한 양의 메모리를 할당하는 코드가 포함되어 있다. 이 코드는 최적화를 위한 것이며, 예제를 단순화하기 위해 여기서는 포함하지 않았다.

`#[macro_export]` 어노테이션은 이 매크로가 정의된 크레이트가 스코프에 포함될 때마다 매크로를 사용할 수 있도록 해준다. 이 어노테이션이 없으면 매크로를 스코프로 가져올 수 없다.

그런 다음 `macro_rules!`와 함께 매크로 정의를 시작하고, 매크로의 이름을 정의한다. 이때 이름 뒤에는 느낌표(`!`)를 붙이지 않는다. 여기서는 `vec`이라는 이름을 사용했으며, 이어서 중괄호를 사용해 매크로 정의의 본문을 표시한다.

`vec!` 본문의 구조는 `match` 표현식의 구조와 유사하다. 여기서는 `( $( $x:expr ),* )`라는 패턴과 `=>` 뒤에 이 패턴과 관련된 코드 블록이 있다. 패턴이 매칭되면, 관련된 코드 블록이 생성된다. 이 매크로에서는 패턴이 하나뿐이므로, 매칭되는 유일한 방법이 있다. 다른 패턴은 오류를 발생시킨다. 더 복잡한 매크로는 여러 개의 패턴을 가질 수 있다.

매크로 정의에서 유효한 패턴 문법은 19장에서 다룬 패턴 문법과 다르다. 매크로 패턴은 값이 아닌 러스트 코드의 구조와 매칭되기 때문이다. 리스트 20-29의 패턴 조각이 무엇을 의미하는지 살펴보자. 전체 매크로 패턴 문법은 [러스트 레퍼런스][ref]를 참조하라.

먼저, 전체 패턴을 감싸기 위해 괄호를 사용한다. 달러 기호(`$`)를 사용해 매크로 시스템에서 패턴과 매칭되는 러스트 코드를 포함할 변수를 선언한다. 달러 기호는 이 변수가 일반 러스트 변수가 아니라 매크로 변수임을 명확히 한다. 다음으로 괄호를 사용해 패턴과 매칭되는 값을 캡처하여 대체 코드에서 사용할 수 있도록 한다. `$()` 내부에는 `$x:expr`이 있는데, 이는 모든 러스트 표현식과 매칭되며 해당 표현식에 `$x`라는 이름을 부여한다.

`$()` 뒤에 오는 쉼표는 `$()` 내부의 코드와 매칭되는 코드 사이에 리터럴 쉼표 구분자가 있어야 함을 나타낸다. `*`는 `*` 앞에 오는 패턴이 0회 이상 반복될 수 있음을 지정한다.

이 매크로를 `vec![1, 2, 3];`으로 호출하면, `$x` 패턴은 `1`, `2`, `3` 세 개의 표현식과 각각 매칭된다.

이제 이 패턴과 관련된 코드 본문의 패턴을 살펴보자: `temp_vec.push()`는 `$()*` 내부에서 패턴이 매칭될 때마다 생성된다. `$x`는 매칭된 각 표현식으로 대체된다. 이 매크로를 `vec![1, 2, 3];`으로 호출하면, 이 매크로 호출을 대체하는 코드는 다음과 같이 생성된다:

```rust,ignore
{
    let mut temp_vec = Vec::new();
    temp_vec.push(1);
    temp_vec.push(2);
    temp_vec.push(3);
    temp_vec
}
```

이렇게 정의한 매크로는 임의의 타입의 인수를 임의의 개수만큼 받아, 지정된 요소를 포함하는 벡터를 생성하는 코드를 만들 수 있다.

매크로를 작성하는 방법에 대해 더 알아보려면 온라인 문서나 Daniel Keep이 시작하고 Lukas Wirth가 이어간 [“The Little Book of Rust Macros”][tlborm]와 같은 리소스를 참조하라.


### 속성을 활용한 코드 생성 프로시저 매크로

두 번째 형태의 매크로는 프로시저 매크로로, 함수와 유사하게 동작한다. _프로시저 매크로_는 코드를 입력으로 받아 처리한 후 새로운 코드를 출력한다. 선언적 매크로와 달리 패턴 매칭을 통해 코드를 대체하는 방식이 아니라, 코드를 직접 조작한다. 프로시저 매크로는 크게 세 가지 종류로 나뉜다: 커스텀 `derive`, 속성 기반, 함수형 매크로. 이들은 모두 유사한 방식으로 동작한다.

프로시저 매크로를 생성할 때는 정의를 특별한 크레이트 타입의 독립된 크레이트에 위치시켜야 한다. 이는 복잡한 기술적 이유로, 향후 개선될 예정이다. 아래 예제는 프로시저 매크로를 정의하는 방법을 보여준다. 여기서 `some_attribute`는 특정 매크로 종류를 사용하기 위한 자리 표시자다.

<Listing number="20-36" file-name="src/lib.rs" caption="프로시저 매크로 정의 예제">

```rust,ignore
use proc_macro;

#[some_attribute]
pub fn some_name(input: TokenStream) -> TokenStream {
}
```

</Listing>

프로시저 매크로를 정의하는 함수는 `TokenStream`을 입력으로 받고 `TokenStream`을 출력으로 반환한다. `TokenStream` 타입은 Rust에 포함된 `proc_macro` 크레이트에서 정의되며, 토큰의 시퀀스를 나타낸다. 이 매크로의 핵심은 입력 `TokenStream`으로 전달된 소스 코드를 처리하고, 출력 `TokenStream`으로 새로운 코드를 생성하는 것이다. 또한 함수에는 생성할 프로시저 매크로의 종류를 지정하는 속성이 부착된다. 동일한 크레이트 내에서 여러 종류의 프로시저 매크로를 정의할 수 있다.

이제 각각의 프로시저 매크로 종류를 살펴보자. 먼저 커스텀 `derive` 매크로를 설명한 후, 다른 형태의 매크로와의 차이점을 알아볼 것이다.


### 커스텀 `derive` 매크로 작성 방법

`hello_macro`라는 크레이트를 만들어 보자. 이 크레이트는 `HelloMacro`라는 트레이트와 `hello_macro`라는 하나의 연관 함수를 정의한다. 사용자가 각 타입에 대해 `HelloMacro` 트레이트를 직접 구현하도록 하는 대신, 프로시저 매크로를 제공하여 사용자가 타입에 `#[derive(HelloMacro)]`를 주석으로 추가하면 `hello_macro` 함수의 기본 구현을 얻을 수 있도록 한다. 기본 구현은 `Hello, Macro! My name is TypeName!`을 출력한다. 여기서 `TypeName`은 이 트레이트가 정의된 타입의 이름이다. 즉, 다른 프로그래머가 우리 크레이트를 사용해 리스트 20-37과 같은 코드를 작성할 수 있도록 하는 크레이트를 만드는 것이다.

<리스트 번호="20-37" 파일명="src/main.rs" 설명="우리 크레이트를 사용하는 프로그래머가 작성할 수 있는 코드">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-37/src/main.rs}}
```

</리스트>

이 코드는 완성되면 `Hello, Macro! My name is Pancakes!`를 출력한다. 첫 번째 단계는 다음과 같이 새로운 라이브러리 크레이트를 만드는 것이다:

```console
$ cargo new hello_macro --lib
```

다음으로 `HelloMacro` 트레이트와 그 연관 함수를 정의한다:

<리스트 파일명="src/lib.rs" 번호="20-38" 설명="`derive` 매크로와 함께 사용할 간단한 트레이트">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-38/hello_macro/src/lib.rs}}
```

</리스트>

이제 트레이트와 함수가 있다. 이 시점에서 크레이트 사용자는 리스트 20-39와 같이 트레이트를 구현해 원하는 기능을 달성할 수 있다.

<리스트 번호="20-39" 파일명="src/main.rs" 설명="사용자가 `HelloMacro` 트레이트를 수동으로 구현한 모습">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-39/pancakes/src/main.rs}}
```

</리스트>

하지만 사용자는 `hello_macro`와 함께 사용하려는 각 타입에 대해 구현 블록을 작성해야 한다. 우리는 이 작업을 없애고 싶다.

또한 러스트는 리플렉션 기능이 없기 때문에 런타임에 타입의 이름을 조회할 수 없다. 따라서 트레이트가 구현된 타입의 이름을 출력하는 `hello_macro` 함수의 기본 구현을 제공할 수 없다. 컴파일 타임에 코드를 생성하는 매크로가 필요하다.

다음 단계는 프로시저 매크로를 정의하는 것이다. 이 글을 쓰는 시점에서 프로시저 매크로는 자체 크레이트에 있어야 한다. 이 제한은 나중에 해제될 수도 있다. 크레이트와 매크로 크레이트를 구조화하는 규칙은 다음과 같다: `foo`라는 크레이트의 경우, 커스텀 `derive` 프로시저 매크로 크레이트는 `foo_derive`라고 한다. `hello_macro` 프로젝트 내부에 `hello_macro_derive`라는 새 크레이트를 시작해 보자:

```console
$ cargo new hello_macro_derive --lib
```

두 크레이트는 밀접하게 연관되어 있으므로 프로시저 매크로 크레이트를 `hello_macro` 크레이트의 디렉토리 내부에 만든다. `hello_macro`에서 트레이트 정의를 변경하면 `hello_macro_derive`에서 프로시저 매크로의 구현도 변경해야 한다. 두 크레이트는 별도로 게시해야 하며, 이 크레이트를 사용하는 프로그래머는 둘 모두를 의존성으로 추가하고 스코프로 가져와야 한다. 대신 `hello_macro` 크레이트가 `hello_macro_derive`를 의존성으로 사용하고 프로시저 매크로 코드를 다시 내보낼 수도 있다. 그러나 우리가 프로젝트를 구조화한 방식은 프로그래머가 `derive` 기능을 원하지 않더라도 `hello_macro`를 사용할 수 있게 한다.

`hello_macro_derive` 크레이트를 프로시저 매크로 크레이트로 선언해야 한다. 또한 `syn`과 `quote` 크레이트의 기능이 필요하므로 이를 의존성으로 추가해야 한다. `hello_macro_derive`의 _Cargo.toml_ 파일에 다음을 추가한다:

<리스트 파일명="hello_macro_derive/Cargo.toml">

```toml
{{#include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/Cargo.toml:6:12}}
```

</리스트>

프로시저 매크로를 정의하기 위해 리스트 20-40의 코드를 `hello_macro_derive` 크레이트의 _src/lib.rs_ 파일에 넣는다. `impl_hello_macro` 함수에 대한 정의를 추가할 때까지 이 코드는 컴파일되지 않는다는 점에 유의하라.

<리스트 번호="20-40" 파일명="hello_macro_derive/src/lib.rs" 설명="러스트 코드를 처리하기 위해 대부분의 프로시저 매크로 크레이트에 필요한 코드">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/src/lib.rs}}
```

</리스트>

코드를 `TokenStream`을 파싱하는 역할을 하는 `hello_macro_derive` 함수와 구문 트리를 변환하는 역할을 하는 `impl_hello_macro` 함수로 나눈 것을 확인할 수 있다. 이렇게 하면 프로시저 매크로를 작성하는 것이 더 편리해진다. 외부 함수(`hello_macro_derive`)의 코드는 거의 모든 프로시저 매크로 크레이트에서 동일하다. 내부 함수(`impl_hello_macro`)의 본문에 지정하는 코드는 프로시저 매크로의 목적에 따라 달라진다.

세 가지 새로운 크레이트를 소개했다: `proc_macro`, [`syn`], 그리고 [`quote`]. `proc_macro` 크레이트는 러스트와 함께 제공되므로 _Cargo.toml_에 의존성으로 추가할 필요가 없다. `proc_macro` 크레이트는 코드에서 러스트 코드를 읽고 조작할 수 있도록 하는 컴파일러의 API이다.

`syn` 크레이트는 문자열에서 러스트 코드를 파싱해 조작할 수 있는 데이터 구조로 변환한다. `quote` 크레이트는 `syn` 데이터 구조를 다시 러스트 코드로 변환한다. 이 크레이트들은 처리하려는 모든 종류의 러스트 코드를 파싱하는 것을 훨씬 간단하게 만든다. 러스트 코드에 대한 완전한 파서를 작성하는 것은 간단한 작업이 아니다.

`hello_macro_derive` 함수는 라이브러리 사용자가 타입에 `#[derive(HelloMacro)]`를 지정할 때 호출된다. 이는 `hello_macro_derive` 함수에 `proc_macro_derive`를 주석으로 추가하고 트레이트 이름과 일치하는 `HelloMacro`를 지정했기 때문에 가능하다. 이는 대부분의 프로시저 매크로가 따르는 규칙이다.

`hello_macro_derive` 함수는 먼저 `input`을 `TokenStream`에서 해석하고 조작할 수 있는 데이터 구조로 변환한다. 여기서 `syn`이 작동한다. `syn`의 `parse` 함수는 `TokenStream`을 받아 파싱된 러스트 코드를 나타내는 `DeriveInput` 구조체를 반환한다. 리스트 20-41은 `struct Pancakes;` 문자열을 파싱할 때 얻는 `DeriveInput` 구조체의 관련 부분을 보여준다.

<리스트 번호="20-41" 설명="리스트 20-37의 매크로 속성이 있는 코드를 파싱할 때 얻는 `DeriveInput` 인스턴스">

```rust,ignore
DeriveInput {
    // --snip--

    ident: Ident {
        ident: "Pancakes",
        span: #0 bytes(95..103)
    },
    data: Struct(
        DataStruct {
            struct_token: Struct,
            fields: Unit,
            semi_token: Some(
                Semi
            )
        }
    )
}
```

</리스트>

이 구조체의 필드는 파싱한 러스트 코드가 `Pancakes`라는 `ident`(식별자, 즉 이름)를 가진 유닛 구조체임을 보여준다. 이 구조체에는 모든 종류의 러스트 코드를 설명하기 위한 더 많은 필드가 있다. 자세한 정보는 [`syn` 문서의 `DeriveInput`][syn-docs]를 참조하라.

곧 `impl_hello_macro` 함수를 정의할 것이다. 이 함수는 포함하려는 새로운 러스트 코드를 작성하는 곳이다. 하지만 그 전에 `derive` 매크로의 출력도 `TokenStream`이라는 점을 알아두자. 반환된 `TokenStream`은 크레이트 사용자가 작성한 코드에 추가되므로, 사용자가 크레이트를 컴파일할 때 우리가 수정한 `TokenStream`에서 제공하는 추가 기능을 얻게 된다.

`syn::parse` 함수 호출이 실패하면 `hello_macro_derive` 함수가 패닉을 일으키도록 `unwrap`을 호출하는 것을 눈치챘을 것이다. 프로시저 매크로는 오류 시 패닉을 일으켜야 한다. 왜냐하면 `proc_macro_derive` 함수는 프로시저 매크로 API에 맞게 `Result`가 아니라 `TokenStream`을 반환해야 하기 때문이다. 이 예제에서는 `unwrap`을 사용해 단순화했다. 프로덕션 코드에서는 `panic!`이나 `expect`를 사용해 무엇이 잘못되었는지에 대한 더 구체적인 오류 메시지를 제공해야 한다.

이제 주석이 달린 러스트 코드를 `TokenStream`에서 `DeriveInput` 인스턴스로 변환하는 코드가 있으므로, 리스트 20-42와 같이 주석이 달린 타입에 `HelloMacro` 트레이트를 구현하는 코드를 생성해 보자.

<리스트 번호="20-42" 파일명="hello_macro_derive/src/lib.rs" 설명="파싱된 러스트 코드를 사용해 `HelloMacro` 트레이트 구현">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-42/hello_macro/hello_macro_derive/src/lib.rs:here}}
```

</리스트>

`ast.ident`를 사용해 주석이 달린 타입의 이름(식별자)을 포함하는 `Ident` 구조체 인스턴스를 얻는다. 리스트 20-33의 구조체는 리스트 20-31의 코드에서 `impl_hello_macro` 함수를 실행할 때 얻는 `ident`가 `"Pancakes"` 값을 가진 `ident` 필드를 가짐을 보여준다. 따라서 리스트 20-34의 `name` 변수는 `Ident` 구조체 인스턴스를 포함하며, 이는 출력될 때 리스트 20-37의 구조체 이름인 `"Pancakes"` 문자열이 된다.

`quote!` 매크로는 반환하려는 러스트 코드를 정의할 수 있게 해준다. 컴파일러는 `quote!` 매크로 실행의 직접적인 결과와는 다른 것을 기대하므로 이를 `TokenStream`으로 변환해야 한다. `into` 메서드를 호출해 이를 수행한다. 이 메서드는 이 중간 표현을 소비하고 필요한 `TokenStream` 타입의 값을 반환한다.

`quote!` 매크로는 또한 매우 멋진 템플릿 메커니즘을 제공한다: `#name`을 입력하면 `quote!`는 이를 `name` 변수의 값으로 대체한다. 일반 매크로와 유사한 방식으로 반복 작업도 할 수 있다. 자세한 소개는 [the `quote` crate’s docs][quote-docs]를 참조하라.

우리의 프로시저 매크로는 사용자가 주석을 단 타입에 대해 `HelloMacro` 트레이트의 구현을 생성하도록 한다. 이는 `#name`을 사용해 얻을 수 있다. 트레이트 구현에는 `hello_macro`라는 하나의 함수가 있으며, 이 함수의 본문에는 제공하려는 기능이 있다: `Hello, Macro! My name is`을 출력한 다음 주석이 달린 타입의 이름을 출력한다.

여기서 사용한 `stringify!` 매크로는 러스트에 내장되어 있다. 이 매크로는 `1 + 2`와 같은 러스트 표현식을 컴파일 타임에 `"1 + 2"`와 같은 문자열 리터럴로 변환한다. 이는 표현식을 평가한 다음 결과를 `String`으로 변환하는 `format!`이나 `println!` 매크로와 다르다. `#name` 입력이 문자 그대로 출력할 표현식일 가능성이 있으므로 `stringify!`를 사용한다. `stringify!`를 사용하면 컴파일 타임에 `#name`을 문자열 리터럴로 변환해 할당을 절약할 수 있다.

이 시점에서 `cargo build`는 `hello_macro`와 `hello_macro_derive` 모두에서 성공적으로 완료되어야 한다. 이 크레이트를 리스트 20-31의 코드에 연결해 프로시저 매크로가 작동하는 것을 확인해 보자! _projects_ 디렉토리에서 `cargo new pancakes`를 사용해 새로운 바이너리 프로젝트를 만든다. `pancakes` 크레이트의 _Cargo.toml_에 `hello_macro`와 `hello_macro_derive`를 의존성으로 추가해야 한다. `hello_macro`와 `hello_macro_derive`의 버전을 [crates.io](https://crates.io/)에 게시한다면 일반 의존성이 될 것이다. 그렇지 않다면 다음과 같이 `path` 의존성으로 지정할 수 있다:

```toml
{{#include ../listings/ch20-advanced-features/no-listing-21-pancakes/pancakes/Cargo.toml:7:9}}
```

리스트 20-37의 코드를 _src/main.rs_에 넣고 `cargo run`을 실행하면 `Hello, Macro! My name is Pancakes!`가 출력되어야 한다. 프로시저 매크로의 `HelloMacro` 트레이트 구현은 `pancakes` 크레이트가 이를 구현하지 않아도 포함되었다. `#[derive(HelloMacro)]`가 트레이트 구현을 추가한 것이다.

다음으로, 다른 종류의 프로시저 매크로가 커스텀 `derive` 매크로와 어떻게 다른지 살펴보자.


### 속성(Attribute)과 유사한 매크로

속성과 유사한 매크로는 커스텀 `derive` 매크로와 비슷하지만, `derive` 속성을 위한 코드를 생성하는 대신 새로운 속성을 만들 수 있다. 또한 더 유연하다. `derive`는 구조체와 열거형에만 적용할 수 있지만, 속성은 함수와 같은 다른 항목에도 적용할 수 있다. 웹 애플리케이션 프레임워크에서 함수를 주석 처리하는 `route`라는 속성을 사용하는 예제를 살펴보자:

```rust,ignore
#[route(GET, "/")]
fn index() {
```

이 `#[route]` 속성은 프레임워크에서 프로시저 매크로로 정의된다. 매크로 정의 함수의 시그니처는 다음과 같다:

```rust,ignore
#[proc_macro_attribute]
pub fn route(attr: TokenStream, item: TokenStream) -> TokenStream {
```

여기서 두 개의 `TokenStream` 타입 매개변수가 있다. 첫 번째 매개변수는 속성의 내용, 즉 `GET, "/"` 부분을 담는다. 두 번째 매개변수는 속성이 적용된 항목의 본문, 이 경우 `fn index() {}`와 함수의 나머지 부분을 담는다.

이 외에도, 속성과 유사한 매크로는 커스텀 `derive` 매크로와 동일한 방식으로 작동한다. `proc-macro` 크레이트 타입으로 크레이트를 만들고, 원하는 코드를 생성하는 함수를 구현하면 된다!


### 함수형 매크로

함수형 매크로는 함수 호출처럼 보이는 매크로를 정의한다. `macro_rules!` 매크로와 마찬가지로, 이 매크로는 함수보다 더 유연하다. 예를 들어, 함수형 매크로는 알려지지 않은 수의 인자를 받을 수 있다. 하지만 `macro_rules!` 매크로는 이전에 [“`macro_rules!`를 사용한 선언적 매크로와 일반 메타프로그래밍”][decl]<!-- ignore -->에서 논의한 것처럼 매치(match)와 유사한 구문을 사용해서만 정의할 수 있다. 함수형 매크로는 `TokenStream` 파라미터를 받고, 다른 두 가지 타입의 프로시저 매크로와 마찬가지로 Rust 코드를 사용해 이 `TokenStream`을 조작한다. 함수형 매크로의 예로는 다음과 같이 호출될 수 있는 `sql!` 매크로가 있다:

```rust,ignore
let sql = sql!(SELECT * FROM posts WHERE id=1);
```

이 매크로는 내부에 있는 SQL 문을 파싱하고 문법적으로 올바른지 확인한다. 이는 `macro_rules!` 매크로가 할 수 있는 것보다 훨씬 더 복잡한 처리 과정이다. `sql!` 매크로는 다음과 같이 정의된다:

```rust,ignore
#[proc_macro]
pub fn sql(input: TokenStream) -> TokenStream {
```

이 정의는 커스텀 `derive` 매크로의 시그니처와 유사하다. 괄호 안에 있는 토큰을 받고, 생성하려는 코드를 반환한다.


## 요약

드디어 여러분의 Rust 도구 상자에 자주 사용하지는 않지만 특정 상황에서 유용하게 활용할 수 있는 기능들이 추가되었다. 이번 장에서는 복잡한 주제들을 소개했는데, 이를 통해 앞으로 에러 메시지 제안이나 다른 사람의 코드에서 이 개념들과 문법을 마주쳤을 때 쉽게 이해할 수 있을 것이다. 이 장을 참고 자료로 활용해 문제를 해결하는 데 도움을 받길 바란다.

다음으로는 지금까지 책에서 다룬 모든 내용을 종합해 하나의 프로젝트를 진행해볼 예정이다!

[ref]: ../reference/macros-by-example.html
[tlborm]: https://veykril.github.io/tlborm/
[`syn`]: https://crates.io/crates/syn
[`quote`]: https://crates.io/crates/quote
[syn-docs]: https://docs.rs/syn/2.0/syn/struct.DeriveInput.html
[quote-docs]: https://docs.rs/quote
[decl]: #declarative-macros-with-macro_rules-for-general-metaprogramming


