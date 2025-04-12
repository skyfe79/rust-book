## 모듈 트리에서 아이템을 참조하는 경로

Rust에서 모듈 트리 내의 아이템을 찾기 위해 경로를 사용한다. 이는 파일 시스템을 탐색할 때 경로를 사용하는 방식과 유사하다. 함수를 호출하려면 해당 함수의 경로를 알아야 한다.

경로는 두 가지 형태를 가진다:

- **_절대 경로_**는 크레이트 루트에서 시작하는 전체 경로다. 외부 크레이트의 코드라면 크레이트 이름으로 시작하고, 현재 크레이트의 코드라면 `crate` 리터럴로 시작한다.
- **_상대 경로_**는 현재 모듈에서 시작하며 `self`, `super`, 또는 현재 모듈의 식별자를 사용한다.

절대 경로와 상대 경로 모두 이중 콜론(`::`)으로 구분된 하나 이상의 식별자를 포함한다.

Listing 7-1로 돌아가서, `add_to_waitlist` 함수를 호출하려 한다고 가정해 보자. 이는 `add_to_waitlist` 함수의 경로가 무엇인지 묻는 것과 같다. Listing 7-3은 Listing 7-1에서 일부 모듈과 함수를 제거한 내용을 담고 있다.

크레이트 루트에 정의된 새로운 함수 `eat_at_restaurant`에서 `add_to_waitlist` 함수를 호출하는 두 가지 방법을 보여준다. 이 경로들은 정확하지만, 이 예제가 그대로 컴파일되지 않게 하는 또 다른 문제가 남아 있다. 이에 대해서는 잠시 후에 설명한다.

`eat_at_restaurant` 함수는 라이브러리 크레이트의 공개 API의 일부이므로 `pub` 키워드로 표시한다. [“`pub` 키워드로 경로 공개하기”][pub]<!-- ignore --> 섹션에서 `pub`에 대해 더 자세히 다룰 것이다.

<Listing number="7-3" file-name="src/lib.rs" caption="절대 경로와 상대 경로를 사용해 `add_to_waitlist` 함수 호출하기">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-03/src/lib.rs}}
```

</Listing>

`eat_at_restaurant`에서 `add_to_waitlist` 함수를 처음 호출할 때 절대 경로를 사용한다. `add_to_waitlist` 함수는 `eat_at_restaurant`와 같은 크레이트에 정의되어 있으므로, `crate` 키워드로 절대 경로를 시작할 수 있다. 그런 다음 `add_to_waitlist`에 도달할 때까지 각 연속 모듈을 포함한다. 같은 구조의 파일 시스템을 상상해 보면, `add_to_waitlist` 프로그램을 실행하기 위해 `/front_of_house/hosting/add_to_waitlist` 경로를 지정하는 것과 같다. `crate` 이름으로 크레이트 루트에서 시작하는 것은 셸에서 `/`로 파일 시스템 루트에서 시작하는 것과 유사하다.

`eat_at_restaurant`에서 `add_to_waitlist`를 두 번째로 호출할 때는 상대 경로를 사용한다. 이 경로는 `eat_at_restaurant`와 같은 모듈 트리 레벨에 정의된 `front_of_house` 모듈 이름으로 시작한다. 여기서 파일 시스템의 동등한 경로는 `front_of_house/hosting/add_to_waitlist`가 된다. 모듈 이름으로 시작한다는 것은 경로가 상대적임을 의미한다.

상대 경로와 절대 경로 중 어떤 것을 사용할지는 프로젝트에 따라 결정한다. 아이템 정의 코드를 사용하는 코드와 함께 이동할지, 아니면 따로 이동할지에 따라 달라진다. 예를 들어, `front_of_house` 모듈과 `eat_at_restaurant` 함수를 `customer_experience`라는 모듈로 이동한다면, `add_to_waitlist`의 절대 경로를 업데이트해야 하지만, 상대 경로는 여전히 유효하다. 반면, `eat_at_restaurant` 함수를 별도로 `dining`이라는 모듈로 이동한다면, `add_to_waitlist` 호출의 절대 경로는 동일하게 유지되지만, 상대 경로는 업데이트해야 한다. 일반적으로 절대 경로를 지정하는 것을 선호한다. 코드 정의와 아이템 호출을 서로 독립적으로 이동할 가능성이 더 높기 때문이다.

이제 Listing 7-3을 컴파일해 보자. 왜 아직 컴파일되지 않는지 확인할 수 있다. 발생한 오류는 Listing 7-4에 나와 있다.

<Listing number="7-4" caption="Listing 7-3의 코드를 빌드할 때 발생한 컴파일러 오류">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-03/output.txt}}
```

