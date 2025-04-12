## 부록 A: 예약어

아래 목록은 Rust 언어가 현재 또는 미래에 사용하기 위해 예약해 둔 키워드들이다. 따라서 이 키워드들은 일반적인 식별자로 사용할 수 없다(단, "[Raw Identifiers][raw-identifiers]<!-- ignore -->" 섹션에서 설명할 raw 식별자로는 사용 가능). 식별자란 함수, 변수, 매개변수, 구조체 필드, 모듈, 크레이트, 상수, 매크로, 정적 값, 속성, 타입, 트레잇, 라이프타임 등의 이름을 의미한다.

[raw-identifiers]: #raw-identifiers


### 현재 사용 중인 키워드

다음은 현재 사용 중인 키워드 목록과 각각의 기능 설명이다.

- `as` - 기본 타입 캐스팅, 특정 트레이트 내 항목의 모호성 제거, `use` 문에서 항목 이름 변경
- `async` - 현재 스레드를 블로킹하지 않고 `Future`를 반환
- `await` - `Future`의 결과가 준비될 때까지 실행을 일시 중지
- `break` - 루프를 즉시 종료
- `const` - 상수 항목 또는 상수 원시 포인터 정의
- `continue` - 다음 루프 반복으로 이동
- `crate` - 모듈 경로에서 크레이트 루트를 참조
- `dyn` - 트레이트 객체에 대한 동적 디스패치
- `else` - `if` 및 `if let` 제어 구조에 대한 대체 처리
- `enum` - 열거형 정의
- `extern` - 외부 함수 또는 변수 연결
- `false` - 불리언 거짓 리터럴
- `fn` - 함수 또는 함수 포인터 타입 정의
- `for` - 이터레이터에서 항목을 순회하거나, 트레이트를 구현하거나, 고차 수명을 지정
- `if` - 조건식의 결과에 따라 분기
- `impl` - 고유 또는 트레이트 기능 구현
- `in` - `for` 루프 문법의 일부
- `let` - 변수 바인딩
- `loop` - 무조건 루프 실행
- `match` - 값을 패턴과 매칭
- `mod` - 모듈 정의
- `move` - 클로저가 모든 캡처를 소유하도록 만듦
- `mut` - 참조, 원시 포인터 또는 패턴 바인딩에서 변경 가능성 표시
- `pub` - 구조체 필드, `impl` 블록 또는 모듈에서 공개 가시성 표시
- `ref` - 참조로 바인딩
- `return` - 함수에서 반환
- `Self` - 정의하거나 구현 중인 타입의 별칭
- `self` - 메서드 주체 또는 현재 모듈
- `static` - 전역 변수 또는 프로그램 실행 전체에 걸친 수명
- `struct` - 구조체 정의
- `super` - 현재 모듈의 상위 모듈
- `trait` - 트레이트 정의
- `true` - 불리언 참 리터럴
- `type` - 타입 별칭 또는 연관 타입 정의
- `union` - [유니온][union] 정의; 유니온 선언에서만 키워드로 사용됨
- `unsafe` - 안전하지 않은 코드, 함수, 트레이트 또는 구현 표시
- `use` - 심볼을 범위로 가져오기; 제네릭 및 수명 경계에 대한 정확한 캡처 지정
- `where` - 타입을 제약하는 절 표시
- `while` - 조건식의 결과에 따라 루프 실행

[union]: ../reference/items/unions.html


### 미래 사용을 위해 예약된 키워드

다음 키워드들은 현재는 아무런 기능이 없지만, Rust에서 미래에 사용할 가능성을 위해 예약되어 있다.

- `abstract`
- `become`
- `box`
- `do`
- `final`
- `gen`
- `macro`
- `override`
- `priv`
- `try`
- `typeof`
- `unsized`
- `virtual`
- `yield`


### Raw Identifiers (원시 식별자)

_원시 식별자_는 일반적으로 허용되지 않는 곳에서 키워드를 사용할 수 있게 해주는 문법이다. 키워드 앞에 `r#`를 붙여 원시 식별자를 사용한다.

예를 들어, `match`는 키워드다. `match`를 함수 이름으로 사용하려고 다음과 같이 코드를 작성하면:

<span class="filename">파일명: src/main.rs</span>

```rust,ignore,does_not_compile
fn match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}
```

다음과 같은 오류가 발생한다:

```text
error: expected identifier, found keyword `match`
 --> src/main.rs:4:4
  |
4 | fn match(needle: &str, haystack: &str) -> bool {
  |    ^^^^^ expected identifier, found keyword
```

오류 메시지는 `match` 키워드를 함수 식별자로 사용할 수 없음을 보여준다. `match`를 함수 이름으로 사용하려면 원시 식별자 문법을 사용해야 한다. 다음과 같이 작성하면 된다:

<span class="filename">파일명: src/main.rs</span>

```rust
fn r#match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}

fn main() {
    assert!(r#match("foo", "foobar"));
}
```

이 코드는 오류 없이 컴파일된다. 함수 정의와 `main` 함수에서 함수를 호출할 때 모두 `r#` 접두사가 붙어 있음을 주목하라.

원시 식별자를 사용하면 예약어로 지정된 단어도 식별자로 사용할 수 있다. 이를 통해 식별자 이름을 더 자유롭게 선택할 수 있으며, 다른 언어로 작성된 프로그램과 통합할 때도 유용하다. 또한 원시 식별자를 사용하면 현재 크레이트와 다른 Rust 버전으로 작성된 라이브러리를 사용할 수 있다. 예를 들어, `try`는 2015 버전에서는 키워드가 아니지만 2018, 2021, 2024 버전에서는 키워드다. 2015 버전으로 작성된 라이브러리를 사용하고 그 안에 `try` 함수가 있다면, 이후 버전에서 이 함수를 호출할 때 원시 식별자 문법인 `r#try`를 사용해야 한다. 버전에 대한 더 자세한 정보는 [부록 E][appendix-e]<!-- ignore -->를 참고하라.

[appendix-e]: appendix-05-editions.html


