## 참조 순환으로 인한 메모리 누수

Rust의 메모리 안전성 보장은 실수로 정리되지 않는 메모리(일명 _메모리 누수_)를 생성하는 것을 어렵게 만들지만, 불가능하게 만들지는 않는다. Rust는 메모리 누수를 완전히 방지하는 것을 보장하지 않는다. 즉, 메모리 누수는 Rust에서 메모리 안전하다. `Rc<T>`와 `RefCell<T>`를 사용하면 Rust가 메모리 누수를 허용한다는 것을 확인할 수 있다. 아이템들이 서로 순환 참조를 하는 참조를 생성할 수 있다. 이렇게 되면 순환에 있는 각 아이템의 참조 카운트가 0에 도달하지 않아 값이 삭제되지 않으므로 메모리 누수가 발생한다.


### 참조 순환 생성

참조 순환이 어떻게 발생하는지, 그리고 이를 방지하는 방법을 살펴보자. 먼저 `List` 열거형과 `tail` 메서드를 정의한 코드를 Listing 15-25에서 확인할 수 있다.

<Listing number="15-25" file-name="src/main.rs" caption="`Cons` 변형이 참조하는 대상을 수정할 수 있도록 `RefCell<T>`를 포함한 cons 리스트 정의">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-25/src/main.rs}}
```

</Listing>

Listing 15-5에서 정의한 `List`의 변형을 사용한다. `Cons` 변형의 두 번째 요소는 이제 `RefCell<Rc<List>>`로, Listing 15-24에서 `i32` 값을 수정할 수 있었던 것과 달리 `Cons` 변형이 가리키는 `List` 값을 수정할 수 있다. 또한 `Cons` 변형이 있을 때 두 번째 항목에 쉽게 접근할 수 있도록 `tail` 메서드를 추가했다.

Listing 15-26에서는 Listing 15-25의 정의를 사용하는 `main` 함수를 추가한다. 이 코드는 `a`에 리스트를 생성하고, `a`의 리스트를 가리키는 `b` 리스트를 생성한다. 그런 다음 `a`의 리스트가 `b`를 가리키도록 수정하여 참조 순환을 만든다. 이 과정에서 참조 카운트를 확인할 수 있도록 `println!` 문을 추가했다.

<Listing number="15-26" file-name="src/main.rs" caption="두 `List` 값이 서로를 가리키는 참조 순환 생성">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-26/src/main.rs:here}}
```

</Listing>

`a` 변수에 `5, Nil`로 초기화된 `List` 값을 담은 `Rc<List>` 인스턴스를 생성한다. 그런 다음 `10`을 포함하고 `a`의 리스트를 가리키는 `List` 값을 담은 `Rc<List>` 인스턴스를 `b` 변수에 생성한다.

`a`가 `Nil` 대신 `b`를 가리키도록 수정하여 순환을 만든다. 이를 위해 `tail` 메서드를 사용해 `a`의 `RefCell<Rc<List>>`에 대한 참조를 얻고, 이를 `link` 변수에 저장한다. 그런 다음 `RefCell<Rc<List>>`의 `borrow_mut` 메서드를 사용해 `Nil` 값을 담은 `Rc<List>`에서 `b`의 `Rc<List>`로 값을 변경한다.