</Listing>

오류 메시지는 `hosting` 모듈이 비공개임을 알려준다. 즉, `hosting` 모듈과 `add_to_waitlist` 함수에 대한 경로는 정확하지만, Rust는 비공개 영역에 접근할 수 없기 때문에 이를 사용할 수 없다. Rust에서는 모든 아이템(함수, 메서드, 구조체, 열거형, 모듈, 상수)이 기본적으로 부모 모듈에 대해 비공개다. 함수나 구조체 같은 아이템을 비공개로 만들려면 모듈 안에 넣으면 된다.

부모 모듈의 아이템은 자식 모듈의 비공개 아이템을 사용할 수 없지만, 자식 모듈의 아이템은 조상 모듈의 아이템을 사용할 수 있다. 이는 자식 모듈이 구현 세부 사항을 감싸고 숨기지만, 자식 모듈은 자신이 정의된 컨텍스트를 볼 수 있기 때문이다. 비유를 계속하자면, 프라이버시 규칙은 레스토랑의 백오피스와 같다. 백오피스에서 일어나는 일은 레스토랑 고객에게는 비공개이지만, 관리자는 운영하는 레스토랑의 모든 것을 보고 할 수 있다.

Rust는 내부 구현 세부 사항을 숨기는 것이 기본 동작이 되도록 모듈 시스템을 설계했다. 이렇게 하면 외부 코드를 깨뜨리지 않고 내부 코드의 어느 부분을 변경할 수 있는지 알 수 있다. 그러나 Rust는 `pub` 키워드를 사용해 자식 모듈의 코드 내부를 외부 조상 모듈에 공개할 수 있는 옵션을 제공한다.


### `pub` 키워드로 경로 공개하기

리스트 7-4에서 발생한 오류를 다시 살펴보자. 이 오류는 `hosting` 모듈이 비공개임을 알려준다. 부모 모듈의 `eat_at_restaurant` 함수가 자식 모듈의 `add_to_waitlist` 함수에 접근할 수 있도록 하기 위해, 리스트 7-5와 같이 `hosting` 모듈에 `pub` 키워드를 추가한다.

<Listing number="7-5" file-name="src/lib.rs" caption="`eat_at_restaurant`에서 사용할 수 있도록 `hosting` 모듈을 `pub`로 선언">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-05/src/lib.rs:here}}
```

</Listing>

하지만 리스트 7-5의 코드는 여전히 컴파일 오류를 발생시킨다. 이 오류는 리스트 7-6에서 확인할 수 있다.

<Listing number="7-6" caption="리스트 7-5의 코드를 빌드했을 때 발생한 컴파일 오류">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-05/output.txt}}
```

</Listing>

어떤 일이 발생했을까? `mod hosting` 앞에 `pub` 키워드를 추가하면 모듈이 공개된다. 이 변경으로 `front_of_house`에 접근할 수 있다면 `hosting`에도 접근할 수 있다. 하지만 `hosting`의 _내용물_ 은 여전히 비공개 상태다. 모듈을 공개한다고 해서 그 안의 내용물까지 공개되지는 않는다. 모듈에 `pub` 키워드를 추가하면 조상 모듈의 코드가 해당 모듈을 참조할 수 있지만, 내부 코드에 접근할 수는 없다. 모듈은 컨테이너이기 때문에 모듈만 공개하는 것으로는 큰 효과를 볼 수 없다. 더 나아가 모듈 내부의 항목 중 하나 이상을 공개해야 한다.

리스트 7-6의 오류는 `add_to_waitlist` 함수가 비공개임을 알려준다. 비공개 규칙은 구조체, 열거형, 함수, 메서드뿐만 아니라 모듈에도 적용된다.

`add_to_waitlist` 함수도 공개하기 위해 `pub` 키워드를 추가해 보자. 리스트 7-7과 같이 수정한다.

