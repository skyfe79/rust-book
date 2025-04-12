## 클린업 코드 실행을 위한 `Drop` 트레이트

스마트 포인터 패턴에서 중요한 두 번째 트레이트는 `Drop`이다. 이 트레이트를 통해 값이 스코프를 벗어날 때 실행될 코드를 커스터마이즈할 수 있다. 어떤 타입이든 `Drop` 트레이트를 구현할 수 있으며, 이 코드를 통해 파일이나 네트워크 연결과 같은 리소스를 해제할 수 있다.

`Drop` 트레이트의 기능은 스마트 포인터를 구현할 때 거의 항상 사용되기 때문에, 스마트 포인터의 맥락에서 `Drop`을 소개한다. 예를 들어, `Box<T>`가 드롭되면 힙에 할당된 공간을 해제한다.

일부 언어에서는 특정 타입의 인스턴스를 사용한 후에 프로그래머가 직접 메모리나 리소스를 해제하는 코드를 호출해야 한다. 파일 핸들, 소켓, 락 등이 그 예시다. 만약 이를 잊어버리면 시스템이 과부하를 겪고 충돌할 수 있다. Rust에서는 값이 스코프를 벗어날 때 특정 코드가 실행되도록 지정할 수 있으며, 컴파일러가 이 코드를 자동으로 삽입한다. 결과적으로 특정 타입의 인스턴스 사용이 끝난 후 클린업 코드를 프로그램 전체에 신경 쓸 필요가 없다. 그래도 리소스가 누수되지 않는다!

`Drop` 트레이트를 구현하면 값이 스코프를 벗어날 때 실행될 코드를 지정할 수 있다. `Drop` 트레이트는 `self`에 대한 가변 참조를 받는 `drop`이라는 메서드를 하나 구현해야 한다. Rust가 `drop`을 호출하는 시점을 확인하기 위해, 일단 `println!` 문을 사용해 `drop`을 구현해 보자.

리스트 15-14는 `CustomSmartPointer`라는 구조체를 보여준다. 이 구조체의 유일한 커스텀 기능은 인스턴스가 스코프를 벗어날 때 `Dropping CustomSmartPointer!`를 출력하는 것이다. 이를 통해 Rust가 `drop` 메서드를 실행하는 시점을 확인할 수 있다.

<Listing number="15-14" file-name="src/main.rs" caption="클린업 코드를 넣을 `Drop` 트레이트를 구현한 `CustomSmartPointer` 구조체">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-14/src/main.rs}}
```

</Listing>

`Drop` 트레이트는 프렐루드에 포함되어 있으므로 스코프로 가져올 필요가 없다. `CustomSmartPointer`에 `Drop` 트레이트를 구현하고 `println!`을 호출하는 `drop` 메서드를 제공한다. `drop` 메서드의 본문은 타입의 인스턴스가 스코프를 벗어날 때 실행하고 싶은 로직을 넣는 곳이다. 여기서는 Rust가 `drop`을 호출하는 시점을 시각적으로 확인하기 위해 텍스트를 출력한다.

`main` 함수에서 `CustomSmartPointer`의 두 인스턴스를 생성한 후 `CustomSmartPointers created`를 출력한다. `main` 함수가 끝나면 `CustomSmartPointer`의 인스턴스가 스코프를 벗어나고, Rust는 `drop` 메서드에 넣은 코드를 호출해 최종 메시지를 출력한다. 여기서 `drop` 메서드를 명시적으로 호출할 필요는 없다.

이 프로그램을 실행하면 다음과 같은 출력을 볼 수 있다:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-14/output.txt}}
```

Rust는 인스턴스가 스코프를 벗어날 때 자동으로 `drop`을 호출해 우리가 지정한 코드를 실행했다. 변수는 생성된 순서의 역순으로 드롭되므로 `d`가 `c`보다 먼저 드롭된다. 이 예제의 목적은 `drop` 메서드가 어떻게 동작하는지 시각적으로 보여주는 것이다. 보통은 출력 메시지 대신 타입이 필요로 하는 클린업 코드를 지정한다.

<!-- Old link, do not remove -->

<a id="dropping-a-value-early-with-std-mem-drop"></a>

