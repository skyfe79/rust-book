## 모듈을 사용해 스코프와 접근 제어하기

이 섹션에서는 모듈과 모듈 시스템의 주요 요소들에 대해 알아본다. 특히, 아이템에 이름을 붙일 수 있게 해주는 *경로(path)*, 특정 경로를 스코프로 가져오는 `use` 키워드, 아이템을 공개하는 `pub` 키워드 등을 다룬다. 또한 `as` 키워드, 외부 패키지, 그리고 glob 연산자에 대해서도 논의한다.


### 모듈 요약 정리

모듈과 경로에 대한 자세한 내용을 살펴보기 전에, 모듈, 경로, `use` 키워드, `pub` 키워드가 컴파일러에서 어떻게 동작하는지, 그리고 대부분의 개발자가 코드를 어떻게 구성하는지 간단히 정리한다. 이 장에서 각 규칙의 예제를 다룰 예정이지만, 모듈의 동작 방식을 다시 떠올리기 위해 참고하기 좋은 자료다.

- **크레이트 루트에서 시작**: 크레이트를 컴파일할 때, 컴파일러는 먼저 크레이트 루트 파일(보통 라이브러리 크레이트의 경우 _src/lib.rs_, 바이너리 크레이트의 경우 _src/main.rs_)에서 컴파일할 코드를 찾는다.
- **모듈 선언**: 크레이트 루트 파일에서 새로운 모듈을 선언할 수 있다. 예를 들어 `mod garden;`으로 "garden" 모듈을 선언하면, 컴파일러는 다음 위치에서 모듈 코드를 찾는다:
  - `mod garden` 뒤의 세미콜론을 중괄호로 대체한 인라인 코드
  - _src/garden.rs_ 파일
  - _src/garden/mod.rs_ 파일
- **서브모듈 선언**: 크레이트 루트 파일이 아닌 다른 파일에서 서브모듈을 선언할 수 있다. 예를 들어 _src/garden.rs_에서 `mod vegetables;`를 선언하면, 컴파일러는 부모 모듈 이름의 디렉토리 내에서 서브모듈 코드를 다음 위치에서 찾는다:
  - `mod vegetables` 바로 뒤에 중괄호로 대체된 인라인 코드
  - _src/garden/vegetables.rs_ 파일
  - _src/garden/vegetables/mod.rs_ 파일
- **모듈 내 코드 경로**: 모듈이 크레이트의 일부가 되면, 프라이버시 규칙이 허용하는 한 같은 크레이트 내 어디서든 해당 모듈의 코드를 경로를 통해 참조할 수 있다. 예를 들어, garden vegetables 모듈의 `Asparagus` 타입은 `crate::garden::vegetables::Asparagus` 경로로 찾을 수 있다.
- **private vs public**: 모듈 내 코드는 기본적으로 부모 모듈에서 private이다. 모듈을 public으로 만들려면 `mod` 대신 `pub mod`로 선언한다. public 모듈 내의 항목들도 public으로 만들려면, 해당 항목 선언 앞에 `pub`을 붙인다.
- **`use` 키워드**: `use` 키워드는 특정 스코프 내에서 항목에 대한 단축 경로를 만들어 긴 경로 반복을 줄인다. 예를 들어 `crate::garden::vegetables::Asparagus`를 참조할 수 있는 스코프에서 `use crate::garden::vegetables::Asparagus;`로 단축 경로를 만들면, 이후 해당 스코프 내에서는 `Asparagus`만으로도 해당 타입을 사용할 수 있다.

여기서는 `backyard`라는 바이너리 크레이트를 만들어 이 규칙들을 설명한다. `backyard`라는 이름의 크레이트 디렉토리에는 다음과 같은 파일과 디렉토리가 포함된다:

```text
backyard
├── Cargo.lock
├── Cargo.toml
└── src
    ├── garden
    │   └── vegetables.rs
    ├── garden.rs
    └── main.rs
```

이 경우 크레이트 루트 파일은 _src/main.rs_이며, 그 내용은 다음과 같다:

<Listing file-name="src/main.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/main.rs}}
```

</Listing>

`pub mod garden;` 라인은 컴파일러에게 _src/garden.rs_에 있는 코드를 포함하라고 지시한다. _src/garden.rs_ 파일의 내용은 다음과 같다:

<Listing file-name="src/garden.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden.rs}}
```

</Listing>

