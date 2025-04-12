## 환경 변수 활용하기

`minigrep`에 새로운 기능을 추가해 보자. 사용자가 환경 변수를 통해 대소문자 구분 없는 검색 옵션을 활성화할 수 있도록 하는 기능이다. 이 기능을 커맨드라인 옵션으로 만들 수도 있지만, 환경 변수로 구현하면 사용자가 한 번 설정한 후 해당 터미널 세션에서는 모든 검색이 대소문자 구분 없이 이루어지도록 할 수 있다.


### 대소문자를 구분하지 않는 `search` 함수를 위한 실패 테스트 작성

먼저, 환경 변수에 값이 있을 때 호출될 새로운 `search_case_insensitive` 함수를 추가한다. 우리는 TDD(Test-Driven Development) 프로세스를 계속 따르기 때문에 첫 번째 단계는 다시 실패하는 테스트를 작성하는 것이다. 새로운 `search_case_insensitive` 함수를 위한 테스트를 추가하고, 기존 테스트의 이름을 `one_result`에서 `case_sensitive`로 변경하여 두 테스트의 차이를 명확히 한다. 이는 리스트 12-20에서 확인할 수 있다.

<Listing number="12-20" file-name="src/lib.rs" caption="추가할 대소문자를 구분하지 않는 함수를 위한 새로운 실패 테스트 추가">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-20/src/lib.rs:here}}
```

</Listing>

기존 테스트의 `contents`도 수정했다. 대문자 _D_를 사용한 `"Duct tape."`라는 새 줄을 추가했는데, 이는 대소문자를 구분하는 방식으로 검색할 때 `"duct"`라는 쿼리와 일치하지 않아야 한다. 이렇게 기존 테스트를 변경하면 이미 구현한 대소문자 구분 검색 기능을 실수로 깨뜨리지 않도록 보장할 수 있다. 이 테스트는 지금 통과해야 하며, 대소문자를 구분하지 않는 검색 기능을 작업하는 동안에도 계속 통과해야 한다.

대소문자를 _구분하지 않는_ 검색을 위한 새 테스트는 `"rUsT"`를 쿼리로 사용한다. 곧 추가할 `search_case_insensitive` 함수에서 `"rUsT"`라는 쿼리는 대문자 _R_이 포함된 `"Rust:"` 줄과 쿼리와 대소문자가 다른 `"Trust me."` 줄 모두와 일치해야 한다. 이는 실패하는 테스트이며, 아직 `search_case_insensitive` 함수를 정의하지 않았기 때문에 컴파일되지 않을 것이다. 리스트 12-16에서 `search` 함수를 위해 했던 것처럼 항상 빈 벡터를 반환하는 기본 구현을 추가하여 테스트가 컴파일되고 실패하는 것을 확인해도 좋다.


### `search_case_insensitive` 함수 구현하기

`search_case_insensitive` 함수는 `search` 함수와 거의 동일하다. 유일한 차이점은 `query`와 각 `line`을 소문자로 변환한다는 점이다. 이를 통해 입력 인자의 대소문자와 상관없이 동일한 대소문자로 비교할 수 있다.

<Listing number="12-21" file-name="src/lib.rs" caption="`search_case_insensitive` 함수를 정의하여 `query`와 `line`을 소문자로 변환한 후 비교하기">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-21/src/lib.rs:here}}
```

</Listing>

먼저 `query` 문자열을 소문자로 변환하고, 동일한 이름의 새로운 변수에 저장한다. 이렇게 하면 원본 `query`가 가려진다. `query`에 `to_lowercase`를 호출하면 사용자의 쿼리가 `"rust"`, `"RUST"`, `"Rust"`, `"rUsT"` 중 어떤 것이든 `"rust"`로 처리되어 대소문자를 구분하지 않는다. `to_lowercase`는 기본적인 유니코드를 처리하지만 100% 정확하지는 않다. 실제 애플리케이션을 작성한다면 여기에 더 많은 작업이 필요하지만, 이 섹션은 유니코드가 아니라 환경 변수에 관한 내용이므로 여기서는 이 정도로 마무리한다.

`query`는 이제 문자열 슬라이스가 아니라 `String` 타입이다. `to_lowercase`를 호출하면 기존 데이터를 참조하는 대신 새로운 데이터를 생성하기 때문이다. 예를 들어 쿼리가 `"rUsT"`라면, 이 문자열 슬라이스에는 소문자 `u`나 `t`가 포함되어 있지 않으므로 `"rust"`를 포함하는 새로운 `String`을 할당해야 한다. 이제 `query`를 `contains` 메서드의 인자로 전달할 때 앰퍼샌드(&)를 추가해야 한다. `contains` 메서드의 시그니처는 문자열 슬라이스를 인자로 받도록 정의되어 있기 때문이다.

다음으로, 각 `line`에 `to_lowercase`를 호출하여 모든 문자를 소문자로 변환한다. 이제 `line`과 `query`를 소문자로 변환했으므로, 쿼리의 대소문자와 상관없이 일치하는 항목을 찾을 수 있다.

이 구현이 테스트를 통과하는지 확인해 보자:

```console
{{#include ../listings/ch12-an-io-project/listing-12-21/output.txt}}
```