<Listing number="7-7" file-name="src/lib.rs" caption="`mod hosting`과 `fn add_to_waitlist`에 `pub` 키워드를 추가해 `eat_at_restaurant`에서 함수를 호출할 수 있게 함">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-07/src/lib.rs:here}}
```

</Listing>

이제 코드가 컴파일된다! `pub` 키워드를 추가하면 `eat_at_restaurant`에서 이 경로를 사용할 수 있는 이유를 이해하기 위해 절대 경로와 상대 경로를 살펴보자.

절대 경로는 크레이트의 모듈 트리 루트인 `crate`로 시작한다. `front_of_house` 모듈은 크레이트 루트에 정의되어 있다. `front_of_house`는 공개되지 않았지만, `eat_at_restaurant` 함수가 `front_of_house`와 같은 모듈에 정의되어 있기 때문에(즉, `eat_at_restaurant`와 `front_of_house`는 형제 관계), `eat_at_restaurant`에서 `front_of_house`를 참조할 수 있다. 다음으로 `pub`로 표시된 `hosting` 모듈이 있다. `hosting`의 부모 모듈에 접근할 수 있으므로 `hosting`에도 접근할 수 있다. 마지막으로 `add_to_waitlist` 함수가 `pub`로 표시되어 있고, 부모 모듈에 접근할 수 있으므로 이 함수 호출이 가능하다!

상대 경로의 논리는 절대 경로와 동일하지만 첫 단계가 다르다. 크레이트 루트가 아니라 `front_of_house`로 시작한다. `front_of_house` 모듈은 `eat_at_restaurant`와 같은 모듈에 정의되어 있으므로, `eat_at_restaurant`가 정의된 모듈에서 시작하는 상대 경로가 유효하다. 그 다음, `hosting`과 `add_to_waitlist`가 `pub`로 표시되어 있으므로 경로의 나머지 부분도 유효하고, 이 함수 호출이 가능하다!

라이브러리 크레이트를 공유해 다른 프로젝트에서 코드를 사용할 계획이라면, 공개 API는 크레이트 사용자와의 계약과 같다. 이 API는 사용자가 코드와 상호작용하는 방식을 결정한다. 공개 API를 변경할 때는 사용자가 크레이트에 의존하기 쉽도록 여러 가지 사항을 고려해야 한다. 이 주제는 이 책의 범위를 벗어나지만, 관심이 있다면 [The Rust API Guidelines][api-guidelines]를 참고하자.

> #### 바이너리와 라이브러리를 포함하는 패키지의 모범 사례
>
> 패키지에는 _src/main.rs_ 바이너리 크레이트 루트와 _src/lib.rs_ 라이브러리 크레이트 루트가 모두 포함될 수 있으며, 두 크레이트는 기본적으로 패키지 이름을 공유한다. 일반적으로 라이브러리와 바이너리 크레이트를 모두 포함하는 패키지는 바이너리 크레이트에 실행 파일을 시작하는 데 필요한 최소한의 코드만 포함하고, 라이브러리 크레이트의 코드를 호출한다. 이렇게 하면 라이브러리 크레이트의 코드를 공유할 수 있으므로 다른 프로젝트도 패키지가 제공하는 대부분의 기능을 활용할 수 있다.
>
> 모듈 트리는 _src/lib.rs_에 정의해야 한다. 그러면 패키지 이름으로 시작하는 경로를 통해 바이너리 크레이트에서 공개 항목을 사용할 수 있다. 바이너리 크레이트는 완전히 외부의 크레이트가 라이브러리 크레이트를 사용하는 것과 마찬가지로 라이브러리 크레이트의 사용자가 된다. 즉, 공개 API만 사용할 수 있다. 이렇게 하면 좋은 API를 설계하는 데 도움이 된다. 여러분이 작성자이면서 동시에 클라이언트이기 때문이다!
>
> [12장][ch12]<!-- ignore -->에서는 바이너리 크레이트와 라이브러리 크레이트를 모두 포함하는 커맨드라인 프로그램을 통해 이 조직적 관행을 보여줄 것이다.


### `super`로 시작하는 상대 경로

`super`를 경로의 시작에 사용하면 현재 모듈이나 크레이트 루트가 아닌 부모 모듈에서 시작하는 상대 경로를 구성할 수 있다. 이는 파일 시스템 경로에서 `..` 문법을 사용하는 것과 유사하다. `super`를 사용하면 부모 모듈에 있는 항목을 참조할 수 있어, 모듈이 부모와 밀접하게 연관되어 있지만 부모가 나중에 모듈 트리의 다른 곳으로 이동할 가능성이 있는 경우, 모듈 트리를 재구성하기가 더 쉬워진다.

리스트 7-8의 코드를 살펴보자. 이 코드는 요리사가 잘못된 주문을 수정하고 직접 고객에게 전달하는 상황을 모델링한다. `back_of_house` 모듈에 정의된 `fix_incorrect_order` 함수는 `super`로 시작하는 경로를 지정하여 부모 모듈에 정의된 `deliver_order` 함수를 호출한다.

<Listing number="7-8" file-name="src/lib.rs" caption="`super`로 시작하는 상대 경로를 사용해 함수 호출하기">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-08/src/lib.rs}}
```

