## 패턴이 사용될 수 있는 모든 곳

러스트에서 패턴은 다양한 곳에서 등장한다. 여러분은 이미 패턴을 많이 사용하고 있었지만, 이를 깨닫지 못했을 수 있다. 이 섹션에서는 패턴이 유효하게 사용될 수 있는 모든 경우를 살펴본다.


### `match` Arm

6장에서 다룬 것처럼, `match` 표현식의 각 Arm에는 패턴을 사용한다. 공식적으로 `match` 표현식은 `match` 키워드, 매칭할 값, 그리고 패턴과 그 패턴에 해당하는 경우 실행할 표현식으로 구성된 하나 이상의 Arm으로 정의된다. 아래와 같은 구조를 가진다.

<pre><code>match <em>VALUE</em> {
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
}</code></pre>

예를 들어, 리스팅 6-5의 `match` 표현식은 변수 `x`에 저장된 `Option<i32>` 타입의 값을 매칭한다.

```rust,ignore
match x {
    None => None,
    Some(i) => Some(i + 1),
}
```

이 `match` 표현식에서 각 화살표 왼쪽에 있는 `None`과 `Some(i)`가 패턴이다.

`match` 표현식은 반드시 모든 가능성을 다뤄야 한다는 점에서 **완전성(exhaustive)**이 요구된다. 모든 가능성을 다루기 위한 한 가지 방법은 마지막 Arm에 모든 경우를 포괄하는 패턴을 추가하는 것이다. 예를 들어, 어떤 값이든 매칭할 수 있는 변수 이름을 사용하면 실패할 일이 없으므로 나머지 모든 경우를 커버할 수 있다.

특히 `_` 패턴은 어떤 값과도 매칭되지만, 변수에 바인딩되지 않는다. 따라서 주로 마지막 `match` Arm에서 사용된다. `_` 패턴은 지정되지 않은 값을 무시하고 싶을 때 유용하다. 이 패턴에 대한 자세한 내용은 이 장의 뒷부분인 ["패턴에서 값 무시하기"][ignoring-values-in-a-pattern]<!-- ignore -->에서 다룰 것이다.


### 조건부 `if let` 표현식

6장에서는 `if let` 표현식을 주로 한 가지 경우만 매칭하는 `match`의 짧은 형태로 사용하는 방법을 다뤘다. 추가적으로, `if let`은 패턴이 매칭되지 않을 때 실행할 코드를 포함하는 `else`를 함께 사용할 수 있다.

Listing 19-1은 `if let`, `else if`, `else if let` 표현식을 혼합하여 사용할 수 있음을 보여준다. 이렇게 하면 하나의 값만 패턴과 비교할 수 있는 `match` 표현식보다 더 많은 유연성을 얻을 수 있다. 또한 Rust는 `if let`, `else if`, `else if let`의 조건들이 서로 관련이 있을 것을 요구하지 않는다.

Listing 19-1의 코드는 여러 조건을 검사하여 배경색을 결정한다. 이 예제에서는 실제 프로그램이 사용자 입력으로 받을 수 있는 값을 하드코딩한 변수를 사용했다.