좋다! 테스트를 통과했다. 이제 `run` 함수에서 새로운 `search_case_insensitive` 함수를 호출해 보자. 먼저 `Config` 구조체에 대소문자 구분 여부를 설정할 수 있는 옵션을 추가한다. 이 필드를 추가하면 아직 초기화하지 않았기 때문에 컴파일러 오류가 발생한다:

<span class="filename">Filename: src/lib.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/lib.rs:here}}
```

`ignore_case` 필드를 추가하여 Boolean 값을 저장한다. 다음으로, `run` 함수가 `ignore_case` 필드의 값을 확인하고, 그에 따라 `search` 함수를 호출할지 `search_case_insensitive` 함수를 호출할지 결정하도록 한다. 이 코드는 아직 컴파일되지 않는다.

<Listing number="12-22" file-name="src/lib.rs" caption="`config.ignore_case`의 값에 따라 `search` 또는 `search_case_insensitive` 호출하기">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/lib.rs:there}}
```

</Listing>

마지막으로, 환경 변수를 확인해야 한다. 환경 변수를 다루는 함수는 표준 라이브러리의 `env` 모듈에 있으므로, _src/lib.rs_ 파일 상단에서 이 모듈을 가져온다. 그런 다음 `env` 모듈의 `var` 함수를 사용하여 `IGNORE_CASE`라는 환경 변수가 설정되었는지 확인한다.

<Listing number="12-23" file-name="src/lib.rs" caption="`IGNORE_CASE`라는 환경 변수의 값 확인하기">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-23/src/lib.rs:here}}
```

</Listing>

여기서 `ignore_case`라는 새로운 변수를 생성한다. 이 변수의 값을 설정하기 위해 `env::var` 함수를 호출하고 `IGNORE_CASE` 환경 변수의 이름을 전달한다. `env::var` 함수는 `Result`를 반환한다. 환경 변수가 설정되어 있으면 `Ok` 변형에 환경 변수의 값이 포함된다. 환경 변수가 설정되어 있지 않으면 `Err` 변형이 반환된다.

`Result`의 `is_ok` 메서드를 사용하여 환경 변수가 설정되었는지 확인한다. 이는 프로그램이 대소문자를 구분하지 않는 검색을 수행해야 함을 의미한다. `IGNORE_CASE` 환경 변수가 설정되어 있지 않으면 `is_ok`는 `false`를 반환하고 프로그램은 대소문자를 구분하는 검색을 수행한다. 환경 변수의 _값_이 아니라 설정 여부만 중요하므로 `unwrap`, `expect` 또는 `Result`에서 본 다른 메서드를 사용하는 대신 `is_ok`를 확인한다.

`ignore_case` 변수의 값을 `Config` 인스턴스에 전달하여 `run` 함수가 이 값을 읽고 `search_case_insensitive`를 호출할지 `search`를 호출할지 결정할 수 있도록 한다.

한번 시도해 보자! 먼저 환경 변수를 설정하지 않고 쿼리 `to`로 프로그램을 실행한다. 이는 소문자로 _to_가 포함된 모든 줄과 일치해야 한다:

```console
{{#include ../listings/ch12-an-io-project/listing-12-23/output.txt}}
```

여전히 잘 작동한다! 이제 `IGNORE_CASE`를 `1`로 설정하고 동일한 쿼리 _to_로 프로그램을 실행해 보자:

```console
$ IGNORE_CASE=1 cargo run -- to poem.txt
```

PowerShell을 사용하는 경우 환경 변수를 설정하고 프로그램을 별도의 명령어로 실행해야 한다:

```console
PS> $Env:IGNORE_CASE=1; cargo run -- to poem.txt
```

이렇게 하면 `IGNORE_CASE`가 현재 셸 세션의 나머지 기간 동안 유지된다. `Remove-Item` cmdlet으로 이를 해제할 수 있다:

```console
PS> Remove-Item Env:IGNORE_CASE
```

대문자가 포함된 _to_가 있는 줄도 결과에 포함되어야 한다:

<!-- manual-regeneration
cd listings/ch12-an-io-project/listing-12-23
IGNORE_CASE=1 cargo run -- to poem.txt
can't extract because of the environment variable
-->

```console
Are you nobody, too?
How dreary to be somebody!
To tell your name the livelong day
To an admiring bog!
```

훌륭하다! _To_가 포함된 줄도 결과에 포함되었다. 이제 `minigrep` 프로그램은 환경 변수로 제어되는 대소문자 구분 없는 검색을 수행할 수 있다. 이제 커맨드라인 인수나 환경 변수를 사용하여 설정된 옵션을 관리하는 방법을 알게 되었다.

일부 프로그램은 동일한 설정에 대해 인수와 환경 변수를 모두 허용한다. 이러한 경우 프로그램은 둘 중 하나가 우선순위를 갖도록 결정한다. 추가 연습으로, 커맨드라인 인수나 환경 변수를 통해 대소문자 구분을 제어해 보자. 프로그램이 대소문자 구분과 무시 중 하나로 실행될 때, 커맨드라인 인수와 환경 변수 중 어느 것이 우선순위를 가져야 할지 결정해 보자.

`std::env` 모듈에는 환경 변수를 다루기 위한 더 많은 유용한 기능이 있다. 사용 가능한 기능을 확인하려면 해당 문서를 참고하라.


