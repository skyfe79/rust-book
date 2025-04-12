# 기여하기

책에 관심을 가져주셔서 감사합니다. 여러분의 도움을 환영합니다!

## 편집 위치

모든 편집은 `src` 디렉토리에서 이루어져야 한다.

`nostarch` 디렉토리는 인쇄 버전 출판사에 편집 내용을 전송하기 위한 스냅샷을 포함한다. 스냅샷 파일은 전송 여부를 반영하므로, No Starch에 편집 내용을 보낼 때만 업데이트된다. **`nostarch` 디렉토리의 파일을 변경하는 풀 리퀘스트를 제출하지 않는다. 해당 풀 리퀘스트는 닫힐 것이다.**

저장소의 러스트 코드에는 표준 형식을 적용하기 위해 [`rustfmt`][rustfmt]를 사용하고, 마크다운 소스와 프로젝트의 비-러스트 코드에는 표준 형식을 적용하기 위해 [`dprint`][dprint]를 사용한다.

[rustfmt]: https://github.com/rust-lang/rustfmt
[dprint]: https://dprint.dev

러스트 툴체인이 설치되어 있다면 일반적으로 `rustfmt`도 함께 설치된다. 어떤 이유로 `rustfmt`가 없다면 다음 커맨드를 실행하여 추가할 수 있다:

```sh
rustup component add rustfmt
```

`dprint`를 설치하려면 다음 커맨드를 실행할 수 있다:

```sh
cargo install dprint
```

또는 `dprint` 웹사이트의 [지침][install-dprint]을 따를 수 있다.

[install-dprint]: https://dprint.dev/install/

러스트 코드 형식을 지정하려면 `rustfmt <파일 경로>`를 실행하고, 다른 파일 형식을 지정하려면 `dprint fmt <파일 경로>`를 전달할 수 있다. 많은 텍스트 에디터는 `rustfmt`와 `dprint` 모두에 대한 기본 지원이나 확장 기능을 제공한다.

## 수정 사항 확인

이 책은 러스트 릴리스 트레인을 따른다. 따라서 https://doc.rust-lang.org/stable/book 에서 문제를 발견했다면, 이미 이 저장소의 `main` 브랜치에서 수정되었지만 아직 nightly -> beta -> stable 과정을 거치지 않았을 수 있다. 이슈를 보고하기 전에 이 저장소의 `main` 브랜치를 확인해본다.

특정 파일의 히스토리를 살펴보면 이슈가 수정되었는지 여부나 방법에 대한 추가 정보를 얻을 수 있다.

새 이슈를 보고하거나 새 PR을 열기 전에 열린 이슈와 닫힌 이슈, 열린 PR과 닫힌 PR도 검색해본다.

## 라이선스

이 저장소는 러스트 자체와 동일한 라이선스인 MIT/Apache2를 따른다. 각 라이선스의 전체 텍스트는 이 저장소의 `LICENSE-*` 파일에서 찾을 수 있다.

## 행동 강령

러스트 프로젝트는 이 프로젝트를 포함한 모든 하위 프로젝트를 관리하는 [행동 강령](http://rust-lang.org/policies/code-of-conduct)을 가지고 있다. 이를 존중해주길 바란다!

## 기대 사항

책이 [인쇄][nostarch]되기 때문에, 그리고 가능한 한 책의 온라인 버전을 인쇄 버전과 가깝게 유지하고자 하기 때문에, 이슈나 풀 리퀘스트를 처리하는 데 예상보다 더 오래 걸릴 수 있다.

[nostarch]: https://nostarch.com/rust-programming-language-2nd-edition

지금까지 [러스트 에디션](https://doc.rust-lang.org/edition-guide/)과 일치하는 대규모 개정을 진행해왔다. 이러한 대규모 개정 사이에는 오류만 수정할 것이다. 이슈나 풀 리퀘스트가 단순히 오류를 수정하는 것이 아니라면, 대규모 개정 작업을 다시 시작할 때까지 기다려야 할 수 있다: 몇 개월 또는 몇 년이 걸릴 수 있다. 참고해주셔서 감사하다!

## 도움 요청

많은 양의 읽기나 쓰기가 필요하지 않은 도움을 찾고 있다면, [E-help-wanted 레이블이 있는 열린 이슈][help-wanted]를 확인해본다. 이는 텍스트, 러스트 코드, 프론트엔드 코드 또는 쉘 스크립트에 대한 작은 수정으로, 효율성을 높이거나 책을 향상시키는 데 도움이 될 것이다!

[help-wanted]: https://github.com/rust-lang/book/issues?q=is%3Aopen+is%3Aissue+label%3AE-help-wanted

## 번역

책 번역을 도와주면 좋겠다! 현재 진행 중인 노력에 참여하려면 [Translations] 레이블을 참조한다. 새 언어로 작업을 시작하려면 새 이슈를 열면 된다! 다중 언어를 위한 [mdbook 지원]을 기다리고 있어 병합하기 전까지는 기다려야 하지만, 자유롭게 시작할 수 있다!

[Translations]: https://github.com/rust-lang/book/issues?q=is%3Aopen+is%3Aissue+label%3ATranslations
[mdbook support]: https://github.com/rust-lang/mdBook/issues/5