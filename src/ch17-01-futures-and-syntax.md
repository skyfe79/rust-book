## 비동기 프로그래밍과 Async 구문

Rust에서 비동기 프로그래밍의 핵심 요소는 _퓨처(future)_와 `async`, `await` 키워드이다.

_퓨처_는 현재는 준비되지 않았지만 미래의 어느 시점에 준비될 값이다. (이 개념은 다른 언어에서도 나타나며, 때로는 _태스크(task)_나 _Promise_와 같은 이름으로 불린다.) Rust는 `Future` 트레이트를 제공하여 다양한 데이터 구조로 비동기 연산을 구현할 수 있도록 한다. Rust에서 퓨처는 `Future` 트레이트를 구현한 타입이다. 각 퓨처는 현재까지의 진행 상황과 "준비됨"이 무엇을 의미하는지에 대한 정보를 담고 있다.

`async` 키워드를 블록이나 함수에 적용하면 해당 블록이나 함수가 중단되고 재개될 수 있음을 지정한다. `async` 블록이나 함수 내에서 `await` 키워드를 사용해 _퓨처를 기다릴_ 수 있다(즉, 퓨처가 준비될 때까지 기다린다). `async` 블록이나 함수 내에서 퓨처를 기다리는 지점은 해당 블록이나 함수가 일시 중단되고 재개될 수 있는 잠재적 지점이다. 퓨처의 값이 준비되었는지 확인하는 과정을 _폴링(polling)_이라고 한다.

C#이나 JavaScript와 같은 다른 언어들도 비동기 프로그래밍을 위해 `async`와 `await` 키워드를 사용한다. 이러한 언어에 익숙하다면 Rust가 이를 처리하는 방식, 특히 구문 처리 방식에서 몇 가지 중요한 차이점을 발견할 수 있다. 이는 합당한 이유가 있으며, 이에 대해 곧 알아볼 것이다.

Rust에서 비동기 코드를 작성할 때는 주로 `async`와 `await` 키워드를 사용한다. Rust는 이 키워드들을 `Future` 트레이트를 사용한 코드로 컴파일한다. 이는 `for` 루프를 `Iterator` 트레이트를 사용한 코드로 컴파일하는 방식과 유사하다. Rust가 `Future` 트레이트를 제공하기 때문에, 필요할 때 자신만의 데이터 타입에 이를 구현할 수도 있다. 이 장에서 살펴볼 많은 함수들은 각자의 `Future` 구현을 가진 타입을 반환한다. 장의 마지막에서 이 트레이트의 정의로 돌아가 더 깊이 파고들어보겠지만, 지금은 이 정도로 충분히 진행할 수 있다.

이 모든 것이 다소 추상적으로 느껴질 수 있으므로, 첫 번째 비동기 프로그램을 작성해보자: 간단한 웹 스크래퍼이다. 커맨드라인에서 두 개의 URL을 입력받아 동시에 두 URL을 가져오고, 먼저 완료된 결과를 반환한다. 이 예제에는 새로운 구문이 꽤 많이 등장하지만, 걱정하지 말자. 진행하면서 필요한 모든 것을 설명할 것이다.


## 첫 번째 비동기 프로그램

이번 장에서는 생태계의 다양한 부분을 다루기보다 비동기 프로그래밍 학습에 집중할 수 있도록 `trpl` 크레이트를 만들었다. (`trpl`은 "The Rust Programming Language"의 약어이다.) 이 크레이트는 주로 [`futures`][futures-crate]<!-- ignore -->와 [`tokio`][tokio]<!-- ignore --> 크레이트에서 필요한 타입, 트레이트, 함수를 다시 내보낸다. `futures` 크레이트는 Rust에서 비동기 코드를 실험하기 위한 공식적인 장소이며, 실제로 `Future` 트레이트가 처음 설계된 곳이다. Tokio는 현재 Rust에서 가장 널리 사용되는 비동기 런타임으로, 특히 웹 애플리케이션에서 많이 사용된다. 다른 훌륭한 런타임도 있지만, `trpl`에서는 `tokio` 크레이트를 사용한다. 이는 잘 테스트되었고 널리 사용되기 때문이다.

경우에 따라 `trpl`은 원래 API의 이름을 바꾸거나 감싸서 이번 장과 관련된 세부 사항에 집중할 수 있도록 했다. 크레이트가 어떤 역할을 하는지 이해하고 싶다면 [소스 코드][crate-source]<!-- ignore -->를 확인해 보길 권한다. 각각의 다시 내보낸 항목이 어떤 크레이트에서 왔는지 확인할 수 있으며, 크레이트의 기능을 설명하는 상세한 주석도 남겨두었다.

