## `Result`를 사용한 복구 가능한 에러 처리

대부분의 에러는 프로그램 전체를 중단시킬 정도로 심각하지 않다. 때로는 함수가 실패하더라도 그 이유를 쉽게 파악하고 대응할 수 있다. 예를 들어, 파일을 열려고 시도했는데 파일이 존재하지 않아 실패한 경우, 프로그램을 종료하는 대신 파일을 생성하는 방식으로 처리할 수 있다.

[2장의 "`Result`를 사용한 실패 처리"][handle_failure]<!-- ignore -->에서 살펴본 것처럼, `Result` 열거형은 `Ok`와 `Err` 두 가지 변형을 가진다. 

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

여기서 `T`와 `E`는 제네릭 타입 매개변수다. 제네릭에 대해서는 10장에서 자세히 다룬다. 지금 알아둘 점은 `T`는 `Ok` 변형에서 반환될 성공 값의 타입을 나타내고, `E`는 `Err` 변형에서 반환될 에러 값의 타입을 나타낸다는 것이다. `Result`가 이러한 제네릭 타입 매개변수를 가지기 때문에, 우리가 반환하고자 하는 성공 값과 에러 값이 다양한 상황에서도 `Result` 타입과 그에 정의된 함수들을 사용할 수 있다.

이제 실패할 가능성이 있는 함수를 호출해 보자. 예제 9-3에서는 파일을 열려고 시도한다.

<Listing number="9-3" file-name="src/main.rs" caption="파일 열기">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-03/src/main.rs}}
```

</Listing>

`File::open`의 반환 타입은 `Result<T, E>`다. 제네릭 매개변수 `T`는 `File::open` 구현에서 성공 값의 타입인 `std::fs::File`(파일 핸들)로 채워진다. 에러 값에 사용되는 `E`의 타입은 `std::io::Error`다. 이 반환 타입은 `File::open` 호출이 성공하여 읽거나 쓸 수 있는 파일 핸들을 반환할 수도 있고, 실패할 수도 있음을 의미한다. 예를 들어 파일이 존재하지 않거나, 파일에 접근할 권한이 없을 수 있다. `File::open` 함수는 성공 여부를 알려주고, 동시에 파일 핸들이나 에러 정보를 제공할 방법이 필요하다. 이 정보는 바로 `Result` 열거형이 전달하는 것이다.

`File::open`이 성공하면, `greeting_file_result` 변수의 값은 파일 핸들을 포함하는 `Ok` 인스턴스가 된다. 실패할 경우, `greeting_file_result` 변수의 값은 발생한 에러의 종류에 대한 정보를 포함하는 `Err` 인스턴스가 된다.

예제 9-3의 코드에 `File::open`이 반환하는 값에 따라 다른 동작을 추가해야 한다. 예제 9-4는 6장에서 다룬 기본 도구인 `match` 표현식을 사용해 `Result`를 처리하는 한 가지 방법을 보여준다.

<Listing number="9-4" file-name="src/main.rs" caption="`match` 표현식을 사용해 반환될 수 있는 `Result` 변형 처리">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-04/src/main.rs}}
```

</Listing>

`Option` 열거형과 마찬가지로, `Result` 열거형과 그 변형들은 프렐루드에 의해 스코프로 가져와지기 때문에, `match` 갈래에서 `Ok`와 `Err` 앞에 `Result::`를 명시할 필요가 없다.

결과가 `Ok`일 때, 이 코드는 `Ok` 변형에서 내부의 `file` 값을 반환하고, 그 파일 핸들 값을 `greeting_file` 변수에 할당한다. `match` 이후에는 파일 핸들을 읽거나 쓰는 데 사용할 수 있다.

`match`의 다른 갈래는 `File::open`에서 `Err` 값을 얻은 경우를 처리한다. 이 예제에서는 `panic!` 매크로를 호출하기로 선택했다. 현재 디렉터리에 _hello.txt_ 파일이 없고 이 코드를 실행하면, `panic!` 매크로로부터 다음과 같은 출력을 볼 수 있다:

