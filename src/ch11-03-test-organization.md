## 테스트 조직화

이 장의 시작 부분에서 언급했듯이, 테스트는 복잡한 분야이며 사람마다 사용하는 용어와 조직화 방식이 다르다. Rust 커뮤니티는 테스트를 크게 두 가지 범주로 나누어 생각한다: 단위 테스트와 통합 테스트. **단위 테스트**는 작고 집중적이며, 한 번에 하나의 모듈을 독립적으로 테스트하고, 비공개 인터페이스도 테스트할 수 있다. **통합 테스트**는 라이브러리 외부에서 이루어지며, 다른 외부 코드가 사용하는 방식과 동일하게 코드를 사용한다. 통합 테스트는 공개 인터페이스만을 사용하며, 하나의 테스트에서 여러 모듈을 동시에 테스트할 수도 있다.

두 종류의 테스트를 모두 작성하는 것은 라이브러리의 각 부분이 개별적으로 그리고 함께 작동할 때 기대한 대로 동작하는지 확인하는 데 중요하다.


### 유닛 테스트

유닛 테스트의 목적은 코드의 각 단위를 독립적으로 테스트하여 예상대로 작동하는지 여부를 빠르게 파악하는 것이다. 유닛 테스트는 테스트 대상 코드가 있는 파일과 동일한 _src_ 디렉토리에 위치시킨다. 일반적인 관례는 각 파일에 `tests`라는 모듈을 만들어 테스트 함수를 포함시키고, 이 모듈에 `cfg(test)`를 어노테이션으로 추가하는 것이다.


#### 테스트 모듈과 `#[cfg(test)]`

`tests` 모듈에 있는 `#[cfg(test)]` 어노테이션은 `cargo test`를 실행할 때만 테스트 코드를 컴파일하고 실행하도록 Rust에 지시한다. `cargo build`를 실행할 때는 테스트 코드가 포함되지 않는다. 이렇게 하면 라이브러리만 빌드하고자 할 때 컴파일 시간을 절약할 수 있으며, 테스트 코드가 포함되지 않기 때문에 최종 컴파일 결과물의 크기도 줄어든다. 통합 테스트는 별도의 디렉터리에 위치하기 때문에 `#[cfg(test)]` 어노테이션이 필요하지 않다. 반면, 단위 테스트는 코드와 같은 파일에 위치하기 때문에 `#[cfg(test)]`를 사용해 컴파일 결과에 포함되지 않도록 지정해야 한다.

이 장의 첫 번째 섹션에서 새로운 `adder` 프로젝트를 생성했을 때, Cargo가 자동으로 생성한 코드를 다시 살펴보자:

<span class="filename">파일명: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

자동으로 생성된 `tests` 모듈에서 `cfg` 속성은 _configuration_을 의미하며, 특정 구성 옵션이 주어졌을 때만 다음 항목을 포함하도록 Rust에 지시한다. 이 경우 구성 옵션은 `test`이며, Rust가 테스트를 컴파일하고 실행하기 위해 제공한다. `cfg` 속성을 사용하면 `cargo test`로 테스트를 실행할 때만 테스트 코드를 컴파일한다. 이는 `#[test]`로 어노테이션된 함수뿐만 아니라 이 모듈 내에 있는 모든 헬퍼 함수도 포함한다.


#### 비공개 함수 테스트

테스트 커뮤니티에서는 비공개 함수를 직접 테스트해야 하는지에 대한 논쟁이 있다. 다른 프로그래밍 언어에서는 비공개 함수를 테스트하기 어렵거나 불가능한 경우가 많다. 그러나 Rust의 접근 제어 규칙은 비공개 함수도 테스트할 수 있도록 허용한다. 비공개 함수 `internal_adder`를 포함한 Listing 11-12의 코드를 살펴보자.