`hello-async`라는 이름의 새로운 바이너리 프로젝트를 생성하고 `trpl` 크레이트를 의존성으로 추가한다:

```console
$ cargo new hello-async
$ cd hello-async
$ cargo add trpl
```

이제 `trpl`이 제공하는 다양한 기능을 사용해 첫 번째 비동기 프로그램을 작성할 수 있다. 두 개의 웹 페이지를 가져와 각각의 `<title>` 엘리먼트를 추출한 후, 전체 과정을 먼저 완료한 페이지의 제목을 출력하는 간단한 커맨드라인 도구를 만들어 볼 것이다.


### page_title 함수 정의하기

먼저, 페이지 URL을 인자로 받아 해당 페이지에 요청을 보내고, `<title>` 엘리먼트의 텍스트를 반환하는 함수를 작성해 보자 (Listing 17-1 참조).

<Listing number="17-1" file-name="src/main.rs" caption="HTML 페이지에서 title 엘리먼트를 가져오는 비동기 함수 정의">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-01/src/main.rs:all}}
```

</Listing>

먼저, `page_title`이라는 함수를 정의하고 `async` 키워드를 붙인다. 그런 다음 `trpl::get` 함수를 사용해 전달된 URL을 가져오고, `await` 키워드를 사용해 응답을 기다린다. 응답의 텍스트를 얻기 위해 `text` 메서드를 호출하고, 다시 `await` 키워드를 사용해 기다린다. 이 두 단계 모두 비동기적으로 동작한다. `get` 함수의 경우, 서버가 응답의 첫 부분(HTTP 헤더, 쿠키 등)을 보내는 것을 기다려야 한다. 특히 응답 본문이 매우 큰 경우, 전체가 도착하는 데 시간이 걸릴 수 있다. 응답 전체가 도착할 때까지 기다려야 하므로 `text` 메서드도 비동기적으로 동작한다.

이 두 가지 퓨처(future)를 명시적으로 `await` 해야 하는 이유는, Rust의 퓨처가 _게으르기(lazy)_ 때문이다. 즉, `await` 키워드로 명시적으로 요청하기 전까지는 아무 작업도 수행하지 않는다. (사실, 퓨처를 사용하지 않으면 Rust 컴파일러가 경고를 보낸다.) 이는 [이터레이터를 사용한 일련의 항목 처리][iterators-lazy]<!-- ignore -->에서 설명한 이터레이터의 동작과 유사하다. 이터레이터는 `next` 메서드를 직접 호출하거나 `for` 루프, `map` 같은 메서드를 사용해 내부적으로 `next`를 호출하기 전까지는 아무 작업도 하지 않는다. 마찬가지로, 퓨처도 명시적으로 요청하기 전까지는 아무 작업도 하지 않는다. 이러한 게으름 덕분에 Rust는 비동기 코드가 실제로 필요할 때까지 실행하지 않을 수 있다.

> 참고: 이는 [스레드 생성][thread-spawn]<!--ignore-->에서 `thread::spawn`을 사용할 때의 동작과 다르다. `thread::spawn`에서는 다른 스레드에 전달한 클로저가 즉시 실행된다. 또한, 많은 다른 언어의 비동기 처리 방식과도 다르다. 하지만 Rust가 성능 보장을 제공하기 위해서는 이 방식이 중요하다. 이는 이터레이터와 마찬가지이다.

`response_text`를 얻은 후, `Html::parse`를 사용해 `Html` 타입의 인스턴스로 파싱한다. 이제 원시 문자열 대신 HTML을 더 풍부한 데이터 구조로 다룰 수 있다. 특히, `select_first` 메서드를 사용해 주어진 CSS 선택자에 해당하는 첫 번째 인스턴스를 찾을 수 있다. `"title"` 문자열을 전달하면 문서 내 첫 번째 `<title>` 엘리먼트를 얻을 수 있다. 일치하는 엘리먼트가 없을 수도 있으므로, `select_first`는 `Option<ElementRef>`를 반환한다. 마지막으로, `Option::map` 메서드를 사용해 `Option` 내부의 항목이 있을 때만 작업을 수행하고, 없으면 아무 작업도 하지 않는다. (여기서 `match` 표현식을 사용할 수도 있지만, `map`이 더 관용적이다.) `map`에 전달한 함수 본문에서는 `title_element`의 `inner_html`을 호출해 내용을 가져오며, 이는 `String` 타입이다. 최종적으로 `Option<String>`을 얻게 된다.

Rust의 `await` 키워드는 기다리는 표현식 _뒤에_ 위치한다는 점에 주목하자. 즉, _후위(postfix)_ 키워드이다. 이는 다른 언어에서 `async`를 사용해 본 경험이 있다면 익숙하지 않을 수 있지만, Rust에서는 메서드 체이닝을 더 편리하게 할 수 있다. 결과적으로, `page_title` 함수의 본문을 `trpl::get`와 `text` 함수 호출을 `await` 키워드로 연결하도록 변경할 수 있다 (Listing 17-2 참조).

<Listing number="17-2" file-name="src/main.rs" caption="`await` 키워드를 사용한 체이닝">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-02/src/main.rs:chaining}}
```