```console
{{#include ../listings/ch09-error-handling/listing-09-04/output.txt}}
```

이 출력은 무엇이 잘못되었는지 정확히 알려준다.


### 다양한 에러에 대한 처리

리스트 9-4의 코드는 `File::open`이 실패한 이유와 상관없이 `panic!`을 일으킨다. 하지만 우리는 실패 이유에 따라 다른 동작을 수행하고 싶다. 만약 `File::open`이 파일이 존재하지 않아서 실패했다면, 우리는 새 파일을 생성하고 그 파일에 대한 핸들을 반환하려고 한다. 반면, 파일을 열 권한이 없어서 실패한 경우와 같은 다른 이유로 실패했다면, 여전히 리스트 9-4와 동일하게 `panic!`을 일으키고 싶다. 이를 위해 리스트 9-5와 같이 내부 `match` 표현식을 추가한다.

<Listing number="9-5" file-name="src/main.rs" caption="다양한 종류의 에러를 다르게 처리하기">

<!-- ignore this test because otherwise it creates hello.txt which causes other
tests to fail lol -->

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-05/src/main.rs}}
```

</Listing>

`File::open`이 반환하는 `Err` 변수 내부의 값은 표준 라이브러리에서 제공하는 `io::Error` 구조체이다. 이 구조체에는 `io::ErrorKind` 값을 얻기 위해 호출할 수 있는 `kind` 메서드가 있다. `io::ErrorKind` 열거형은 표준 라이브러리에서 제공되며, `io` 연산으로 인해 발생할 수 있는 다양한 종류의 에러를 나타내는 변수들을 포함한다. 우리가 사용하려는 변수는 `ErrorKind::NotFound`로, 열려고 시도한 파일이 아직 존재하지 않음을 나타낸다. 따라서 `greeting_file_result`에 대해 매칭을 수행하지만, 내부적으로 `error.kind()`에 대해서도 매칭을 수행한다.

내부 `match`에서 확인하려는 조건은 `error.kind()`가 반환한 값이 `ErrorKind` 열거형의 `NotFound` 변수인지 여부이다. 만약 그렇다면, `File::create`를 사용해 파일을 생성하려고 시도한다. 하지만 `File::create`도 실패할 수 있으므로, 내부 `match` 표현식에 두 번째 분기를 추가해야 한다. 파일을 생성할 수 없을 때는 다른 에러 메시지를 출력한다. 외부 `match`의 두 번째 분기는 그대로 유지되므로, 파일이 없어서 발생한 에러 외의 다른 에러가 발생하면 프로그램은 `panic!`을 일으킨다.

> #### `Result<T, E>`와 `match` 사용의 대안
>
> `match`가 너무 많다! `match` 표현식은 매우 유용하지만 동시에 매우 기본적인 도구이다. 13장에서는 `Result<T, E>`에 정의된 여러 메서드와 함께 사용되는 클로저에 대해 배울 것이다. 이러한 메서드는 코드에서 `Result<T, E>` 값을 처리할 때 `match`를 사용하는 것보다 더 간결할 수 있다.
>
> 예를 들어, 리스트 9-5와 동일한 로직을 클로저와 `unwrap_or_else` 메서드를 사용해 작성한 다른 방법은 다음과 같다:
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore
> use std::fs::File;
> use std::io::ErrorKind;
>
> fn main() {
>     let greeting_file = File::open("hello.txt").unwrap_or_else(|error| {
>         if error.kind() == ErrorKind::NotFound {
>             File::create("hello.txt").unwrap_or_else(|error| {
>                 panic!("Problem creating the file: {error:?}");
>             })
>         } else {
>             panic!("Problem opening the file: {error:?}");
>         }
>     });
> }
> ```
>
> 이 코드는 리스트 9-5와 동일한 동작을 하지만, `match` 표현식이 전혀 포함되어 있지 않으며 더 깔끔하게 읽을 수 있다. 13장을 읽은 후 이 예제로 돌아와서, 표준 라이브러리 문서에서 `unwrap_or_else` 메서드를 찾아보라. 에러를 처리할 때 이러한 메서드들을 사용하면 복잡하게 중첩된 `match` 표현식을 깔끔하게 정리할 수 있다.


