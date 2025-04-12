## 트레이트: 공유 가능한 동작 정의하기

**트레이트(trait)**는 특정 타입이 가진 기능을 정의하고, 이를 다른 타입과 공유할 수 있게 해준다. 트레이트를 사용해 추상적인 방식으로 공유 가능한 동작을 정의할 수 있다. **트레이트 바운드(trait bounds)**를 활용하면 특정 동작을 가진 모든 타입을 일반화된 타입으로 지정할 수 있다.

> 참고: 트레이트는 다른 언어에서 흔히 **인터페이스(interfaces)**라고 부르는 기능과 유사하지만, 몇 가지 차이점이 있다.


### 트레이트 정의하기

타입의 동작은 해당 타입에서 호출할 수 있는 메서드들로 구성된다. 여러 타입이 동일한 메서드를 호출할 수 있다면, 그 타입들은 동일한 동작을 공유한다고 볼 수 있다. 트레이트 정의는 메서드 시그니처를 그룹화하여 특정 목적을 달성하는 데 필요한 동작 집합을 정의하는 방법이다.

예를 들어, 다양한 종류와 양의 텍스트를 담고 있는 여러 구조체가 있다고 가정해보자. 특정 지역에서 작성된 뉴스 기사를 담는 `NewsArticle` 구조체와, 최대 280자의 텍스트와 함께 새 게시물인지, 리포스트인지, 다른 게시물에 대한 답글인지를 나타내는 메타데이터를 포함하는 `SocialPost` 구조체가 있다.

이제 `aggregator`라는 이름의 미디어 집계 라이브러리 크레이트를 만들어 `NewsArticle`이나 `SocialPost` 인스턴스에 저장된 데이터의 요약을 표시하고 싶다. 이를 위해 각 타입에서 요약 정보를 제공해야 하며, 인스턴스에서 `summarize` 메서드를 호출해 요약 정보를 요청할 것이다. 아래 코드는 이 동작을 표현하는 공개 `Summary` 트레이트의 정의를 보여준다.

<Listing number="10-12" file-name="src/lib.rs" caption="`summarize` 메서드가 제공하는 동작을 포함하는 `Summary` 트레이트">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-12/src/lib.rs}}
```

</Listing>

여기서 `trait` 키워드를 사용해 트레이트를 선언하고, 이 경우에는 `Summary`라는 이름을 붙였다. 또한 이 트레이트를 `pub`으로 선언해 이 크레이트에 의존하는 다른 크레이트들도 이 트레이트를 사용할 수 있도록 했다. 중괄호 안에는 이 트레이트를 구현하는 타입들의 동작을 설명하는 메서드 시그니처를 선언했는데, 이 경우에는 `fn summarize(&self) -> String`이다.

메서드 시그니처 뒤에는 중괄호 안에 구현을 제공하는 대신 세미콜론을 사용했다. 이 트레이트를 구현하는 각 타입은 메서드 본문에 대해 자신만의 커스텀 동작을 제공해야 한다. 컴파일러는 `Summary` 트레이트를 가진 모든 타입이 정확히 이 시그니처와 함께 `summarize` 메서드를 정의하도록 강제한다.

트레이트 본문에는 여러 메서드를 포함할 수 있다. 메서드 시그니처는 한 줄에 하나씩 나열되며, 각 줄은 세미콜론으로 끝난다.


### 타입에 트레잇 구현하기

이제 `Summary` 트레잇 메서드의 원하는 시그니처를 정의했으므로, 미디어 애그리게이터의 타입에 이를 구현할 수 있다. 리스트 10-13은 `NewsArticle` 구조체에 `Summary` 트레잇을 구현한 예시를 보여준다. 여기서는 헤드라인, 작성자, 위치를 사용해 `summarize`의 반환 값을 생성한다. `SocialPost` 구조체의 경우, `summarize`를 사용자 이름 뒤에 게시물 전체 텍스트가 오도록 정의한다. 이때 게시물 내용이 이미 280자로 제한되어 있다고 가정한다.

<Listing number="10-13" file-name="src/lib.rs" caption="`NewsArticle` 및 `SocialPost` 타입에 `Summary` 트레잇 구현">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-13/src/lib.rs:here}}
```

</Listing>

