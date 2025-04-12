## 모듈성과 에러 처리 개선을 위한 리팩토링

프로그램의 구조와 잠재적 에러 처리를 개선하기 위해 네 가지 문제를 해결한다. 첫째, 현재 `main` 함수는 인자를 파싱하고 파일을 읽는 두 가지 작업을 동시에 수행한다. 프로그램이 커질수록 `main` 함수가 처리하는 작업의 수가 늘어난다. 함수의 책임이 많아질수록 이해하기 어려워지고, 테스트하기도 어려워지며, 수정 시 다른 부분에 영향을 미칠 가능성이 커진다. 따라서 각 함수가 하나의 작업만 담당하도록 기능을 분리하는 것이 좋다.

이 문제는 두 번째 문제와도 연결된다. `query`와 `file_path`는 프로그램의 설정 변수이지만, `contents`와 같은 변수는 프로그램의 로직을 수행하는 데 사용된다. `main` 함수가 길어질수록 더 많은 변수를 범위에 포함해야 하며, 변수가 많아질수록 각 변수의 목적을 추적하기 어려워진다. 따라서 설정 변수를 하나의 구조체로 묶어 목적을 명확히 하는 것이 좋다.

세 번째 문제는 파일 읽기 실패 시 `expect`를 사용해 에러 메시지를 출력하지만, `Should have been able to read the file`이라는 일반적인 메시지만 표시한다는 점이다. 파일 읽기는 다양한 이유로 실패할 수 있다. 예를 들어, 파일이 없거나, 파일을 열 권한이 없을 수 있다. 현재는 상황에 관계없이 동일한 에러 메시지를 출력하므로 사용자에게 유용한 정보를 제공하지 못한다.

네 번째 문제는 에러 처리를 위해 `expect`를 사용하며, 사용자가 충분한 인수를 지정하지 않고 프로그램을 실행하면 Rust에서 `index out of bounds` 에러가 발생한다. 이는 문제를 명확히 설명하지 못한다. 모든 에러 처리 코드를 한 곳에 모아두면 향후 유지보수 시 에러 처리 로직을 변경할 때 한 곳만 참조하면 된다. 또한, 모든 에러 처리 코드를 한 곳에 모아두면 최종 사용자에게 의미 있는 메시지를 출력할 수 있다.

이제 이 네 가지 문제를 해결하기 위해 프로젝트를 리팩토링해보자.


### 바이너리 프로젝트의 관심사 분리

많은 바이너리 프로젝트에서 여러 작업의 책임을 `main` 함수에 할당하는 조직화 문제가 자주 발생한다. 이에 따라 Rust 커뮤니티는 `main` 함수가 커질 때 바이너리 프로그램의 관심사를 분리하기 위한 가이드라인을 개발했다. 이 과정은 다음과 같은 단계로 진행된다:

- 프로그램을 _main.rs_ 파일과 _lib.rs_ 파일로 나누고, 프로그램의 로직을 _lib.rs_로 옮긴다.
- 커맨드라인 파싱 로직이 작은 경우, _main.rs_에 그대로 둘 수 있다.
- 커맨드라인 파싱 로직이 복잡해지면, _main.rs_에서 추출하여 _lib.rs_로 옮긴다.

이 과정 이후 `main` 함수에 남은 책임은 다음과 같이 제한된다:

- 인자 값을 사용해 커맨드라인 파싱 로직을 호출한다.
- 다른 설정을 구성한다.
- _lib.rs_에 있는 `run` 함수를 호출한다.
- `run` 함수가 에러를 반환하면 이를 처리한다.

이 패턴은 관심사를 분리하는 것에 관한 것이다: _main.rs_는 프로그램 실행을 처리하고, _lib.rs_는 작업의 모든 로직을 처리한다. `main` 함수를 직접 테스트할 수 없기 때문에, 이 구조를 통해 프로그램의 모든 로직을 _lib.rs_의 함수로 옮겨 테스트할 수 있다. _main.rs_에 남아 있는 코드는 읽기만 해도 정확성을 확인할 수 있을 만큼 간결해진다. 이제 이 과정을 따라 프로그램을 재구성해 보자.


