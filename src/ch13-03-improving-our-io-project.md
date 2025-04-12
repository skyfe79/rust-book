## I/O 프로젝트 개선하기

이제 이터레이터에 대해 배운 새로운 지식을 활용해 12장의 I/O 프로젝트를 개선할 수 있다. 이터레이터를 사용하면 코드를 더 명확하고 간결하게 만들 수 있다. 이제 `Config::build` 함수와 `search` 함수의 구현을 어떻게 개선할 수 있는지 살펴보자.


### `clone` 제거하기: 이터레이터 활용

리스트 12-6에서는 `String` 값들의 슬라이스를 가져와 `Config` 구조체의 인스턴스를 생성했다. 이때 슬라이스의 특정 인덱스에 접근해 값을 복제(clone)하는 방식을 사용했는데, 이는 `Config` 구조체가 해당 값들의 소유권을 가지기 위함이었다. 리스트 13-17에서는 리스트 12-23의 `Config::build` 함수 구현을 그대로 재현했다.

<Listing number="13-17" file-name="src/lib.rs" caption="리스트 12-23의 `Config::build` 함수 재현">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-23-reproduced/src/lib.rs:ch13}}
```

</Listing>

당시에는 비효율적인 `clone` 호출에 대해 걱정하지 말라고 했는데, 그 이유는 나중에 이를 제거할 계획이었기 때문이다. 이제 그때가 왔다!

`clone`이 필요했던 이유는 `args` 파라미터에 `String` 요소를 가진 슬라이스가 있었지만, `build` 함수가 `args`의 소유권을 가지지 않기 때문이다. `Config` 인스턴스의 소유권을 반환하려면 `Config`의 `query`와 `file_path` 필드의 값을 복제해야 했다. 이렇게 해야 `Config` 인스턴스가 자신의 값을 소유할 수 있었다.

이제 이터레이터에 대한 새로운 지식을 활용해 `build` 함수를 수정할 수 있다. 슬라이스를 빌려오는 대신 이터레이터를 인자로 받아 소유권을 가지도록 변경한다. 슬라이스의 길이를 확인하고 특정 위치에 접근하는 코드 대신 이터레이터 기능을 사용할 것이다. 이렇게 하면 `Config::build` 함수가 무엇을 하는지 더 명확해진다. 이터레이터가 값을 직접 접근하기 때문이다.

`Config::build`가 이터레이터의 소유권을 가지고, 빌려오는 인덱스 연산을 더 이상 사용하지 않으면, `clone`을 호출해 새로운 메모리를 할당하는 대신 이터레이터에서 `String` 값을 `Config`로 바로 이동시킬 수 있다.


#### 반환된 이터레이터 직접 사용하기

I/O 프로젝트의 _src/main.rs_ 파일을 열면 다음과 같은 코드가 보일 것이다:

<span class="filename">파일명: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-24-reproduced/src/main.rs:ch13}}
```

먼저 리스팅 12-24에서 작성한 `main` 함수의 시작 부분을 리스팅 13-18의 코드로 변경한다. 이번에는 이터레이터를 사용한다. `Config::build`도 업데이트하기 전까지는 컴파일되지 않는다.

<Listing number="13-18" file-name="src/main.rs" caption="`env::args`의 반환 값을 `Config::build`에 전달">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-18/src/main.rs:here}}
```

</Listing>

`env::args` 함수는 이터레이터를 반환한다! 이터레이터 값을 벡터로 모아서 슬라이스를 `Config::build`에 전달하는 대신, 이제는 `env::args`에서 반환된 이터레이터의 소유권을 직접 `Config::build`에 전달한다.

다음으로 `Config::build`의 정의를 업데이트해야 한다. I/O 프로젝트의 _src/lib.rs_ 파일에서 `Config::build`의 시그니처를 리스팅 13-19와 같이 변경한다. 함수 본문도 업데이트해야 하기 때문에 아직 컴파일되지 않는다.

<Listing number="13-19" file-name="src/lib.rs" caption="이터레이터를 기대하도록 `Config::build`의 시그니처 업데이트">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-19/src/lib.rs:here}}
```

</Listing>

`env::args` 함수의 표준 라이브러리 문서를 보면, 이 함수가 반환하는 이터레이터의 타입은 `std::env::Args`이며, 이 타입은 `Iterator` 트레잇을 구현하고 `String` 값을 반환한다.

`Config::build` 함수의 시그니처를 업데이트하여 `args` 매개변수가 `&[String]` 대신 `impl Iterator<Item = String>` 트레잇 바운드를 가진 제네릭 타입을 갖도록 했다. [“트레잇을 매개변수로 사용하기”][impl-trait]<!-- ignore --> 섹션에서 논의한 `impl Trait` 문법을 사용하면, `args`는 `Iterator` 트레잇을 구현하고 `String` 아이템을 반환하는 어떤 타입이든 될 수 있다.