타입에 트레잇을 구현하는 것은 일반 메서드를 구현하는 것과 유사하다. 차이점은 `impl` 뒤에 구현하려는 트레잇 이름을 적고, `for` 키워드를 사용한 다음, 트레잇을 구현할 타입의 이름을 지정한다는 것이다. `impl` 블록 내부에는 트레잇 정의에서 정의한 메서드 시그니처를 넣는다. 각 시그니처 뒤에 세미콜론을 추가하는 대신, 중괄호를 사용하고 해당 타입에 대해 트레잇 메서드가 가져야 할 특정 동작을 메서드 본문에 작성한다.

이제 라이브러리가 `NewsArticle`과 `SocialPost`에 `Summary` 트레잇을 구현했으므로, 크레이트 사용자는 `NewsArticle`과 `SocialPost` 인스턴스에서 일반 메서드를 호출하는 것과 같은 방식으로 트레잇 메서드를 호출할 수 있다. 유일한 차이점은 사용자가 타입뿐만 아니라 트레잇도 스코프로 가져와야 한다는 것이다. 다음은 바이너리 크레이트가 `aggregator` 라이브러리 크레이트를 사용하는 예시다:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-01-calling-trait-method/src/main.rs}}
```

이 코드는 `1 new post: horse_ebooks: of course, as you probably already know, people`을 출력한다.

`aggregator` 크레이트에 의존하는 다른 크레이트도 `Summary` 트레잇을 스코프로 가져와 자신의 타입에 `Summary`를 구현할 수 있다. 주의할 점은 트레잇이나 타입 중 하나가 우리 크레이트에 로컬로 정의되어 있을 때만 해당 타입에 트레잇을 구현할 수 있다는 것이다. 예를 들어, `SocialPost`와 같은 커스텀 타입에 `Display`와 같은 표준 라이브러리 트레잇을 `aggregator` 크레이트 기능의 일부로 구현할 수 있다. 이는 `SocialPost` 타입이 `aggregator` 크레이트에 로컬로 정의되어 있기 때문이다. 또한 `aggregator` 크레이트에서 `Vec<T>`에 `Summary`를 구현할 수도 있다. 이는 `Summary` 트레잇이 `aggregator` 크레이트에 로컬로 정의되어 있기 때문이다.

하지만 외부 트레잇을 외부 타입에 구현할 수는 없다. 예를 들어, `aggregator` 크레이트 내에서 `Vec<T>`에 `Display` 트레잇을 구현할 수 없다. 이는 `Display`와 `Vec<T>` 모두 표준 라이브러리에 정의되어 있고 `aggregator` 크레이트에 로컬로 정의되어 있지 않기 때문이다. 이 제한은 _코히어런스(coherence)_ 속성의 일부이며, 더 구체적으로는 _오펀 룰(orphan rule)_이라고 한다. 이 규칙은 다른 사람의 코드가 여러분의 코드를 망가뜨리지 않도록 보장한다. 이 규칙이 없다면 두 크레이트가 동일한 타입에 동일한 트레잇을 구현할 수 있고, Rust는 어떤 구현을 사용해야 할지 알 수 없게 된다.


### 기본 구현

특정 트레이트의 일부 또는 모든 메서드에 대해 기본 동작을 정의하는 것이 유용할 때가 있다. 이렇게 하면 모든 타입에서 모든 메서드를 구현할 필요 없이, 특정 타입에 트레이트를 구현할 때 각 메서드의 기본 동작을 유지하거나 재정의할 수 있다.

리스트 10-14에서는 `Summary` 트레이트의 `summarize` 메서드에 대해 기본 문자열을 지정한다. 이전 리스트 10-12에서 메서드 시그니처만 정의했던 것과 달리, 이번에는 기본 구현을 제공한다.

<Listing number="10-14" file-name="src/lib.rs" caption="`summarize` 메서드의 기본 구현을 포함한 `Summary` 트레이트 정의">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-14/src/lib.rs:here}}
```

</Listing>

`NewsArticle` 인스턴스를 요약하기 위해 기본 구현을 사용하려면, `impl Summary for NewsArticle {}`와 같이 빈 `impl` 블록을 지정한다.

