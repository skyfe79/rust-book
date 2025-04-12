## 단일 스레드 서버를 멀티스레드 서버로 전환하기

현재 서버는 요청을 순차적으로 처리한다. 즉, 첫 번째 요청이 완전히 처리될 때까지 두 번째 연결을 처리하지 않는다. 서버가 점점 더 많은 요청을 받게 되면, 이와 같은 직렬 처리 방식은 점점 더 비효율적이 된다. 서버가 처리하는 데 오랜 시간이 걸리는 요청을 받게 되면, 그 요청이 끝날 때까지 새로운 요청들은 기다려야 한다. 새로운 요청이 빠르게 처리될 수 있는 경우에도 말이다. 이 문제를 해결해야 하지만, 우선 이 문제가 어떻게 발생하는지 살펴보자.


### 현재 서버 구현에서 느린 요청 시뮬레이션

현재 서버 구현에서 느리게 처리되는 요청이 다른 요청에 어떤 영향을 미치는지 살펴본다. 리스트 21-10은 _/sleep_ 요청을 처리하는 코드를 보여준다. 이 코드는 서버가 응답하기 전에 5초간 대기하도록 해서 느린 응답을 시뮬레이션한다.

<Listing number="21-10" file-name="src/main.rs" caption="5초간 대기하여 느린 요청 시뮬레이션">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-10/src/main.rs:here}}
```

</Listing>

이제 세 가지 경우를 처리하기 위해 `if` 대신 `match`를 사용한다. `match`는 자동으로 참조 및 역참조를 수행하지 않기 때문에, 문자열 리터럴 값과 비교하기 위해 `request_line`의 슬라이스를 명시적으로 매칭해야 한다. 이는 `==` 연산자와는 다르게 동작한다.

첫 번째 매칭은 리스트 21-9의 `if` 블록과 동일하다. 두 번째 매칭은 _/sleep_ 요청을 처리한다. 이 요청을 받으면, 서버는 5초간 대기한 후 성공 HTML 페이지를 렌더링한다. 세 번째 매칭은 리스트 21-9의 `else` 블록과 동일하다.

우리 서버가 얼마나 기본적인지 확인할 수 있다. 실제 라이브러리는 여러 요청을 훨씬 간결하게 처리할 것이다!

`cargo run`으로 서버를 시작한다. 그런 다음 두 개의 브라우저 창을 연다. 하나는 _http://127.0.0.1:7878/_, 다른 하나는 _http://127.0.0.1:7878/sleep_로 접속한다. _/_ URI를 여러 번 입력하면 이전처럼 빠르게 응답하는 것을 볼 수 있다. 하지만 _/sleep_을 입력한 후 _/_를 로드하면, _/_는 `sleep`이 5초 동안 대기한 후에야 로드된다.

느린 요청 뒤에 다른 요청이 밀리는 현상을 방지하기 위해 여러 기술을 사용할 수 있다. 17장에서 다룬 async를 사용하는 방법도 있고, 이번에는 스레드 풀을 구현해 볼 것이다.


### 스레드 풀을 통한 처리량 향상

_스레드 풀_은 태스크를 처리하기 위해 대기 중인 스레드 그룹이다. 프로그램이 새로운 태스크를 받으면, 풀에 있는 스레드 중 하나를 해당 태스크에 할당한다. 이 스레드는 태스크를 처리하며, 나머지 스레드는 첫 번째 스레드가 작업을 처리하는 동안 들어오는 다른 태스크를 처리할 수 있다. 첫 번째 스레드가 태스크를 완료하면, 다시 풀에 돌아가 새로운 태스크를 처리할 준비를 한다. 스레드 풀을 사용하면 연결을 동시에 처리할 수 있어 서버의 처리량을 높일 수 있다.

우리는 DoS 공격을 방지하기 위해 풀에 있는 스레드 수를 적은 수로 제한할 것이다. 만약 프로그램이 들어오는 요청마다 새로운 스레드를 생성한다면, 누군가가 서버에 1천만 개의 요청을 보내면 서버의 리소스를 모두 사용해 요청 처리를 중단시킬 수 있다.

따라서 무제한으로 스레드를 생성하는 대신, 풀에 고정된 수의 스레드를 대기시킨다. 들어오는 요청은 풀로 전달되어 처리된다. 풀은 들어오는 요청의 큐를 유지한다. 풀에 있는 각 스레드는 이 큐에서 요청을 꺼내 처리한 후, 큐에서 다음 요청을 요청한다. 이 설계를 통해 *`N`*개의 요청을 동시에 처리할 수 있다. 여기서 *`N`*은 스레드의 수이다. 각 스레드가 오래 실행되는 요청에 응답하고 있다면, 후속 요청은 큐에 백업될 수 있지만, 그 지점에 도달하기 전에 처리할 수 있는 오래 실행되는 요청의 수를 늘릴 수 있다.

이 기법은 웹 서버의 처리량을 향상시키는 여러 방법 중 하나일 뿐이다. 다른 옵션으로는 fork/join 모델, 단일 스레드 비동기 I/O 모델, 다중 스레드 비동기 I/O 모델 등을 탐구할 수 있다. 이 주제에 관심이 있다면, 다른 솔루션에 대해 더 읽어보고 구현해 볼 수 있다. Rust와 같은 저수준 언어를 사용하면 이러한 모든 옵션을 구현할 수 있다.

스레드 풀을 구현하기 전에, 풀을 사용하는 것이 어떻게 보여야 하는지 이야기해 보자. 코드를 설계할 때 클라이언트 인터페이스를 먼저 작성하면 설계를 안내하는 데 도움이 될 수 있다. 코드의 API를 원하는 방식으로 호출할 수 있도록 구조화한 후, 그 구조 내에서 기능을 구현하는 것이 좋다. 기능을 먼저 구현하고 공개 API를 설계하는 것보다 더 나은 접근 방식이다.

12장 프로젝트에서 테스트 주도 개발을 사용한 것과 유사하게, 여기서는 컴파일러 주도 개발을 사용할 것이다. 우리가 원하는 함수를 호출하는 코드를 작성한 후, 컴파일러의 오류를 보고 코드가 작동하도록 다음에 무엇을 변경해야 하는지 결정할 것이다. 그러나 그 전에, 시작점으로 사용하지 않을 기법에 대해 먼저 알아보자.

<!-- Old headings. Do not remove or links may break. -->

<a id="code-structure-if-we-could-spawn-a-thread-for-each-request"></a>


#### 각 요청마다 스레드 생성하기

먼저, 모든 연결에 대해 새로운 스레드를 생성하는 코드가 어떻게 동작하는지 살펴보자. 앞서 언급했듯이, 이 방식은 무제한으로 스레드를 생성할 가능성이 있어 최종적인 해결책은 아니다. 하지만 동작하는 멀티스레드 서버를 만들기 위한 시작점으로 적합하다. 이후에 스레드 풀을 추가해 개선할 것이며, 두 해결책을 비교하는 것도 더 쉬워질 것이다. 아래 코드는 `for` 루프 내에서 각 스트림을 처리하기 위해 새로운 스레드를 생성하도록 `main` 함수를 수정한 예제이다.

<Listing number="21-11" file-name="src/main.rs" caption="각 스트림에 대해 새로운 스레드 생성">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-11/src/main.rs:here}}
```