<Listing number="19-1" file-name="src/main.rs" caption="`if let`, `else if`, `else if let`, `else` 혼합 사용">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-01/src/main.rs}}
```

</Listing>

사용자가 선호하는 색상을 지정하면 그 색상이 배경색으로 사용된다. 선호하는 색상이 지정되지 않고 오늘이 화요일이라면 배경색은 초록색이 된다. 그렇지 않고 사용자가 나이를 문자열로 지정했고 이를 숫자로 성공적으로 파싱할 수 있다면, 숫자의 값에 따라 보라색 또는 주황색이 배경색이 된다. 이 모든 조건에 해당하지 않으면 배경색은 파란색이 된다.

이 조건부 구조는 복잡한 요구사항을 지원할 수 있게 해준다. 여기서 사용한 하드코딩된 값으로 인해, 이 예제는 `Using purple as the background color`를 출력할 것이다.

`if let`은 `match`의 경우와 마찬가지로 기존 변수를 가리는 새로운 변수를 도입할 수 있다. `if let Ok(age) = age` 라인은 `Ok` 변형 내부의 값을 포함하는 새로운 `age` 변수를 도입하며, 이는 기존의 `age` 변수를 가린다. 이는 `if age > 30` 조건을 해당 블록 내에 위치시켜야 함을 의미한다. 즉, `if let Ok(age) = age && age > 30`과 같이 두 조건을 결합할 수 없다. 새로운 `age`가 30과 비교되기 위해서는 중괄호로 시작하는 새로운 스코프가 시작되어야 한다.

`if let` 표현식을 사용할 때의 단점은 컴파일러가 모든 경우를 검사하지 않는다는 점이다. 반면 `match` 표현식은 모든 경우를 검사한다. 만약 마지막 `else` 블록을 생략하고 일부 경우를 처리하지 않았다면, 컴파일러는 잠재적인 논리 오류에 대해 경고하지 않을 것이다.


### `while let` 조건부 루프

`if let`과 유사한 구조를 가진 `while let` 조건부 루프는 패턴이 계속 일치하는 동안 `while` 루프를 실행한다. 예제 19-2에서는 스레드 간에 전송된 메시지를 기다리는 `while let` 루프를 보여주지만, 이 경우 `Option` 대신 `Result`를 확인한다.

<Listing number="19-2" caption="`rx.recv()`가 `Ok`를 반환하는 동안 값을 출력하는 `while let` 루프 사용">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-02/src/main.rs:here}}
```

</Listing>

이 예제는 `1`, `2`, 그리고 `3`을 출력한다. `recv` 메서드는 채널의 수신 측에서 첫 번째 메시지를 가져와 `Ok(value)`를 반환한다. 16장에서 `recv`를 처음 봤을 때, 에러를 직접 언래핑하거나 `for` 루프를 사용해 반복자로 다뤘다. 그러나 예제 19-2에서 보듯이, `while let`을 사용할 수도 있다. `recv` 메서드는 메시지가 도착할 때마다 `Ok`를 반환하며, 송신자가 존재하는 한 계속해서 메시지를 받다가 송신자 측이 연결을 끊으면 `Err`를 생성한다.


### `for` 반복문

`for` 반복문에서 `for` 키워드 바로 뒤에 오는 값은 패턴이다. 예를 들어, `for x in y`에서 `x`는 패턴이다. 리스트 19-3은 `for` 반복문에서 튜플을 분해하거나 나누기 위해 패턴을 사용하는 방법을 보여준다.

<Listing number="19-3" caption="`for` 반복문에서 튜플을 분해하기 위해 패턴 사용">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-03/src/main.rs:here}}
```

</Listing>

리스트 19-3의 코드는 다음과 같은 결과를 출력한다:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-03/output.txt}}
```

`enumerate` 메서드를 사용해 이터레이터를 조정하면 해당 값과 그 값의 인덱스를 튜플로 생성한다. 첫 번째로 생성된 값은 튜플 `(0, 'a')`이다. 이 값을 패턴 `(index, value)`와 매칭하면 `index`는 `0`이 되고 `value`는 `'a'`가 되어 출력의 첫 번째 줄을 출력한다.


### `let` 문

이 장을 시작하기 전에, 우리는 `match`와 `if let`에서 패턴을 사용하는 것만 명시적으로 다뤘다. 하지만 사실, 우리는 `let` 문을 포함한 다른 곳에서도 패턴을 사용해 왔다. 예를 들어, 다음과 같이 `let`을 사용한 간단한 변수 할당을 생각해 보자:

```rust
let x = 5;
```

이렇게 `let` 문을 사용할 때마다 패턴을 사용하고 있다. 물론 그것을 깨닫지 못했을 수도 있지만! 좀 더 공식적으로, `let` 문은 다음과 같이 구성된다:

<pre>
<code>let <em>PATTERN</em> = <em>EXPRESSION</em>;</code>
</pre>