<Listing number="11-12" file-name="src/lib.rs" caption="비공개 함수 테스트">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-12/src/lib.rs}}
```

</Listing>

`internal_adder` 함수는 `pub`으로 표시되지 않았다. 테스트는 단순히 Rust 코드이며, `tests` 모듈은 또 다른 모듈일 뿐이다. [“모듈 트리에서 항목 참조하기”][paths]<!-- ignore -->에서 논의한 바와 같이, 자식 모듈의 항목은 상위 모듈의 항목을 사용할 수 있다. 이 테스트에서는 `use super::*`를 통해 `tests` 모듈의 상위 모듈 항목을 스코프로 가져오고, `internal_adder`를 호출할 수 있다. 비공개 함수를 테스트하지 않으려는 경우, Rust는 이를 강제하지 않는다.


### 통합 테스트

Rust에서 통합 테스트는 라이브러리 외부에 완전히 분리되어 있다. 통합 테스트는 다른 코드와 마찬가지로 라이브러리를 사용하며, 이는 라이브러리의 공개 API에 속한 함수만 호출할 수 있다는 의미다. 통합 테스트의 목적은 라이브러리의 여러 부분이 올바르게 함께 작동하는지 확인하는 것이다. 각각의 코드 단위가 독립적으로는 정상적으로 작동하더라도 통합 시 문제가 발생할 수 있으므로, 통합된 코드에 대한 테스트 커버리지도 중요하다. 통합 테스트를 생성하려면 먼저 _tests_ 디렉토리가 필요하다.


#### _tests_ 디렉토리

프로젝트 디렉토리의 최상위 레벨에 _src_ 디렉토리 옆에 _tests_ 디렉토리를 만든다. Cargo는 이 디렉토리에서 통합 테스트 파일을 찾는다. 필요한 만큼 테스트 파일을 만들 수 있으며, Cargo는 각 파일을 개별 크레이트로 컴파일한다.

통합 테스트를 만들어 보자. _src/lib.rs_ 파일에 있는 코드를 그대로 유지한 상태에서 _tests_ 디렉토리를 만들고, _tests/integration_test.rs_ 파일을 생성한다. 디렉토리 구조는 다음과 같아야 한다:

```text
adder
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    └── integration_test.rs
```

_tests/integration_test.rs_ 파일에 다음 코드를 입력한다.

<Listing number="11-13" file-name="tests/integration_test.rs" caption="`adder` 크레이트의 함수를 테스트하는 통합 테스트">

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-13/tests/integration_test.rs}}
```

</Listing>

_tests_ 디렉토리의 각 파일은 별도의 크레이트이므로, 라이브러리를 각 테스트 크레이트의 스코프로 가져와야 한다. 그래서 코드 상단에 `use adder::add_two;`를 추가한다. 이 과정은 단위 테스트에서는 필요하지 않다.

_tests/integration_test.rs_ 파일의 코드에 `#[cfg(test)]`를 붙일 필요는 없다. Cargo는 _tests_ 디렉토리를 특별히 취급하며, `cargo test`를 실행할 때만 이 디렉토리의 파일을 컴파일한다. 이제 `cargo test`를 실행해 보자:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-13/output.txt}}
```

출력 결과는 세 부분으로 나뉜다: 단위 테스트, 통합 테스트, 문서 테스트. 한 섹션의 테스트가 실패하면 다음 섹션은 실행되지 않는다. 예를 들어, 단위 테스트가 실패하면 통합 테스트와 문서 테스트는 실행되지 않는다.

단위 테스트 섹션의 첫 부분은 이전과 동일하다: 각 단위 테스트에 대한 한 줄(Listing 11-12에서 추가한 `internal` 테스트)과 단위 테스트 결과 요약 줄이 표시된다.

통합 테스트 섹션은 `Running tests/integration_test.rs` 줄로 시작한다. 그 다음에는 통합 테스트 파일의 각 테스트 함수에 대한 줄과 통합 테스트 결과 요약 줄이 표시된다. 그 후 `Doc-tests adder` 섹션이 시작된다.

각 통합 테스트 파일은 별도의 섹션을 가지므로, _tests_ 디렉토리에 더 많은 파일을 추가하면 통합 테스트 섹션도 늘어난다.

특정 통합 테스트 함수만 실행하려면 `cargo test`에 테스트 함수 이름을 인자로 전달한다. 특정 통합 테스트 파일의 모든 테스트를 실행하려면 `cargo test`의 `--test` 인자 뒤에 파일 이름을 붙인다:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-05-single-integration/output.txt}}
```

이 명령어는 _tests/integration_test.rs_ 파일의 테스트만 실행한다.


#### 통합 테스트에서의 서브모듈

통합 테스트를 추가하면서, 테스트를 체계적으로 관리하기 위해 _tests_ 디렉터리에 더 많은 파일을 만들고 싶을 수 있다. 예를 들어, 테스트 기능에 따라 테스트 함수를 그룹화할 수 있다. 앞서 언급했듯이, _tests_ 디렉터리의 각 파일은 별도의 크레이트로 컴파일된다. 이는 엔드 유저가 크레이트를 사용하는 방식을 더 정확히 모방하기 위해 별도의 스코프를 만드는 데 유용하다. 하지만 이는 _tests_ 디렉터리의 파일들이 _src_ 디렉터리의 파일들과 동일한 동작을 공유하지 않는다는 것을 의미한다. 이는 7장에서 코드를 모듈과 파일로 분리하는 방법을 배울 때 이미 다룬 내용이다.

