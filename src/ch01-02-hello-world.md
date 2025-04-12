## Hello, World!

이제 Rust를 설치했으니 첫 번째 Rust 프로그램을 작성해보자. 새로운 언어를 배울 때 화면에 `Hello, world!`라는 텍스트를 출력하는 작은 프로그램을 만드는 것은 전통적인 방식이다. 여기서도 그 전통을 따라가보자.

> 참고: 이 책은 커맨드라인에 대한 기본적인 이해를 전제로 한다. Rust는 코드를 작성하는 도구나 코드가 위치한 장소에 대해 특별한 요구사항을 두지 않는다. 따라서 커맨드라인 대신 통합 개발 환경(IDE)을 사용하고 싶다면, 여러분이 선호하는 IDE를 자유롭게 사용해도 된다. 많은 IDE들이 어느 정도 Rust를 지원하고 있으며, 자세한 내용은 IDE의 문서를 확인하면 된다. Rust 팀은 `rust-analyzer`를 통해 뛰어난 IDE 지원을 제공하는 데 주력하고 있다. 더 자세한 내용은 [부록 D][devtools]<!-- ignore -->를 참고하자.


### 프로젝트 디렉토리 생성하기

Rust 코드를 저장할 디렉토리를 먼저 만든다. Rust는 코드가 어디에 있는지 상관하지 않지만, 이 책의 연습 문제와 프로젝트를 위해 홈 디렉토리 안에 _projects_ 디렉토리를 만들고 모든 프로젝트를 그 안에 보관하는 것을 권장한다.

터미널을 열고 다음 명령어를 입력해 _projects_ 디렉토리와 그 안에 "Hello, world!" 프로젝트를 위한 디렉토리를 생성한다.

Linux, macOS, 그리고 Windows의 PowerShell에서는 다음 명령어를 입력한다:

```console
$ mkdir ~/projects
$ cd ~/projects
$ mkdir hello_world
$ cd hello_world
```

Windows CMD에서는 다음 명령어를 입력한다:

```cmd
> mkdir "%USERPROFILE%\projects"
> cd /d "%USERPROFILE%\projects"
> mkdir hello_world
> cd hello_world
```


### Rust 프로그램 작성과 실행

다음으로, 새로운 소스 파일을 만들고 _main.rs_라는 이름으로 저장한다. Rust 파일은 항상 _.rs_ 확장자로 끝난다. 파일 이름에 여러 단어를 사용할 경우, 관례적으로 밑줄(_)로 단어를 구분한다. 예를 들어, _helloworld.rs_ 대신 _hello_world.rs_를 사용한다.

이제 방금 만든 _main.rs_ 파일을 열고, Listing 1-1의 코드를 입력한다.

<Listing number="1-1" file-name="main.rs" caption="`Hello, world!`를 출력하는 프로그램">

```rust
fn main() {
    println!("Hello, world!");
}
```

</Listing>

파일을 저장한 후, 터미널 창에서 _~/projects/hello_world_ 디렉토리로 이동한다. Linux나 macOS에서는 다음 명령어를 입력해 파일을 컴파일하고 실행한다:

```console
$ rustc main.rs
$ ./main
Hello, world!
```

Windows에서는 `./main` 대신 `.\main.exe` 명령어를 입력한다:

```powershell
> rustc main.rs
> .\main
Hello, world!
```

운영체제와 상관없이, 터미널에 `Hello, world!` 문자열이 출력된다. 만약 이 결과가 보이지 않는다면, [“문제 해결”][troubleshooting]<!-- ignore --> 섹션을 참고해 도움을 받을 수 있다.

`Hello, world!`가 정상적으로 출력되었다면, 축하한다! 여러분은 공식적으로 Rust 프로그램을 작성한 것이다. 이제 여러분은 Rust 프로그래머가 된 것이다. 환영한다!


### 러스트 프로그램의 구조


"Hello, world!" 프로그램을 자세히 살펴보자. 먼저 다음 코드를 보자:

```rust
fn main() {

}
```

이 코드는 `main`이라는 함수를 정의한다. `main` 함수는 특별한데, 모든 실행 가능한 러스트 프로그램에서 가장 먼저 실행되는 코드다. 여기서 첫 번째 줄은 매개변수가 없고 반환 값도 없는 `main` 함수를 선언한다. 만약 매개변수가 있다면, 괄호 `()` 안에 들어갈 것이다.

함수 본문은 `{}`로 감싸져 있다. 러스트는 모든 함수 본문을 중괄호로 감싸도록 요구한다. 함수 선언과 여는 중괄호를 같은 줄에 두고, 사이에 한 칸을 띄우는 것이 좋은 스타일이다.

