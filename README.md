# 러스트 프로그래밍 언어

![빌드 상태](https://github.com/rust-lang/book/workflows/CI/badge.svg)

이 저장소는 "러스트 프로그래밍 언어" 책의 소스 코드를 포함한다.

[책은 No Starch Press에서 종이책 형태로 구매할 수 있다][nostarch].

[nostarch]: https://nostarch.com/rust-programming-language-2nd-edition

또한 온라인에서 무료로 책을 읽을 수 있다. 최신 [안정(stable)], [베타(beta)], 또는 [나이틀리(nightly)] 러스트 릴리스와 함께 제공되는 책을 참조한다. 해당 버전들은 이 저장소보다 덜 자주 업데이트되므로, 이 저장소에서 이미 수정된 문제점이 있을 수 있음을 유의한다.

[안정(stable)]: https://doc.rust-lang.org/stable/book/
[베타(beta)]: https://doc.rust-lang.org/beta/book/
[나이틀리(nightly)]: https://doc.rust-lang.org/nightly/book/

책에 등장하는 모든 코드 리스팅만 다운로드하려면 [릴리스]를 참조한다.

[릴리스]: https://github.com/rust-lang/book/releases

## 요구 사항

책을 빌드하려면 [mdBook]이 필요하며, 이상적으로는 rust-lang/rust가 [이 파일][rust-mdbook]에서 사용하는 것과 동일한 버전을 사용한다. 설치하려면:

[mdBook]: https://github.com/rust-lang/mdBook
[rust-mdbook]: https://github.com/rust-lang/rust/blob/master/src/tools/rustbook/Cargo.toml

```bash
$ cargo install mdbook --locked --version <버전_번호>
```

이 책은 또한 이 저장소의 일부인 두 개의 mdbook 플러그인을 사용한다. 이들을 설치하지 않으면 빌드 시 경고가 표시되고 결과물이 올바르게 보이지 않을 수 있지만, 여전히 책을 빌드할 수는 있다. 플러그인을 사용하려면 다음을 실행한다:

```bash
$ cargo install --locked --path packages/mdbook-trpl
```

## 빌드하기

책을 빌드하려면 다음을 입력한다:

```bash
$ mdbook build
```

결과물은 `book` 하위 디렉토리에 위치한다. 확인하려면 웹 브라우저에서 열어본다.

_Firefox:_

```bash
$ firefox book/index.html                       # 리눅스
$ open -a "Firefox" book/index.html             # OS X
$ Start-Process "firefox.exe" .\book\index.html # 윈도우 (PowerShell)
$ start firefox.exe .\book\index.html           # 윈도우 (Cmd)
```

_Chrome:_

```bash
$ google-chrome book/index.html                 # 리눅스
$ open -a "Google Chrome" book/index.html       # OS X
$ Start-Process "chrome.exe" .\book\index.html  # 윈도우 (PowerShell)
$ start chrome.exe .\book\index.html            # 윈도우 (Cmd)
```

테스트를 실행하려면:

```bash
$ cd packages/trpl
$ mdbook test --library-path packages/trpl/target/debug/deps
```

## 기여하기

여러분의 도움을 환영한다! 어떤 종류의 기여를 찾고 있는지 알아보려면 [CONTRIBUTING.md][contrib]를 참조한다.

[contrib]: https://github.com/rust-lang/book/blob/main/CONTRIBUTING.md

책이 [인쇄][nostarch]되기 때문에, 그리고 가능한 한 온라인 버전을 인쇄 버전과 가깝게 유지하고 싶기 때문에, 이슈나 풀 리퀘스트를 처리하는 데 일반적으로 예상하는 것보다 더 오래 걸릴 수 있다.

지금까지 [러스트 에디션](https://doc.rust-lang.org/edition-guide/)과 일치하는 대규모 개정을 진행해 왔다. 이러한 대규모 개정 사이에는 오류만 수정한다. 이슈나 풀 리퀘스트가 단순히 오류를 수정하는 것이 아니라면, 대규모 개정 작업을 다시 시작할 때까지 기다릴 수 있다: 몇 개월 또는 몇 년 정도를 예상한다. 인내심을 가져주셔서 감사하다!

### 번역

책 번역에 도움을 주면 정말 좋을 것이다! 현재 진행 중인 노력에 동참하려면 [Translations] 라벨을 참조한다. 새 언어 작업을 시작하려면 새 이슈를 열면 된다! 다국어를 위한 [mdbook 지원]을 기다리고 있어서 병합하기 전까지는 기다려야 하지만, 언제든지 시작해도 좋다!

[Translations]: https://github.com/rust-lang/book/issues?q=is%3Aopen+is%3Aissue+label%3ATranslations
[mdbook 지원]: https://github.com/rust-lang/mdBook/issues/5

## 맞춤법 검사

소스 파일의 맞춤법 오류를 스캔하려면 `ci` 디렉토리에서 제공하는 `spellcheck.sh` 스크립트를 사용할 수 있다. 이 스크립트는 `ci/dictionary.txt`에 제공된 유효한 단어 사전이 필요하다. 스크립트가 거짓 양성(예: 스크립트가 유효하지 않다고 판단하는 `BTreeMap` 단어를 사용한 경우)을 생성하면, 이 단어를 `ci/dictionary.txt`에 추가해야 한다(일관성을 위해 정렬된 순서를 유지한다).