_tests_ 디렉터리 파일들의 다른 동작은 여러 통합 테스트 파일에서 사용할 헬퍼 함수 세트가 있고, 이를 공통 모듈로 추출하기 위해 7장의 [“모듈을 다른 파일로 분리하기”][separating-modules-into-files]<!-- ignore --> 섹션의 단계를 따르려고 할 때 가장 두드러진다. 예를 들어, _tests/common.rs_ 파일을 만들고 그 안에 `setup`이라는 함수를 추가한다면, 여러 테스트 파일의 여러 테스트 함수에서 호출하고 싶은 코드를 `setup`에 추가할 수 있다:

<span class="filename">파일명: tests/common.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/tests/common.rs}}
```

테스트를 다시 실행하면, _common.rs_ 파일에 대한 새로운 섹션이 테스트 출력에 나타난다. 이 파일은 테스트 함수를 포함하지도 않았고, `setup` 함수를 어디에서도 호출하지 않았음에도 불구하고:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/output.txt}}
```

`common`이 테스트 결과에 나타나고 `running 0 tests`가 표시되는 것은 원하는 바가 아니다. 단지 다른 통합 테스트 파일과 일부 코드를 공유하고 싶었을 뿐이다. `common`이 테스트 출력에 나타나지 않도록 하려면, _tests/common.rs_ 파일을 만드는 대신 _tests/common/mod.rs_ 파일을 만든다. 이제 프로젝트 디렉터리는 다음과 같이 보인다:

```text
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    ├── common
    │   └── mod.rs
    └── integration_test.rs
```

이것은 7장의 [“대체 파일 경로”][alt-paths]<!-- ignore -->에서 언급한 Rust가 이해하는 오래된 명명 규칙이다. 파일을 이렇게 명명하면 Rust는 `common` 모듈을 통합 테스트 파일로 취급하지 않는다. `setup` 함수 코드를 _tests/common/mod.rs_로 옮기고 _tests/common.rs_ 파일을 삭제하면, 테스트 출력의 해당 섹션은 더 이상 나타나지 않는다. _tests_ 디렉터리의 하위 디렉터리에 있는 파일들은 별도의 크레이트로 컴파일되지 않으며, 테스트 출력에 섹션이 나타나지 않는다.

_tests/common/mod.rs_ 파일을 생성한 후에는, 이를 모듈로 사용해 어떤 통합 테스트 파일에서든 사용할 수 있다. 다음은 _tests/integration_test.rs_ 파일의 `it_adds_two` 테스트에서 `setup` 함수를 호출하는 예제다:

<span class="filename">파일명: tests/integration_test.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-13-fix-shared-test-code-problem/tests/integration_test.rs}}
```

`mod common;` 선언은 Listing 7-21에서 보여준 모듈 선언과 동일하다. 그런 다음 테스트 함수에서 `common::setup()` 함수를 호출할 수 있다.


#### 바이너리 크레이트의 통합 테스트

프로젝트가 _src/main.rs_ 파일만 포함하고 있고 _src/lib.rs_ 파일이 없는 바이너리 크레이트라면, _tests_ 디렉토리에서 통합 테스트를 작성하고 _src/main.rs_ 파일에 정의된 함수를 `use` 문으로 가져올 수 없다. 다른 크레이트가 사용할 수 있는 함수를 노출하는 것은 라이브러리 크레이트뿐이다. 바이너리 크레이트는 독립적으로 실행되도록 설계되었다.

이것이 Rust 프로젝트에서 바이너리를 제공할 때 _src/main.rs_ 파일이 _src/lib.rs_ 파일에 있는 로직을 호출하는 간단한 구조를 사용하는 이유 중 하나이다. 이러한 구조를 사용하면 통합 테스트에서 `use`를 통해 라이브러리 크레이트를 테스트하고 주요 기능을 사용할 수 있다. 주요 기능이 제대로 동작한다면, _src/main.rs_ 파일에 있는 소량의 코드도 잘 동작할 것이며, 이 작은 코드는 테스트할 필요가 없다.


## 요약

Rust의 테스트 기능은 코드가 예상대로 동작하는지 확인할 수 있는 방법을 제공한다. 이를 통해 코드를 변경하더라도 기존 기능이 정상적으로 작동하는지 보장할 수 있다. 유닛 테스트는 라이브러리의 각 부분을 개별적으로 검증하며, 비공개 구현 세부 사항도 테스트할 수 있다. 통합 테스트는 라이브러리의 여러 부분이 함께 올바르게 동작하는지 확인하며, 외부 코드에서 사용하는 방식과 동일하게 공개 API를 통해 테스트를 수행한다. Rust의 타입 시스템과 소유권 규칙이 특정 종류의 버그를 방지해 주지만, 코드의 예상 동작과 관련된 논리적 버그를 줄이기 위해 테스트는 여전히 중요하다.

이 장과 이전 장에서 배운 지식을 활용해 프로젝트를 진행해 보자!

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
[separating-modules-into-files]: ch07-05-separating-modules-into-different-files.html
[alt-paths]: ch07-05-separating-modules-into-different-files.html#alternate-file-paths