#### 인자 파서 추출하기

우리는 인자 파싱 기능을 `main` 함수가 호출할 수 있는 별도의 함수로 추출할 것이다. 이렇게 하면 커맨드라인 파싱 로직을 _src/lib.rs_로 옮길 준비를 할 수 있다. 리스트 12-5는 `parse_config`라는 새로운 함수를 호출하는 `main` 함수의 시작 부분을 보여준다. 이 함수는 현재 _src/main.rs_에 정의되어 있다.

<Listing number="12-5" file-name="src/main.rs" caption="`main`에서 `parse_config` 함수 추출하기">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-05/src/main.rs:here}}
```

</Listing>

여전히 커맨드라인 인자를 벡터로 수집하지만, `main` 함수 내에서 인덱스 1의 값을 `query` 변수에, 인덱스 2의 값을 `file_path` 변수에 할당하는 대신, 전체 벡터를 `parse_config` 함수에 전달한다. `parse_config` 함수는 어떤 인자가 어떤 변수에 해당하는지 결정하는 로직을 담당하고, 값을 `main` 함수로 반환한다. `main` 함수에서는 여전히 `query`와 `file_path` 변수를 생성하지만, 이제는 커맨드라인 인자와 변수 간의 매핑을 결정할 책임이 없다.

이렇게 리팩토링하는 것이 작은 프로그램에서는 과한 작업처럼 보일 수 있지만, 우리는 작은 단계로 점진적으로 리팩토링을 진행하고 있다. 이 변경을 적용한 후에는 프로그램을 다시 실행해 인자 파싱이 여전히 잘 동작하는지 확인한다. 문제가 발생했을 때 원인을 쉽게 찾을 수 있도록 자주 진행 상황을 확인하는 것이 좋다.


#### 설정 값 그룹화

`parse_config` 함수를 더 개선할 수 있는 작은 단계를 하나 더 살펴보자. 현재는 튜플을 반환하고 있는데, 반환된 튜플을 다시 개별 부분으로 분리하고 있다. 이는 아직 적절한 추상화를 하지 못했다는 신호일 수 있다.

또 다른 개선의 여지가 있다는 것을 보여주는 지표는 `parse_config` 함수의 `config` 부분이다. 이는 우리가 반환하는 두 값이 서로 관련이 있으며 하나의 설정 값의 일부라는 것을 암시한다. 현재는 이 두 값을 튜플로 묶는 것 외에는 데이터 구조에서 이러한 의미를 전달하지 않고 있다. 대신, 이 두 값을 하나의 구조체에 넣고 각 필드에 의미 있는 이름을 부여할 것이다. 이렇게 하면 향후 이 코드를 유지보수하는 사람들이 서로 다른 값들이 어떻게 관련되어 있는지, 그리고 그 목적이 무엇인지 더 쉽게 이해할 수 있다.

Listing 12-6은 `parse_config` 함수를 개선한 결과를 보여준다.

<Listing number="12-6" file-name="src/main.rs" caption="`parse_config` 함수를 리팩토링하여 `Config` 구조체의 인스턴스를 반환">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-06/src/main.rs:here}}
```

</Listing>

`query`와 `file_path`라는 필드를 가진 `Config` 구조체를 추가했다. 이제 `parse_config` 함수의 시그니처는 `Config` 값을 반환한다는 것을 나타낸다. `parse_config` 함수의 본문에서는 이전에 `args`의 `String` 값을 참조하는 문자열 슬라이스를 반환했던 부분을 `Config`가 소유한 `String` 값을 포함하도록 변경했다. `main` 함수의 `args` 변수는 인자 값의 소유자이며, `parse_config` 함수가 이를 빌려 쓰도록 허용하고 있다. 따라서 `Config`가 `args`의 값을 소유하려고 하면 Rust의 빌림 규칙을 위반하게 된다.

