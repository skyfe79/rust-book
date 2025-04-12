## 그레이스풀 셧다운과 정리

리스트 21-20의 코드는 의도한 대로 스레드 풀을 사용해 요청에 비동기적으로 응답한다. 하지만 `workers`, `id`, `thread` 필드를 직접 사용하지 않아 경고가 발생한다. 이는 정리 작업을 하지 않았다는 것을 알려주는 신호다. <kbd>ctrl</kbd>-<kbd>c</kbd>와 같은 간단한 방법으로 메인 스레드를 중단하면, 다른 모든 스레드도 즉시 중단된다. 심지어 요청을 처리 중인 스레드도 예외는 아니다.

다음으로, 스레드 풀의 각 스레드에서 `join`을 호출해 진행 중인 요청을 마무리한 후 종료할 수 있도록 `Drop` 트레이트를 구현한다. 그리고 스레드가 새로운 요청을 받지 않고 종료하도록 지시하는 방법도 추가한다. 이 코드를 실제로 확인하기 위해, 서버를 수정해 두 개의 요청만 처리한 후 스레드 풀을 그레이스풀하게 종료하도록 한다.

한 가지 주목할 점은, 이 모든 작업이 클로저를 실행하는 코드 부분에는 영향을 미치지 않는다는 것이다. 따라서 비동기 런타임을 위해 스레드 풀을 사용하더라도 여기서 다루는 내용은 동일하게 적용된다.


### `ThreadPool`에 `Drop` 트레이트 구현하기

먼저 스레드 풀에 `Drop`을 구현해 보자. 풀이 드롭될 때, 모든 스레드가 작업을 마칠 수 있도록 `join`을 호출해야 한다. 아래 예제는 `Drop` 구현을 위한 첫 번째 시도다. 이 코드는 아직 완벽하게 동작하지 않는다.