</Listing>

`fix_incorrect_order` 함수는 `back_of_house` 모듈에 있으므로, `super`를 사용해 `back_of_house`의 부모 모듈로 이동할 수 있다. 이 경우 부모 모듈은 크레이트 루트인 `crate`이다. 여기서 `deliver_order`를 찾아 호출한다. 성공! `back_of_house` 모듈과 `deliver_order` 함수는 서로 같은 관계를 유지하며 함께 이동할 가능성이 높기 때문에, `super`를 사용하면 나중에 이 코드가 다른 모듈로 이동하더라도 코드를 수정할 부분이 줄어든다.


### 구조체와 열거형을 공개로 만들기

`pub` 키워드를 사용해 구조체와 열거형을 공개로 지정할 수 있다. 하지만 구조체와 열거형에 `pub`을 사용할 때는 몇 가지 추가적인 세부 사항이 있다. 구조체 정의 앞에 `pub`을 사용하면 구조체 자체는 공개되지만, 구조체의 필드는 여전히 비공개 상태로 남는다. 각 필드를 개별적으로 공개할지 여부를 결정할 수 있다. 예제 7-9에서는 `back_of_house::Breakfast` 구조체를 공개로 정의했고, `toast` 필드는 공개로, `seasonal_fruit` 필드는 비공개로 설정했다. 이는 레스토랑에서 고객이 식사에 포함된 빵 종류를 선택할 수 있지만, 셰프가 계절과 재고에 따라 어떤 과일을 제공할지 결정하는 상황을 모델링한 것이다. 과일은 빠르게 변동되기 때문에 고객은 과일을 선택하거나 어떤 과일이 제공될지 미리 알 수 없다.

<Listing number="7-9" file-name="src/lib.rs" caption="일부 필드는 공개, 일부는 비공개인 구조체">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-09/src/lib.rs}}
```

</Listing>

`back_of_house::Breakfast` 구조체의 `toast` 필드는 공개이기 때문에, `eat_at_restaurant` 함수에서 점 표기법을 사용해 `toast` 필드에 읽고 쓸 수 있다. 하지만 `seasonal_fruit` 필드는 비공개이기 때문에 `eat_at_restaurant` 함수에서 사용할 수 없다. `seasonal_fruit` 필드 값을 수정하는 줄의 주석을 해제하면 어떤 에러가 발생하는지 확인해보자!

또한, `back_of_house::Breakfast` 구조체에 비공개 필드가 있기 때문에, `Breakfast` 인스턴스를 생성하는 공개 연관 함수를 제공해야 한다(여기서는 `summer`라는 이름을 사용했다). 만약 `Breakfast`에 이런 함수가 없다면, `eat_at_restaurant` 함수에서 `Breakfast` 인스턴스를 생성할 수 없다. 왜냐하면 비공개 필드인 `seasonal_fruit`의 값을 설정할 수 없기 때문이다.

반면, 열거형을 공개로 만들면 모든 변형체도 자동으로 공개된다. 열거형 앞에 `pub` 키워드만 붙이면 된다. 예제 7-10에서 이를 확인할 수 있다.

<Listing number="7-10" file-name="src/lib.rs" caption="열거형을 공개로 지정하면 모든 변형체도 공개된다.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-10/src/lib.rs}}
```

</Listing>

`Appetizer` 열거형을 공개로 만들었기 때문에, `eat_at_restaurant` 함수에서 `Soup`과 `Salad` 변형체를 사용할 수 있다.

열거형은 변형체가 공개되지 않으면 그다지 유용하지 않다. 모든 열거형 변형체에 `pub`을 붙이는 것은 번거로우므로, 열거형 변형체는 기본적으로 공개로 설정된다. 반면, 구조체는 필드가 공개되지 않아도 유용한 경우가 많기 때문에, 구조체 필드는 기본적으로 비공개로 설정된다. 단, `pub`으로 명시적으로 공개할 수 있다.

`pub`과 관련해 다루지 않은 한 가지 상황이 더 있다. 바로 `use` 키워드와 관련된 내용이다. 먼저 `use` 키워드 자체를 살펴본 다음, `pub`과 `use`를 함께 사용하는 방법을 알아볼 것이다.

[pub]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[api-guidelines]: https://rust-lang.github.io/api-guidelines/
[ch12]: ch12-00-an-io-project.html