#### 에러 발생 시 패닉을 유발하는 단축키: `unwrap`과 `expect`

`match`를 사용하는 방법도 유효하지만, 다소 장황할 수 있고 의도를 명확히 전달하지 못할 때가 있다. `Result<T, E>` 타입에는 다양한 작업을 수행하기 위한 여러 헬퍼 메서드가 정의되어 있다. `unwrap` 메서드는 우리가 Listing 9-4에서 작성한 `match` 표현식과 동일하게 구현된 단축 메서드다. `Result` 값이 `Ok` 변형이라면, `unwrap`은 `Ok` 내부의 값을 반환한다. `Result`가 `Err` 변형이라면, `unwrap`은 `panic!` 매크로를 호출한다. 다음은 `unwrap`을 사용한 예제다:

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-04-unwrap/src/main.rs}}
```

</Listing>

만약 _hello.txt_ 파일이 없는 상태에서 이 코드를 실행하면, `unwrap` 메서드가 호출한 `panic!`로 인해 다음과 같은 에러 메시지가 출력된다:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-04-unwrap
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:4:49:
called `Result::unwrap()` on an `Err` value: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

비슷하게, `expect` 메서드는 `panic!` 에러 메시지를 직접 선택할 수 있게 해준다. `unwrap` 대신 `expect`를 사용하고 적절한 에러 메시지를 제공하면 의도를 더 명확히 전달할 수 있고, 패닉의 원인을 추적하는 데도 도움이 된다. `expect`의 문법은 다음과 같다:

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-05-expect/src/main.rs}}
```

</Listing>

`expect`는 `unwrap`과 같은 방식으로 사용된다: 파일 핸들을 반환하거나 `panic!` 매크로를 호출한다. `expect`가 `panic!`을 호출할 때 사용하는 에러 메시지는 우리가 `expect`에 전달한 매개변수이며, `unwrap`이 사용하는 기본 `panic!` 메시지와는 다르다. 실행 결과는 다음과 같다:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-05-expect
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:5:10:
hello.txt should be included in this project: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

프로덕션 수준의 코드에서는 대부분의 Rust 개발자들이 `unwrap`보다 `expect`를 선택하고, 해당 작업이 항상 성공할 것으로 예상되는 이유에 대한 더 많은 컨텍스트를 제공한다. 이렇게 하면 가정이 틀렸을 때 디버깅에 활용할 수 있는 정보가 더 많아진다.


### 에러 전파

함수 내부에서 실패할 가능성이 있는 작업을 호출할 때, 해당 에러를 함수 내부에서 처리하는 대신 호출한 코드로 반환할 수 있다. 이를 **_에러 전파_**라고 하며, 호출한 코드가 더 많은 정보를 가지고 있거나 에러 처리에 대한 로직을 결정할 수 있는 경우에 유용하다.

예를 들어, 아래 예제는 파일에서 사용자 이름을 읽는 함수를 보여준다. 파일이 존재하지 않거나 읽을 수 없는 경우, 이 함수는 해당 에러를 호출한 코드로 반환한다.

<Listing number="9-6" file-name="src/main.rs" caption="`match`를 사용해 에러를 호출한 코드로 반환하는 함수">

```rust
{{#include ../listings/ch09-error-handling/listing-09-06/src/main.rs:here}}
```

</Listing>

이 함수는 더 짧게 작성할 수 있지만, 에러 처리를 자세히 이해하기 위해 일부러 수동으로 작성했다. 마지막에는 더 짧은 방법을 보여줄 것이다. 먼저 함수의 반환 타입을 살펴보자: `Result<String, io::Error>`. 이는 함수가 `Result<T, E>` 타입의 값을 반환한다는 의미이며, 여기서 제네릭 타입 `T`는 `String`으로, `E`는 `io::Error`로 구체화되었다.