`args`의 소유권을 가져오고, 이터레이터를 통해 `args`를 변경할 것이기 때문에, `args` 매개변수에 `mut` 키워드를 추가하여 가변적으로 만들 수 있다.


#### 인덱싱 대신 `Iterator` 트레이트 메서드 사용하기

이제 `Config::build` 함수의 본문을 수정한다. `args`가 `Iterator` 트레이트를 구현하기 때문에 `next` 메서드를 호출할 수 있다. 리스팅 13-20은 리스팅 12-23의 코드를 업데이트하여 `next` 메서드를 사용한다.

<Listing number="13-20" file-name="src/lib.rs" caption="`Config::build`의 본문을 iterator 메서드를 사용하도록 변경">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-20/src/lib.rs:here}}
```

</Listing>

`env::args`의 반환값에서 첫 번째 값은 프로그램 이름이다. 이 값을 무시하고 다음 값으로 넘어가기 위해 먼저 `next`를 호출하고 반환값은 사용하지 않는다. 그런 다음 `next`를 다시 호출해 `Config`의 `query` 필드에 넣을 값을 가져온다. `next`가 `Some`을 반환하면 `match`를 사용해 값을 추출한다. `None`을 반환하면 충분한 인자가 제공되지 않았다는 의미이므로 `Err` 값을 반환하고 함수를 종료한다. `file_path` 값에 대해서도 동일한 작업을 수행한다.


### 이터레이터 어댑터로 코드를 명확하게 만들기

우리는 I/O 프로젝트의 `search` 함수에서도 이터레이터를 활용할 수 있다. 이 함수는 12장의 리스트 12-19와 동일하게 리스트 13-21에 재현되어 있다:

<Listing number="13-21" file-name="src/lib.rs" caption="리스트 12-19의 `search` 함수 구현">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:ch13}}
```

</Listing>

이 코드를 이터레이터 어댑터 메서드를 사용해 더 간결하게 작성할 수 있다. 이렇게 하면 가변적인 중간 `results` 벡터를 사용하지 않아도 된다. 함수형 프로그래밍 스타일은 코드를 명확하게 만들기 위해 가변 상태를 최소화하는 것을 선호한다. 가변 상태를 제거하면 나중에 검색을 병렬로 수행할 수 있는 개선이 가능해질 수 있다. 왜냐하면 `results` 벡터에 대한 동시 접근을 관리할 필요가 없기 때문이다. 리스트 13-22는 이 변경 사항을 보여준다:

<Listing number="13-22" file-name="src/lib.rs" caption="`search` 함수 구현에서 이터레이터 어댑터 메서드 사용">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-22/src/lib.rs:here}}
```

</Listing>

`search` 함수의 목적은 `contents`에서 `query`를 포함하는 모든 라인을 반환하는 것이다. 리스트 13-16의 `filter` 예제와 유사하게, 이 코드는 `filter` 어댑터를 사용해 `line.contains(query)`가 `true`를 반환하는 라인만 유지한다. 그런 다음 일치하는 라인들을 `collect`를 사용해 다른 벡터로 모은다. 훨씬 간단하다! `search_case_insensitive` 함수에서도 동일한 변경을 적용해 이터레이터 메서드를 사용해 보자.


### 루프와 이터레이터 중 선택하기

다음으로 자연스럽게 떠오르는 질문은 여러분의 코드에서 어떤 스타일을 선택해야 하는지와 그 이유이다. 리스트 13-21의 원래 구현과 리스트 13-22의 이터레이터를 사용한 버전 중 어떤 것을 선택할 것인가? 대부분의 Rust 프로그래머는 이터레이터 스타일을 선호한다. 처음에는 익숙해지기 어려울 수 있지만, 다양한 이터레이터 어댑터와 그 기능을 이해하면 이터레이터가 더 쉽게 이해될 수 있다. 루프의 다양한 부분을 다루고 새로운 벡터를 만드는 대신, 코드는 루프의 상위 목표에 집중한다. 이는 일반적인 코드를 추상화하여 이터레이터의 각 요소가 통과해야 하는 필터링 조건과 같은 이 코드에만 해당하는 개념을 더 쉽게 파악할 수 있도록 한다.

하지만 두 구현이 정말 동등한가? 직관적으로는 더 낮은 수준의 루프가 더 빠를 것이라고 가정할 수 있다. 이제 성능에 대해 이야기해보자.

[impl-trait]: ch10-02-traits.html#traits-as-parameters


