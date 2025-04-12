## 슬라이스 타입

**슬라이스**는 컬렉션 전체가 아닌 연속된 일부 엘리먼트를 참조할 수 있게 해준다. 슬라이스는 참조 타입이기 때문에 소유권을 가지지 않는다.

간단한 프로그래밍 문제를 살펴보자: 공백으로 구분된 단어들로 이루어진 문자열을 입력받아 첫 번째 단어를 반환하는 함수를 작성해 보자. 만약 문자열에 공백이 없다면 전체 문자열이 하나의 단어이므로, 문자열 전체를 반환해야 한다.

슬라이스가 어떤 문제를 해결하는지 이해하기 위해, 먼저 슬라이스를 사용하지 않고 이 함수의 시그니처를 작성하는 방법을 생각해 보자:

```rust,ignore
fn first_word(s: &String) -> ?
```

`first_word` 함수는 `&String`을 파라미터로 받는다. 소유권이 필요하지 않으므로 이 방식은 적절하다. (관용적인 Rust 코드에서는 필요하지 않은 경우 함수가 인자의 소유권을 가져가지 않는다. 이에 대한 이유는 계속 진행하면서 명확해질 것이다!) 하지만 무엇을 반환해야 할까? 문자열의 일부를 표현할 방법이 없다. 대신 공백으로 표시된 단어의 끝 인덱스를 반환할 수 있다. 이를 시도해 보자. 아래 리스트 4-7에서 확인할 수 있다.

<Listing number="4-7" file-name="src/main.rs" caption="`String` 파라미터의 바이트 인덱스 값을 반환하는 `first_word` 함수">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:here}}
```

</Listing>

`String`을 하나씩 순회하며 공백인지 확인해야 하므로, `as_bytes` 메서드를 사용해 `String`을 바이트 배열로 변환한다.

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:as_bytes}}
```

다음으로, `iter` 메서드를 사용해 바이트 배열에 대한 이터레이터를 생성한다:

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:iter}}
```

이터레이터에 대해서는 [13장][ch13]<!-- ignore -->에서 자세히 다룰 것이다. 지금은 `iter`가 컬렉션의 각 엘리먼트를 반환하는 메서드이고, `enumerate`가 `iter`의 결과를 감싸서 각 엘리먼트를 튜플의 일부로 반환한다는 점만 알아두자. `enumerate`가 반환하는 튜플의 첫 번째 요소는 인덱스이고, 두 번째 요소는 엘리먼트에 대한 참조이다. 이는 인덱스를 직접 계산하는 것보다 편리하다.

`enumerate` 메서드는 튜플을 반환하므로, 패턴을 사용해 튜플을 분해할 수 있다. 패턴에 대해서는 [6장][ch6]<!-- ignore -->에서 더 자세히 설명할 것이다. `for` 루프에서 튜플의 인덱스에 해당하는 `i`와 튜플의 단일 바이트에 해당하는 `&item` 패턴을 지정한다. `.iter().enumerate()`에서 엘리먼트에 대한 참조를 얻기 때문에 패턴에 `&`를 사용한다.

`for` 루프 내부에서는 바이트 리터럴 문법을 사용해 공백을 나타내는 바이트를 찾는다. 공백을 찾으면 해당 위치를 반환한다. 그렇지 않으면 `s.len()`을 사용해 문자열의 길이를 반환한다.

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:inside_for}}
```

이제 문자열에서 첫 번째 단어의 끝 인덱스를 찾는 방법을 알게 되었지만, 문제가 있다. `usize`를 단독으로 반환하지만, 이 값은 `&String`의 컨텍스트에서만 의미가 있다. 즉, `String`과 별개의 값이기 때문에 이 값이 나중에도 유효할 것이라는 보장이 없다. 리스트 4-7의 `first_word` 함수를 사용하는 리스트 4-8의 프로그램을 살펴보자.

