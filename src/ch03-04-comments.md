## 주석

모든 프로그래머는 자신의 코드를 이해하기 쉽게 만들기 위해 노력하지만, 때로는 추가적인 설명이 필요하다. 이럴 때 프로그래머는 소스 코드에 _주석_을 남긴다. 주석은 컴파일러는 무시하지만, 소스 코드를 읽는 사람들에게 유용한 정보를 제공한다.

다음은 간단한 주석의 예시다:

```rust
// hello, world
```

Rust에서 관용적으로 사용하는 주석 스타일은 두 개의 슬래시(`//`)로 시작하며, 주석은 해당 줄의 끝까지 이어진다. 여러 줄에 걸친 주석을 작성하려면 각 줄마다 `//`를 포함해야 한다:

```rust
// 여기서는 복잡한 작업을 수행하고 있습니다. 이 작업은
// 여러 줄의 주석이 필요할 정도로 길죠! 흠! 이 주석이
// 무슨 일이 벌어지고 있는지 설명해 주길 바랍니다.
```

주석은 코드가 있는 줄의 끝에도 추가할 수 있다:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-24-comments-end-of-line/src/main.rs}}
```

하지만 주석은 보통 해당 코드 위에 별도의 줄로 작성하는 형식을 더 자주 볼 수 있다:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-25-comments-above-line/src/main.rs}}
```

Rust에는 또 다른 종류의 주석인 문서 주석도 있다. 이에 대해서는 14장의 ["Publishing a Crate to Crates.io"][publishing]<!-- ignore --> 섹션에서 다룬다.

[publishing]: ch14-02-publishing-to-crates-io.html


