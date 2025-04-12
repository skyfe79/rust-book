## 모듈을 별도의 파일로 분리하기

지금까지는 이 장의 모든 예제에서 여러 모듈을 하나의 파일에 정의했다. 모듈이 커지면 코드를 더 쉽게 탐색할 수 있도록 모듈 정의를 별도의 파일로 옮기고 싶을 때가 있다.

예를 들어, 레스토랑 관련 모듈이 여러 개 있는 Listing 7-17의 코드를 살펴보자. 모든 모듈을 크레이트 루트 파일에 정의하는 대신, 모듈을 별도의 파일로 추출할 것이다. 이 경우 크레이트 루트 파일은 _src/lib.rs_이지만, 이 절차는 크레이트 루트 파일이 _src/main.rs_인 바이너리 크레이트에서도 동일하게 적용된다.

먼저 `front_of_house` 모듈을 별도의 파일로 추출한다. `front_of_house` 모듈의 중괄호 안에 있는 코드를 제거하고, `mod front_of_house;` 선언만 남긴다. 그러면 _src/lib.rs_는 Listing 7-21에 나온 코드와 같이 된다. 이 코드는 Listing 7-22에서 _src/front_of_house.rs_ 파일을 만들기 전까지 컴파일되지 않는다.

<Listing number="7-21" file-name="src/lib.rs" caption="`front_of_house` 모듈을 선언하고, 본문은 *src/front_of_house.rs*에 위치">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-21-and-22/src/lib.rs}}
```

</Listing>

다음으로, 중괄호 안에 있던 코드를 _src/front_of_house.rs_라는 새 파일에 넣는다. Listing 7-22와 같이 작성한다. 컴파일러는 크레이트 루트에서 `front_of_house`라는 모듈 선언을 발견했기 때문에 이 파일을 찾아본다.

<Listing number="7-22" file-name="src/front_of_house.rs" caption="`front_of_house` 모듈의 정의가 *src/front_of_house.rs*에 위치">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-21-and-22/src/front_of_house.rs}}
```

</Listing>

모듈 트리에서 `mod` 선언을 사용해 파일을 로드하는 작업은 _한 번만_ 하면 된다. 컴파일러가 파일이 프로젝트의 일부임을 알고, `mod` 문을 어디에 넣었는지에 따라 모듈 트리에서 코드가 어디에 위치하는지 알게 되면, 프로젝트의 다른 파일들은 선언된 경로를 사용해 로드된 파일의 코드를 참조해야 한다. 이는 ["모듈 트리에서 아이템 참조하기"][paths]<!-- ignore --> 섹션에서 다룬 내용이다. 즉, `mod`는 다른 프로그래밍 언어에서 볼 수 있는 "임포트" 연산이 아니다.

다음으로 `hosting` 모듈을 별도의 파일로 추출한다. 이 과정은 `hosting`이 루트 모듈의 자식이 아니라 `front_of_house`의 자식 모듈이기 때문에 조금 다르다. `hosting` 파일은 모듈 트리에서 조상 모듈의 이름을 따서 만든 새 디렉터리에 위치한다. 이 경우 _src/front_of_house_ 디렉터리다.

`hosting`을 옮기기 위해 _src/front_of_house.rs_ 파일을 `hosting` 모듈의 선언만 포함하도록 변경한다:

<Listing file-name="src/front_of_house.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-02-extracting-hosting/src/front_of_house.rs}}
```

</Listing>

그런 다음 _src/front_of_house_ 디렉터리와 _hosting.rs_ 파일을 생성해 `hosting` 모듈의 정의를 넣는다:

<Listing file-name="src/front_of_house/hosting.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-02-extracting-hosting/src/front_of_house/hosting.rs}}
```

</Listing>

만약 _hosting.rs_ 파일을 _src_ 디렉터리에 넣으면, 컴파일러는 _hosting.rs_ 코드가 크레이트 루트에서 선언된 `hosting` 모듈에 속할 것으로 예상한다. `front_of_house` 모듈의 자식으로 선언되지 않을 것이다. 컴파일러가 어떤 파일을 어떤 모듈의 코드로 인식하는지에 대한 규칙은 디렉터리와 파일이 모듈 트리와 더 밀접하게 일치하도록 한다.

> ### 대체 파일 경로
>
> 지금까지는 Rust 컴파일러가 사용하는 가장 일반적인 파일 경로를 다뤘지만, Rust는 이전 스타일의 파일 경로도 지원한다. 크레이트 루트에서 선언된 `front_of_house` 모듈의 경우, 컴파일러는 모듈의 코드를 다음 위치에서 찾는다:
>
> - _src/front_of_house.rs_ (지금까지 다룬 방식)
> - _src/front_of_house/mod.rs_ (이전 스타일, 여전히 지원되는 경로)
>
> `front_of_house`의 하위 모듈인 `hosting` 모듈의 경우, 컴파일러는 모듈의 코드를 다음 위치에서 찾는다:
>
> - _src/front_of_house/hosting.rs_ (지금까지 다룬 방식)
> - _src/front_of_house/hosting/mod.rs_ (이전 스타일, 여전히 지원되는 경로)
>
> 같은 모듈에 대해 두 스타일을 모두 사용하면 컴파일 오류가 발생한다. 같은 프로젝트에서 다른 모듈에 대해 두 스타일을 혼용하는 것은 허용되지만, 프로젝트를 탐색하는 사람들에게 혼란을 줄 수 있다.
>
> _mod.rs_라는 파일 이름을 사용하는 스타일의 주요 단점은 프로젝트에 _mod.rs_ 파일이 많아질 수 있다는 점이다. 이는 편집기에서 여러 파일을 동시에 열었을 때 혼란을 줄 수 있다.

각 모듈의 코드를 별도의 파일로 옮겼지만, 모듈 트리는 그대로 유지된다. `eat_at_restaurant`의 함수 호출은 정의가 다른 파일에 있더라도 수정 없이 동작한다. 이 기법을 사용하면 모듈이 커짐에 따라 새 파일로 옮길 수 있다.

_src/lib.rs_의 `pub use crate::front_of_house::hosting` 문도 변경되지 않았으며, `use`는 크레이트의 일부로 컴파일되는 파일에 영향을 주지 않는다. `mod` 키워드는 모듈을 선언하며, Rust는 모듈과 같은 이름의 파일에서 해당 모듈의 코드를 찾는다.


## 요약

Rust는 패키지를 여러 크레이트(crate)로 나누고, 크레이트를 모듈로 분할할 수 있다. 이를 통해 한 모듈에서 다른 모듈에 정의된 항목을 참조할 수 있다. 항목을 참조할 때는 절대 경로나 상대 경로를 지정하면 된다. 이러한 경로는 `use` 문을 사용해 스코프 내로 가져올 수 있으며, 해당 스코프에서 항목을 여러 번 사용할 때 더 짧은 경로를 사용할 수 있다. 모듈 코드는 기본적으로 비공개(private)이지만, `pub` 키워드를 추가해 정의를 공개(public)로 만들 수 있다.

다음 장에서는 표준 라이브러리의 컬렉션 데이터 구조를 살펴본다. 이를 통해 잘 정리된 코드를 작성할 수 있다.

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html


