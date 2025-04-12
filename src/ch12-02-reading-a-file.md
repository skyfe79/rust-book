## 파일 읽기

이제 `file_path` 인자로 지정된 파일을 읽는 기능을 추가한다. 먼저 테스트할 샘플 파일이 필요하다. 여러 줄에 걸쳐 적은 양의 텍스트가 있고, 반복되는 단어가 포함된 파일을 사용할 것이다. 리스팅 12-3은 에밀리 디킨슨의 시로, 테스트에 적합하다! 프로젝트 루트 레벨에 _poem.txt_ 파일을 생성하고 "I'm Nobody! Who are you?"라는 시를 입력한다.

<Listing number="12-3" file-name="poem.txt" caption="에밀리 디킨슨의 시는 좋은 테스트 케이스가 된다.">

```text
{{#include ../listings/ch12-an-io-project/listing-12-03/poem.txt}}
```

</Listing>

텍스트를 입력한 후, _src/main.rs_ 파일을 편집하여 리스팅 12-4와 같이 파일을 읽는 코드를 추가한다.

<Listing number="12-4" file-name="src/main.rs" caption="두 번째 인자로 지정된 파일의 내용을 읽는다">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-04/src/main.rs:here}}
```

</Listing>

먼저 `use` 문을 사용해 표준 라이브러리의 관련 부분을 가져온다. 파일을 다루기 위해 `std::fs`가 필요하다.

`main` 함수에서 `fs::read_to_string`은 `file_path`를 받아 해당 파일을 열고, 파일 내용을 포함한 `std::io::Result<String>` 타입의 값을 반환한다.

그 후, 파일을 읽은 후 `contents`의 값을 출력하기 위해 임시로 `println!` 문을 추가한다. 이를 통해 프로그램이 제대로 동작하는지 확인할 수 있다.

아직 검색 기능을 구현하지 않았으므로, 첫 번째 커맨드라인 인자로 아무 문자열을 넣고, 두 번째 인자로 _poem.txt_ 파일을 지정해 이 코드를 실행해 보자:

```console
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-04/output.txt}}
```

잘 동작한다! 코드가 파일의 내용을 읽고 출력했다. 하지만 이 코드에는 몇 가지 문제가 있다. 현재 `main` 함수는 여러 가지 책임을 지고 있다. 일반적으로 각 함수가 하나의 개념만 담당하면 코드가 더 명확하고 유지보수하기 쉬워진다. 또 다른 문제는 에러 처리가 충분히 잘 이루어지지 않는다는 점이다. 프로그램이 아직 작기 때문에 이 문제가 크게 부각되지는 않지만, 프로그램이 커지면 깔끔하게 수정하기가 더 어려워진다. 프로그램을 개발할 때는 초기부터 리팩토링을 시작하는 것이 좋다. 코드 양이 적을 때 리팩토링하는 것이 훨씬 쉽기 때문이다. 다음 단계에서 이를 진행할 것이다.