이제 `NewsArticle`에서 직접 `summarize` 메서드를 정의하지 않더라도, 기본 구현을 제공했고 `NewsArticle`이 `Summary` 트레이트를 구현한다고 명시했기 때문에, 여전히 `NewsArticle` 인스턴스에서 `summarize` 메서드를 호출할 수 있다. 예를 들면 다음과 같다:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-02-calling-default-impl/src/main.rs:here}}
```

이 코드는 `New article available! (Read more...)`를 출력한다.

기본 구현을 생성해도 리스트 10-13의 `SocialPost`에 대한 `Summary` 구현은 변경할 필요가 없다. 기본 구현을 재정의하는 구문은 기본 구현이 없는 트레이트 메서드를 구현하는 구문과 동일하기 때문이다.

기본 구현은 동일한 트레이트 내의 다른 메서드를 호출할 수 있다. 심지어 해당 메서드에 기본 구현이 없더라도 가능하다. 이렇게 하면 트레이트가 많은 유용한 기능을 제공하면서도 구현자에게는 일부만 구현하도록 요구할 수 있다. 예를 들어, `Summary` 트레이트에 `summarize_author` 메서드를 정의하고 이 메서드의 구현을 필수로 요구한 다음, `summarize` 메서드의 기본 구현에서 `summarize_author` 메서드를 호출하도록 정의할 수 있다:

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:here}}
```

이 버전의 `Summary`를 사용하려면, 타입에 트레이트를 구현할 때 `summarize_author`만 정의하면 된다:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:impl}}
```

`summarize_author`를 정의한 후에는 `SocialPost` 구조체의 인스턴스에서 `summarize`를 호출할 수 있고, `summarize`의 기본 구현은 우리가 제공한 `summarize_author`의 정의를 호출한다. `summarize_author`를 구현했기 때문에, `Summary` 트레이트는 추가 코드 없이도 `summarize` 메서드의 동작을 제공한다. 이렇게 사용할 수 있다:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/main.rs:here}}
```

이 코드는 `1 new post: (Read more from @horse_ebooks...)`를 출력한다.

동일한 메서드의 재정의 구현에서 기본 구현을 호출할 수 없다는 점에 유의한다.


### 트레이트를 매개변수로 사용하기