`String` 데이터를 관리하는 방법에는 여러 가지가 있지만, 가장 간단한 방법은 값에 `clone` 메서드를 호출하는 것이다. 이는 데이터의 전체 복사본을 만들어 `Config` 인스턴스가 소유하도록 하기 때문에, 문자열 데이터에 대한 참조를 저장하는 것보다 더 많은 시간과 메모리를 소비한다. 그러나 데이터를 복제하면 참조의 수명을 관리할 필요가 없기 때문에 코드가 매우 직관적이 된다. 이러한 상황에서는 약간의 성능을 포기하고 단순함을 얻는 것이 가치 있는 절충안이다.

> ### `clone` 사용의 절충점
>
> 많은 Rust 개발자들은 런타임 비용 때문에 `clone`을 사용하여 소유권 문제를 해결하는 것을 피하려는 경향이 있다. [13장][ch13]<!-- ignore -->에서는 이러한 상황에서 더 효율적인 방법을 사용하는 법을 배울 것이다. 하지만 지금은 몇 개의 문자열을 복사하여 진행하는 것이 괜찮다. 이러한 복사는 한 번만 이루어지며, 파일 경로와 쿼리 문자열은 매우 작기 때문이다. 처음부터 코드를 과도하게 최적화하려고 하는 것보다, 조금 비효율적이지만 동작하는 프로그램을 갖는 것이 더 낫다. Rust에 더 익숙해지면 가장 효율적인 해결책부터 시작하는 것이 더 쉬워지겠지만, 지금은 `clone`을 호출하는 것이 완벽하게 허용된다.

`main` 함수를 업데이트하여 `parse_config`가 반환한 `Config` 인스턴스를 `config`라는 변수에 저장하도록 했다. 이전에 `query`와 `file_path`라는 별도의 변수를 사용했던 코드도 이제 `Config` 구조체의 필드를 사용하도록 업데이트했다.

이제 우리 코드는 `query`와 `file_path`가 서로 관련이 있으며, 프로그램이 어떻게 동작할지를 설정하는 데 사용된다는 것을 더 명확히 전달한다. 이 값을 사용하는 모든 코드는 그 목적에 맞게 명명된 필드에서 `config` 인스턴스 안에 있음을 알 수 있다.


#### `Config` 생성자 만들기

지금까지 `main` 함수에서 커맨드라인 인자를 파싱하는 로직을 추출해 `parse_config` 함수로 옮겼다. 이를 통해 `query`와 `file_path` 값이 서로 관련이 있다는 점을 명확히 확인했고, 코드에서 이 관계를 표현할 필요가 있었다. 이후 `Config` 구조체를 추가해 `query`와 `file_path`의 관련성을 명시하고, `parse_config` 함수에서 이 값들의 이름을 구조체 필드 이름으로 반환할 수 있게 했다.

이제 `parse_config` 함수의 목적이 `Config` 인스턴스를 생성하는 것이므로, `parse_config`를 일반 함수에서 `Config` 구조체와 연관된 `new` 함수로 변경할 수 있다. 이렇게 변경하면 코드가 더 관용적으로 변한다. 표준 라이브러리에서 `String` 같은 타입의 인스턴스를 생성할 때 `String::new`를 호출하는 것과 마찬가지로, `parse_config`를 `Config`와 연관된 `new` 함수로 변경하면 `Config::new`를 호출해 `Config` 인스턴스를 생성할 수 있다. 아래 코드는 필요한 변경 사항을 보여준다.

