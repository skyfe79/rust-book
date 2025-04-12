## `panic!`로 처리할 수 없는 오류

코드에서 예기치 못한 문제가 발생할 때가 있다. 이런 경우 Rust는 `panic!` 매크로를 제공한다. 실제로 패닉을 일으키는 방법은 두 가지다: 코드가 패닉을 일으키는 동작을 수행하거나(예: 배열의 끝을 넘어서 접근), `panic!` 매크로를 직접 호출하는 것이다. 두 경우 모두 프로그램에서 패닉이 발생한다. 기본적으로 패닉은 실패 메시지를 출력하고, 스택을 되감은 뒤 정리하고 프로그램을 종료한다. 환경 변수를 통해 패닉이 발생할 때 Rust가 호출 스택을 표시하도록 설정할 수도 있다. 이렇게 하면 패닉의 원인을 더 쉽게 추적할 수 있다.

> ### 스택 되감기와 즉시 종료
>
> 기본적으로 패닉이 발생하면 프로그램은 스택을 되감기 시작한다. 이는 Rust가 스택을 거슬러 올라가면서 각 함수에서 사용한 데이터를 정리한다는 의미다. 하지만 이 과정은 많은 작업을 필요로 한다. 따라서 Rust는 즉시 종료하는 방식을 선택할 수도 있다. 이 경우 프로그램은 정리 과정 없이 바로 종료된다.
>
> 프로그램이 사용하던 메모리는 운영체제가 정리하게 된다. 프로젝트에서 생성되는 바이너리 파일의 크기를 최대한 작게 만들고 싶다면, `Cargo.toml` 파일의 `[profile]` 섹션에 `panic = 'abort'`를 추가해 패닉 발생 시 스택 되감기 대신 즉시 종료하도록 설정할 수 있다. 예를 들어, 릴리스 모드에서 패닉 발생 시 즉시 종료하려면 다음과 같이 설정한다:
>
> ```toml
> [profile.release]
> panic = 'abort'
> ```

간단한 프로그램에서 `panic!`을 호출해 보자:

<Listing file-name="src/main.rs">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-01-panic/src/main.rs}}
```

</Listing>

프로그램을 실행하면 다음과 같은 결과를 볼 수 있다:

```console
{{#include ../listings/ch09-error-handling/no-listing-01-panic/output.txt}}
```

`panic!` 호출은 마지막 두 줄에 있는 오류 메시지를 발생시킨다. 첫 번째 줄은 패닉 메시지와 소스 코드에서 패닉이 발생한 위치를 보여준다: `src/main.rs:2:5`는 `src/main.rs` 파일의 두 번째 줄, 다섯 번째 문자를 가리킨다.

이 경우, 표시된 줄은 우리 코드의 일부이며, 해당 줄을 보면 `panic!` 매크로 호출을 확인할 수 있다. 다른 경우에는 `panic!` 호출이 우리 코드가 호출한 다른 코드에서 발생할 수도 있다. 이때 오류 메시지가 표시하는 파일 이름과 줄 번호는 `panic!` 매크로가 호출된 다른 코드의 위치를 가리키게 된다.

<!-- Old heading. Do not remove or links may break. -->

<a id="using-a-panic-backtrace"></a>

`panic!` 호출이 발생한 함수의 백트레이스를 사용해 문제의 원인을 찾을 수 있다. `panic!` 백트레이스를 어떻게 사용하는지 이해하기 위해 또 다른 예제를 살펴보자. 이번에는 우리 코드가 직접 `panic!` 매크로를 호출하는 대신, 라이브러리에서 버그로 인해 `panic!`이 발생하는 경우를 살펴본다. 리스트 9-1은 벡터의 유효한 인덱스 범위를 벗어난 위치에 접근하려는 코드다.

<Listing number="9-1" file-name="src/main.rs" caption="벡터의 끝을 넘어선 위치에 접근하려는 시도로 인해 `panic!`이 호출되는 예제">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-01/src/main.rs}}
```

</Listing>

여기서는 벡터의 100번째 요소(인덱스는 0부터 시작하므로 실제로는 99번째)에 접근하려고 하지만, 벡터에는 세 개의 요소만 있다. 이런 상황에서 Rust는 패닉을 발생시킨다. `[]`는 요소를 반환해야 하지만, 유효하지 않은 인덱스를 전달하면 Rust가 반환할 수 있는 올바른 요소가 없다.

C 언어에서는 데이터 구조의 끝을 넘어서 읽으려고 하면 정의되지 않은 동작이 발생한다. 데이터 구조에 속하지 않는 메모리 위치에 있는 값을 반환할 수도 있다. 이를 _버퍼 오버리드(buffer overread)_ 라고 하며, 공격자가 인덱스를 조작해 데이터 구조 뒤에 저장된 접근 권한이 없는 데이터를 읽을 수 있게 되면 보안 취약점으로 이어질 수 있다.

이런 취약점으로부터 프로그램을 보호하기 위해, Rust는 존재하지 않는 인덱스의 요소를 읽으려고 하면 실행을 중단하고 더 이상 진행하지 않는다. 한번 실행해 보자:

```console
{{#include ../listings/ch09-error-handling/listing-09-01/output.txt}}
```

이 오류는 `main.rs` 파일의 4번째 줄에서 벡터 `v`의 인덱스 `99`에 접근하려는 시도를 가리킨다.

`note:` 줄은 `RUST_BACKTRACE` 환경 변수를 설정해 오류의 원인이 된 정확한 백트레이스를 확인할 수 있다고 알려준다. _백트레이스(backtrace)_ 는 이 지점에 도달하기까지 호출된 모든 함수의 목록이다. Rust의 백트레이스는 다른 언어와 동일하게 동작한다: 백트레이스를 읽는 핵심은 위에서부터 시작해 우리가 작성한 파일을 볼 때까지 읽는 것이다. 그곳이 문제의 시작점이다. 그 위의 줄들은 우리 코드가 호출한 코드고, 아래의 줄들은 우리 코드를 호출한 코드다. 이 앞뒤 줄들은 Rust의 코어 코드, 표준 라이브러리 코드, 또는 사용 중인 크레이트의 코드일 수 있다. `RUST_BACKTRACE` 환경 변수를 `0`이 아닌 값으로 설정해 백트레이스를 확인해 보자. 리스트 9-2는 이렇게 했을 때 볼 수 있는 출력 예제를 보여준다.

<!-- manual-regeneration
cd listings/ch09-error-handling/listing-09-01
RUST_BACKTRACE=1 cargo run
copy the backtrace output below
check the backtrace number mentioned in the text below the listing
-->

<Listing number="9-2" caption="`RUST_BACKTRACE` 환경 변수가 설정되었을 때 `panic!` 호출로 생성된 백트레이스">

```console
$ RUST_BACKTRACE=1 cargo run
thread 'main' panicked at src/main.rs:4:6:
index out of bounds: the len is 3 but the index is 99
stack backtrace:
   0: rust_begin_unwind
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/std/src/panicking.rs:692:5
   1: core::panicking::panic_fmt
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:75:14
   2: core::panicking::panic_bounds_check
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:273:5
   3: <usize as core::slice::index::SliceIndex<[T]>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:274:10
   4: core::slice::index::<impl core::ops::index::Index<I> for [T]>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:16:9
   5: <alloc::vec::Vec<T,A> as core::ops::index::Index<I>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/alloc/src/vec/mod.rs:3361:9
   6: panic::main
             at ./src/main.rs:4:6
   7: core::ops::function::FnOnce::call_once
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/ops/function.rs:250:5
note: Some details are omitted, run with `RUST_BACKTRACE=full` for a verbose backtrace.
```

</Listing>

출력이 상당히 많다! 정확한 출력은 운영체제와 Rust 버전에 따라 다를 수 있다. 이 정보를 포함한 백트레이스를 얻으려면 디버그 심볼이 활성화되어 있어야 한다. 디버그 심볼은 `cargo build`나 `cargo run`을 `--release` 플래그 없이 사용할 때 기본적으로 활성화된다.

리스트 9-2의 출력에서 백트레이스의 6번째 줄은 문제를 일으키는 프로젝트의 줄을 가리킨다: `src/main.rs` 파일의 4번째 줄이다. 프로그램이 패닉을 일으키지 않도록 하려면, 우리가 작성한 파일을 언급하는 첫 번째 줄이 가리키는 위치에서 조사를 시작해야 한다. 리스트 9-1에서 의도적으로 패닉을 일으키는 코드를 작성했으므로, 패닉을 수정하려면 벡터 인덱스 범위를 벗어난 위치에 접근하지 않아야 한다. 앞으로 코드에서 패닉이 발생하면, 어떤 동작을 어떤 값으로 수행했는지, 그리고 코드가 대신 무엇을 해야 하는지 파악해야 한다.

`panic!`과 이를 사용해야 하는 경우와 사용하지 말아야 하는 경우에 대해서는 이 장의 [“`panic!`을 사용할 것인가, 사용하지 말 것인가”][to-panic-or-not-to-panic]<!-- ignore --> 섹션에서 다시 다룬다. 다음으로는 `Result`를 사용해 오류를 복구하는 방법을 살펴본다.

[to-panic-or-not-to-panic]: ch09-03-to-panic-or-not-to-panic.html#to-panic-or-not-to-panic


