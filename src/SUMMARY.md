# Rust 프로그래밍 언어

[Rust 프로그래밍 언어](title-page.md)  
[서문](foreword.md)  
[소개](ch00-00-introduction.md)


## 시작하기

- [시작하기](ch01-00-getting-started.md)
  - [설치](ch01-01-installation.md)
  - [Hello, World!](ch01-02-hello-world.md)
  - [Hello, Cargo!](ch01-03-hello-cargo.md)

- [숫자 맞추기 게임 프로그래밍](ch02-00-guessing-game-tutorial.md)

- [일반적인 프로그래밍 개념](ch03-00-common-programming-concepts.md)
  - [변수와 가변성](ch03-01-variables-and-mutability.md)
  - [데이터 타입](ch03-02-data-types.md)
  - [함수](ch03-03-how-functions-work.md)
  - [주석](ch03-04-comments.md)
  - [제어 흐름](ch03-05-control-flow.md)

- [소유권 이해하기](ch04-00-understanding-ownership.md)
  - [소유권이란?](ch04-01-what-is-ownership.md)
  - [참조와 빌림](ch04-02-references-and-borrowing.md)
  - [슬라이스 타입](ch04-03-slices.md)

- [관련 데이터를 구조화하기 위해 구조체 사용하기](ch05-00-structs.md)
  - [구조체 정의와 인스턴스화](ch05-01-defining-structs.md)
  - [구조체를 사용한 예제 프로그램](ch05-02-example-structs.md)
  - [메서드 문법](ch05-03-method-syntax.md)

- [열거형과 패턴 매칭](ch06-00-enums.md)
  - [열거형 정의하기](ch06-01-defining-an-enum.md)
  - [`match` 제어 흐름 구조](ch06-02-match.md)
  - [`if let`과 `let else`를 사용한 간결한 제어 흐름](ch06-03-if-let.md)


## Rust 프로그래밍 기초

- [패키지, 크레이트, 모듈로 프로젝트 관리하기](ch07-00-managing-growing-projects-with-packages-crates-and-modules.md)
  - [패키지와 크레이트](ch07-01-packages-and-crates.md)
  - [모듈 정의로 스코프와 접근 제어 관리하기](ch07-02-defining-modules-to-control-scope-and-privacy.md)
  - [모듈 트리 내 아이템 참조 경로](ch07-03-paths-for-referring-to-an-item-in-the-module-tree.md)
  - [`use` 키워드로 경로를 스코프로 가져오기](ch07-04-bringing-paths-into-scope-with-the-use-keyword.md)
  - [모듈을 다른 파일로 분리하기](ch07-05-separating-modules-into-different-files.md)

- [컬렉션 다루기](ch08-00-common-collections.md)
  - [벡터로 값 목록 저장하기](ch08-01-vectors.md)
  - [UTF-8 인코딩 텍스트를 문자열로 저장하기](ch08-02-strings.md)
  - [해시 맵으로 키와 연관된 값 저장하기](ch08-03-hash-maps.md)

- [에러 처리](ch09-00-error-handling.md)
  - [`panic!`으로 복구 불가능한 에러 처리하기](ch09-01-unrecoverable-errors-with-panic.md)
  - [`Result`로 복구 가능한 에러 처리하기](ch09-02-recoverable-errors-with-result.md)
  - [`panic!`을 사용할지 말지 결정하기](ch09-03-to-panic-or-not-to-panic.md)

- [제네릭 타입, 트레이트, 라이프타임](ch10-00-generics.md)
  - [제네릭 데이터 타입](ch10-01-syntax.md)
  - [트레이트: 공유 동작 정의하기](ch10-02-traits.md)
  - [라이프타임으로 참조 유효성 검사하기](ch10-03-lifetime-syntax.md)

- [자동화된 테스트 작성하기](ch11-00-testing.md)
  - [테스트 작성 방법](ch11-01-writing-tests.md)
  - [테스트 실행 방식 제어하기](ch11-02-running-tests.md)
  - [테스트 조직화](ch11-03-test-organization.md)

- [I/O 프로젝트: 커맨드라인 프로그램 만들기](ch12-00-an-io-project.md)
  - [커맨드라인 인수 받기](ch12-01-accepting-command-line-arguments.md)
  - [파일 읽기](ch12-02-reading-a-file.md)
  - [모듈성과 에러 처리를 개선하기 위한 리팩토링](ch12-03-improving-error-handling-and-modularity.md)
  - [테스트 주도 개발로 라이브러리 기능 확장하기](ch12-04-testing-the-librarys-functionality.md)
  - [환경 변수 다루기](ch12-05-working-with-environment-variables.md)
  - [에러 메시지를 표준 출력 대신 표준 에러로 출력하기](ch12-06-writing-to-stderr-instead-of-stdout.md)


## Rust로 생각하기