</Listing>

16장에서 배웠듯이, `thread::spawn`은 새로운 스레드를 생성하고, 그 스레드에서 클로저 내부의 코드를 실행한다. 이 코드를 실행한 후 브라우저에서 _/sleep_을 로드하고, 두 개의 추가 탭에서 _/_를 로드하면, _/_에 대한 요청이 _/sleep_이 끝날 때까지 기다리지 않는다는 것을 확인할 수 있다. 하지만 앞서 언급했듯이, 이 방식은 스레드를 무제한으로 생성하기 때문에 결국 시스템에 부하를 줄 것이다.

17장에서 배운 내용을 떠올려보면, 이 상황은 바로 async와 await가 빛을 발휘하는 곳이다! 스레드 풀을 구축하면서 이 점을 염두에 두고, async를 사용했을 때 어떤 점이 달라지거나 동일할지 생각해보자.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-a-similar-interface-for-a-finite-number-of-threads"></a>


#### 제한된 수의 스레드 생성하기

우리는 스레드 풀이 익숙한 방식으로 동작하도록 만들어, 스레드에서 스레드 풀로 전환할 때 API를 사용하는 코드에 큰 변경이 필요 없도록 하고 싶다. 리스트 21-12는 `thread::spawn` 대신 사용할 `ThreadPool` 구조체의 가상 인터페이스를 보여준다.