트레이트를 정의하고 구현하는 방법을 배웠으니, 이제 다양한 타입을 받는 함수를 정의할 때 트레이트를 어떻게 활용할 수 있는지 알아보자. 리스트 10-13에서 `NewsArticle`과 `SocialPost` 타입에 구현한 `Summary` 트레이트를 사용해 `notify` 함수를 정의할 것이다. 이 함수는 `Summary` 트레이트를 구현한 어떤 타입의 `item` 매개변수에서 `summarize` 메서드를 호출한다. 이를 위해 `impl Trait` 구문을 사용한다:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-04-traits-as-parameters/src/lib.rs:here}}
```

`item` 매개변수에 구체적인 타입 대신 `impl` 키워드와 트레이트 이름을 지정한다. 이 매개변수는 지정된 트레이트를 구현한 모든 타입을 받아들인다. `notify` 함수 본문에서는 `item`에서 `Summary` 트레이트의 메서드인 `summarize`와 같은 메서드를 호출할 수 있다. `notify`를 호출할 때 `NewsArticle`이나 `SocialPost`의 인스턴스를 전달할 수 있다. `String`이나 `i32`와 같은 다른 타입으로 함수를 호출하려고 하면 컴파일되지 않는다. 이 타입들은 `Summary` 트레이트를 구현하지 않았기 때문이다.

<!-- Old headings. Do not remove or links may break. -->

<a id="fixing-the-largest-function-with-trait-bounds"></a>


#### 트레이트 바운드 문법

`impl Trait` 문법은 간단한 경우에 유용하지만, 이는 사실 _트레이트 바운드_라고 불리는 더 긴 형태의 문법을 간단히 표현한 것이다. 트레이트 바운드 문법은 다음과 같다:

```rust,ignore
pub fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}
```

이 더 긴 형태는 이전 섹션의 예제와 동일하지만 더 장황하다. 트레이트 바운드는 제네릭 타입 파라미터 선언 뒤에 콜론을 붙이고 꺾쇠 괄호 안에 위치시킨다.

`impl Trait` 문법은 편리하며 간단한 경우에 코드를 간결하게 만들어준다. 반면, 더 완전한 트레이트 바운드 문법은 다른 경우에 더 복잡한 표현을 가능하게 한다. 예를 들어, `Summary`를 구현하는 두 개의 파라미터를 가질 수 있다. `impl Trait` 문법을 사용하면 다음과 같다:

```rust,ignore
pub fn notify(item1: &impl Summary, item2: &impl Summary) {
```

`impl Trait`를 사용하면 `item1`과 `item2`가 서로 다른 타입을 가질 수 있다(단, 두 타입 모두 `Summary`를 구현해야 한다). 그러나 두 파라미터가 동일한 타입을 가지도록 강제하려면 트레이트 바운드를 사용해야 한다:

```rust,ignore
pub fn notify<T: Summary>(item1: &T, item2: &T) {
```

`item1`과 `item2` 파라미터의 타입으로 지정된 제네릭 타입 `T`는 함수를 제한하여 `item1`과 `item2`에 전달된 인자의 구체적인 타입이 동일해야 한다.


#### 여러 트레이트 바운드를 `+` 구문으로 지정하기

여러 개의 트레이트 바운드를 지정할 수도 있다. 예를 들어, `notify` 함수가 `item`에 대해 `summarize`뿐만 아니라 디스플레이 포맷팅도 사용하도록 하고 싶다면, `notify` 정의에서 `item`이 `Display`와 `Summary` 두 트레이트를 모두 구현해야 한다고 지정할 수 있다. 이때 `+` 구문을 사용한다:

```rust,ignore
pub fn notify(item: &(impl Summary + Display)) {
```

`+` 구문은 제네릭 타입의 트레이트 바운드에서도 유효하다:

```rust,ignore
pub fn notify<T: Summary + Display>(item: &T) {
```

두 트레이트 바운드를 지정하면, `notify` 함수 본문에서 `summarize`를 호출하고 `{}`를 사용해 `item`을 포맷팅할 수 있다.


#### `where` 절을 사용한 명확한 트레이트 바운드

너무 많은 트레이트 바운드를 사용하면 단점이 있다. 각 제네릭 타입은 고유한 트레이트 바운드를 가지므로, 여러 제네릭 타입 파라미터를 가진 함수는 함수 이름과 파라미터 목록 사이에 많은 트레이트 바운드 정보를 포함하게 된다. 이로 인해 함수 시그니처를 읽기 어렵게 만든다. 이러한 이유로 Rust는 함수 시그니처 뒤에 `where` 절을 사용해 트레이트 바운드를 지정하는 대체 구문을 제공한다. 따라서 다음과 같이 작성하는 대신:

```rust,ignore
fn some_function<T: Display + Clone, U: Clone + Debug>(t: &T, u: &U) -> i32 {
```

`where` 절을 사용해 다음과 같이 작성할 수 있다:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-07-where-clause/src/lib.rs:here}}
```

이렇게 하면 함수 시그니처가 덜 복잡해진다. 함수 이름, 파라미터 목록, 반환 타입이 서로 가까이 위치하게 되어, 트레이트 바운드가 많지 않은 함수와 비슷한 형태가 된다.


### 트레이트를 구현한 타입 반환하기

`impl Trait` 구문을 반환 위치에서 사용하여 특정 트레이트를 구현한 타입의 값을 반환할 수도 있다. 아래 예제를 참고하자:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-05-returning-impl-trait/src/lib.rs:here}}
```

`impl Summary`를 반환 타입으로 지정함으로써, `returns_summarizable` 함수가 `Summary` 트레이트를 구현한 어떤 타입을 반환한다는 것을 명시한다. 이 경우 `returns_summarizable`는 `SocialPost`를 반환하지만, 이 함수를 호출하는 코드는 구체적인 타입을 알 필요가 없다.

트레이트를 구현한 타입만으로 반환 타입을 지정할 수 있는 기능은 특히 클로저와 이터레이터와 같은 경우에 유용하다. 이는 13장에서 다룰 내용이다. 클로저와 이터레이터는 컴파일러만 아는 타입이거나 매우 길게 지정해야 하는 타입을 생성한다. `impl Trait` 구문을 사용하면 `Iterator` 트레이트를 구현한 어떤 타입을 반환한다는 것을 간결하게 표현할 수 있다.

하지만 `impl Trait`는 단일 타입을 반환할 때만 사용할 수 있다. 예를 들어, `NewsArticle` 또는 `SocialPost`를 반환하는 아래 코드는 `impl Summary`를 반환 타입으로 지정했기 때문에 동작하지 않는다:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-06-impl-trait-returns-one-type/src/lib.rs:here}}
```

`NewsArticle` 또는 `SocialPost`를 반환하는 것은 컴파일러에서 `impl Trait` 구문이 구현된 방식의 제약 때문에 허용되지 않는다. 이러한 동작을 하는 함수를 작성하는 방법은 18장의 [“다양한 타입의 값을 허용하는 트레이트 객체 사용하기”][using-trait-objects-that-allow-for-values-of-different-types]<!-- ignore --> 섹션에서 다룰 것이다.


### 트레이트 바운드를 사용해 조건부 메서드 구현하기

`impl` 블록에 제네릭 타입 매개변수와 함께 트레이트 바운드를 사용하면, 특정 트레이트를 구현한 타입에 대해서만 메서드를 조건부로 구현할 수 있다. 예를 들어, 리스트 10-15의 `Pair<T>` 타입은 항상 `new` 함수를 구현해 `Pair<T>`의 새 인스턴스를 반환한다. (5장의 [“메서드 정의하기”][methods]<!-- ignore --> 섹션에서 `Self`는 `impl` 블록의 타입 별칭이며, 이 경우에는 `Pair<T>`임을 상기하자.) 하지만 다음 `impl` 블록에서는 `Pair<T>`가 내부 타입 `T`가 비교를 가능하게 하는 `PartialOrd` 트레이트와 출력을 가능하게 하는 `Display` 트레이트를 모두 구현한 경우에만 `cmp_display` 메서드를 구현한다.

<리스트 번호="10-15" 파일 이름="src/lib.rs" 설명="트레이트 바운드에 따라 제네릭 타입에 조건부로 메서드 구현하기">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-15/src/lib.rs}}
```

</리스트>

또한, 특정 트레이트를 구현한 모든 타입에 대해 다른 트레이트를 조건부로 구현할 수도 있다. 트레이트 바운드를 만족하는 모든 타입에 대한 트레이트 구현을 *일괄 구현(blanket implementation)*이라고 하며, 이는 Rust 표준 라이브러리에서 광범위하게 사용된다. 예를 들어, 표준 라이브러리는 `Display` 트레이트를 구현한 모든 타입에 대해 `ToString` 트레이트를 구현한다. 표준 라이브러리의 `impl` 블록은 다음과 비슷하게 생겼다:

```rust,ignore
impl<T: Display> ToString for T {
    // --snip--
}
```

표준 라이브러리에 이 일괄 구현이 있기 때문에, `Display` 트레이트를 구현한 모든 타입에서 `ToString` 트레이트에 정의된 `to_string` 메서드를 호출할 수 있다. 예를 들어, 정수는 `Display`를 구현하므로 다음과 같이 정수를 해당하는 `String` 값으로 변환할 수 있다:

```rust
let s = 3.to_string();
```

일괄 구현은 트레이트 문서의 "구현자(Implementors)" 섹션에 나타난다.

트레이트와 트레이트 바운드를 사용하면 제네릭 타입 매개변수를 활용해 코드 중복을 줄이면서도 컴파일러에게 제네릭 타입이 특정 동작을 갖도록 요구할 수 있다. 컴파일러는 트레이트 바운드 정보를 사용해 코드에서 사용되는 모든 구체적 타입이 올바른 동작을 제공하는지 확인할 수 있다. 동적 타입 언어에서는 메서드가 정의되지 않은 타입에서 메서드를 호출할 경우 런타임에 오류가 발생한다. 하지만 Rust는 이러한 오류를 컴파일 타임으로 옮겨서 코드가 실행되기 전에 문제를 해결하도록 강제한다. 또한, 런타임에 동작을 확인하는 코드를 작성할 필요가 없는데, 이미 컴파일 타임에 확인했기 때문이다. 이렇게 하면 제네릭의 유연성을 포기하지 않으면서도 성능을 향상시킬 수 있다.

[using-trait-objects-that-allow-for-values-of-different-types]: ch18-02-trait-objects.html#using-trait-objects-that-allow-for-values-of-different-types
[methods]: ch05-03-method-syntax.html#defining-methods