<Listing number="4-8" file-name="src/main.rs" caption="`first_word` 함수를 호출한 결과를 저장한 후 `String` 내용을 변경">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-08/src/main.rs:here}}
```

</Listing>

이 프로그램은 아무런 오류 없이 컴파일되며, `s.clear()`를 호출한 후에도 `word`를 사용할 수 있다. `word`는 `s`의 상태와 전혀 연결되어 있지 않기 때문에, `word`는 여전히 값 `5`를 가지고 있다. 이 값 `5`를 변수 `s`와 함께 사용해 첫 번째 단어를 추출하려고 할 수 있지만, 이는 버그이다. 왜냐하면 `word`에 `5`를 저장한 이후로 `s`의 내용이 변경되었기 때문이다.

`word`의 인덱스가 `s`의 데이터와 동기화되지 않을까 걱정하는 것은 지루하고 오류가 발생하기 쉽다! `second_word` 함수를 작성한다면 이러한 인덱스 관리가 더욱 까다로워질 것이다. 이 함수의 시그니처는 다음과 같을 것이다:

```rust,ignore
fn second_word(s: &String) -> (usize, usize) {
```

이제 시작 인덱스와 끝 인덱스를 모두 추적해야 하며, 특정 상태에서 계산되었지만 그 상태와 전혀 연결되지 않은 더 많은 값들이 생긴다. 동기화를 유지해야 하는 서로 관련 없는 세 변수가 존재하게 된다.

다행히 Rust는 이 문제에 대한 해결책을 제공한다: 문자열 슬라이스.


### 문자열 슬라이스

_문자열 슬라이스_는 `String`의 일부를 참조하는 것으로, 다음과 같이 생겼다:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-17-slice/src/main.rs:here}}
```

`hello`는 전체 `String`을 참조하는 대신, 추가적인 `[0..5]` 부분으로 지정된 `String`의 일부를 참조한다. 슬라이스는 대괄호 안에 범위를 지정해 생성하며, `[시작_인덱스..종료_인덱스]` 형식을 사용한다. 여기서 _`시작_인덱스`_는 슬라이스의 첫 번째 위치이고, _`종료_인덱스`_는 슬라이스의 마지막 위치보다 하나 더 큰 값이다. 내부적으로 슬라이스 데이터 구조는 시작 위치와 슬라이스의 길이를 저장하며, 이 길이는 _`종료_인덱스`_에서 _`시작_인덱스`_를 뺀 값과 같다. 따라서 `let world = &s[6..11];`의 경우, `world`는 `s`의 인덱스 6에 있는 바이트를 가리키는 포인터와 길이 값 `5`를 갖는 슬라이스가 된다.

그림 4-7은 이를 다이어그램으로 보여준다.

<img alt="Three tables: a table representing the stack data of s, which points
to the byte at index 0 in a table of the string data &quot;hello world&quot; on
the heap. The third table rep-resents the stack data of the slice world, which
has a length value of 5 and points to byte 6 of the heap data table."
src="img/trpl04-07.svg" class="center" style="width: 50%;" />

<span class="caption">그림 4-7: `String`의 일부를 참조하는 문자열 슬라이스</span>

Rust의 `..` 범위 문법을 사용할 때, 인덱스 0에서 시작하려면 두 점 앞의 값을 생략할 수 있다. 즉, 다음 두 코드는 동일하다:

```rust
let s = String::from("hello");

let slice = &s[0..2];
let slice = &s[..2];
```

마찬가지로, 슬라이스가 `String`의 마지막 바이트를 포함한다면, 뒤의 숫자를 생략할 수 있다. 따라서 다음 두 코드는 동일하다:

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[3..len];
let slice = &s[3..];
```

두 값을 모두 생략하면 전체 문자열의 슬라이스를 가져올 수 있다. 따라서 다음 두 코드는 동일하다:

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[0..len];
let slice = &s[..];
```

> 주의: 문자열 슬라이스의 범위 인덱스는 유효한 UTF-8 문자 경계에서 발생해야 한다. 멀티바이트 문자 중간에 문자열 슬라이스를 만들려고 하면 프로그램이 오류와 함께 종료된다. 문자열 슬라이스를 소개하는 목적상, 이 섹션에서는 ASCII만 가정한다. UTF-8 처리에 대한 더 자세한 내용은 8장의 [“Storing UTF-8 Encoded Text with Strings”][strings]<!-- ignore --> 섹션에서 다룬다.

이 모든 정보를 염두에 두고, `first_word` 함수를 슬라이스를 반환하도록 다시 작성해보자. "문자열 슬라이스"를 나타내는 타입은 `&str`로 작성한다:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-18-first-word-slice/src/main.rs:here}}
```

</Listing>

단어의 끝 인덱스는 Listing 4-7에서와 같은 방식으로, 첫 번째 공백을 찾아서 얻는다. 공백을 찾으면 문자열의 시작과 공백의 인덱스를 각각 시작과 종료 인덱스로 사용해 문자열 슬라이스를 반환한다.

이제 `first_word`를 호출하면, 기본 데이터에 연결된 단일 값을 반환한다. 이 값은 슬라이스의 시작점을 참조하는 포인터와 슬라이스의 요소 수로 구성된다.

슬라이스를 반환하는 방식은 `second_word` 함수에도 동일하게 적용할 수 있다:

```rust,ignore
fn second_word(s: &String) -> &str {
```

이제 컴파일러가 `String`에 대한 참조가 유효한지 확인해주기 때문에, 실수하기 어려운 직관적인 API를 갖게 되었다. Listing 4-8의 버그를 기억하는가? 첫 번째 단어의 끝 인덱스를 얻은 후 문자열을 비워서 인덱스가 무효화된 상황이었다. 그 코드는 논리적으로 잘못되었지만 즉각적인 오류를 표시하지 않았다. 빈 문자열과 함께 첫 번째 단어 인덱스를 계속 사용하려고 하면 나중에 문제가 발생할 것이다. 슬라이스를 사용하면 이 버그를 불가능하게 만들고, 코드에 문제가 있음을 훨씬 빨리 알 수 있다. 슬라이스 버전의 `first_word`를 사용하면 컴파일 타임 오류가 발생한다:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-19-slice-error/src/main.rs:here}}
```

</Listing>

컴파일러 오류는 다음과 같다:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-19-slice-error/output.txt}}
```

빌림 규칙을 떠올려보면, 무언가에 대한 불변 참조가 있는 경우 가변 참조를 동시에 가질 수 없다. `clear`는 `String`을 잘라내야 하므로 가변 참조가 필요하다. `clear` 호출 후의 `println!`은 `word`의 참조를 사용하므로, 그 시점에 불변 참조가 여전히 활성 상태여야 한다. Rust는 `clear`의 가변 참조와 `word`의 불변 참조가 동시에 존재하는 것을 허용하지 않으며, 컴파일이 실패한다. Rust는 우리의 API를 더 쉽게 사용할 수 있게 만들었을 뿐만 아니라, 컴파일 타임에 오류의 전체 클래스를 제거했다!

<!-- Old heading. Do not remove or links may break. -->

<a id="string-literals-are-slices"></a>


#### 문자열 리터럴과 슬라이스

이전에 문자열 리터럴이 바이너리 안에 저장된다고 설명했다. 이제 슬라이스에 대해 알았으니 문자열 리터럴을 제대로 이해할 수 있다:

```rust
let s = "Hello, world!";
```

여기서 `s`의 타입은 `&str`이다. 이는 바이너리의 특정 지점을 가리키는 슬라이스를 의미한다. 이것이 문자열 리터럴이 불변인 이유이기도 하다. `&str`은 불변 참조이기 때문이다.


#### 문자열 슬라이스를 파라미터로 사용하기

리터럴과 `String` 값에서 슬라이스를 추출할 수 있다는 사실을 알면, `first_word` 함수를 한 단계 더 개선할 수 있다. 현재 함수 시그니처는 다음과 같다:

```rust,ignore
fn first_word(s: &String) -> &str {
```

경험이 많은 Rust 개발자라면 리스트 4-9와 같은 시그니처를 작성할 것이다. 이 방식은 `&String` 값과 `&str` 값 모두에 동일한 함수를 사용할 수 있게 해준다.

<Listing number="4-9" caption="`first_word` 함수 개선: `s` 파라미터 타입을 문자열 슬라이스로 변경">

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-09/src/main.rs:here}}
```

</Listing>

문자열 슬라이스가 있다면 이를 직접 전달할 수 있다. `String`이 있다면 `String`의 슬라이스나 `String`에 대한 참조를 전달할 수 있다. 이 유연성은 *역참조 강제 변환(deref coercions)*을 활용한 것으로, 이 기능은 15장의 ["함수와 메서드에서의 암묵적 역참조 강제 변환"][deref-coercions]<!--ignore--> 섹션에서 자세히 다룬다.

`String`에 대한 참조 대신 문자열 슬라이스를 파라미터로 받도록 함수를 정의하면, 기능을 잃지 않으면서도 API를 더 일반적이고 유용하게 만들 수 있다:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-09/src/main.rs:usage}}
```

</Listing>


### 다른 슬라이스

문자열 슬라이스는 문자열에 특화된 개념이다. 하지만 더 일반적인 슬라이스 타입도 존재한다. 다음 배열을 살펴보자:

```rust
let a = [1, 2, 3, 4, 5];
```

문자열의 일부를 참조하듯이, 배열의 일부를 참조할 수도 있다. 이를 다음과 같이 구현할 수 있다:

```rust
let a = [1, 2, 3, 4, 5];