<Listing number="12-7" file-name="src/main.rs" caption="`parse_config`를 `Config::new`로 변경">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-07/src/main.rs:here}}
```

</Listing>

이제 `main` 함수에서 `parse_config`를 호출하던 부분을 `Config::new`로 변경했다. `parse_config`의 이름을 `new`로 바꾸고, `impl` 블록 안으로 옮겨 `new` 함수를 `Config`와 연관시켰다. 이 코드를 다시 컴파일해 동작을 확인해 보자.


### 에러 처리 개선

이제 에러 처리를 개선해 보자. `args` 벡터에 인덱스 1이나 2에 접근하려고 할 때, 벡터에 세 개 미만의 항목이 있으면 프로그램이 패닉 상태에 빠진다. 아무런 인자 없이 프로그램을 실행해 보면 다음과 같은 결과가 나타난다:

```console
{{#include ../listings/ch12-an-io-project/listing-12-07/output.txt}}
```

`index out of bounds: the len is 1 but the index is 1`라는 메시지는 프로그래머를 위한 에러 메시지다. 이는 최종 사용자가 무엇을 해야 하는지 이해하는 데 도움이 되지 않는다. 이제 이를 수정해 보자.


#### 에러 메시지 개선

리스트 12-8에서는 `new` 함수에 인덱스 1과 2에 접근하기 전에 슬라이스가 충분히 긴지 확인하는 검사를 추가한다. 슬라이스가 충분히 길지 않으면 프로그램이 패닉 상태에 빠지고 더 나은 에러 메시지를 표시한다.

<Listing number="12-8" file-name="src/main.rs" caption="인수 개수 확인 추가">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-08/src/main.rs:here}}
```

</Listing>

이 코드는 [리스트 9-13][ch9-custom-types]<!-- ignore -->에서 작성한 `Guess::new` 함수와 유사하다. `value` 인자가 유효한 값 범위를 벗어날 때 `panic!`을 호출했다. 여기서는 값의 범위를 확인하는 대신 `args`의 길이가 최소 `3`인지 확인하고, 함수의 나머지 부분은 이 조건이 충족되었다는 가정 하에 동작한다. `args`에 세 개 미만의 항목이 있으면 이 조건이 `true`가 되고, `panic!` 매크로를 호출해 프로그램을 즉시 종료한다.

`new` 함수에 이 몇 줄의 코드를 추가한 후, 다시 아무런 인수 없이 프로그램을 실행해 에러가 어떻게 표시되는지 확인해 보자:

```console
{{#include ../listings/ch12-an-io-project/listing-12-08/output.txt}}
```

이 출력은 더 나아졌다. 이제는 합리적인 에러 메시지를 제공한다. 하지만 여전히 사용자에게 제공하고 싶지 않은 불필요한 정보도 포함되어 있다. 리스트 9-13에서 사용한 기법이 여기서는 최선의 선택이 아닐 수 있다. `panic!` 호출은 사용법 문제보다는 프로그래밍 문제에 더 적합하다. [9장에서 논의한 것처럼][ch9-error-guidelines]<!-- ignore -->, 대신 9장에서 배운 다른 기법인 [성공 또는 에러를 나타내는 `Result` 반환][ch9-result]<!-- ignore -->을 사용할 것이다.

<!-- 이전 헤딩. 제거하지 마세요. 링크가 깨질 수 있습니다. -->

<a id="returning-a-result-from-new-instead-of-calling-panic"></a>


#### `panic!` 호출 대신 `Result` 반환하기

`Config` 인스턴스를 성공적으로 생성한 경우에는 `Config` 인스턴스를 포함하고, 오류가 발생한 경우에는 문제를 설명하는 `Result` 값을 반환할 수 있다. 또한 함수 이름을 `new`에서 `build`로 변경한다. 많은 프로그래머들이 `new` 함수가 실패하지 않을 것이라고 기대하기 때문이다. `Config::build`가 `main`과 통신할 때, `Result` 타입을 사용해 문제가 발생했음을 알릴 수 있다. 그런 다음 `main`을 수정해 `Err` 변형을 사용자에게 더 실용적인 오류로 변환할 수 있다. 이렇게 하면 `panic!` 호출로 인해 발생하는 `thread 'main'`과 `RUST_BACKTRACE`와 같은 텍스트를 제거할 수 있다.

목록 12-9는 이제 `Config::build`라고 부르는 함수의 반환 값과 `Result`를 반환하기 위해 필요한 함수 본문의 변경 사항을 보여준다. 참고로 이 코드는 `main`을 업데이트할 때까지 컴파일되지 않는다. 이 작업은 다음 목록에서 진행할 것이다.

<Listing number="12-9" file-name="src/main.rs" caption="`Config::build`에서 `Result` 반환하기">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-09/src/main.rs:here}}
```

</Listing>

`build` 함수는 성공한 경우 `Config` 인스턴스를, 오류가 발생한 경우 문자열 리터럴을 포함한 `Result`를 반환한다. 오류 값은 항상 `'static` 라이프타임을 가진 문자열 리터럴이다.