</Listing>

이제 첫 번째 비동기 함수를 성공적으로 작성했다! `main` 함수에서 이 함수를 호출하는 코드를 추가하기 전에, 작성한 내용과 그 의미에 대해 조금 더 이야기해 보자.

Rust는 `async` 키워드가 붙은 블록을 보면, `Future` 트레잇을 구현하는 고유한 익명 데이터 타입으로 컴파일한다. `async` 키워드가 붙은 함수를 보면, 그 본문이 비동기 블록인 비동기 함수로 컴파일한다. 비동기 함수의 반환 타입은 컴파일러가 해당 비동기 블록을 위해 생성한 익명 데이터 타입의 타입이다.

따라서 `async fn`을 작성하는 것은 반환 타입의 _퓨처_를 반환하는 함수를 작성하는 것과 동일하다. 컴파일러에게는 Listing 17-1의 `async fn page_title`과 같은 함수 정의가 다음과 같이 정의된 비동기 함수와 동일하다:

```rust
# extern crate trpl; // mdbook 테스트를 위해 필요
use std::future::Future;
use trpl::Html;

fn page_title(url: &str) -> impl Future<Output = Option<String>> {
    async move {
        let text = trpl::get(url).await.text().await;
        Html::parse(&text)
            .select_first("title")
            .map(|title| title.inner_html())
    }
}
```

변환된 버전의 각 부분을 살펴보자:

- [“트레잇을 파라미터로 사용하기”][impl-trait]<!-- ignore -->에서 논의한 `impl Trait` 구문을 사용한다.
- 반환된 트레잇은 `Output`이라는 연관 타입을 가진 `Future`이다. `Output` 타입은 `Option<String>`으로, `async fn` 버전의 `page_title`과 동일한 반환 타입이다.
- 원래 함수 본문에서 호출된 모든 코드는 `async move` 블록으로 감싸져 있다. 블록은 표현식임을 기억하자. 이 전체 블록이 함수에서 반환되는 표현식이다.
- 이 비동기 블록은 `Option<String>` 타입의 값을 생성한다. 이 값은 반환 타입의 `Output` 타입과 일치한다. 이는 다른 블록과 동일하다.
- 새로운 함수 본문은 `url` 파라미터를 사용하는 방식 때문에 `async move` 블록이다. (`async`와 `async move`의 차이에 대해서는 이 장 후반에 더 자세히 논의할 것이다.)

이제 `main` 함수에서 `page_title`을 호출할 수 있다.


## 단일 페이지의 제목 추출하기

먼저 단일 페이지의 제목을 가져오는 방법부터 시작한다. 리스팅 17-3에서는 [커맨드라인 인자 처리하기][cli-args]<!-- ignore --> 섹션에서 다룬 패턴을 그대로 사용한다. 첫 번째 URL을 `page_title`에 전달하고 결과를 기다린다. 이때 반환되는 값은 `Option<String>` 타입이므로, `match` 표현식을 사용해 페이지에 `<title>` 태그가 있는지 여부에 따라 다른 메시지를 출력한다.

<Listing number="17-3" file-name="src/main.rs" caption="사용자가 입력한 인자를 사용해 `main` 함수에서 `page_title` 함수 호출">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-03/src/main.rs:main}}
```

</Listing>

하지만 이 코드는 컴파일되지 않는다. `await` 키워드는 async 함수나 블록 내에서만 사용할 수 있는데, Rust에서는 특수한 `main` 함수를 async로 표시할 수 없기 때문이다.

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-03
cargo build
copy just the compiler error
-->

```text
error[E0752]: `main` function is not allowed to be `async`
 --> src/main.rs:6:1
  |
