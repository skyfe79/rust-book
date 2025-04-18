# I/O 프로젝트: 커맨드라인 프로그램 만들기

이번 장은 지금까지 배운 다양한 기술을 복습하고, 몇 가지 표준 라이브러리 기능을 더 탐구해 보는 시간이다. 파일과 커맨드라인 입출력을 다루는 도구를 만들어 보며, Rust 개념을 실제로 적용해 볼 것이다.

Rust는 빠른 속도, 안전성, 단일 바이너리 출력, 그리고 크로스 플랫폼 지원 덕분에 커맨드라인 도구를 만들기에 이상적인 언어다. 이번 프로젝트에서는 고전적인 검색 도구인 `grep`(**g**lobally search a **r**egular **e**xpression and **p**rint)의 간단한 버전을 만들어 볼 것이다. 가장 기본적인 사용법에서 `grep`은 지정된 파일에서 특정 문자열을 찾는다. 이를 위해 `grep`은 파일 경로와 문자열을 인자로 받는다. 그런 다음 파일을 읽어서 해당 문자열이 포함된 줄을 찾고, 그 줄을 출력한다.

이 과정에서 다른 커맨드라인 도구들이 사용하는 터미널 기능을 어떻게 활용하는지 알아볼 것이다. 사용자가 도구의 동작을 설정할 수 있도록 환경 변수의 값을 읽어오는 방법도 배울 것이다. 또한 오류 메시지를 표준 출력(`stdout`) 대신 표준 에러 스트림(`stderr`)에 출력하는 방법을 알아볼 것이다. 이렇게 하면 사용자가 성공적인 출력을 파일로 리다이렉트하면서도 화면에 오류 메시지를 계속 볼 수 있다.

Rust 커뮤니티의 한 멤버인 Andrew Gallant는 이미 `ripgrep`이라는 완전한 기능을 갖춘 매우 빠른 `grep` 버전을 만들었다. 우리가 만드는 버전은 상대적으로 단순하지만, 이번 장을 통해 `ripgrep` 같은 실제 프로젝트를 이해하는 데 필요한 배경 지식을 얻을 수 있을 것이다.

우리의 `grep` 프로젝트는 지금까지 배운 여러 개념을 종합적으로 활용할 것이다:

- 코드 조직화 ([7장][ch7]<!-- ignore -->)
- 벡터와 문자열 사용 ([8장][ch8]<!-- ignore -->)
- 오류 처리 ([9장][ch9]<!-- ignore -->)
- 적절한 상황에서 트레이트와 라이프타임 사용 ([10장][ch10]<!-- ignore -->)
- 테스트 작성 ([11장][ch11]<!-- ignore -->)

또한 클로저, 이터레이터, 트레이트 객체에 대해 간략히 소개할 것이다. 이 주제들은 [13장][ch13]<!-- ignore -->과 [18장][ch18]<!-- ignore -->에서 자세히 다룰 예정이다.

[ch7]: ch07-00-managing-growing-projects-with-packages-crates-and-modules.html
[ch8]: ch08-00-common-collections.html
[ch9]: ch09-00-error-handling.html
[ch10]: ch10-00-generics.html
[ch11]: ch11-00-testing.html
[ch13]: ch13-00-functional-features.html
[ch18]: ch18-00-oop.html