- [함수형 언어 기능: 이터레이터와 클로저](ch13-00-functional-features.md)
  - [클로저: 환경을 캡처하는 익명 함수](ch13-01-closures.md)
  - [일련의 항목을 이터레이터로 처리하기](ch13-02-iterators.md)
  - [I/O 프로젝트 개선하기](ch13-03-improving-our-io-project.md)
  - [성능 비교: 루프 vs 이터레이터](ch13-04-performance.md)

- [Cargo와 Crates.io에 대한 추가 정보](ch14-00-more-about-cargo.md)
  - [릴리스 프로필로 빌드 커스터마이징](ch14-01-release-profiles.md)
  - [Crates.io에 크레이트 게시하기](ch14-02-publishing-to-crates-io.md)
  - [Cargo 작업 공간](ch14-03-cargo-workspaces.md)
  - [`cargo install`로 Crates.io에서 바이너리 설치하기](ch14-04-installing-binaries.md)
  - [커스텀 커맨드로 Cargo 확장하기](ch14-05-extending-cargo.md)

- [스마트 포인터](ch15-00-smart-pointers.md)
  - [`Box<T>`로 힙 데이터 가리키기](ch15-01-box.md)
  - [`Deref`로 스마트 포인터를 일반 참조처럼 다루기](ch15-02-deref.md)
  - [`Drop` 트레이트로 정리 시 코드 실행하기](ch15-03-drop.md)
  - [`Rc<T>`, 참조 카운트 스마트 포인터](ch15-04-rc.md)
  - [`RefCell<T>`와 내부 가변성 패턴](ch15-05-interior-mutability.md)
  - [참조 순환으로 인한 메모리 누수](ch15-06-reference-cycles.md)

- [두려움 없는 동시성](ch16-00-concurrency.md)
  - [스레드를 사용해 코드 동시 실행하기](ch16-01-threads.md)
  - [메시지 전달로 스레드 간 데이터 전송하기](ch16-02-message-passing.md)
  - [공유 상태 동시성](ch16-03-shared-state.md)
  - [`Send`와 `Sync` 트레이트로 확장 가능한 동시성](ch16-04-extensible-concurrency-sync-and-send.md)

- [비동기 프로그래밍의 기초: Async, Await, Futures, Streams](ch17-00-async-await.md)
  - [Futures와 Async 문법](ch17-01-futures-and-syntax.md)
  - [Async로 동시성 적용하기](ch17-02-concurrency-with-async.md)
  - [여러 Futures 다루기](ch17-03-more-futures.md)
  - [Streams: 순차적인 Futures](ch17-04-streams.md)
  - [Async 트레이트 자세히 살펴보기](ch17-05-traits-for-async.md)
  - [Futures, Tasks, Threads](ch17-06-futures-tasks-threads.md)

- [Rust의 객체 지향 프로그래밍 기능](ch18-00-oop.md)
  - [객체 지향 언어의 특징](ch18-01-what-is-oo.md)
  - [다양한 타입의 값을 허용하는 트레이트 객체 사용하기](ch18-02-trait-objects.md)
  - [객체 지향 디자인 패턴 구현하기](ch18-03-oo-design-patterns.md)


## 고급 주제

- [패턴과 매칭](ch19-00-patterns.md)
  - [패턴을 사용할 수 있는 모든 곳](ch19-01-all-the-places-for-patterns.md)
  - [반증 가능성: 패턴이 매칭에 실패할 가능성](ch19-02-refutability.md)
  - [패턴 문법](ch19-03-pattern-syntax.md)

- [고급 기능](ch20-00-advanced-features.md)
  - [안전하지 않은 Rust](ch20-01-unsafe-rust.md)
  - [고급 트레이트](ch20-02-advanced-traits.md)
  - [고급 타입](ch20-03-advanced-types.md)
  - [고급 함수와 클로저](ch20-04-advanced-functions-and-closures.md)
  - [매크로](ch20-05-macros.md)

- [최종 프로젝트: 멀티스레드 웹 서버 구축](ch21-00-final-project-a-web-server.md)
  - [단일 스레드 웹 서버 구축](ch21-01-single-threaded.md)
  - [단일 스레드 서버를 멀티스레드 서버로 변환](ch21-02-multithreaded.md)
  - [우아한 종료와 정리](ch21-03-graceful-shutdown-and-cleanup.md)

- [부록](appendix-00.md)
  - [A - 키워드](appendix-01-keywords.md)
  - [B - 연산자와 기호](appendix-02-operators.md)
  - [C - 파생 가능한 트레이트](appendix-03-derivable-traits.md)
  - [D - 유용한 개발 도구](appendix-04-useful-development-tools.md)
  - [E - 에디션](appendix-05-editions.md)
  - [F - 책의 번역](appendix-06-translation.md)
  - [G - Rust의 제작 과정과 "Nightly Rust"](appendix-07-nightly-rust.md)