6 | async fn main() {
  | ^^^^^^^^^^^^^^^ `main` function is not allowed to be `async`
```

`main` 함수를 async로 표시할 수 없는 이유는 async 코드가 실행되려면 _런타임_이 필요하기 때문이다. 런타임은 비동기 코드의 실행을 관리하는 Rust 크레이트이다. 프로그램의 `main` 함수는 런타임을 _초기화_할 수 있지만, 런타임 _자체_는 아니다. (이에 대한 자세한 내용은 잠시 후에 살펴본다.) 비동기 코드를 실행하는 모든 Rust 프로그램은 최소 한 군데에서 런타임을 설정하고 퓨처를 실행한다.

대부분의 언어는 async를 지원하면서 런타임을 함께 제공하지만, Rust는 그렇지 않다. 대신 다양한 async 런타임이 존재하며, 각각은 특정 사용 사례에 적합한 방식으로 설계되었다. 예를 들어, 많은 CPU 코어와 대용량 메모리를 가진 고성능 웹 서버의 요구사항은 단일 코어, 작은 메모리, 그리고 힙 할당 기능이 없는 마이크로컨트롤러와는 완전히 다르다. 이러한 런타임을 제공하는 크레이트는 종종 파일이나 네트워크 I/O와 같은 일반적인 기능의 비동기 버전도 함께 제공한다.

이 장에서는 `trpl` 크레이트의 `run` 함수를 사용한다. 이 함수는 퓨처를 인자로 받아 완료될 때까지 실행한다. 내부적으로 `run`을 호출하면 전달된 퓨처를 실행하기 위한 런타임이 설정된다. 퓨처가 완료되면 `run`은 퓨처가 생성한 값을 반환한다.

`page_title`이 반환한 퓨처를 직접 `run`에 전달하고, 완료된 후 `Option<String>`에 대해 `match`를 수행할 수도 있다. 하지만 이 장의 대부분의 예제(그리고 실제 세계의 대부분의 async 코드)에서는 단일 async 함수 호출 이상의 작업을 수행할 것이므로, 리스팅 17-4와 같이 `async` 블록을 전달하고 `page_title` 호출 결과를 명시적으로 기다리는 방식을 사용한다.

<Listing number="17-4" caption="`trpl::run`을 사용해 async 블록 실행" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook test does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-04/src/main.rs:run}}
```

</Listing>

이 코드를 실행하면 처음 기대한 동작을 확인할 수 있다:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-04
cargo build # skip all the build noise
cargo run https://www.rust-lang.org
```


-->

```console
$ cargo run -- https://www.rust-lang.org
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.05s
     Running `target/debug/async_await 'https://www.rust-lang.org'`
The title for https://www.rust-lang.org was
            Rust Programming Language
```

드디어 동작하는 비동기 코드를 완성했다! 하지만 두 사이트를 경쟁시키는 코드를 추가하기 전에, 잠시 퓨처(Future)가 어떻게 동작하는지 다시 살펴보자.

각 _await 포인트_—즉, 코드에서 `await` 키워드를 사용하는 모든 지점—는 런타임에 제어권을 반환하는 위치를 나타낸다. 이를 동작하게 하려면 Rust는 비동기 블록과 관련된 상태를 추적해야 한다. 그래야 런타임이 다른 작업을 시작하고, 준비가 되면 다시 돌아와 첫 번째 작업을 계속 진행할 수 있다. 이는 마치 여러분이 각 await 포인트에서 현재 상태를 저장하기 위해 다음과 같은 enum을 작성한 것과 같은 보이지 않는 상태 머신이다:

```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-state-machine/src/lib.rs:enum}}
```

각 상태 사이를 전환하는 코드를 직접 작성하는 것은 지루하고 오류가 발생하기 쉽다. 특히 나중에 더 많은 기능과 상태를 추가해야 할 때 더욱 그렇다. 다행히 Rust 컴파일러는 비동기 코드를 위한 상태 머신 데이터 구조를 자동으로 생성하고 관리한다. 데이터 구조 주변의 일반적인 빌림과 소유권 규칙은 여전히 적용되며, 컴파일러는 이를 검사하고 유용한 오류 메시지를 제공한다. 이 장의 후반부에서 몇 가지 예를 살펴볼 것이다.

궁극적으로, 이 상태 머신을 실행해야 하는 무언가가 필요하며, 그 무언가는 런타임이다. (이것이 런타임을 조사할 때 _실행자(executor)_에 대한 참조를 보게 되는 이유다: 실행자는 런타임의 일부로, 비동기 코드를 실행하는 역할을 담당한다.)

이제 Listing 17-3에서 왜 컴파일러가 `main` 함수 자체를 비동기 함수로 만들지 못하게 했는지 이해할 수 있다. 만약 `main`이 비동기 함수라면, `main`이 반환한 퓨처의 상태 머신을 관리할 무언가가 필요하지만, `main`은 프로그램의 시작점이다! 대신, `main`에서 `trpl::run` 함수를 호출하여 런타임을 설정하고, 비동기 블록이 반환한 퓨처가 완료될 때까지 실행했다.

> 참고: 일부 런타임은 async `main` 함수를 작성할 수 있도록 매크로를 제공한다. 이러한 매크로는 `async fn main() { ... }`를 일반 `fn main`으로 재작성하며, 이는 Listing 17-4에서 수동으로 한 것과 동일한 작업을 수행한다: `trpl::run`이 하는 것처럼 퓨처를 완료할 때까지 실행하는 함수를 호출한다.

이제 이 조각들을 모아 동시성 코드를 어떻게 작성할 수 있는지 알아보자.


### 두 URL 간의 경쟁

리스트 17-5에서는 커맨드라인에서 전달된 두 개의 다른 URL을 `page_title` 함수에 전달하고, 이 둘을 경쟁시킨다.

<Listing number="17-5" caption="" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-05/src/main.rs:all}}
```