let slice = &a[1..3];

assert_eq!(slice, &[2, 3]);
```

이 슬라이스는 `&[i32]` 타입을 가진다. 문자열 슬라이스와 동일한 방식으로 작동하며, 첫 번째 요소에 대한 참조와 길이를 저장한다. 다양한 컬렉션에서 이와 같은 슬라이스를 사용할 수 있다. 8장에서 벡터를 다룰 때 이러한 컬렉션에 대해 자세히 설명할 것이다.


## 요약

Rust에서 소유권(ownership), 대여(borrowing), 그리고 슬라이스(slices) 개념은 컴파일 타임에 메모리 안전성을 보장한다. Rust는 다른 시스템 프로그래밍 언어와 마찬가지로 메모리 사용을 제어할 수 있게 해주지만, 데이터의 소유자가 범위를 벗어날 때 자동으로 데이터를 정리하는 기능을 제공한다. 이를 통해 추가 코드를 작성하거나 디버깅하지 않아도 메모리 관리를 효과적으로 할 수 있다.

소유권은 Rust의 여러 기능에 영향을 미치기 때문에, 이 책의 나머지 부분에서 이 개념들을 더 깊이 다룰 것이다. 이제 5장으로 넘어가서 `struct`를 사용해 데이터를 그룹화하는 방법을 살펴보자.

[ch13]: ch13-02-iterators.html
[ch6]: ch06-02-match.html#patterns-that-bind-to-values
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[deref-coercions]: ch15-02-deref.html#implicit-deref-coercions-with-functions-and-methods


