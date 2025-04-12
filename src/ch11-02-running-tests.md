## 테스트 실행 방식 제어하기

`cargo run`이 코드를 컴파일한 후 결과 바이너리를 실행하는 것처럼, `cargo test`는 코드를 테스트 모드로 컴파일한 후 결과 테스트 바이너리를 실행한다. `cargo test`로 생성된 바이너리의 기본 동작은 모든 테스트를 병렬로 실행하고, 테스트 실행 중 생성된 출력을 캡처하여 화면에 표시하지 않는다. 이렇게 하면 테스트 결과와 관련된 출력을 더 쉽게 읽을 수 있다. 하지만 커맨드라인 옵션을 지정해 이 기본 동작을 변경할 수 있다.

일부 커맨드라인 옵션은 `cargo test`에 전달되고, 다른 옵션은 결과 테스트 바이너리에 전달된다. 이 두 가지 유형의 인자를 구분하려면, `cargo test`에 전달할 인자를 먼저 나열한 후 구분자 `--`를 넣고, 그 다음에 테스트 바이너리에 전달할 인자를 나열한다. `cargo test --help`를 실행하면 `cargo test`와 함께 사용할 수 있는 옵션을 확인할 수 있고, `cargo test -- --help`를 실행하면 구분자 뒤에 사용할 수 있는 옵션을 확인할 수 있다. 이 옵션들은 [rustc 책][rustc]의 [“Tests” 섹션][tests]에 문서화되어 있다.

[tests]: https://doc.rust-lang.org/rustc/tests/index.html
[rustc]: https://doc.rust-lang.org/rustc/index.html


### 테스트를 병렬 또는 순차적으로 실행하기

여러 테스트를 실행할 때 기본적으로 스레드를 사용해 병렬로 실행한다. 이렇게 하면 테스트가 더 빨리 완료되고 결과를 빠르게 확인할 수 있다. 하지만 테스트가 동시에 실행되기 때문에, 각 테스트가 서로 의존하거나 공유 상태(예: 현재 작업 디렉토리나 환경 변수와 같은 공유 환경)에 의존하지 않도록 주의해야 한다.

예를 들어, 각 테스트가 디스크에 _test-output.txt_라는 파일을 생성하고 데이터를 쓰는 코드를 실행한다고 가정하자. 그런 다음 각 테스트는 해당 파일의 데이터를 읽고 파일에 특정 값이 포함되어 있는지 확인한다. 이때 각 테스트는 서로 다른 값을 검사한다. 테스트가 동시에 실행되면 한 테스트가 파일을 쓰는 동안 다른 테스트가 파일을 덮어쓸 수 있다. 이 경우 두 번째 테스트는 코드가 잘못된 것이 아니라 병렬 실행 중에 테스트가 서로 간섭했기 때문에 실패할 수 있다. 이를 해결하는 한 가지 방법은 각 테스트가 서로 다른 파일에 쓰도록 하는 것이다. 또 다른 방법은 테스트를 하나씩 순차적으로 실행하는 것이다.

테스트를 병렬로 실행하고 싶지 않거나 사용할 스레드 수를 더 세밀하게 제어하고 싶다면 `--test-threads` 플래그와 사용할 스레드 수를 테스트 바이너리에 전달할 수 있다. 다음 예제를 살펴보자:

```console
$ cargo test -- --test-threads=1
```

테스트 스레드 수를 `1`로 설정해 프로그램이 병렬 처리를 사용하지 않도록 한다. 하나의 스레드로 테스트를 실행하면 병렬로 실행할 때보다 시간이 더 오래 걸리지만, 테스트가 상태를 공유하더라도 서로 간섭하지 않는다.


### 함수 출력 보여주기

기본적으로 테스트가 성공하면, Rust의 테스트 라이브러리는 표준 출력에 출력된 모든 내용을 캡처한다. 예를 들어, 테스트에서 `println!`을 호출하고 테스트가 성공하면, 터미널에서 `println!`의 출력을 볼 수 없다. 대신 테스트가 성공했다는 메시지만 보게 된다. 테스트가 실패하면, 실패 메시지와 함께 표준 출력에 출력된 내용을 확인할 수 있다.

예를 들어, 리스트 11-10에는 매개변수의 값을 출력하고 10을 반환하는 단순한 함수가 있다. 이 함수에 대한 테스트 중 하나는 성공하고, 다른 하나는 실패한다.

<Listing number="11-10" file-name="src/lib.rs" caption="`println!`을 호출하는 함수에 대한 테스트">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-10/src/lib.rs}}
```

</Listing>

`cargo test`로 이 테스트를 실행하면 다음과 같은 출력을 볼 수 있다:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-10/output.txt}}
```