</Listing>

먼저 사용자가 제공한 각 URL에 대해 `page_title` 함수를 호출한다. 그 결과로 반환된 퓨처를 `title_fut_1`과 `title_fut_2`에 저장한다. 이 퓨처들은 아직 아무 작업도 하지 않는다는 점을 기억하자. 퓨처는 지연 평가되며, 아직 `await`로 기다리지 않았기 때문이다. 이후 이 퓨처들을 `trpl::race` 함수에 전달한다. 이 함수는 전달된 퓨처 중 어떤 것이 먼저 완료되었는지를 나타내는 값을 반환한다.

> 참고: 내부적으로 `race` 함수는 더 일반적인 함수인 `select`를 기반으로 동작한다. 실제 러스트 코드에서는 `select` 함수를 더 자주 접하게 될 것이다. `select` 함수는 `trpl::race` 함수가 할 수 없는 많은 작업을 수행할 수 있지만, 지금은 넘어갈 수 있는 추가적인 복잡성도 있다.

어느 퓨처가 먼저 완료될지 예측할 수 없기 때문에 `Result`를 반환하는 것은 적절하지 않다. 대신 `race` 함수는 이전에 본 적 없는 `trpl::Either` 타입을 반환한다. `Either` 타입은 `Result`와 유사하게 두 가지 경우를 가진다. 하지만 `Result`와 달리 `Either`에는 성공이나 실패라는 개념이 없다. 대신 `Left`와 `Right`를 사용해 "둘 중 하나"를 나타낸다:

```rust
enum Either<A, B> {
    Left(A),
    Right(B),
}
```

`race` 함수는 첫 번째 퓨처 인자가 먼저 완료되면 `Left`와 함께 그 결과를 반환하고, 두 번째 퓨처 인자가 먼저 완료되면 `Right`와 함께 그 결과를 반환한다. 이는 함수를 호출할 때 인자가 나타나는 순서와 일치한다: 첫 번째 인자는 두 번째 인자의 왼쪽에 위치한다.

또한 `page_title` 함수를 수정해 전달된 URL을 그대로 반환하도록 했다. 이렇게 하면 먼저 반환된 페이지에 `<title>`이 없더라도 의미 있는 메시지를 출력할 수 있다. 이 정보를 활용해 `println!` 출력을 업데이트하여 어떤 URL이 먼저 완료되었는지와 해당 URL의 웹 페이지 `<title>`이 무엇인지(있는 경우)를 표시한다.

이제 간단한 웹 스크래퍼를 만들었다! 몇 개의 URL을 선택하고 커맨드라인 도구를 실행해 보자. 어떤 사이트는 항상 더 빠르게 응답하는 반면, 다른 경우에는 실행마다 더 빠른 사이트가 달라질 수 있다. 더 중요한 것은, 여러분이 퓨처를 다루는 기본을 배웠다는 점이다. 이제 비동기 작업을 통해 무엇을 할 수 있는지 더 깊이 파고들 준비가 되었다.

[impl-trait]: ch10-02-traits.html#traits-as-parameters
[iterators-lazy]: ch13-02-iterators.html
[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[cli-args]: ch12-01-accepting-command-line-arguments.html

<!-- TODO: map source link version to version of Rust? -->

[crate-source]: https://github.com/rust-lang/book/tree/main/packages/trpl
[futures-crate]: https://crates.io/crates/futures
[tokio]: https://tokio.rs