<Listing number="21-12" file-name="src/main.rs" caption="우리가 원하는 `ThreadPool` 인터페이스">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-12/src/main.rs:here}}
```

</Listing>

`ThreadPool::new`를 사용해 구성 가능한 수의 스레드를 가진 새로운 스레드 풀을 생성한다. 이 예제에서는 4개의 스레드를 사용한다. 그런 다음 `for` 루프에서 `pool.execute`는 `thread::spawn`과 유사한 인터페이스를 가지며, 풀이 각 스트림에 대해 실행할 클로저를 받는다. `pool.execute`를 구현해야 하는데, 이는 클로저를 받아 풀 내의 스레드에게 실행하도록 전달하는 역할을 한다. 이 코드는 아직 컴파일되지 않지만, 컴파일러가 문제를 해결하는 방법을 안내할 수 있도록 시도해 볼 것이다.

<!-- Old headings. Do not remove or links may break. -->

<a id="building-the-threadpool-struct-using-compiler-driven-development"></a>


#### 컴파일러 주도 개발로 `ThreadPool` 구현하기

`src/main.rs` 파일에 목록 21-12의 변경 사항을 적용한 후, `cargo check`의 컴파일러 오류를 활용해 개발을 진행한다. 첫 번째로 발생한 오류는 다음과 같다:

```console
{{#include ../listings/ch21-web-server/listing-21-12/output.txt}}
```

이 오류는 `ThreadPool` 타입이나 모듈이 필요하다는 것을 알려준다. 따라서 이제 `ThreadPool`을 구현할 것이다. 이 `ThreadPool` 구현은 웹 서버의 작업 종류와는 독립적이다. 따라서 `hello` 크레이트를 바이너리 크레이트에서 라이브러리 크레이트로 전환해 `ThreadPool` 구현을 포함시킨다. 라이브러리 크레이트로 변경한 후에는 웹 요청 처리뿐만 아니라 스레드 풀을 사용해 수행할 다른 작업에도 별도의 스레드 풀 라이브러리를 사용할 수 있다.

`src/lib.rs` 파일을 생성하고 다음 코드를 추가한다. 이 코드는 현재로서는 가장 간단한 `ThreadPool` 구조체 정의이다:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/lib.rs}}
```

</Listing>

그런 다음 `src/main.rs` 파일을 편집해 라이브러리 크레이트에서 `ThreadPool`을 스코프로 가져온다. 이를 위해 `src/main.rs` 파일 상단에 다음 코드를 추가한다:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/main.rs:here}}
```

</Listing>

이 코드는 아직 동작하지 않지만, 다음 오류를 확인하기 위해 다시 검사한다:

```console
{{#include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/output.txt}}
```

이 오류는 `ThreadPool`에 `new`라는 연관 함수가 필요하다는 것을 알려준다. 또한 `new` 함수는 `4`를 인자로 받을 수 있는 하나의 매개변수를 가져야 하며, `ThreadPool` 인스턴스를 반환해야 한다. 이러한 특성을 가진 가장 간단한 `new` 함수를 구현한다:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/src/lib.rs}}
```

</Listing>

`size` 매개변수의 타입으로 `usize`를 선택한 이유는 음수의 스레드 수는 의미가 없기 때문이다. 또한 이 `4`를 스레드 컬렉션의 요소 수로 사용할 것이며, 이는 `usize` 타입이 적합하다. 이에 대한 자세한 내용은 3장의 ["정수 타입"][integer-types]에서 다룬다.

다시 코드를 검사한다:

```console
{{#include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/output.txt}}
```

이제 오류는 `ThreadPool`에 `execute` 메서드가 없기 때문에 발생한다. ["유한한 수의 스레드 생성"](#creating-a-finite-number-of-threads)에서 스레드 풀의 인터페이스가 `thread::spawn`과 유사해야 한다고 결정한 것을 기억할 것이다. 추가적으로 `execute` 함수를 구현해 주어진 클로저를 풀의 유휴 스레드에 전달해 실행하도록 할 것이다.

`ThreadPool`에 `execute` 메서드를 정의해 클로저를 매개변수로 받도록 한다. 13장의 ["클로저에서 캡처된 값을 이동시키기와 `Fn` 트레이트"][fn-traits]에서 클로저를 매개변수로 받는 세 가지 트레이트(`Fn`, `FnMut`, `FnOnce`)를 사용할 수 있다는 것을 기억할 것이다. 여기서 어떤 종류의 클로저를 사용할지 결정해야 한다. 표준 라이브러리의 `thread::spawn` 구현과 유사한 작업을 수행할 것이므로, `thread::spawn`의 매개변수에 어떤 제약이 있는지 확인할 수 있다. 문서는 다음과 같이 보여준다:

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

여기서 관심 있는 타입 매개변수는 `F`이다. `T` 타입 매개변수는 반환 값과 관련이 있으며, 여기서는 다루지 않는다. `spawn`이 `F`에 `FnOnce` 트레이트를 사용하는 것을 볼 수 있다. 이는 `execute`에서 받은 인자를 `spawn`에 전달할 것이므로, 아마도 우리가 원하는 것과 일치한다. 또한 요청을 실행할 스레드는 해당 요청의 클로저를 한 번만 실행할 것이므로, `FnOnce`의 `Once`와 일치한다는 점에서 더 확신할 수 있다.

`F` 타입 매개변수는 `Send` 트레이트와 `'static` 라이프타임 제약을 가진다. 이는 우리의 상황에서 유용하다: 클로저를 한 스레드에서 다른 스레드로 전달하기 위해 `Send`가 필요하며, 스레드가 실행될 때까지 얼마나 걸릴지 모르기 때문에 `'static`이 필요하다. 이제 `ThreadPool`에 `execute` 메서드를 생성해 이러한 제약을 가진 `F` 타입의 제네릭 매개변수를 받도록 한다:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-03-define-execute/src/lib.rs:here}}
```

</Listing>

`FnOnce` 뒤에 `()`를 사용하는 이유는 이 `FnOnce`가 매개변수를 받지 않고 유닛 타입 `()`을 반환하는 클로저를 나타내기 때문이다. 함수 정의와 마찬가지로 반환 타입은 시그니처에서 생략할 수 있지만, 매개변수가 없더라도 여전히 괄호가 필요하다.

다시 한 번, 이 `execute` 메서드의 가장 간단한 구현이다: 아무것도 하지 않지만, 코드가 컴파일되도록 하는 데 목적이 있다. 다시 검사한다:

```console
{{#include ../listings/ch21-web-server/no-listing-03-define-execute/output.txt}}
```

컴파일이 성공한다! 하지만 `cargo run`을 실행하고 브라우저에서 요청을 보내면, 장 초반에 본 오류가 브라우저에 표시된다. 우리의 라이브러리는 아직 `execute`에 전달된 클로저를 호출하지 않는다!

> 참고: Haskell이나 Rust와 같이 엄격한 컴파일러를 가진 언어에 대해 "코드가 컴파일되면 동작한다"는 말을 들을 수 있다. 하지만 이 말은 항상 사실이 아니다. 우리의 프로젝트는 컴파일되지만, 아무것도 하지 않는다! 실제 완전한 프로젝트를 구축한다면, 이 시점에서 단위 테스트를 작성해 코드가 컴파일되고 원하는 동작을 하는지 확인하는 것이 좋다.

고려해볼 점: 클로저 대신 _future_를 실행한다면 여기서 무엇이 달라질까?


#### `new` 함수에서 스레드 수 검증하기

현재 `new`와 `execute` 함수의 인자를 활용하지 않고 있다. 이제 이 함수들의 동작을 구현해 보자. 먼저 `new` 함수부터 생각해 보자. 이전에 `size` 매개변수의 타입으로 부호 없는 정수(unsigned type)를 선택했는데, 음수 개수의 스레드를 가진 스레드 풀은 말이 되지 않기 때문이다. 하지만 스레드가 0개인 풀도 말이 되지 않는데, 0은 `usize` 타입에서 유효한 값이다. 따라서 `size`가 0보다 큰지 확인하는 코드를 추가하고, 0이 들어오면 프로그램이 패닉 상태에 빠지도록 `assert!` 매크로를 사용할 것이다. 이는 리스트 21-13에 나와 있다.

<Listing number="21-13" file-name="src/lib.rs" caption="`size`가 0일 경우 패닉을 발생시키는 `ThreadPool::new` 구현">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-13/src/lib.rs:here}}
```

</Listing>

또한 `ThreadPool`에 대한 문서 주석도 추가했다. 14장에서 논의한 것처럼, 함수가 패닉을 일으킬 수 있는 상황을 명시하는 섹션을 추가해 좋은 문서 작성 관례를 따랐다. `cargo doc --open`을 실행하고 `ThreadPool` 구조체를 클릭해 `new` 함수에 대해 생성된 문서가 어떻게 보이는지 확인해 보자.

여기서 `assert!` 매크로를 추가하는 대신, `new`를 `build`로 변경하고 I/O 프로젝트의 리스트 12-9에서 `Config::build`와 같이 `Result`를 반환하도록 할 수도 있다. 하지만 이 경우 스레드가 없는 스레드 풀을 생성하려는 시도는 복구할 수 없는 오류로 간주하기로 결정했다. 만약 도전하고 싶다면, 다음 시그니처를 가진 `build` 함수를 작성해 `new` 함수와 비교해 보자:

```rust,ignore
pub fn build(size: usize) -> Result<ThreadPool, PoolCreationError> {
```


#### 스레드를 저장할 공간 만들기

이제 스레드 풀에 저장할 유효한 스레드 수를 확인할 수 있으므로, 해당 스레드를 생성하고 `ThreadPool` 구조체에 저장한 후 구조체를 반환할 수 있다. 그런데 스레드를 어떻게 "저장"할까? `thread::spawn` 시그니처를 다시 살펴보자:

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

`spawn` 함수는 `JoinHandle<T>`를 반환한다. 여기서 `T`는 클로저가 반환하는 타입이다. 우리도 `JoinHandle`을 사용해 보자. 이 경우에는 스레드 풀에 전달한 클로저가 연결을 처리하고 아무것도 반환하지 않으므로, `T`는 유닛 타입 `()`이 된다.

리스트 21-14의 코드는 컴파일되지만 아직 스레드를 생성하지는 않는다. `ThreadPool`의 정의를 변경해 `thread::JoinHandle<()>` 인스턴스의 벡터를 보유하도록 했다. 벡터를 `size` 크기로 초기화하고, 스레드를 생성하기 위해 일부 코드를 실행할 `for` 루프를 설정한 후, 이를 포함한 `ThreadPool` 인스턴스를 반환한다.

<Listing number="21-14" file-name="src/lib.rs" caption="`ThreadPool`이 스레드를 보유할 벡터 생성">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-14/src/lib.rs:here}}
```

</Listing>

`std::thread`를 라이브러리 크레이트의 스코프로 가져왔다. `ThreadPool`의 벡터 항목 타입으로 `thread::JoinHandle`을 사용하기 때문이다.

유효한 크기를 받으면, `ThreadPool`은 `size` 항목을 보유할 수 있는 새 벡터를 생성한다. `with_capacity` 함수는 `Vec::new`와 동일한 작업을 수행하지만 중요한 차이가 있다. 벡터에 공간을 미리 할당한다. 벡터에 `size` 요소를 저장해야 한다는 것을 알고 있기 때문에, 이렇게 미리 할당하는 것이 `Vec::new`를 사용하는 것보다 약간 더 효율적이다. `Vec::new`는 요소가 삽입될 때마다 크기를 조정한다.

`cargo check`를 다시 실행하면 성공할 것이다.


#### `ThreadPool`에서 스레드로 코드를 전달하는 `Worker` 구조체

이전에 21-14 목록의 `for` 루프에서 스레드를 생성하는 부분에 대해 주석을 남겼다. 이제 실제로 스레드를 어떻게 생성하는지 알아보자. 표준 라이브러리는 `thread::spawn`을 통해 스레드를 생성하는 방법을 제공하며, `thread::spawn`은 스레드가 생성되자마자 실행할 코드를 받기를 기대한다. 하지만 우리의 경우, 스레드를 생성하고 나중에 보낼 코드를 _기다리도록_ 하고 싶다. 표준 라이브러리의 스레드 구현에는 이를 위한 방법이 포함되어 있지 않으므로, 직접 구현해야 한다.

이 동작을 구현하기 위해 `ThreadPool`과 스레드 사이에 새로운 데이터 구조를 도입한다. 이 데이터 구조를 _Worker_라고 부르며, 풀링 구현에서 흔히 사용되는 용어다. `Worker`는 실행해야 할 코드를 받아서 해당 Worker의 스레드에서 코드를 실행한다.

레스토랑 주방에서 일하는 사람들을 생각해보자. 직원들은 고객으로부터 주문이 들어올 때까지 기다렸다가, 그 주문을 받아서 처리하는 역할을 한다.

`ThreadPool`에서 `JoinHandle<()>` 인스턴스의 벡터를 저장하는 대신, `Worker` 구조체의 인스턴스를 저장한다. 각 `Worker`는 단일 `JoinHandle<()>` 인스턴스를 저장한다. 그리고 `Worker`에 실행할 코드 클로저를 받아서 이미 실행 중인 스레드로 보내는 메서드를 구현한다. 또한 각 `Worker`에 `id`를 부여해 로깅이나 디버깅 시 풀 안의 다른 `Worker` 인스턴스와 구별할 수 있도록 한다.

`ThreadPool`을 생성할 때 발생하는 새로운 프로세스는 다음과 같다. `Worker`를 이렇게 설정한 후 클로저를 스레드로 보내는 코드를 구현할 것이다:

1. `id`와 `JoinHandle<()>`을 포함하는 `Worker` 구조체를 정의한다.
2. `ThreadPool`이 `Worker` 인스턴스의 벡터를 보유하도록 변경한다.
3. `id` 번호를 받아서 `id`와 빈 클로저로 생성된 스레드를 포함하는 `Worker` 인스턴스를 반환하는 `Worker::new` 함수를 정의한다.
4. `ThreadPool::new`에서 `for` 루프의 카운터를 사용해 `id`를 생성하고, 해당 `id`로 새로운 `Worker`를 생성한 후 벡터에 저장한다.

도전해보고 싶다면, 21-15 목록의 코드를 보기 전에 이 변경사항을 직접 구현해보자.

준비가 되었다면, 앞서 설명한 수정사항을 반영한 21-15 목록을 확인해보자.

<Listing number="21-15" file-name="src/lib.rs" caption="`ThreadPool`이 스레드를 직접 보유하는 대신 `Worker` 인스턴스를 보유하도록 수정">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-15/src/lib.rs:here}}
```

</Listing>

`ThreadPool`의 필드 이름을 `threads`에서 `workers`로 변경했다. 이제 `JoinHandle<()>` 인스턴스 대신 `Worker` 인스턴스를 보유하기 때문이다. `for` 루프의 카운터를 `Worker::new`의 인자로 사용하고, 각 새로운 `Worker`를 `workers`라는 벡터에 저장한다.

외부 코드(예: _src/main.rs_의 서버)는 `ThreadPool` 내에서 `Worker` 구조체를 사용하는 구현 세부사항을 알 필요가 없으므로, `Worker` 구조체와 그 `new` 함수를 비공개로 만든다. `Worker::new` 함수는 우리가 제공한 `id`를 사용하고, 빈 클로저를 사용해 생성된 새로운 스레드의 `JoinHandle<()>` 인스턴스를 저장한다.

> 참고: 운영체제가 시스템 리소스가 부족해 스레드를 생성할 수 없는 경우, `thread::spawn`이 패닉을 일으킬 수 있다. 이로 인해 일부 스레드 생성은 성공했더라도 전체 서버가 패닉 상태에 빠질 수 있다. 간단함을 위해 이 동작은 괜찮지만, 실제 프로덕션 스레드 풀 구현에서는 [`std::thread::Builder`][builder]<!-- ignore -->와 그 [`spawn`][builder-spawn]<!-- ignore --> 메서드를 사용해 `Result`를 반환하도록 하는 것이 좋다.

이 코드는 컴파일되며, `ThreadPool::new`에 인자로 지정한 수만큼의 `Worker` 인스턴스를 저장한다. 하지만 여전히 `execute`에서 받은 클로저를 처리하지는 않는다. 다음으로 이를 어떻게 처리하는지 알아보자.


#### 채널을 통해 스레드에 요청 보내기

다음으로 해결해야 할 문제는 `thread::spawn`에 전달된 클로저가 아무런 동작을 하지 않는다는 점이다. 현재 `execute` 메서드에서 실행할 클로저를 가져오지만, `ThreadPool` 생성 시 각 `Worker`를 만들 때 `thread::spawn`에 실행할 클로저를 전달해야 한다.

방금 생성한 `Worker` 구조체가 `ThreadPool`에 있는 큐에서 실행할 코드를 가져와 해당 스레드로 전달하도록 하고 싶다.

16장에서 배운 채널은 두 스레드 간 통신을 위한 간단한 방법으로, 이 사용 사례에 완벽하게 적합하다. 채널을 작업 큐로 사용하고, `execute`는 `ThreadPool`에서 `Worker` 인스턴스로 작업을 보낸다. 그러면 `Worker`는 해당 작업을 스레드로 전달한다. 계획은 다음과 같다:

1. `ThreadPool`은 채널을 생성하고 송신자를 보유한다.
2. 각 `Worker`는 수신자를 보유한다.
3. 채널을 통해 보낼 클로저를 담을 새로운 `Job` 구조체를 생성한다.
4. `execute` 메서드는 실행할 작업을 송신자를 통해 보낸다.
5. `Worker`는 스레드 내에서 수신자를 반복적으로 확인하고 받은 작업의 클로저를 실행한다.

먼저 `ThreadPool::new`에서 채널을 생성하고 `ThreadPool` 인스턴스에 송신자를 보관한다. 현재 `Job` 구조체는 아무것도 포함하지 않지만, 채널을 통해 보낼 항목의 타입이 될 것이다.

<Listing number="21-16" file-name="src/lib.rs" caption="`Job` 인스턴스를 전송하는 채널의 송신자를 저장하도록 `ThreadPool` 수정">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-16/src/lib.rs:here}}
```

</Listing>

`ThreadPool::new`에서 새로운 채널을 생성하고 풀이 송신자를 보유하도록 한다. 이 코드는 성공적으로 컴파일된다.

이제 스레드 풀이 채널을 생성할 때 각 `Worker`에 채널의 수신자를 전달해 보자. `Worker` 인스턴스가 생성하는 스레드에서 수신자를 사용하고 싶으므로, 클로저 내에서 `receiver` 매개변수를 참조한다. Listing 21-17의 코드는 아직 컴파일되지 않는다.

<Listing number="21-17" file-name="src/lib.rs" caption="각 `Worker`에 수신자 전달">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-17/src/lib.rs:here}}
```