`let x = 5;`와 같은 문장에서 _`PATTERN`_ 자리에 변수 이름이 오면, 이 변수 이름은 패턴의 매우 간단한 형태이다. Rust는 표현식을 패턴과 비교하고, 패턴에서 발견된 이름에 값을 할당한다. 따라서 `let x = 5;` 예제에서 `x`는 "여기에 매칭되는 값을 변수 `x`에 바인딩하라"는 의미의 패턴이다. `x`라는 이름이 전체 패턴이기 때문에, 이 패턴은 "어떤 값이든 상관없이 모든 것을 변수 `x`에 바인딩하라"는 의미가 된다.

`let`의 패턴 매칭 측면을 더 명확히 이해하기 위해, Listing 19-4를 살펴보자. 이 예제는 `let`과 함께 패턴을 사용해 튜플을 분해한다.

<Listing number="19-4" caption="패턴을 사용해 튜플을 분해하고 한 번에 세 개의 변수를 생성">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-04/src/main.rs:here}}
```

</Listing>

여기서는 튜플을 패턴과 매칭시킨다. Rust는 값 `(1, 2, 3)`을 패턴 `(x, y, z)`와 비교하고, 두 요소의 개수가 동일하므로 값이 패턴과 일치한다고 판단한다. 따라서 Rust는 `1`을 `x`에, `2`를 `y`에, `3`을 `z`에 바인딩한다. 이 튜플 패턴은 세 개의 개별 변수 패턴을 중첩한 것으로 생각할 수 있다.

만약 패턴의 요소 개수가 튜플의 요소 개수와 일치하지 않으면, 전체 타입이 일치하지 않아 컴파일러 에러가 발생한다. 예를 들어, Listing 19-5는 세 개의 요소를 가진 튜플을 두 개의 변수로 분해하려는 시도를 보여준다. 이 코드는 동작하지 않는다.

<Listing number="19-5" caption="튜플의 요소 개수와 변수 개수가 일치하지 않는 패턴을 잘못 구성한 예">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-05/src/main.rs:here}}
```

</Listing>

이 코드를 컴파일하려고 하면 다음과 같은 타입 에러가 발생한다:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-05/output.txt}}
```

이 에러를 해결하기 위해, 튜플의 값 중 하나 이상을 `_`나 `..`를 사용해 무시할 수 있다. 이 방법은 [“패턴에서 값 무시하기”][ignoring-values-in-a-pattern]<!-- ignore --> 섹션에서 자세히 다룬다. 만약 패턴에 변수가 너무 많아 문제가 된다면, 변수를 제거해 패턴의 변수 개수와 튜플의 요소 개수가 일치하도록 수정하면 된다.


### 함수 파라미터

함수의 파라미터도 패턴으로 사용할 수 있다. `i32` 타입의 `x`라는 하나의 파라미터를 받는 `foo` 함수를 선언한 Listing 19-6의 코드는 이제 익숙할 것이다.

<Listing number="19-6" caption="함수 시그니처에서 파라미터로 패턴 사용">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-06/src/main.rs:here}}
```

</Listing>

여기서 `x` 부분이 바로 패턴이다! `let`과 마찬가지로, 함수의 인자로 튜플을 패턴에 매칭시킬 수 있다. Listing 19-7은 튜플의 값을 함수에 전달하면서 분해하는 예제를 보여준다.

<Listing number="19-7" file-name="src/main.rs" caption="튜플을 분해하는 파라미터를 가진 함수">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-07/src/main.rs}}
```

</Listing>

이 코드는 `Current location: (3, 5)`를 출력한다. `&(3, 5)` 값이 `&(x, y)` 패턴과 매칭되므로, `x`는 `3`이고 `y`는 `5`가 된다.

클로저 파라미터 목록에서도 함수 파라미터 목록과 같은 방식으로 패턴을 사용할 수 있다. 클로저는 함수와 유사하기 때문이다. 이에 대해서는 13장에서 이미 설명했다.

지금까지 패턴을 사용하는 여러 방법을 살펴봤지만, 패턴을 사용할 수 있는 모든 곳에서 동일하게 작동하지는 않는다. 어떤 곳에서는 패턴이 반드시 무조건적이어야 하고, 다른 상황에서는 조건적일 수 있다. 이 두 개념에 대해 다음에 자세히 설명할 것이다.

[ignoring-values-in-a-pattern]: ch19-03-pattern-syntax.html#ignoring-values-in-a-pattern


