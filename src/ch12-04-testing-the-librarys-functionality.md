## 테스트 주도 개발로 라이브러리 기능 구현하기

이제 로직을 _src/lib.rs_로 분리하고 인자 수집과 오류 처리는 _src/main.rs_에 남겨두었으므로, 코드의 핵심 기능에 대한 테스트를 작성하기가 훨씬 쉬워졌다. 커맨드라인에서 바이너리를 호출할 필요 없이 다양한 인자를 직접 함수에 전달하고 반환 값을 확인할 수 있다.

이 섹션에서는 테스트 주도 개발(TDD) 프로세스를 통해 `minigrep` 프로그램에 검색 로직을 추가한다. TDD는 다음과 같은 단계로 진행된다:

1. 실패하는 테스트를 작성하고, 예상대로 실패하는지 확인한다.
2. 새로운 테스트를 통과할 만큼의 코드를 작성하거나 수정한다.
3. 방금 추가하거나 변경한 코드를 리팩토링하고 테스트가 계속 통과하는지 확인한다.
4. 1단계부터 반복한다!

TDD는 소프트웨어를 작성하는 여러 방법 중 하나이지만, 코드 설계를 이끌어내는 데 도움이 된다. 테스트를 통과시키는 코드를 작성하기 전에 테스트를 먼저 작성하면, 전체 과정에서 높은 테스트 커버리지를 유지할 수 있다.

이제 파일 내용에서 쿼리 문자열을 검색하고 일치하는 줄의 목록을 반환하는 기능을 구현해보자. 이 기능을 `search`라는 함수에 추가할 것이다.


### 실패하는 테스트 작성하기

이제 더 이상 필요 없으므로, 프로그램 동작을 확인하기 위해 사용했던 `println!` 문을 _src/lib.rs_와 _src/main.rs_에서 제거한다. 그런 다음 _src/lib.rs_에 [11장][ch11-anatomy]에서 했던 것처럼 `tests` 모듈과 테스트 함수를 추가한다. 테스트 함수는 `search` 함수가 가져야 할 동작을 정의한다: 쿼리와 검색할 텍스트를 받아서, 쿼리를 포함하는 라인만 반환해야 한다. 아래 목록 12-15는 아직 컴파일되지 않는 이 테스트를 보여준다.

<Listing number="12-15" file-name="src/lib.rs" caption="원하는 `search` 함수를 위한 실패하는 테스트 작성">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-15/src/lib.rs:here}}
```

</Listing>

이 테스트는 문자열 `"duct"`를 검색한다. 검색할 텍스트는 세 줄로 구성되어 있으며, 그 중 한 줄만 `"duct"`를 포함한다(여는 큰따옴표 뒤의 백슬래시는 Rust에게 이 문자열 리터럴의 내용 앞에 개행 문자를 추가하지 말라고 알려준다). `search` 함수가 반환한 값이 예상한 라인만 포함하는지 확인한다.

아직 이 테스트를 실행해 실패하는 모습을 볼 수는 없다. 왜냐하면 테스트가 컴파일조차 되지 않기 때문이다: `search` 함수가 아직 존재하지 않는다! TDD 원칙에 따라, 테스트가 컴파일되고 실행될 수 있도록 최소한의 코드를 추가한다. 목록 12-16과 같이 항상 빈 벡터를 반환하는 `search` 함수를 정의한다. 그러면 테스트는 컴파일되고 실패할 것이다. 빈 벡터는 `"safe, fast, productive."` 라인을 포함하는 벡터와 일치하지 않기 때문이다.

<Listing number="12-16" file-name="src/lib.rs" caption="테스트가 컴파일되도록 `search` 함수의 최소한의 정의 추가">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-16/src/lib.rs:here}}
```

</Listing>

`search` 함수의 시그니처에서 명시적 라이프타임 `'a`를 정의하고, 이 라이프타임을 `contents` 인자와 반환 값에 사용한다. [10장][ch10-lifetimes]에서 라이프타임 매개변수가 반환 값의 라이프타임과 어떤 인자의 라이프타임이 연결되는지 지정한다고 설명했다. 이 경우, 반환된 벡터가 `query`가 아닌 `contents` 인자의 슬라이스를 참조하는 문자열 슬라이스를 포함해야 한다고 표시한다.