</Listing>

몇 가지 간단한 변경을 했다: 수신자를 `Worker::new`에 전달하고, 클로저 내부에서 사용한다.

이 코드를 확인하려고 하면 다음과 같은 오류가 발생한다:

```console
{{#include ../listings/ch21-web-server/listing-21-17/output.txt}}
```

코드는 `receiver`를 여러 `Worker` 인스턴스에 전달하려고 한다. 16장에서 배웠듯이, 이는 작동하지 않는다. Rust가 제공하는 채널 구현은 다중 _생산자_, 단일 _소비자_ 방식이다. 즉, 채널의 소비 측을 복제해서 이 코드를 고칠 수 없다. 또한 여러 소비자에게 메시지를 여러 번 보내고 싶지 않다. 여러 `Worker` 인스턴스가 하나의 메시지 목록을 공유하고 각 메시지가 한 번만 처리되도록 하고 싶다.

또한, 채널 큐에서 작업을 가져오는 것은 `receiver`를 변경하는 작업이므로, 스레드가 `receiver`를 안전하게 공유하고 수정할 방법이 필요하다. 그렇지 않으면 경쟁 조건이 발생할 수 있다(16장에서 다룬 내용).

16장에서 논의한 스레드 안전한 스마트 포인터를 떠올려 보자: 여러 스레드 간에 소유권을 공유하고 스레드가 값을 변경할 수 있도록 하려면 `Arc<Mutex<T>>`를 사용해야 한다. `Arc` 타입은 여러 `Worker` 인스턴스가 수신자를 소유할 수 있게 하고, `Mutex`는 한 번에 하나의 `Worker`만 수신자에서 작업을 가져올 수 있도록 보장한다. Listing 21-18은 필요한 변경 사항을 보여준다.