이 코드를 실행하면 (마지막 `println!`을 주석 처리한 상태에서) 다음과 같은 출력을 얻는다:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-26/output.txt}}
```

`a`의 리스트가 `b`를 가리키도록 변경한 후, `a`와 `b`의 `Rc<List>` 인스턴스의 참조 카운트는 모두 2가 된다. `main` 함수의 끝에서 Rust는 `b` 변수를 드롭하며, `b`의 `Rc<List>` 인스턴스의 참조 카운트를 2에서 1로 감소시킨다. 이 시점에서 `Rc<List>`가 힙에 가진 메모리는 드롭되지 않는다. 참조 카운트가 1이기 때문이다. 그런 다음 Rust는 `a`를 드롭하며, `a`의 `Rc<List>` 인스턴스의 참조 카운트도 2에서 1로 감소시킨다. 이 인스턴스의 메모리도 드롭되지 않는다. 다른 `Rc<List>` 인스턴스가 여전히 이를 참조하고 있기 때문이다. 리스트에 할당된 메모리는 영원히 회수되지 않는다. 이 참조 순환을 시각적으로 표현하기 위해 Figure 15-4의 다이어그램을 만들었다.

<img alt="Reference cycle of lists" src="img/trpl15-04.svg" class="center" />

<span class="caption">Figure 15-4: 서로를 가리키는 리스트 `a`와 `b`의 참조 순환</span>

마지막 `println!`의 주석을 해제하고 프로그램을 실행하면, Rust는 `a`가 `b`를 가리키고 `b`가 `a`를 가리키는 순환을 출력하려고 시도하다가 스택 오버플로가 발생한다.

실제 프로그램과 비교했을 때, 이 예제에서 참조 순환을 생성한 결과는 그리 심각하지 않다: 참조 순환을 생성한 직후 프로그램이 종료되기 때문이다. 하지만 더 복잡한 프로그램에서 순환을 통해 많은 메모리를 할당하고 오랫동안 유지한다면, 프로그램은 필요 이상의 메모리를 사용하게 되고 시스템에 과부하를 줄 수 있다. 이로 인해 사용 가능한 메모리가 부족해질 수 있다.

참조 순환을 만드는 것은 쉽지 않지만 불가능한 것도 아니다. `Rc<T>` 값을 포함하는 `RefCell<T>` 값이나 내부 가변성과 참조 카운팅을 가진 유사한 중첩 타입 조합을 사용한다면, 순환을 생성하지 않도록 주의해야 한다. Rust가 이를 알아채주길 기대할 수 없다. 참조 순환을 생성하는 것은 프로그램의 논리적 버그로, 자동화된 테스트, 코드 리뷰, 기타 소프트웨어 개발 관행을 통해 최소화해야 한다.

참조 순환을 피하는 또 다른 해결책은 데이터 구조를 재구성하여 일부 참조는 소유권을 표현하고 일부 참조는 소유권을 표현하지 않도록 하는 것이다. 그 결과, 소유 관계와 비소유 관계로 이루어진 순환을 만들 수 있으며, 오직 소유 관계만이 값이 드롭될 수 있는지 여부에 영향을 미친다. Listing 15-25에서는 항상 `Cons` 변형이 자신의 리스트를 소유하길 원하므로 데이터 구조를 재구성할 수 없다. 부모 노드와 자식 노드로 구성된 그래프를 사용해 비소유 관계가 참조 순환을 방지하는 적절한 방법이 되는 예제를 살펴보자.

<!-- Old link, do not remove -->

<a id="preventing-reference-cycles-turning-an-rct-into-a-weakt"></a>


### `Weak<T>`를 사용해 참조 순환 방지하기

지금까지 `Rc::clone`을 호출하면 `Rc<T>` 인스턴스의 `strong_count`가 증가하고, `strong_count`가 0이 되어야만 `Rc<T>` 인스턴스가 정리된다는 것을 확인했다. 또한 `Rc<T>` 인스턴스에 대한 참조를 `Rc::downgrade`에 전달하여 값에 대한 **약한 참조**를 만들 수 있다. 강한 참조는 `Rc<T>` 인스턴스의 소유권을 공유하는 방법이다. 약한 참조는 소유권 관계를 표현하지 않으며, 그 수가 `Rc<T>` 인스턴스의 정리 시점에 영향을 미치지 않는다. 약한 참조가 포함된 순환 구조는 강한 참조 카운트가 0이 되면 깨지기 때문에 참조 순환을 일으키지 않는다.

`Rc::downgrade`를 호출하면 `Weak<T>` 타입의 스마트 포인터를 얻는다. `Rc::downgrade`를 호출하면 `Rc<T>` 인스턴스의 `strong_count`가 1 증가하는 대신 `weak_count`가 1 증가한다. `Rc<T>` 타입은 `strong_count`와 유사하게 `weak_count`를 사용해 `Weak<T>` 참조의 수를 추적한다. 차이점은 `Rc<T>` 인스턴스가 정리되기 위해 `weak_count`가 0이 될 필요가 없다는 것이다.

`Weak<T>`가 참조하는 값은 이미 제거되었을 수 있기 때문에, `Weak<T>`가 가리키는 값으로 무언가를 하려면 값이 여전히 존재하는지 확인해야 한다. 이를 위해 `Weak<T>` 인스턴스에서 `upgrade` 메서드를 호출하면 `Option<Rc<T>>`를 반환한다. `Rc<T>` 값이 아직 제거되지 않았다면 `Some` 결과를 얻고, `Rc<T>` 값이 제거되었다면 `None` 결과를 얻는다. `upgrade`가 `Option<Rc<T>>`를 반환하기 때문에 Rust는 `Some`과 `None` 경우를 모두 처리하도록 보장하며, 유효하지 않은 포인터가 발생하지 않는다.

예를 들어, 각 항목이 다음 항목만 알고 있는 리스트를 사용하는 대신, 각 항목이 자식 항목과 부모 항목을 모두 알고 있는 트리를 만들어 보자.


#### 트리 데이터 구조 만들기: 자식 노드를 가진 `Node`

먼저, 자식 노드에 대한 정보를 알고 있는 노드로 트리를 만들어 보자. `Node`라는 구조체를 생성하고, 이 구조체는 `i32` 타입의 값을 가지며 자식 `Node`에 대한 참조도 포함한다.

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-27/src/main.rs:here}}
```

