## Cargo를 커스텀 커맨드로 확장하기

Cargo는 수정 없이도 새로운 서브커맨드로 확장할 수 있도록 설계되었다. `$PATH`에 있는 바이너리 파일의 이름이 `cargo-something`이라면, `cargo something`을 실행하여 Cargo 서브커맨드처럼 사용할 수 있다. 이러한 커스텀 커맨드는 `cargo --list`를 실행할 때도 함께 표시된다. `cargo install`을 사용해 확장 기능을 설치하고, 내장된 Cargo 도구처럼 실행할 수 있다는 점은 Cargo 설계의 큰 장점이다!


## 요약

Cargo와 [crates.io](https://crates.io/)를 통해 코드를 공유하는 것은 Rust 생태계가 다양한 작업에 유용하게 활용될 수 있는 중요한 부분이다. Rust의 표준 라이브러리는 작고 안정적이지만, crates는 언어와는 다른 속도로 쉽게 공유하고 사용하며 개선할 수 있다. 여러분에게 유용한 코드를 [crates.io](https://crates.io/)에 공유하는 것을 주저하지 말자. 그 코드가 다른 누군가에게도 유용할 가능성이 크다!