<Listing number="21-18" file-name="src/lib.rs" caption="`Arc`와 `Mutex`를 사용해 `Worker` 인스턴스 간에 수신자 공유">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-18/src/lib.rs:here}}
```

</Listing>

`ThreadPool::new`에서 수신자를 `Arc`와 `Mutex`에 넣는다. 새로운 `Worker`를 생성할 때마다 `Arc`를 복제해 참조 카운트를 증가시키고, `Worker` 인스턴스가 수신자의 소유권을 공유할 수 있도록 한다.

이러한 변경을 통해 코드가 컴파일된다! 거의 다 왔다!


#### `execute` 메서드 구현

이제 `ThreadPool`에 `execute` 메서드를 구현해 보자. 또한 `Job`을 구조체에서 `execute`가 받는 클로저 타입을 담는 트레이트 객체의 타입 별칭으로 변경한다. 20장의 ["타입 별칭으로 타입 동의어 만들기"][creating-type-synonyms-with-type-aliases]에서 논의한 대로, 타입 별칭을 사용하면 긴 타입을 짧게 만들어 사용하기 편리하다. 목록 21-19를 살펴보자.

<Listing number="21-19" file-name="src/lib.rs" caption="각 클로저를 담는 `Box`에 대한 `Job` 타입 별칭을 생성하고, 채널을 통해 작업을 전송">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-19/src/lib.rs:here}}
```