만약 이 함수가 문제 없이 성공하면, 호출한 코드는 `String` 타입의 `username`을 담은 `Ok` 값을 받는다. 반면 함수가 문제를 겪으면, 호출한 코드는 `io::Error` 인스턴스를 담은 `Err` 값을 받는다. 이 함수의 반환 타입으로 `io::Error`를 선택한 이유는, 함수 내부에서 호출하는 두 작업(`File::open` 함수와 `read_to_string` 메서드) 모두 실패 시 `io::Error` 타입의 에러 값을 반환하기 때문이다.

함수의 본문은 `File::open` 함수를 호출하는 것으로 시작한다. 그리고 `match`를 사용해 `Result` 값을 처리한다. `File::open`이 성공하면, 패턴 변수 `file`의 파일 핸들이 `username_file` 변수의 값이 되고 함수는 계속 실행된다. `Err` 경우에는 `panic!`을 호출하는 대신, `return` 키워드를 사용해 함수를 조기에 종료하고 `File::open`에서 반환된 에러 값을 호출한 코드로 전달한다.

`username_file`에 파일 핸들이 있다면, 함수는 `username` 변수에 새로운 `String`을 생성하고 `username_file`의 파일 핸들에서 `read_to_string` 메서드를 호출해 파일 내용을 `username`에 읽어온다. `read_to_string` 메서드도 실패할 수 있으므로 `Result`를 반환한다. 따라서 이 `Result`를 처리하기 위해 또 다른 `match`가 필요하다. `read_to_string`이 성공하면, 함수는 성공한 것으로 간주하고 `username`에 있는 파일 내용을 `Ok`로 감싸 반환한다. `read_to_string`이 실패하면, `File::open`의 반환 값을 처리한 `match`와 동일한 방식으로 에러 값을 반환한다. 단, `return`을 명시적으로 쓸 필요는 없는데, 이는 함수의 마지막 표현식이기 때문이다.

이 함수를 호출한 코드는 `username`을 담은 `Ok` 값이나 `io::Error`를 담은 `Err` 값을 받게 된다. 호출한 코드는 이 값을 어떻게 처리할지 결정할 수 있다. 예를 들어, `Err` 값을 받으면 `panic!`을 호출해 프로그램을 종료하거나, 기본 사용자 이름을 사용하거나, 파일 이외의 다른 곳에서 사용자 이름을 조회할 수 있다. 호출한 코드가 실제로 무엇을 하려는지 충분한 정보가 없으므로, 모든 성공 또는 에러 정보를 위로 전파해 적절히 처리하도록 한다.

이러한 에러 전파 패턴은 Rust에서 매우 흔하기 때문에, Rust는 이를 더 쉽게 만들기 위해 물음표 연산자 `?`를 제공한다.


#### 오류 전파를 위한 단축키: `?` 연산자

리스트 9-7은 `read_username_from_file` 함수를 구현한 코드로, 리스트 9-6과 동일한 기능을 수행하지만 이번에는 `?` 연산자를 사용한다.

<Listing number="9-7" file-name="src/main.rs" caption="`?` 연산자를 사용해 오류를 호출 코드로 반환하는 함수">

```rust
{{#include ../listings/ch09-error-handling/listing-09-07/src/main.rs:here}}
```

</Listing>

`Result` 값 뒤에 위치한 `?`는 리스트 9-6에서 `Result` 값을 처리하기 위해 정의한 `match` 표현식과 거의 동일하게 동작한다. `Result` 값이 `Ok`라면, `Ok` 내부의 값이 반환되고 프로그램은 계속 실행된다. 만약 값이 `Err`라면, `Err`은 `return` 키워드를 사용한 것처럼 전체 함수에서 반환되며, 오류 값이 호출 코드로 전파된다.