안타깝게도 자동 `drop` 기능을 비활성화하는 것은 간단하지 않다. `drop`을 비활성화할 필요는 거의 없다. `Drop` 트레이트의 핵심은 자동으로 처리된다는 점이다. 하지만 가끔은 값을 조기에 클린업하고 싶을 때가 있다. 예를 들어, 락을 관리하는 스마트 포인터를 사용할 때 락을 해제하는 `drop` 메서드를 강제로 호출해 동일한 스코프의 다른 코드가 락을 획득할 수 있도록 하고 싶을 수 있다. Rust는 `Drop` 트레이트의 `drop` 메서드를 수동으로 호출할 수 없게 한다. 대신, 스코프가 끝나기 전에 값을 강제로 드롭하고 싶다면 표준 라이브러리에서 제공하는 `std::mem::drop` 함수를 호출해야 한다.

리스트 15-14의 `main` 함수를 수정해 `Drop` 트레이트의 `drop` 메서드를 수동으로 호출하려고 하면, 리스트 15-15와 같이 컴파일러 에러가 발생한다.

<Listing number="15-15" file-name="src/main.rs" caption="조기에 클린업하기 위해 `Drop` 트레이트의 `drop` 메서드를 수동으로 호출하려는 시도">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-15/src/main.rs:here}}
```

</Listing>

이 코드를 컴파일하려고 하면 다음과 같은 에러가 발생한다:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-15/output.txt}}
```

이 에러 메시지는 `drop`을 명시적으로 호출할 수 없다고 알려준다. 에러 메시지는 _destructor_라는 용어를 사용하는데, 이는 인스턴스를 클린업하는 함수를 일반적으로 지칭하는 프로그래밍 용어다. _destructor_는 인스턴스를 생성하는 _constructor_와 유사하다. Rust의 `drop` 함수는 특정한 destructor이다.

Rust는 `drop`을 명시적으로 호출할 수 없게 한다. 왜냐하면 Rust는 여전히 `main` 함수가 끝날 때 값에 대해 자동으로 `drop`을 호출하기 때문이다. 이로 인해 Rust가 동일한 값을 두 번 클린업하려고 시도하면서 _double free_ 에러가 발생할 수 있다.

값이 스코프를 벗어날 때 `drop`이 자동으로 삽입되는 것을 비활성화할 수 없고, `drop` 메서드를 명시적으로 호출할 수도 없다. 따라서 값을 조기에 클린업해야 한다면 `std::mem::drop` 함수를 사용해야 한다.

`std::mem::drop` 함수는 `Drop` 트레이트의 `drop` 메서드와 다르다. 강제로 드롭할 값을 인자로 전달해 호출한다. 이 함수는 프렐루드에 포함되어 있으므로, 리스트 15-15의 `main` 함수를 수정해 `drop` 함수를 호출할 수 있다. 리스트 15-16에서 이를 확인할 수 있다.

<Listing number="15-16" file-name="src/main.rs" caption="스코프가 끝나기 전에 값을 명시적으로 드롭하기 위해 `std::mem::drop` 호출">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-16/src/main.rs:here}}
```

</Listing>

이 코드를 실행하면 다음과 같은 출력이 나타난다:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-16/output.txt}}
```

`CustomSmartPointer created.`와 `CustomSmartPointer dropped before the end of main.` 텍스트 사이에 ``Dropping CustomSmartPointer with data `some data`!``가 출력되어, `drop` 메서드 코드가 그 시점에 `c`를 드롭하기 위해 호출되었음을 보여준다.

`Drop` 트레이트 구현에서 지정한 코드는 클린업을 편리하고 안전하게 만드는 다양한 방법으로 사용할 수 있다. 예를 들어, 자신만의 메모리 할당자를 만드는 데 사용할 수도 있다! `Drop` 트레이트와 Rust의 소유권 시스템 덕분에 클린업을 기억할 필요가 없다. Rust가 자동으로 처리해준다.

또한 여전히 사용 중인 값을 실수로 클린업해 발생하는 문제에 대해 걱정할 필요도 없다. 참조가 항상 유효하도록 보장하는 소유권 시스템은 값이 더 이상 사용되지 않을 때 `drop`이 한 번만 호출되도록 보장한다.

이제 `Box<T>`와 스마트 포인터의 몇 가지 특성을 살펴봤으니, 표준 라이브러리에 정의된 다른 스마트 포인터들을 살펴보자.