`Node`가 자식 노드를 소유하도록 하고, 이 소유권을 변수와 공유해 트리의 각 `Node`에 직접 접근할 수 있게 하려 한다. 이를 위해 `Vec<T>`의 항목을 `Rc<Node>` 타입의 값으로 정의한다. 또한 어떤 노드가 다른 노드의 자식인지 수정할 수 있도록 `children`에 `Vec<Rc<Node>>`를 감싸는 `RefCell<T>`를 사용한다.

다음으로, 이 구조체 정의를 사용해 `leaf`라는 이름의 `Node` 인스턴스를 생성한다. 이 인스턴스는 값 `3`을 가지며 자식 노드가 없다. 또 다른 인스턴스인 `branch`는 값 `5`를 가지고 `leaf`를 자식 노드 중 하나로 포함한다. 이는 Listing 15-27에 나와 있다.

<Listing number="15-27" file-name="src/main.rs" caption="자식 노드가 없는 `leaf` 노드와 `leaf`를 자식 노드로 가지는 `branch` 노드 생성">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-27/src/main.rs:there}}
```

</Listing>

`leaf`의 `Rc<Node>`를 복제해 `branch`에 저장한다. 이제 `leaf`의 `Node`는 `leaf`와 `branch` 두 소유자를 가지게 된다. `branch`에서 `branch.children`을 통해 `leaf`로 접근할 수 있지만, `leaf`에서 `branch`로 접근할 방법은 없다. 그 이유는 `leaf`가 `branch`에 대한 참조를 가지고 있지 않으며, 둘이 관련되어 있다는 것을 모르기 때문이다. 다음으로 `leaf`가 `branch`가 부모 노드임을 알 수 있도록 해 보자.


#### 자식 노드에서 부모 노드로의 참조 추가하기

자식 노드가 부모 노드를 인식할 수 있도록 하려면 `Node` 구조체 정의에 `parent` 필드를 추가해야 한다. 여기서 문제는 `parent`의 타입을 어떻게 정할지 결정하는 것이다. `Rc<T>`를 사용할 수는 없다. 왜냐하면 `leaf.parent`가 `branch`를 가리키고 `branch.children`가 `leaf`를 가리키는 참조 순환을 만들기 때문이다. 이렇게 되면 `strong_count` 값이 절대 0이 되지 않는다.

관계를 다른 방식으로 생각해보면, 부모 노드는 자식 노드를 소유해야 한다. 즉, 부모 노드가 제거되면 자식 노드도 함께 제거되어야 한다. 그러나 자식 노드는 부모 노드를 소유해서는 안 된다. 자식 노드를 제거하더라도 부모 노드는 여전히 존재해야 한다. 이 경우 약한 참조(weak reference)를 사용해야 한다!

따라서 `Rc<T>` 대신 `parent`의 타입으로 `Weak<T>`, 구체적으로는 `RefCell<Weak<Node>>`를 사용한다. 이제 `Node` 구조체 정의는 다음과 같다:

<span class="filename">파일명: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-28/src/main.rs:here}}
```

이제 노드는 부모 노드를 참조할 수 있지만, 부모 노드를 소유하지는 않는다. Listing 15-28에서 `main` 함수를 업데이트하여 `leaf` 노드가 부모 노드인 `branch`를 참조할 수 있도록 한다.