함수 본문에서 두 가지 변경 사항을 적용했다. 사용자가 충분한 인수를 전달하지 않았을 때 `panic!`을 호출하는 대신, 이제는 `Err` 값을 반환한다. 또한 `Config` 반환 값을 `Ok`로 감쌌다. 이러한 변경 사항은 함수가 새로운 타입 시그니처를 따르도록 만든다.

`Config::build`에서 `Err` 값을 반환하면 `main` 함수가 `build` 함수에서 반환된 `Result` 값을 처리하고, 오류가 발생한 경우 프로세스를 더 깔끔하게 종료할 수 있다.

<!-- Old headings. Do not remove or links may break. -->

<a id="calling-confignew-and-handling-errors"></a>


#### `Config::build` 호출 및 에러 처리

에러 케이스를 처리하고 사용자 친화적인 메시지를 출력하려면 `main` 함수를 업데이트해야 한다. `Config::build`가 반환하는 `Result`를 처리하는 방식은 Listing 12-10에서 확인할 수 있다. 또한, `panic!`을 통해 명령줄 도구를 0이 아닌 에러 코드로 종료하는 책임을 제거하고, 직접 구현할 것이다. 0이 아닌 종료 상태는 프로그램이 에러 상태로 종료되었음을 호출한 프로세스에게 알리는 관례적인 방법이다.