<Listing number="21-22" file-name="src/lib.rs" caption="스레드 풀이 스코프를 벗어날 때 각 스레드에 join 호출하기">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-22/src/lib.rs:here}}
```

</Listing>

먼저 스레드 풀의 각 `worker`를 순회한다. `self`가 가변 참조이기 때문에 `&mut`를 사용하며, `worker`도 변경할 수 있어야 한다. 각 `worker`에 대해 해당 `Worker` 인스턴스가 종료된다는 메시지를 출력한 후, `Worker` 인스턴스의 스레드에 `join`을 호출한다. `join` 호출이 실패하면 `unwrap`을 사용해 Rust가 패닉에 빠지도록 하고, 비정상 종료를 유도한다.

이 코드를 컴파일하면 다음과 같은 에러가 발생한다:

```console
{{#include ../listings/ch21-web-server/listing-21-22/output.txt}}
```

에러 메시지는 각 `worker`에 대해 가변 참조만 가지고 있기 때문에 `join`을 호출할 수 없다고 알려준다. `join`은 인수의 소유권을 가져가기 때문이다. 이 문제를 해결하려면 `thread`를 소유한 `Worker` 인스턴스에서 스레드를 이동시켜 `join`이 스레드를 소비할 수 있도록 해야 한다. 한 가지 방법은 예제 18-15에서 사용한 접근 방식을 따르는 것이다. 만약 `Worker`가 `Option<thread::JoinHandle<()>>`를 가지고 있다면, `Option`의 `take` 메서드를 호출해 `Some` 변형에서 값을 꺼내고 그 자리에 `None`을 남길 수 있다. 즉, 실행 중인 `Worker`는 `thread`에 `Some` 변형을 가지고 있고, `Worker`를 정리할 때 `Some`을 `None`으로 대체해 `Worker`가 더 이상 실행할 스레드를 가지지 않도록 할 수 있다.

그러나 이 방법은 `Worker`를 드롭할 때만 필요하다. 대신 `worker.thread`에 접근할 때마다 `Option<thread::JoinHandle<()>>`를 처리해야 한다. Rust에서는 `Option`을 자주 사용하지만, 항상 존재할 것이 확실한 값을 `Option`으로 감싸는 것은 코드를 더 깔끔하고 오류가 적게 만드는 대안을 찾는 것이 좋다.

이 경우 더 나은 대안이 있다: `Vec::drain` 메서드다. 이 메서드는 `Vec`에서 제거할 항목을 지정하는 범위 매개변수를 받고, 해당 항목의 이터레이터를 반환한다. `..` 범위 구문을 전달하면 `Vec`의 모든 값을 제거한다.

따라서 `ThreadPool`의 `drop` 구현을 다음과 같이 업데이트해야 한다:

<Listing file-name="src/lib.rs">

```rust
{{#rustdoc_include ../listings/ch21-web-server/no-listing-04-update-drop-definition/src/lib.rs:here}}
```

</Listing>

이렇게 하면 컴파일러 에러가 해결되며, 코드의 다른 부분을 변경할 필요가 없다.


### 스레드에게 작업 수신을 중단하도록 신호 보내기

지금까지 수정한 내용을 통해 코드는 경고 없이 컴파일된다. 그러나 아쉽게도 이 코드는 아직 원하는 대로 동작하지 않는다. 문제의 핵심은 `Worker` 인스턴스의 스레드가 실행하는 클로저의 로직에 있다. 현재는 `join`을 호출하지만, 이는 스레드가 작업을 계속해서 찾는 무한 루프 때문에 스레드를 종료하지 못한다. 만약 현재 구현된 `drop`을 통해 `ThreadPool`을 삭제하려고 하면, 메인 스레드는 첫 번째 스레드가 종료되기를 기다리며 영원히 블록될 것이다.

이 문제를 해결하기 위해 `ThreadPool`의 `drop` 구현을 변경하고, `Worker`의 루프도 수정해야 한다.

먼저 `ThreadPool`의 `drop` 구현을 변경하여 스레드가 종료되기를 기다리기 전에 `sender`를 명시적으로 삭제한다. 리스트 21-23은 `sender`를 명시적으로 삭제하기 위해 `ThreadPool`에 적용한 변경 사항을 보여준다. 스레드와 달리 여기서는 `Option::take`를 사용해 `sender`를 `ThreadPool`에서 이동시키기 위해 `Option`을 사용해야 한다.

<Listing number="21-23" file-name="src/lib.rs" caption="`Worker` 스레드를 `join`하기 전에 `sender`를 명시적으로 삭제">

```rust,noplayground,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-23/src/lib.rs:here}}
```

</Listing>

`sender`를 삭제하면 채널이 닫히고, 더 이상 메시지가 전송되지 않음을 나타낸다. 이 경우 `Worker` 인스턴스가 무한 루프에서 수행하는 `recv` 호출은 모두 에러를 반환한다. 리스트 21-24에서는 이 경우에 루프를 정상적으로 종료하도록 `Worker` 루프를 변경한다. 이는 `ThreadPool`의 `drop` 구현이 `join`을 호출할 때 스레드가 종료됨을 의미한다.

<Listing number="21-24" file-name="src/lib.rs" caption="`recv`가 에러를 반환할 때 루프를 명시적으로 종료">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-24/src/lib.rs:here}}
```

</Listing>

이 코드가 동작하는 모습을 보기 위해, 리스트 21-25와 같이 `main`을 수정하여 서버가 두 개의 요청만 처리한 후 정상적으로 종료하도록 한다.

<Listing number="21-25" file-name="src/main.rs" caption="루프를 종료하여 두 개의 요청을 처리한 후 서버 종료">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/listing-21-25/src/main.rs:here}}
```

</Listing>

실제 웹 서버는 단 두 개의 요청만 처리하고 종료하도록 만들지는 않을 것이다. 이 코드는 단순히 정상적인 종료와 정리 작업이 제대로 동작하는지 보여주기 위한 예제이다.

`take` 메서드는 `Iterator` 트레이트에 정의되어 있으며, 반복을 최대 두 개의 항목으로 제한한다. `ThreadPool`은 `main`의 끝에서 스코프를 벗어나며, `drop` 구현이 실행된다.

`cargo run`으로 서버를 시작하고, 세 번의 요청을 보낸다. 세 번째 요청은 에러를 반환해야 하며, 터미널에서 다음과 유사한 출력을 확인할 수 있다:

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.41s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Shutting down.
Shutting down worker 0
Worker 3 got a job; executing.
Worker 1 disconnected; shutting down.
Worker 2 disconnected; shutting down.
Worker 3 disconnected; shutting down.
Worker 0 disconnected; shutting down.
Shutting down worker 1
Shutting down worker 2
Shutting down worker 3
```

