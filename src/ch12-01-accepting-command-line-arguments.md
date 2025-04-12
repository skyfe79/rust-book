## 커맨드라인 인자 받아들이기

항상 그렇듯이 `cargo new`로 새로운 프로젝트를 생성한다. 이 프로젝트는 시스템에 이미 설치되어 있을 수 있는 `grep` 도구와 구분하기 위해 `minigrep`이라고 이름 짓는다.

```console
$ cargo new minigrep
     Created binary (application) `minigrep` project
$ cd minigrep
```

첫 번째 작업은 `minigrep`이 두 개의 커맨드라인 인자를 받아들이도록 만드는 것이다. 파일 경로와 검색할 문자열이 바로 그것이다. 즉, 프로그램을 `cargo run`으로 실행할 때, 두 개의 하이픈을 사용해 뒤따르는 인자가 `cargo`가 아닌 우리 프로그램을 위한 것임을 나타내고, 검색할 문자열과 검색할 파일의 경로를 다음과 같이 전달할 수 있도록 만드는 것이다:

```console
$ cargo run -- searchstring example-filename.txt
```

현재 `cargo new`로 생성된 프로그램은 우리가 전달한 인자를 처리할 수 없다. [crates.io](https://crates.io/)에는 커맨드라인 인자를 받아들이는 프로그램을 작성하는 데 도움을 주는 여러 라이브러리가 있지만, 이 개념을 배우는 중이므로 이 기능을 직접 구현해보자.


### 인자 값 읽기

`minigrep`이 전달받은 커맨드라인 인자 값을 읽으려면 Rust 표준 라이브러리에서 제공하는 `std::env::args` 함수를 사용해야 한다. 이 함수는 `minigrep`에 전달된 커맨드라인 인자들의 이터레이터를 반환한다. 이터레이터에 대해서는 [13장][ch13]<!-- ignore -->에서 자세히 다룬다. 지금은 이터레이터가 일련의 값을 생성하고, 이터레이터에 `collect` 메서드를 호출해 벡터와 같은 컬렉션으로 변환할 수 있다는 점만 알면 된다.

리스트 12-1의 코드는 `minigrep` 프로그램이 전달받은 커맨드라인 인자를 읽고, 그 값을 벡터로 수집한다.

<Listing number="12-1" file-name="src/main.rs" caption="커맨드라인 인자를 벡터로 수집하고 출력하기">

```rust
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-01/src/main.rs}}
```

</Listing>

먼저 `use` 문을 사용해 `std::env` 모듈을 스코프로 가져와 `args` 함수를 사용할 수 있게 한다. `std::env::args` 함수는 두 단계의 모듈 안에 중첩되어 있다. [7장][ch7-idiomatic-use]<!-- ignore -->에서 논의한 것처럼, 원하는 함수가 여러 모듈에 중첩된 경우, 함수 자체보다는 상위 모듈을 스코프로 가져오는 것이 일반적이다. 이렇게 하면 `std::env`의 다른 함수도 쉽게 사용할 수 있다. 또한 `use std::env::args`를 추가하고 `args` 함수를 호출하는 것보다 모호함이 적다. `args`는 현재 모듈에 정의된 함수와 혼동될 수 있기 때문이다.

> ### `args` 함수와 유효하지 않은 유니코드
>
> `std::env::args`는 인자가 유효하지 않은 유니코드를 포함할 경우 패닉을 일으킨다. 프로그램이 유효하지 않은 유니코드를 포함하는 인자를 받아야 한다면 `std::env::args_os`를 대신 사용해야 한다. 이 함수는 `String` 값 대신 `OsString` 값을 생성하는 이터레이터를 반환한다. 여기서는 간단하게 `std::env::args`를 사용했는데, `OsString` 값은 플랫폼마다 다르고 `String` 값보다 다루기 복잡하기 때문이다.

`main` 함수의 첫 줄에서 `env::args`를 호출하고, 바로 `collect`를 사용해 이터레이터가 생성한 모든 값을 포함하는 벡터로 변환한다. `collect` 함수는 다양한 종류의 컬렉션을 생성할 수 있으므로, `args`의 타입을 명시적으로 어노테이션해 문자열 벡터를 원한다는 것을 나타낸다. Rust에서는 타입을 어노테이션할 필요가 거의 없지만, `collect`는 Rust가 원하는 컬렉션 종류를 추론할 수 없기 때문에 종종 어노테이션이 필요하다.

마지막으로, 디버그 매크로를 사용해 벡터를 출력한다. 이 코드를 인자 없이 실행한 후 두 개의 인자를 전달해 실행해 보자:

```console
{{#include ../listings/ch12-an-io-project/listing-12-01/output.txt}}
```

```console
{{#include ../listings/ch12-an-io-project/output-only-01-with-args/output.txt}}
```

벡터의 첫 번째 값은 `"target/debug/minigrep"`으로, 바이너리의 이름이다. 이는 C 언어에서의 인자 리스트 동작과 일치하며, 프로그램이 실행될 때 호출된 이름을 사용할 수 있게 한다. 메시지에 프로그램 이름을 출력하거나, 프로그램을 호출할 때 사용한 커맨드라인 별칭에 따라 프로그램의 동작을 변경하는 경우에 유용하다. 하지만 이 장에서는 이 값을 무시하고 필요한 두 개의 인자만 저장한다.


### 인자 값을 변수에 저장하기

현재 프로그램은 커맨드라인 인자로 지정된 값에 접근할 수 있다. 이제 두 인자의 값을 변수에 저장해 프로그램의 나머지 부분에서 활용할 수 있도록 해야 한다. 이를 위해 리스트 12-2와 같이 코드를 작성한다.

<Listing number="12-2" file-name="src/main.rs" caption="쿼리 인자와 파일 경로 인자를 저장할 변수 생성">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-02/src/main.rs}}
```

</Listing>

벡터를 출력했을 때 확인했듯이, 프로그램 이름은 벡터의 첫 번째 값인 `args[0]`에 저장된다. 따라서 인자는 인덱스 1부터 시작한다. `minigrep`이 받는 첫 번째 인자는 검색할 문자열이므로, 첫 번째 인자의 참조를 `query` 변수에 저장한다. 두 번째 인자는 파일 경로이므로, 두 번째 인자의 참조를 `file_path` 변수에 저장한다.

코드가 의도한 대로 동작하는지 확인하기 위해 이 변수들의 값을 임시로 출력한다. 이제 `test`와 `sample.txt` 인자를 사용해 프로그램을 다시 실행해 보자:

```console
{{#include ../listings/ch12-an-io-project/listing-12-02/output.txt}}
```

잘 동작한다! 필요한 인자 값이 올바른 변수에 저장되고 있다. 나중에 사용자가 인자를 제공하지 않는 경우와 같은 잠재적인 오류 상황을 처리하기 위해 에러 핸들링을 추가할 것이다. 지금은 그 상황을 무시하고 파일 읽기 기능을 추가하는 데 집중한다.

[ch13]: ch13-00-functional-features.html
[ch7-idiomatic-use]: ch07-04-bringing-paths-into-scope-with-the-use-keyword.html#creating-idiomatic-use-paths