<Listing number="12-10" file-name="src/main.rs" caption="`Config` 생성 실패 시 에러 코드로 종료">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-10/src/main.rs:here}}
```

</Listing>

이 예제에서는 아직 자세히 다루지 않은 메서드인 `unwrap_or_else`를 사용한다. 이 메서드는 표준 라이브러리에서 `Result<T, E>`에 정의되어 있다. `unwrap_or_else`를 사용하면 `panic!`이 아닌 커스텀 에러 처리를 정의할 수 있다. `Result`가 `Ok` 값인 경우, 이 메서드는 `unwrap`과 유사하게 동작한다. 즉, `Ok`가 감싸고 있는 내부 값을 반환한다. 그러나 값이 `Err`인 경우, 이 메서드는 *클로저* 내의 코드를 호출한다. 클로저는 익명 함수로, `unwrap_or_else`에 인자로 전달된다. 클로저에 대한 자세한 내용은 [13장][ch13]<!-- ignore -->에서 다룰 것이다. 지금은 `unwrap_or_else`가 `Err`의 내부 값을 클로저의 인자 `err`로 전달한다는 점만 이해하면 된다. 여기서 `err`는 Listing 12-9에서 추가한 정적 문자열 `"not enough arguments"`가 된다. 클로저 내의 코드는 실행 시 `err` 값을 사용할 수 있다.

새로운 `use` 라인을 추가해 표준 라이브러리의 `process`를 스코프로 가져왔다. 에러 케이스에서 실행될 클로저 내의 코드는 단 두 줄이다. `err` 값을 출력한 다음 `process::exit`를 호출한다. `process::exit` 함수는 프로그램을 즉시 중단하고 전달된 숫자를 종료 상태 코드로 반환한다. 이는 Listing 12-8에서 사용한 `panic!` 기반의 처리와 유사하지만, 불필요한 출력이 더 이상 발생하지 않는다. 이제 이를 실행해 보자:

```console
{{#include ../listings/ch12-an-io-project/listing-12-10/output.txt}}
```

좋다! 이 출력은 사용자에게 훨씬 더 친절하다.


### `main` 함수에서 로직 분리하기

이제 설정 파싱 부분을 리팩토링했으니, 프로그램의 주요 로직으로 넘어가보자. 앞서 [“바이너리 프로젝트의 관심사 분리”](#separation-of-concerns-for-binary-projects)<!-- ignore -->에서 언급했듯이, `main` 함수에서 설정과 오류 처리와 관련 없는 모든 로직을 담을 `run` 함수를 추출할 것이다. 이 작업을 마치면 `main` 함수는 간결해지고, 코드를 눈으로 확인하기 쉬워지며, 나머지 로직에 대한 테스트를 작성할 수 있게 된다.

리스트 12-11은 추출된 `run` 함수를 보여준다. 지금은 함수를 추출하는 작은 단계적 개선만 진행한다. 여전히 이 함수를 _src/main.rs_ 파일에 정의한다.

<리스트 번호="12-11" 파일명="src/main.rs" 설명="프로그램의 나머지 로직을 담은 `run` 함수 추출">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-11/src/main.rs:here}}
```

</리스트>

`run` 함수는 이제 파일 읽기부터 시작해 `main` 함수의 나머지 모든 로직을 포함한다. `run` 함수는 `Config` 인스턴스를 인자로 받는다.


#### `run` 함수에서 에러 반환하기

`run` 함수로 분리된 나머지 프로그램 로직에서 에러 처리를 개선할 수 있다. 이는 `Config::build`에서 했던 것과 유사하다. `expect`를 호출해 프로그램이 패닉 상태에 빠지도록 두는 대신, `run` 함수는 문제가 발생했을 때 `Result<T, E>`를 반환한다. 이를 통해 에러 처리 로직을 `main` 함수에 통합해 사용자 친화적인 방식으로 처리할 수 있다. 목록 12-12는 `run` 함수의 시그니처와 본문에 필요한 변경 사항을 보여준다.

<Listing number="12-12" file-name="src/main.rs" caption="`run` 함수가 `Result`를 반환하도록 변경">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-12/src/main.rs:here}}
```

</Listing>

여기서 세 가지 주요 변경 사항을 적용했다. 첫째, `run` 함수의 반환 타입을 `Result<(), Box<dyn Error>>`로 변경했다. 이 함수는 이전에 유닛 타입 `()`을 반환했으며, `Ok` 케이스에서도 동일한 값을 반환하도록 유지했다.

에러 타입으로는 _트레잇 객체_ `Box<dyn Error>`를 사용했다. (상단에 `use` 구문을 통해 `std::error::Error`를 스코프로 가져왔다.) 트레잇 객체는 [18장][ch18]에서 다룬다. 지금은 `Box<dyn Error>`가 `Error` 트레잇을 구현하는 타입을 반환한다는 점만 이해하면 된다. 이렇게 하면 다양한 에러 케이스에서 서로 다른 타입의 에러 값을 반환할 수 있는 유연성을 얻는다. `dyn` 키워드는 _동적_을 의미한다.

둘째, `expect` 호출을 제거하고 `?` 연산자로 대체했다. 이는 [9장][ch9-question-mark]에서 다룬 내용이다. 에러가 발생했을 때 `panic!`을 일으키는 대신, `?`는 현재 함수에서 에러 값을 반환해 호출자가 처리하도록 한다.

셋째, `run` 함수는 이제 성공 시 `Ok` 값을 반환한다. `run` 함수의 성공 타입을 시그니처에서 `()`로 선언했기 때문에, 유닛 타입 값을 `Ok` 값으로 감싸야 한다. `Ok(())` 구문은 처음 보면 조금 이상해 보일 수 있지만, 이렇게 `()`를 사용하는 것은 `run` 함수를 부수 효과만을 위해 호출한다는 것을 나타내는 관용적인 방법이다. 즉, 반환할 값이 필요하지 않다는 의미다.

이 코드를 실행하면 컴파일은 되지만 경고 메시지가 표시된다:

```console
{{#include ../listings/ch12-an-io-project/listing-12-12/output.txt}}
```

러스트는 코드가 `Result` 값을 무시했으며, `Result` 값이 에러가 발생했음을 나타낼 수 있다고 알려준다. 하지만 우리는 에러가 발생했는지 확인하지 않았고, 컴파일러는 여기에 에러 처리 코드가 필요하다고 알려준다. 이제 이 문제를 해결해보자.


#### `run` 함수에서 반환된 오류를 `main`에서 처리하기

`run` 함수에서 반환된 오류를 확인하고 처리하기 위해, 목록 12-10에서 `Config::build`를 사용했던 방식과 유사한 기법을 사용한다. 하지만 약간의 차이가 있다:

<span class="filename">파일명: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/no-listing-01-handling-errors-in-main/src/main.rs:here}}
```

여기서는 `unwrap_or_else` 대신 `if let`을 사용하여 `run` 함수가 `Err` 값을 반환하는지 확인한다. 만약 오류가 발생하면 `process::exit(1)`을 호출한다. `run` 함수는 `Config::build`가 `Config` 인스턴스를 반환하는 것과 달리, `unwrap`할 값을 반환하지 않는다. 성공 시 `run` 함수는 `()`를 반환하므로, 오류를 감지하는 것만 중요하다. 따라서 `unwrap_or_else`를 사용해 `()`와 같은 값을 반환할 필요가 없다.

`if let`과 `unwrap_or_else` 함수의 본문은 두 경우 모두 동일하다: 오류를 출력하고 프로그램을 종료한다.


### 코드를 라이브러리 크레이트로 분리하기

지금까지 `minigrep` 프로젝트가 잘 진행되고 있다! 이제 _src/main.rs_ 파일을 분리하고 일부 코드를 _src/lib.rs_ 파일로 옮길 것이다. 이렇게 하면 코드를 테스트할 수 있고, _src/main.rs_ 파일의 책임을 줄일 수 있다.

_src/main.rs_에서 `main` 함수에 속하지 않은 모든 코드를 _src/lib.rs_로 옮겨보자:

- `run` 함수 정의
- 관련된 `use` 문
- `Config` 정의
- `Config::build` 함수 정의

_src/lib.rs_의 내용은 Listing 12-13에 나온 시그니처를 따라야 한다(간결함을 위해 함수 본문은 생략했다). 이 코드는 Listing 12-14에서 _src/main.rs_를 수정할 때까지 컴파일되지 않을 것이다.

<Listing number="12-13" file-name="src/lib.rs" caption="`Config`와 `run`을 *src/lib.rs*로 이동">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-13/src/lib.rs:here}}
```

</Listing>

`pub` 키워드를 적극적으로 사용했다: `Config`, 그 필드와 `build` 메서드, 그리고 `run` 함수에 적용했다. 이제 테스트할 수 있는 공개 API를 가진 라이브러리 크레이트가 생겼다!

이제 _src/lib.rs_로 옮긴 코드를 _src/main.rs_의 바이너리 크레이트 범위로 가져와야 한다. Listing 12-14에서 보여주는 것처럼 말이다.

<Listing number="12-14" file-name="src/main.rs" caption="*src/main.rs*에서 `minigrep` 라이브러리 크레이트 사용">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-14/src/main.rs:here}}
```