`Worker` ID와 메시지의 순서는 다를 수 있다. 메시지를 통해 이 코드가 어떻게 동작하는지 확인할 수 있다: `Worker` 인스턴스 0과 3이 처음 두 요청을 받았다. 서버는 두 번째 연결 이후에 연결을 수락하지 않았고, `ThreadPool`의 `Drop` 구현은 `Worker` 3이 작업을 시작하기 전에 실행되기 시작했다. `sender`를 삭제하면 모든 `Worker` 인스턴스의 연결이 끊어지고 종료하도록 지시한다. 각 `Worker` 인스턴스는 연결이 끊어질 때 메시지를 출력하고, 스레드 풀은 각 `Worker` 스레드가 종료되기를 기다리기 위해 `join`을 호출한다.

이 실행에서 흥미로운 점은 `ThreadPool`이 `sender`를 삭제한 후, 어떤 `Worker`도 에러를 받기 전에 `Worker` 0을 `join`하려고 시도했다는 것이다. `Worker` 0은 아직 `recv`에서 에러를 받지 않았기 때문에, 메인 스레드는 `Worker` 0이 종료되기를 기다리며 블록되었다. 그 동안 `Worker` 3은 작업을 받고, 이후 모든 스레드가 에러를 받았다. `Worker` 0이 종료되면, 메인 스레드는 나머지 `Worker` 인스턴스가 종료되기를 기다렸다. 이 시점에서 모든 스레드는 루프를 종료하고 정지했다.

축하한다! 이제 프로젝트를 완성했다. 스레드 풀을 사용해 비동기적으로 응답하는 기본적인 웹 서버를 만들었다. 또한 서버를 정상적으로 종료하고 풀의 모든 스레드를 정리할 수 있게 되었다.

참고를 위해 전체 코드는 다음과 같다:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/main.rs}}
```

</Listing>

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/lib.rs}}
```

</Listing>

여기서 더 많은 작업을 할 수 있다! 이 프로젝트를 계속 개선하고 싶다면 다음 아이디어를 고려해보자:

- `ThreadPool`과 그 공개 메서드에 대한 문서를 추가한다.
- 라이브러리의 기능을 테스트한다.
- `unwrap` 호출을 더 강력한 에러 처리로 변경한다.
- 웹 요청 처리 외에 다른 작업을 수행하기 위해 `ThreadPool`을 사용한다.
- [crates.io](https://crates.io/)에서 스레드 풀 크레이트를 찾아 이를 사용해 비슷한 웹 서버를 구현한다. 그리고 그 크레이트의 API와 견고성을 우리가 구현한 스레드 풀과 비교한다.


## 요약

축하한다! 지금까지 Rust 여정을 함께 해줘서 고맙다. 이제 여러분은 자신만의 Rust 프로젝트를 구현하고 다른 사람들의 프로젝트에도 기여할 준비가 되었다. Rust 여정에서 마주칠 수 있는 도전 과제를 해결하는 데 도움을 줄 Rust 커뮤니티가 항상 열려 있다는 것을 기억하길 바란다.