</Listing>

`execute`에서 받은 클로저를 사용해 새로운 `Job` 인스턴스를 생성한 후, 해당 작업을 채널의 송신 측으로 보낸다. `send`에 대해 `unwrap`을 호출하는데, 이는 전송이 실패할 경우를 대비한 것이다. 예를 들어, 모든 스레드의 실행을 중지하면 수신 측이 새로운 메시지를 받는 것을 중지할 수 있다. 현재로서는 스레드 실행을 중지할 수 없는데, 풀이 존재하는 한 스레드는 계속 실행된다. `unwrap`을 사용하는 이유는 실패 사례가 발생하지 않을 것임을 알지만, 컴파일러는 이를 알지 못하기 때문이다.

하지만 아직 완전히 끝난 것은 아니다! `Worker`에서 `thread::spawn`에 전달된 클로저는 여전히 채널의 수신 측만 참조하고 있다. 대신, 클로저가 영원히 반복하면서 채널의 수신 측에서 작업을 요청하고, 작업을 받으면 실행하도록 해야 한다. 목록 21-20에서 보이는 변경을 `Worker::new`에 적용해 보자.

<Listing number="21-20" file-name="src/lib.rs" caption="`Worker` 인스턴스의 스레드에서 작업을 수신하고 실행">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-20/src/lib.rs:here}}
```

</Listing>

여기서는 먼저 `receiver`에 대해 `lock`을 호출해 뮤텍스를 획득하고, 그런 다음 `unwrap`을 호출해 오류가 발생하면 패닉을 일으킨다. 뮤텍스가 _poisoned_ 상태일 경우 락 획득이 실패할 수 있는데, 이는 다른 스레드가 락을 해제하지 않고 패닉을 일으킨 경우에 발생할 수 있다. 이 상황에서 `unwrap`을 호출해 이 스레드가 패닉을 일으키는 것은 올바른 조치이다. 이 `unwrap`을 의미 있는 오류 메시지와 함께 `expect`로 변경해도 좋다.

뮤텍스에 대한 락을 획득하면 `recv`를 호출해 채널에서 `Job`을 받는다. 여기서도 마지막 `unwrap`은 오류를 넘어가는데, 이는 송신 측을 담당하는 스레드가 종료된 경우 발생할 수 있으며, 이는 `send` 메서드가 수신 측이 종료된 경우 `Err`를 반환하는 것과 유사하다.

`recv` 호출은 블로킹되므로, 아직 작업이 없으면 현재 스레드는 작업이 사용 가능해질 때까지 대기한다. `Mutex<T>`는 한 번에 하나의 `Worker` 스레드만 작업을 요청하도록 보장한다.

이제 스레드 풀이 작동 상태이다! `cargo run`을 실행하고 몇 가지 요청을 보내 보자.

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-20
cargo run
make some requests to 127.0.0.1:7878
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
warning: field `workers` is never read
 --> src/lib.rs:7:5
  |
6 | pub struct ThreadPool {
  |            ---------- field in this struct
7 |     workers: Vec<Worker>,
  |     ^^^^^^^
  |
  = note: `#[warn(dead_code)]` on by default