</Listing>

`use minigrep::Config` 라인을 추가해 라이브러리 크레이트의 `Config` 타입을 바이너리 크레이트의 범위로 가져왔다. 그리고 `run` 함수 앞에 크레이트 이름을 붙였다. 이제 모든 기능이 연결되어 제대로 작동할 것이다. `cargo run`으로 프로그램을 실행해 모든 것이 정상적으로 동작하는지 확인하자.

휴! 많은 작업이었지만, 앞으로의 성공을 위한 기반을 다졌다. 이제 에러 처리가 훨씬 쉬워졌고, 코드도 더 모듈화되었다. 이제부터는 거의 모든 작업을 _src/lib.rs_에서 진행할 것이다.

이 새로운 모듈성의 장점을 활용해 보자. 이전 코드로는 어려웠지만, 새로운 코드로는 쉬운 작업을 해보자: 테스트를 작성해 보는 것이다!

[ch13]: ch13-00-functional-features.html
[ch9-custom-types]: ch09-03-to-panic-or-not-to-panic.html#creating-custom-types-for-validation
[ch9-error-guidelines]: ch09-03-to-panic-or-not-to-panic.html#guidelines-for-error-handling
[ch9-result]: ch09-02-recoverable-errors-with-result.html
[ch18]: ch18-00-oop.html
[ch9-question-mark]: ch09-02-recoverable-errors-with-result.html#a-shortcut-for-propagating-errors-the--operator