다시 말해, `search` 함수가 반환하는 데이터는 `contents` 인자로 전달된 데이터만큼 오래 유지될 것이라고 Rust에게 알린다. 이는 중요하다! 슬라이스가 참조하는 데이터는 참조가 유효하려면 유효해야 한다. 만약 컴파일러가 `contents`가 아닌 `query`의 문자열 슬라이스를 만든다고 가정하면, 안전성 검사를 잘못 수행할 것이다.

만약 라이프타임 어노테이션을 잊어버리고 이 함수를 컴파일하려고 하면, 다음과 같은 오류가 발생한다:

```console
{{#include ../listings/ch12-an-io-project/output-only-02-missing-lifetimes/output.txt}}
```

Rust는 두 인자 중 어느 것이 필요한지 알 수 없으므로, 명시적으로 알려야 한다. `contents`는 모든 텍스트를 포함하는 인자이며, 일치하는 텍스트 부분을 반환하려고 하므로, `contents`가 라이프타임 구문을 사용해 반환 값과 연결되어야 한다는 것을 알고 있다.

다른 프로그래밍 언어에서는 시그니처에서 인자를 반환 값과 연결할 필요가 없지만, 이 연습은 시간이 지나면 점점 쉬워질 것이다. 이 예제를 [10장의 "라이프타임으로 참조 유효성 검사"][validating-references-with-lifetimes] 섹션의 예제와 비교해보는 것도 좋다.

이제 테스트를 실행해보자:

```console
{{#include ../listings/ch12-an-io-project/listing-12-16/output.txt}}
```

좋다, 테스트가 예상대로 실패한다. 이제 테스트를 통과시키자!


### 테스트를 통과하는 코드 작성하기

현재 테스트가 실패하는 이유는 항상 빈 벡터를 반환하기 때문이다. 이를 수정하고 `search` 함수를 구현하려면 프로그램이 다음 단계를 따라야 한다:

1. `contents`의 각 줄을 순회한다.
2. 해당 줄에 쿼리 문자열이 포함되어 있는지 확인한다.
3. 포함되어 있다면, 반환할 값 목록에 추가한다.
4. 포함되어 있지 않다면, 아무 작업도 하지 않는다.
5. 일치하는 결과 목록을 반환한다.

이제 각 단계를 차례대로 살펴보자. 먼저 줄을 순회하는 것부터 시작하자.


#### `lines` 메서드를 사용한 줄 단위 반복

Rust는 문자열을 줄 단위로 반복 처리할 수 있는 유용한 메서드를 제공한다. 이 메서드는 `lines`라는 이름으로, 리스트 12-17에서와 같이 동작한다. 현재는 컴파일되지 않는다는 점에 유의하자.

<Listing number="12-17" file-name="src/lib.rs" caption="`contents`의 각 줄을 반복 처리">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-17/src/lib.rs:here}}
```

</Listing>

`lines` 메서드는 반복자(iterator)를 반환한다. 반복자에 대해서는 [13장][ch13-iterators]<!-- ignore -->에서 자세히 다룰 예정이지만, [리스트 3-5][ch3-iter]<!-- ignore -->에서 반복자를 사용한 방식을 떠올려보자. 그때는 `for` 루프와 반복자를 사용해 컬렉션의 각 항목에 대해 코드를 실행했다.


#### 각 줄에서 쿼리 검색하기

다음으로, 현재 줄에 우리가 찾는 쿼리 문자열이 포함되어 있는지 확인한다. 다행히 문자열에는 이를 처리해주는 `contains`라는 유용한 메서드가 있다! `search` 함수에 `contains` 메서드를 호출하는 코드를 추가한다. Listing 12-18을 참고하면 된다. 아직은 이 코드가 컴파일되지 않는다는 점에 유의한다.

<Listing number="12-18" file-name="src/lib.rs" caption="`query`에 지정된 문자열이 줄에 포함되어 있는지 확인하는 기능 추가">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-18/src/lib.rs:here}}
```