여기서 `pub mod vegetables;`는 _src/garden/vegetables.rs_에 있는 코드도 포함한다는 의미다. 해당 코드는 다음과 같다:

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden/vegetables.rs}}
```

이제 이 규칙들의 세부 사항을 살펴보고 실제로 동작하는 모습을 확인해 보자!


### 관련 코드를 모듈로 그룹화하기

모듈은 코드를 가독성 있게 정리하고 재사용하기 쉽게 만든다. 또한 모듈 내부의 코드는 기본적으로 비공개이기 때문에, 모듈을 통해 아이템의 접근 제어를 관리할 수 있다. 비공개 아이템은 외부에서 사용할 수 없는 내부 구현 세부 사항이다. 필요에 따라 모듈과 그 안의 아이템을 공개하여 외부 코드가 사용할 수 있게 할 수도 있다.

예를 들어, 레스토랑 기능을 제공하는 라이브러리 크레이트를 작성해 보자. 함수의 시그니처만 정의하고 본문은 비워둘 것이다. 이렇게 하면 레스토랑의 구현보다 코드의 구조에 집중할 수 있다.

레스토랑 업계에서는 레스토랑의 일부를 _프런트 오브 하우스_와 _백 오브 하우스_로 구분한다. 프런트 오브 하우스는 고객이 있는 곳으로, 호스트가 고객을 안내하고, 서버가 주문과 결제를 처리하며, 바텐더가 음료를 만드는 공간이다. 백 오브 하우스는 요리사와 주방 직원이 일하고, 접시를 닦는 직원이 청소를 하며, 관리자가 행정 업무를 처리하는 곳이다.

이 구조를 반영해 크레이트를 구성하기 위해, 함수를 중첩된 모듈로 정리할 수 있다. `cargo new restaurant --lib` 명령을 실행해 `restaurant`라는 새 라이브러리를 생성한다. 그런 다음 _src/lib.rs_ 파일에 아래 코드를 입력해 모듈과 함수 시그니처를 정의한다. 이 코드는 프런트 오브 하우스 섹션을 나타낸다.

<Listing number="7-1" file-name="src/lib.rs" caption="다른 모듈을 포함하는 `front_of_house` 모듈과 그 안의 함수들">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-01/src/lib.rs}}
```

</Listing>

`mod` 키워드 뒤에 모듈 이름을 붙여 모듈을 정의한다 (여기서는 `front_of_house`). 모듈의 본문은 중괄호 안에 위치한다. 모듈 내부에는 다른 모듈을 포함할 수 있다. 여기서는 `hosting`과 `serving` 모듈이 그 예이다. 모듈은 구조체, 열거형, 상수, 트레이트와 같은 다른 아이템의 정의도 포함할 수 있다. Listing 7-1에서는 함수를 포함하고 있다.

모듈을 사용하면 관련 정의를 그룹화하고 그룹화된 이유를 명확히 할 수 있다. 이 코드를 사용하는 프로그래머는 모든 정의를 읽어야 하는 대신 그룹을 기반으로 코드를 탐색할 수 있어, 관련 정의를 더 쉽게 찾을 수 있다. 새로운 기능을 추가하는 프로그래머는 코드를 어디에 배치해야 프로그램이 체계적으로 유지될지 알 수 있다.

앞서 _src/main.rs_와 _src/lib.rs_를 크레이트 루트라고 언급했다. 이 두 파일의 내용은 크레이트의 모듈 구조에서 루트에 위치한 `crate`라는 모듈을 형성하기 때문에 이런 이름이 붙었다. 이를 _모듈 트리_라고 한다.

Listing 7-2는 Listing 7-1의 구조에 대한 모듈 트리를 보여준다.

<Listing number="7-2" caption="Listing 7-1의 코드에 대한 모듈 트리">

```text
crate
 └── front_of_house
     ├── hosting
     │   ├── add_to_waitlist
     │   └── seat_at_table
     └── serving
         ├── take_order
         ├── serve_order
         └── take_payment
```

</Listing>

이 트리는 일부 모듈이 다른 모듈 내부에 중첩되는 방식을 보여준다. 예를 들어, `hosting`은 `front_of_house` 내부에 중첩된다. 또한 일부 모듈은 같은 모듈 내에 정의된 _형제_ 관계이다. `hosting`과 `serving`은 `front_of_house` 내부에 정의된 형제 모듈이다. 모듈 A가 모듈 B 내부에 포함되어 있다면, 모듈 A는 모듈 B의 _자식_이고, 모듈 B는 모듈 A의 _부모_이다. 전체 모듈 트리는 암묵적으로 `crate`라는 모듈 아래에 루트를 두고 있다.

모듈 트리는 컴퓨터의 파일 시스템 디렉터리 트리를 떠올리게 할 수 있다. 이 비교는 매우 적절하다! 파일 시스템에서 디렉터리를 사용하듯, 모듈을 사용해 코드를 정리한다. 그리고 디렉터리 내의 파일을 찾듯, 모듈을 찾는 방법이 필요하다.