출력 결과에서 `I got the value 4`라는 메시지를 찾을 수 없다. 이 메시지는 테스트가 성공할 때 출력되지만, 캡처되었다. 반면, 실패한 테스트의 출력인 `I got the value 8`은 테스트 요약 출력 부분에 나타나며, 테스트 실패의 원인도 함께 표시된다.

성공한 테스트의 출력값도 확인하고 싶다면, `--show-output` 플래그를 사용해 Rust에게 성공한 테스트의 출력도 보여주도록 지시할 수 있다:

```console
$ cargo test -- --show-output
```

`--show-output` 플래그를 사용해 리스트 11-10의 테스트를 다시 실행하면, 다음과 같은 출력을 볼 수 있다:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-01-show-output/output.txt}}
```


### 이름으로 테스트의 일부만 실행하기

전체 테스트 스위트를 실행하면 시간이 오래 걸릴 수 있다. 특정 코드 영역을 작업 중이라면 해당 코드와 관련된 테스트만 실행하고 싶을 수 있다. `cargo test`에 실행하려는 테스트의 이름을 인자로 전달하면 원하는 테스트만 선택적으로 실행할 수 있다.

테스트의 일부만 실행하는 방법을 보여주기 위해, 먼저 `add_two` 함수에 대한 세 가지 테스트를 작성한다. Listing 11-11에서 이를 확인할 수 있으며, 어떤 테스트를 실행할지 선택할 수 있다.

<Listing number="11-11" file-name="src/lib.rs" caption="서로 다른 이름을 가진 세 가지 테스트">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-11/src/lib.rs}}
```

</Listing>

앞서 보았듯이, 아무런 인자 없이 테스트를 실행하면 모든 테스트가 병렬로 실행된다:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-11/output.txt}}
```


#### 단일 테스트 실행하기

`cargo test` 명령어에 특정 테스트 함수의 이름을 전달하면 해당 테스트만 실행할 수 있다:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-02-single-test/output.txt}}
```

`one_hundred`라는 이름의 테스트만 실행되었고, 나머지 두 테스트는 이름이 일치하지 않아 실행되지 않았다. 테스트 출력 결과 끝부분에 `2 filtered out`이라는 메시지가 표시되어 실행되지 않은 테스트가 두 개 있음을 알려준다.

이 방식으로는 여러 테스트의 이름을 동시에 지정할 수 없다. `cargo test`에 전달된 첫 번째 값만 사용되기 때문이다. 하지만 여러 테스트를 실행할 수 있는 방법이 있다.


#### 여러 테스트를 실행하기 위한 필터링

테스트 이름의 일부를 지정하면 해당 값과 일치하는 이름을 가진 모든 테스트가 실행된다. 예를 들어, 두 테스트의 이름에 `add`가 포함되어 있으므로 `cargo test add`를 실행하면 해당 두 테스트만 실행할 수 있다:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-03-multiple-tests/output.txt}}
```

이 커맨드는 이름에 `add`가 포함된 모든 테스트를 실행하고 `one_hundred`라는 이름의 테스트는 제외했다. 또한 테스트가 속한 모듈 이름도 테스트 이름의 일부가 되므로, 모듈 이름으로 필터링하면 해당 모듈의 모든 테스트를 실행할 수 있다.


### 특별히 요청하지 않는 한 일부 테스트 무시하기


때로는 특정 테스트를 실행하는 데 시간이 오래 걸릴 수 있다. 이 경우 `cargo test`를 실행할 때 대부분의 경우 해당 테스트를 제외하고 싶을 수 있다. 실행하고 싶은 모든 테스트를 인수로 나열하는 대신, 시간이 오래 걸리는 테스트에 `ignore` 속성을 추가해 제외할 수 있다.

<span class="filename">파일명: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/src/lib.rs:here}}
```

`#[test]` 뒤에 제외하고 싶은 테스트에 `#[ignore]` 줄을 추가한다. 이제 테스트를 실행하면 `it_works`는 실행되지만 `expensive_test`는 실행되지 않는다.

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/output.txt}}
```

`expensive_test` 함수는 `ignored`로 표시된다. 만약 무시된 테스트만 실행하고 싶다면 `cargo test -- --ignored`를 사용할 수 있다.

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-04-running-ignored/output.txt}}
```

어떤 테스트를 실행할지 제어함으로써 `cargo test` 결과를 빠르게 확인할 수 있다. `ignored` 테스트의 결과를 확인할 필요가 있고, 결과를 기다릴 시간이 있다면 `cargo test -- --ignored`를 실행하면 된다. 무시된 테스트를 포함해 모든 테스트를 실행하고 싶다면 `cargo test -- --include-ignored`를 사용할 수 있다.