</Listing>

현재는 기능을 점진적으로 구축하고 있다. 코드가 컴파일되려면 함수 시그니처에서 명시한 대로 본문에서 값을 반환해야 한다.


#### 매칭된 라인 저장하기

이 함수를 완성하려면 반환할 매칭된 라인을 저장할 방법이 필요하다. 이를 위해 `for` 루프 전에 변경 가능한 벡터를 만들고, `push` 메서드를 호출해 `line`을 벡터에 저장한다. `for` 루프가 끝나면 벡터를 반환한다. 아래 리스트 12-19에서 이를 확인할 수 있다.

<Listing number="12-19" file-name="src/lib.rs" caption="반환할 매칭된 라인 저장하기">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:here}}
```

</Listing>

이제 `search` 함수는 `query`를 포함하는 라인만 반환하며, 테스트는 통과할 것이다. 테스트를 실행해 보자:

```console
{{#include ../listings/ch12-an-io-project/listing-12-19/output.txt}}
```

테스트가 통과했으므로, 이제 이 함수가 잘 작동한다는 것을 알 수 있다!

이 시점에서, 테스트를 통과하면서 동일한 기능을 유지하며 `search` 함수의 구현을 리팩토링할 기회를 고려할 수 있다. `search` 함수의 코드는 나쁘지 않지만, 이터레이터의 유용한 기능을 충분히 활용하지는 못한다. 이 예제는 [13장][ch13-iterators]<!-- ignore -->에서 다시 다룰 것이다. 그곳에서 이터레이터를 자세히 살펴보고, 이 코드를 어떻게 개선할 수 있는지 알아볼 것이다.


#### `run` 함수에서 `search` 함수 사용하기

이제 `search` 함수가 정상적으로 동작하고 테스트를 마쳤으니, `run` 함수에서 `search`를 호출해야 한다. `config.query` 값과 `run` 함수가 파일에서 읽어온 `contents`를 `search` 함수에 전달한다. 그리고 `search` 함수가 반환한 각 줄을 `run` 함수에서 출력한다.

<span class="filename">파일명: src/lib.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/no-listing-02-using-search-in-run/src/lib.rs:here}}
```

`search` 함수에서 반환된 각 줄을 출력하기 위해 여전히 `for` 루프를 사용한다.

이제 전체 프로그램이 동작해야 한다! 먼저 Emily Dickinson의 시에서 정확히 한 줄을 반환해야 하는 단어인 _frog_로 테스트해 보자.

```console
{{#include ../listings/ch12-an-io-project/no-listing-02-using-search-in-run/output.txt}}
```

잘 동작한다! 이번에는 여러 줄과 일치하는 단어인 _body_로 테스트해 보자.

```console
{{#include ../listings/ch12-an-io-project/output-only-03-multiple-matches/output.txt}}
```

마지막으로, 시에 전혀 등장하지 않는 단어인 _monomorphization_으로 검색했을 때 아무런 결과가 나오지 않는지 확인해 보자.

```console
{{#include ../listings/ch12-an-io-project/output-only-04-no-matches/output.txt}}
```

훌륭하다! 우리는 고전적인 도구의 미니 버전을 직접 만들었고, 애플리케이션을 구조화하는 방법에 대해 많이 배웠다. 또한 파일 입출력, 라이프타임, 테스트, 커맨드라인 파싱에 대해서도 배웠다.

이 프로젝트를 마무리하기 위해, 환경 변수를 다루는 방법과 표준 에러로 출력하는 방법을 간단히 살펴볼 것이다. 이 두 가지는 커맨드라인 프로그램을 작성할 때 유용하게 사용된다.

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[ch11-anatomy]: ch11-01-writing-tests.html#the-anatomy-of-a-test-function
[ch10-lifetimes]: ch10-03-lifetime-syntax.html
[ch3-iter]: ch03-05-control-flow.html#looping-through-a-collection-with-for
[ch13-iterators]: ch13-02-iterators.html


