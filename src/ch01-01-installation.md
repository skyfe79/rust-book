## 설치

첫 번째 단계는 Rust를 설치하는 것이다. Rust 버전과 관련 도구를 관리하는 커맨드라인 도구인 `rustup`을 통해 Rust를 다운로드한다. 다운로드를 위해 인터넷 연결이 필요하다.

> 참고: 특정 이유로 `rustup`을 사용하지 않으려면 [다른 Rust 설치 방법 페이지][otherinstall]에서 추가 옵션을 확인할 수 있다.

다음 단계는 Rust 컴파일러의 최신 안정 버전을 설치하는 것이다. Rust의 안정성 보장은 이 책의 예제가 새로운 Rust 버전에서도 계속 컴파일될 것임을 의미한다. Rust가 에러 메시지와 경고를 지속적으로 개선하기 때문에 출력 결과가 버전 간에 약간 다를 수 있다. 즉, 이 단계를 통해 설치한 최신 안정 버전의 Rust는 이 책의 내용과 호환될 것이다.

> ### 커맨드라인 표기법
>
> 이 장과 책 전체에서 터미널에서 사용하는 몇 가지 커맨드를 보여준다. 터미널에 입력해야 하는 줄은 모두 `$`로 시작한다. `$` 문자를 입력할 필요는 없으며, 이는 각 커맨드의 시작을 나타내는 커맨드라인 프롬프트다. `$`로 시작하지 않는 줄은 일반적으로 이전 커맨드의 출력을 보여준다. 또한 PowerShell 전용 예제는 `$` 대신 `>`를 사용한다.


### Linux 또는 macOS에서 `rustup` 설치하기

Linux나 macOS를 사용 중이라면, 터미널을 열고 다음 커맨드를 입력한다:

```console
$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
```

이 커맨드는 스크립트를 다운로드하고 `rustup` 도구의 설치를 시작한다. `rustup`은 Rust의 최신 안정 버전을 설치한다. 설치 과정에서 비밀번호를 입력하라는 메시지가 나타날 수 있다. 설치가 성공적으로 완료되면 다음과 같은 메시지가 표시된다:

```text
Rust is installed now. Great!
```

또한 _링커_가 필요하다. 링커는 Rust가 컴파일된 출력물을 하나의 파일로 합치는 데 사용하는 프로그램이다. 대부분의 경우 이미 링커가 설치되어 있을 것이다. 만약 링커 관련 오류가 발생한다면, C 컴파일러를 설치해야 한다. C 컴파일러는 일반적으로 링커를 포함하고 있다. 또한, 일부 일반적인 Rust 패키지가 C 코드에 의존하고 있어 C 컴파일러가 필요할 수 있다.

macOS에서는 다음 커맨드를 실행하여 C 컴파일러를 설치할 수 있다:

```console
$ xcode-select --install
```

Linux 사용자는 일반적으로 배포판의 문서에 따라 GCC나 Clang을 설치해야 한다. 예를 들어, Ubuntu를 사용한다면 `build-essential` 패키지를 설치하면 된다.


### 윈도우에 `rustup` 설치하기