<Listing number="15-28" file-name="src/main.rs" caption="부모 노드 `branch`에 대한 약한 참조를 가진 `leaf` 노드">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-28/src/main.rs:there}}
```

</Listing>

`leaf` 노드를 생성하는 부분은 Listing 15-27과 비슷하지만, `parent` 필드가 추가되었다. `leaf`는 처음에 부모가 없으므로 새로운 빈 `Weak<Node>` 참조 인스턴스를 생성한다.

이 시점에서 `leaf`의 부모에 대한 참조를 얻기 위해 `upgrade` 메서드를 사용하면 `None` 값을 반환한다. 첫 번째 `println!` 문의 출력에서 이를 확인할 수 있다:

```text
leaf parent = None
```

`branch` 노드를 생성할 때도 `parent` 필드에 새로운 `Weak<Node>` 참조가 추가된다. 왜냐하면 `branch`는 부모 노드가 없기 때문이다. 여전히 `branch`의 자식 중 하나로 `leaf`가 있다. `branch`에 `Node` 인스턴스를 생성한 후, `leaf`를 수정하여 부모에 대한 `Weak<Node>` 참조를 추가한다. `leaf`의 `parent` 필드에 있는 `RefCell<Weak<Node>>`에 `borrow_mut` 메서드를 사용하고, `branch`의 `Rc<Node>`에서 `Rc::downgrade` 함수를 사용해 `branch`에 대한 `Weak<Node>` 참조를 생성한다.

이제 `leaf`의 부모를 다시 출력하면, 이번에는 `branch`를 담고 있는 `Some` 변형이 반환된다. 이제 `leaf`는 부모에 접근할 수 있다! `leaf`를 출력할 때, Listing 15-26에서 발생했던 스택 오버플로우로 이어지는 순환을 피할 수 있다. `Weak<Node>` 참조는 `(Weak)`로 출력된다:

```text
leaf parent = Some(Node { value: 5, parent: RefCell { value: (Weak) },
children: RefCell { value: [Node { value: 3, parent: RefCell { value: (Weak) },
children: RefCell { value: [] } }] } })
```

무한 출력이 발생하지 않는다는 것은 이 코드가 참조 순환을 만들지 않았음을 의미한다. 또한 `Rc::strong_count`와 `Rc::weak_count`를 호출해 반환된 값을 확인함으로써 이를 확인할 수 있다.


#### `strong_count`와 `weak_count` 변화 시각화

`Rc<Node>` 인스턴스의 `strong_count`와 `weak_count` 값이 어떻게 변하는지 확인하기 위해, 새로운 내부 스코프를 만들고 `branch` 생성 부분을 그 안으로 옮겨보자. 이렇게 하면 `branch`가 생성된 후 스코프를 벗어나면서 삭제될 때 어떤 일이 발생하는지 관찰할 수 있다. 이 변경 사항은 Listing 15-29에 나와 있다.

<Listing number="15-29" file-name="src/main.rs" caption="내부 스코프에서 `branch`를 생성하고 강한 참조와 약한 참조 카운트 확인">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-29/src/main.rs:here}}
```

</Listing>

`leaf`가 생성된 후, `Rc<Node>`는 `strong_count`가 1이고 `weak_count`가 0이다. 내부 스코프에서 `branch`를 생성하고 `leaf`와 연결하면, 카운트를 출력할 때 `branch`의 `Rc<Node>`는 `strong_count`가 1이고 `weak_count`가 1이 된다(`leaf.parent`가 `Weak<Node>`를 사용해 `branch`를 가리키기 때문). `leaf`의 카운트를 출력하면 `strong_count`가 2인 것을 확인할 수 있다. 이는 `branch`가 `branch.children`에 `leaf`의 `Rc<Node>` 복사본을 저장했기 때문이다. 하지만 `weak_count`는 여전히 0이다.

내부 스코프가 끝나면 `branch`가 스코프를 벗어나고, `Rc<Node>`의 `strong_count`가 0으로 감소한다. 이로 인해 `Node`가 삭제된다. `leaf.parent`의 `weak_count`가 1이더라도 `Node`가 삭제되는 데는 영향을 미치지 않으므로 메모리 누수가 발생하지 않는다.

스코프가 끝난 후 `leaf`의 부모에 접근하려고 하면 다시 `None`을 얻게 된다. 프로그램이 끝날 때 `leaf`의 `Rc<Node>`는 `strong_count`가 1이고 `weak_count`가 0이다. 이는 `leaf` 변수가 다시 `Rc<Node>`의 유일한 참조이기 때문이다.

카운트 관리와 값 삭제를 위한 모든 로직은 `Rc<T>`와 `Weak<T>` 그리고 `Drop` 트레이트의 구현에 내장되어 있다. `Node` 정의에서 자식에서 부모로의 관계를 `Weak<T>` 참조로 지정함으로써, 부모 노드가 자식 노드를 가리키고 그 반대도 가능하게 하면서도 참조 순환과 메모리 누수를 방지할 수 있다.


## 요약

이 장에서는 스마트 포인터를 사용해 일반 참조와는 다른 보장과 트레이드오프를 만드는 방법을 다뤘다. `Box<T>` 타입은 크기가 정해져 있으며 힙에 할당된 데이터를 가리킨다. `Rc<T>` 타입은 힙에 있는 데이터에 대한 참조 개수를 추적해 데이터가 여러 소유자를 가질 수 있게 한다. `RefCell<T>` 타입은 내부 가변성을 제공해 불변 타입이 필요하지만 그 타입의 내부 값을 변경해야 할 때 사용할 수 있다. 또한 빌림 규칙을 컴파일 타임이 아닌 런타임에 강제한다.

스마트 포인터의 많은 기능을 가능하게 하는 `Deref`와 `Drop` 트레이트도 살펴봤다. 메모리 누수를 일으킬 수 있는 참조 순환과 이를 `Weak<T>`를 사용해 방지하는 방법도 탐구했다.

이 장이 흥미를 끌어 직접 스마트 포인터를 구현해 보고 싶다면 ["The Rustonomicon"][nomicon]을 참고해 더 유용한 정보를 얻을 수 있다.

다음 장에서는 Rust의 동시성에 대해 이야기할 것이다. 몇 가지 새로운 스마트 포인터도 배울 예정이다.

[nomicon]: ../nomicon/index.html