warning: fields `id` and `thread` are never read
  --> src/lib.rs:48:5
   |
47 | struct Worker {
   |        ------ fields in this struct
48 |     id: usize,
   |     ^^
49 |     thread: thread::JoinHandle<()>,
   |     ^^^^^^

warning: `hello` (lib) generated 2 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 4.91s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
```

성공! 이제 비동기적으로 연결을 실행하는 스레드 풀이 준비되었다. 생성되는 스레드는 네 개를 넘지 않으므로, 서버가 많은 요청을 받더라도 시스템이 과부하되지 않는다. _/sleep_에 요청을 보내면, 서버는 다른 스레드가 요청을 실행하도록 하여 다른 요청을 처리할 수 있다.

> 참고: 여러 브라우저 창에서 동시에 _/sleep_을 열면, 5초 간격으로 하나씩 로드될 수 있다. 일부 웹 브라우저는 캐싱 이유로 동일한 요청의 여러 인스턴스를 순차적으로 실행한다. 이 제한은 우리 웹 서버로 인한 것이 아니다.

이제 잠시 멈추고 목록 21-18, 21-19, 21-20의 코드가 클로저 대신 futures를 사용한다면 어떻게 달라질지 생각해 볼 좋은 시기이다. 어떤 타입이 변경될까? 메서드 시그니처는 어떻게 달라질까? 코드의 어떤 부분이 동일하게 유지될까?

17장과 18장에서 `while let` 루프에 대해 배운 후, 왜 목록 21-21과 같이 작업자 스레드 코드를 작성하지 않았는지 궁금할 수 있다.

<Listing number="21-21" file-name="src/lib.rs" caption="`while let`을 사용한 `Worker::new`의 대체 구현">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-21/src/lib.rs:here}}
```

</Listing>

이 코드는 컴파일되고 실행되지만, 원하는 스레딩 동작을 얻지 못한다: 느린 요청이 여전히 다른 요청이 처리되기를 기다리게 할 수 있다. 그 이유는 다소 미묘한데, `Mutex` 구조체에는 공개된 `unlock` 메서드가 없기 때문이다. 락의 소유권은 `lock` 메서드가 반환하는 `LockResult<MutexGuard<T>>` 내의 `MutexGuard<T>`의 수명에 기반한다. 컴파일 시, 빌림 검사기는 `Mutex`로 보호된 리소스는 락을 보유하지 않으면 접근할 수 없다는 규칙을 강제할 수 있다. 그러나 이 구현은 `MutexGuard<T>`의 수명을 주의하지 않으면 락이 의도보다 오래 보유될 수 있다.

목록 21-20의 코드는 `let job = receiver.lock().unwrap().recv().unwrap();`을 사용하는데, 이는 `let`을 사용하면 등호 오른쪽의 표현식에 사용된 임시 값이 `let` 문이 끝나면 즉시 삭제되기 때문이다. 그러나 `while let` (그리고 `if let` 및 `match`)은 관련 블록이 끝날 때까지 임시 값을 삭제하지 않는다. 목록 21-21에서는 `job()` 호출 동안 락이 계속 보유되므로, 다른 `Worker` 인스턴스가 작업을 받을 수 없다.

[creating-type-synonyms-with-type-aliases]: ch20-03-advanced-types.html#creating-type-synonyms-with-type-aliases
[integer-types]: ch03-02-data-types.html#integer-types
[fn-traits]: ch13-01-closures.html#moving-captured-values-out-of-the-closure-and-the-fn-traits
[builder]: ../std/thread/struct.Builder.html
[builder-spawn]: ../std/thread/struct.Builder.html#method.spawn