> 참고: 여러분이 러스트 프로젝트에서 표준 스타일을 유지하고 싶다면, `rustfmt`라는 자동 포맷터 도구를 사용할 수 있다. 이 도구는 코드를 특정 스타일로 포맷한다 (자세한 내용은 [부록 D][devtools]<!-- ignore -->에서 확인할 수 있다). 러스트 팀은 이 도구를 표준 러스트 배포판에 포함시켰으므로, `rustc`와 마찬가지로 여러분의 컴퓨터에 이미 설치되어 있을 것이다.

`main` 함수의 본문에는 다음 코드가 들어 있다:

```rust
println!("Hello, world!");
```

이 한 줄이 이 작은 프로그램의 모든 작업을 수행한다: 화면에 텍스트를 출력한다. 여기서 주목할 세 가지 중요한 세부 사항이 있다.

첫째, `println!`은 러스트 매크로를 호출한다. 만약 함수를 호출했다면, `println` (느낌표 없이)으로 입력했을 것이다. 러스트 매크로에 대해서는 20장에서 더 자세히 다룰 것이다. 지금은 `!`를 사용하면 일반 함수가 아니라 매크로를 호출한다는 것과, 매크로가 항상 함수와 같은 규칙을 따르지는 않는다는 것만 알아두자.

둘째, `"Hello, world!"` 문자열이 보인다. 이 문자열을 `println!`에 인자로 전달하면, 화면에 문자열이 출력된다.

셋째, 줄 끝에 세미콜론(`;`)이 붙어 있다. 이는 이 표현식이 끝났고 다음 표현식이 시작될 준비가 되었다는 것을 나타낸다. 러스트 코드의 대부분은 세미콜론으로 끝난다.


### 컴파일과 실행은 별개의 단계

새로 만든 프로그램을 실행해봤으니, 이제 각 단계를 자세히 살펴보자.

Rust 프로그램을 실행하기 전에, Rust 컴파일러를 사용해 프로그램을 먼저 컴파일해야 한다. `rustc` 명령어를 입력하고 소스 파일 이름을 인자로 전달하면 된다. 예를 들어 다음과 같이 실행한다:

```console
$ rustc main.rs
```

C나 C++에 익숙하다면, 이 과정이 `gcc`나 `clang`과 비슷하다는 것을 알 수 있다. 컴파일이 성공적으로 완료되면, Rust는 바이너리 실행 파일을 생성한다.

Linux, macOS, 그리고 Windows의 PowerShell에서는 쉘에서 `ls` 명령어를 입력해 실행 파일을 확인할 수 있다:

```console
$ ls
main  main.rs
```

Linux와 macOS에서는 두 개의 파일이 보인다. Windows의 PowerShell에서는 CMD를 사용할 때와 동일한 세 개의 파일이 나타난다. Windows의 CMD에서는 다음과 같이 입력한다:

```cmd
> dir /B %= /B 옵션은 파일 이름만 보여주라는 의미 =%
main.exe
main.pdb
main.rs
```

이 명령어를 실행하면 _.rs_ 확장자를 가진 소스 코드 파일, 실행 파일(Windows에서는 _main.exe_, 다른 플랫폼에서는 _main_), 그리고 Windows에서는 디버깅 정보를 포함한 _.pdb_ 확장자의 파일이 보인다. 이제 _main_ 또는 _main.exe_ 파일을 실행할 수 있다. 다음과 같이 입력하면 된다:

```console
$ ./main # Windows에서는 .\main.exe
```

만약 _main.rs_ 파일이 "Hello, world!" 프로그램이라면, 이 명령어를 실행하면 터미널에 `Hello, world!`가 출력된다.

Ruby, Python, JavaScript와 같은 동적 언어에 익숙하다면, 컴파일과 실행을 별도의 단계로 나누는 것에 익숙하지 않을 수 있다. Rust는 **사전 컴파일(ahead-of-time compiled)** 언어로, 프로그램을 컴파일한 후 실행 파일을 다른 사람에게 전달하면, 그 사람은 Rust가 설치되어 있지 않아도 프로그램을 실행할 수 있다. 반면 _.rb_, _.py_, _.js_ 파일을 전달하면, 각각 Ruby, Python, JavaScript 구현체가 설치되어 있어야 한다. 하지만 이 언어들은 단 하나의 명령어로 컴파일과 실행을 동시에 처리할 수 있다. 모든 언어 설계에는 트레이드오프가 존재한다.

`rustc`로 컴파일하는 것은 간단한 프로그램에는 적합하지만, 프로젝트가 커지면 모든 옵션을 관리하고 코드를 쉽게 공유할 수 있는 방법이 필요하다. 다음에는 실제 Rust 프로그램을 작성하는 데 도움이 되는 Cargo 도구를 소개한다.

[troubleshooting]: ch01-01-installation.html#troubleshooting
[devtools]: appendix-04-useful-development-tools.html