리스트 9-6의 `match` 표현식과 `?` 연산자의 차이점이 있다. `?` 연산자가 호출된 오류 값은 표준 라이브러리의 `From` 트레이트에 정의된 `from` 함수를 거친다. 이 함수는 한 타입의 값을 다른 타입으로 변환하는 데 사용된다. `?` 연산자가 `from` 함수를 호출하면, 받은 오류 타입은 현재 함수의 반환 타입으로 정의된 오류 타입으로 변환된다. 이는 함수가 여러 가지 이유로 실패할 수 있는 경우에도, 하나의 오류 타입을 반환해 모든 실패 사례를 표현할 때 유용하다.

예를 들어, 리스트 9-7의 `read_username_from_file` 함수를 수정해 `OurError`라는 커스텀 오류 타입을 반환하도록 할 수 있다. 만약 `io::Error`에서 `OurError` 인스턴스를 생성하기 위해 `impl From<io::Error> for OurError`를 정의한다면, `read_username_from_file` 함수 본문의 `?` 연산자 호출은 `from`을 호출해 오류 타입을 변환한다. 이때 함수에 추가 코드를 작성할 필요는 없다.

리스트 9-7의 맥락에서, `File::open` 호출 끝에 있는 `?`는 `Ok` 내부의 값을 `username_file` 변수에 반환한다. 만약 오류가 발생하면, `?` 연산자는 전체 함수에서 조기에 반환되며, `Err` 값을 호출 코드에 전달한다. `read_to_string` 호출 끝에 있는 `?`도 동일하게 동작한다.

`?` 연산자는 많은 보일러플레이트 코드를 제거하고 함수 구현을 더 간단하게 만든다. 메서드 호출을 `?` 뒤에 바로 연결해 코드를 더 짧게 만들 수도 있다. 리스트 9-8에서 이를 확인할 수 있다.

<Listing number="9-8" file-name="src/main.rs" caption="`?` 연산자 뒤에 메서드 호출 연결하기">

```rust
{{#include ../listings/ch09-error-handling/listing-09-08/src/main.rs:here}}
```

</Listing>

`username`에 새로운 `String`을 생성하는 부분을 함수 시작 부분으로 옮겼다. 이 부분은 변경되지 않았다. `username_file` 변수를 생성하는 대신, `read_to_string` 호출을 `File::open("hello.txt")?`의 결과에 바로 연결했다. `read_to_string` 호출 끝에는 여전히 `?`가 있으며, `File::open`과 `read_to_string`이 모두 성공하면 `username`을 포함한 `Ok` 값을 반환한다. 이 구현은 리스트 9-6과 리스트 9-7과 동일한 기능을 제공하지만, 더 간결하고 편리한 방식으로 작성되었다.

리스트 9-9는 `fs::read_to_string`을 사용해 코드를 더 짧게 만드는 방법을 보여준다.

<Listing number="9-9" file-name="src/main.rs" caption="파일을 열고 읽는 대신 `fs::read_to_string` 사용하기">

```rust
{{#include ../listings/ch09-error-handling/listing-09-09/src/main.rs:here}}
```

</Listing>

파일을 문자열로 읽어오는 작업은 꽤 일반적이기 때문에, 표준 라이브러리는 파일을 열고, 새로운 `String`을 생성하고, 파일 내용을 읽어 그 내용을 `String`에 넣어 반환하는 편리한 `fs::read_to_string` 함수를 제공한다. 물론, `fs::read_to_string`을 사용하면 모든 오류 처리에 대해 설명할 기회를 제공하지 않기 때문에, 먼저 더 긴 방식으로 설명했다.


#### `?` 연산자를 사용할 수 있는 위치

`?` 연산자는 반환 타입이 `?`가 사용된 값과 호환되는 함수에서만 사용할 수 있다. 이는 `?` 연산자가 함수에서 값을 조기에 반환하도록 정의되어 있기 때문이다. 이 동작은 리스트 9-6에서 정의한 `match` 표현식과 유사하다. 리스트 9-6에서 `match`는 `Result` 값을 사용했고, 조기 반환 분기에서는 `Err(e)` 값을 반환했다. 함수의 반환 타입은 이 `return`과 호환되도록 `Result`여야 한다.