윈도우에서 Rust를 설치하려면 [https://www.rust-lang.org/tools/install][install]로 이동해 설치 안내를 따르면 된다. 설치 과정 중 Visual Studio를 설치하라는 메시지가 나타난다. 이는 프로그램을 컴파일하는 데 필요한 링커와 네이티브 라이브러리를 제공한다. 이 단계에서 더 많은 도움이 필요하다면 [https://rust-lang.github.io/rustup/installation/windows-msvc.html][msvc]를 참고한다.

이 책의 나머지 부분에서는 _cmd.exe_와 PowerShell 모두에서 동작하는 명령어를 사용한다. 만약 특정 차이점이 있다면, 어떤 것을 사용해야 하는지 설명할 것이다.


### 문제 해결

Rust가 올바르게 설치되었는지 확인하려면 셸을 열고 다음 명령어를 입력한다:

```console
$ rustc --version
```

최신 안정 버전의 버전 번호, 커밋 해시, 커밋 날짜가 다음과 같은 형식으로 표시된다:

```text
rustc x.y.z (abcabcabc yyyy-mm-dd)
```

이 정보가 보이면 Rust가 성공적으로 설치된 것이다. 정보가 표시되지 않는다면, Rust가 `%PATH%` 시스템 변수에 제대로 추가되었는지 확인해야 한다.

Windows CMD에서는 다음 명령어를 사용한다:

```console
> echo %PATH%
```

PowerShell에서는 다음 명령어를 사용한다:

```powershell
> echo $env:Path
```

Linux와 macOS에서는 다음 명령어를 사용한다:

```console
$ echo $PATH
```

모든 것이 정상인데도 Rust가 작동하지 않는다면, 여러 도움을 받을 수 있는 곳이 있다. [커뮤니티 페이지][community]에서 다른 Rust 사용자(우리가 스스로를 부르는 재미있는 별명)와 연락하는 방법을 찾아볼 수 있다.

[community]: https://www.rust-lang.org/community


### 업데이트 및 제거

`rustup`을 통해 Rust를 설치했다면, 새 버전으로 업데이트하는 것은 간단하다. 커맨드라인에서 다음 업데이트 스크립트를 실행하면 된다:

```console
$ rustup update
```

Rust와 `rustup`을 제거하려면 커맨드라인에서 다음 제거 스크립트를 실행한다:

```console
$ rustup self uninstall
```


### 로컬 문서

Rust를 설치하면 오프라인에서도 문서를 확인할 수 있도록 로컬에 문서 사본이 함께 설치된다. 브라우저에서 로컬 문서를 열려면 `rustup doc` 명령을 실행한다.

표준 라이브러리에서 제공하는 타입이나 함수의 기능이 궁금하거나 사용법을 모를 때는 API 문서를 참고하면 된다!


### 텍스트 편집기와 통합 개발 환경(IDE)

이 책은 여러분이 Rust 코드를 작성할 때 어떤 도구를 사용하는지에 대해 특별한 가정을 하지 않는다. 거의 모든 텍스트 편집기로도 충분히 작업을 수행할 수 있다! 하지만 많은 텍스트 편집기와 통합 개발 환경(IDE)은 Rust를 내장 지원한다. Rust 웹사이트의 [도구 페이지][tools]에서 다양한 편집기와 IDE에 대한 최신 목록을 항상 확인할 수 있다.


### 오프라인에서 이 책 활용하기

이 책의 여러 예제에서는 표준 라이브러리 외에도 다양한 Rust 패키지를 사용한다. 이러한 예제를 따라 하려면 인터넷 연결이 필요하거나, 미리 해당 의존성을 다운로드해야 한다. 의존성을 미리 다운로드하려면 다음 명령어를 실행한다. (나중에 `cargo`가 무엇인지, 이 명령어들이 무엇을 하는지 자세히 설명할 것이다.)

```console
$ cargo new get-dependencies
$ cd get-dependencies
$ cargo add rand@0.8.5 trpl@0.2.0
```

이 명령어를 실행하면 해당 패키지가 캐시에 저장되어 나중에 다시 다운로드할 필요가 없다. 이 명령어를 실행한 후에는 `get-dependencies` 폴더를 유지할 필요가 없다. 이 명령어를 실행했다면, 책의 나머지 부분에서 모든 `cargo` 명령어에 `--offline` 플래그를 사용해 네트워크를 사용하지 않고 캐시된 버전을 활용할 수 있다.

[otherinstall]: https://forge.rust-lang.org/infra/other-installation-methods.html
[install]: https://www.rust-lang.org/tools/install
[msvc]: https://rust-lang.github.io/rustup/installation/windows-msvc.html
[community]: https://www.rust-lang.org/community
[tools]: https://www.rust-lang.org/tools