리스트 9-10에서는 반환 타입이 `?`를 사용한 값의 타입과 호환되지 않는 `main` 함수에서 `?` 연산자를 사용할 때 발생하는 오류를 살펴본다.

<Listing number="9-10" file-name="src/main.rs" caption="`()`를 반환하는 `main` 함수에서 `?`를 사용하려고 하면 컴파일되지 않는다.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-10/src/main.rs}}
```

</Listing>

이 코드는 파일을 열려고 시도하며, 이 작업은 실패할 수 있다. `?` 연산자는 `File::open`이 반환한 `Result` 값을 따라가지만, 이 `main` 함수의 반환 타입은 `Result`가 아닌 `()`이다. 이 코드를 컴파일하면 다음과 같은 오류 메시지가 나타난다:

```console
{{#include ../listings/ch09-error-handling/listing-09-10/output.txt}}
```

이 오류는 `?` 연산자를 `Result`, `Option`, 또는 `FromResidual`을 구현한 타입을 반환하는 함수에서만 사용할 수 있음을 지적한다.

이 오류를 해결하려면 두 가지 선택지가 있다. 첫 번째는 함수의 반환 타입을 `?` 연산자를 사용한 값과 호환되도록 변경하는 것이다. 두 번째는 `match` 또는 `Result<T, E>` 메서드 중 하나를 사용해 `Result<T, E>`를 적절히 처리하는 것이다.

오류 메시지는 `?`가 `Option<T>` 값과도 사용될 수 있음을 언급한다. `Result`에서 `?`를 사용하는 것과 마찬가지로, `Option`에서 `?`를 사용하려면 함수가 `Option`을 반환해야 한다. `Option<T>`에서 `?` 연산자를 호출할 때의 동작은 `Result<T, E>`에서 호출할 때와 유사하다. 값이 `None`이면 `None`이 함수에서 조기 반환된다. 값이 `Some`이면 `Some` 내부의 값이 표현식의 결과 값이 되고, 함수는 계속 실행된다. 리스트 9-11은 주어진 텍스트의 첫 번째 줄의 마지막 문자를 찾는 함수의 예제를 보여준다.

<Listing number="9-11" caption="`Option<T>` 값에서 `?` 연산자 사용">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-11/src/main.rs:here}}
```

</Listing>

이 함수는 `Option<char>`를 반환한다. 문자가 있을 수도 있지만, 없을 수도 있기 때문이다. 이 코드는 `text` 문자열 슬라이스를 인자로 받아 `lines` 메서드를 호출한다. 이 메서드는 문자열의 줄에 대한 반복자를 반환한다. 이 함수는 첫 번째 줄을 검사하려고 하므로, 반복자에서 첫 번째 값을 가져오기 위해 `next`를 호출한다. `text`가 빈 문자열이면 `next`는 `None`을 반환하며, 이 경우 `?`를 사용해 `last_char_of_first_line`에서 `None`을 반환한다. `text`가 빈 문자열이 아니면 `next`는 `text`의 첫 번째 줄에 대한 문자열 슬라이스를 포함한 `Some` 값을 반환한다.

`?`는 문자열 슬라이스를 추출하고, 이 문자열 슬라이스에 대해 `chars`를 호출해 문자에 대한 반복자를 얻는다. 첫 번째 줄의 마지막 문자에 관심이 있으므로, `last`를 호출해 반복자의 마지막 항목을 반환한다. 이는 `Option`인데, 첫 번째 줄이 빈 문자열일 수도 있기 때문이다. 예를 들어, `text`가 빈 줄로 시작하지만 다른 줄에 문자가 있는 경우(`"\nhi"`와 같이)가 있다. 그러나 첫 번째 줄에 마지막 문자가 있으면 `Some` 변형으로 반환된다. 중간에 있는 `?` 연산자는 이 로직을 간결하게 표현할 수 있게 해주며, 함수를 한 줄로 구현할 수 있게 한다. `Option`에서 `?` 연산자를 사용할 수 없다면, 더 많은 메서드 호출이나 `match` 표현식을 사용해 이 로직을 구현해야 할 것이다.

`Result`를 반환하는 함수에서는 `Result`에 대해 `?` 연산자를 사용할 수 있고, `Option`을 반환하는 함수에서는 `Option`에 대해 `?` 연산자를 사용할 수 있지만, 둘을 혼합해서 사용할 수는 없다. `?` 연산자는 `Result`를 `Option`으로 자동 변환하거나 그 반대로 변환하지 않는다. 이러한 경우에는 `Result`의 `ok` 메서드나 `Option`의 `ok_or` 메서드를 사용해 명시적으로 변환할 수 있다.

지금까지 사용한 모든 `main` 함수는 `()`를 반환했다. `main` 함수는 실행 파일의 진입점이자 종료점이므로, 프로그램이 예상대로 동작하도록 반환 타입에 제한이 있다.

다행히, `main` 함수는 `Result<(), E>`를 반환할 수도 있다. 리스트 9-12는 리스트 9-10의 코드를 보여주지만, `main`의 반환 타입을 `Result<(), Box<dyn Error>>`로 변경하고 마지막에 `Ok(())` 반환 값을 추가했다. 이제 이 코드는 컴파일된다.

<Listing number="9-12" file-name="src/main.rs" caption="`main`이 `Result<(), E>`를 반환하도록 변경하면 `Result` 값에서 `?` 연산자를 사용할 수 있다.">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-12/src/main.rs}}
```

</Listing>

`Box<dyn Error>` 타입은 _트레이트 객체_로, 18장의 ["다양한 타입의 값을 허용하는 트레이트 객체 사용하기"][trait-objects]<!-- ignore -->에서 설명할 것이다. 지금은 `Box<dyn Error>`를 "어떤 종류의 오류"로 이해하면 된다. `main` 함수에서 오류 타입이 `Box<dyn Error>`인 `Result` 값에 `?`를 사용할 수 있는 이유는, 이 타입이 모든 `Err` 값을 조기에 반환할 수 있기 때문이다. 이 `main` 함수의 본문이 `std::io::Error` 타입의 오류만 반환하더라도, `Box<dyn Error>`를 지정하면 `main`의 본문에 다른 오류를 반환하는 코드를 추가해도 이 시그니처는 계속 유효하다.

`main` 함수가 `Result<(), E>`를 반환하면, `main`이 `Ok(())`를 반환하면 실행 파일은 `0`으로 종료되고, `Err` 값을 반환하면 0이 아닌 값으로 종료된다. C로 작성된 실행 파일은 종료 시 정수를 반환한다. 성공적으로 종료된 프로그램은 정수 `0`을 반환하고, 오류가 발생한 프로그램은 0이 아닌 정수를 반환한다. Rust도 이 관례와 호환되도록 실행 파일에서 정수를 반환한다.

`main` 함수는 [`std::process::Termination` 트레이트][termination]<!-- ignore -->를 구현한 모든 타입을 반환할 수 있다. 이 트레이트는 `ExitCode`를 반환하는 `report` 함수를 포함한다. 자신만의 타입에 대해 `Termination` 트레이트를 구현하는 방법에 대한 자세한 내용은 표준 라이브러리 문서를 참조하라.

이제 `panic!`을 호출하거나 `Result`를 반환하는 방법에 대해 논의했으므로, 어떤 경우에 어떤 것을 사용할지 결정하는 방법으로 돌아가보자.

[handle_failure]: ch02-00-guessing-game-tutorial.html#handling-potential-failure-with-result
[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-that-allow-for-values-of-different-types
[termination]: ../std/process/trait.Termination.html


