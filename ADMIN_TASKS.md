# 관리 작업

이 문서는 저장소를 관리하는 담당자가 가끔 필요한 유지보수 작업을 수행하는 방법을 기억하기 위한 참고 자료다.

## `rustc` 버전 업데이트하기

- `target` 디렉토리를 삭제한다. 어차피 모든 것을 다시 컴파일할 예정이다
- `.github/workflows/main.yml`에서 버전 번호를 변경한다
- `rust-toolchain`의 버전 번호를 변경한다. 이렇게 하면 `rustup`으로 로컬에서 사용하는 버전도 변경된다
- `src/title-page.md`의 버전 번호를 변경한다
- `./tools/update-rustc.sh`를 실행한다(스크립트의 주석 코드에서 수행하는 작업에 대한 세부 정보 확인 가능)
- 변경 사항을 검토한다(git에서 보고한 변경된 파일을 확인하고) 그 효과를 확인한다(`tmp/book-before`와 `tmp/book-after` 디렉토리의 파일을 확인하여). 문제가 없으면 변경 사항을 커밋한다
- `manual-regeneration`을 검색하고 스크립트로 생성할 수 없는 출력을 업데이트하기 위해 해당 위치의 지침을 따른다

## 모든 리스팅의 `edition` 업데이트

모든 리스팅의 `Cargo.toml`에서 `edition = "[year]"` 메타데이터를 업데이트하려면 `./tools/update-editions.sh` 스크립트를 실행한다. 차이점을 확인하여 합리적으로 보이는지 확인하고, 특히 업데이트로 인해 텍스트 변경이 필요한지 확인한다. 그런 다음 변경 사항을 커밋한다.

## mdBook 설정에서 `edition` 업데이트

`book.toml`과 `nostarch/book.toml`을 열고 `[rust]` 테이블의 `edition` 값을 새 에디션으로 설정한다.

## 리스팅의 새 버전 릴리스하기

이제 모든 리스팅이 포함된 완전한 프로젝트의 `.tar` 파일을 [GitHub 릴리스](https://github.com/rust-lang/book/releases)로 제공한다. 편집이나 Rust 및 `rustfmt` 업데이트로 인한 코드 변경이 있는 경우 새 릴리스 아티팩트를 만들려면 다음을 수행한다:

- 릴리스를 위한 git 태그를 생성하고 GitHub에 푸시하거나, GitHub UI로 이동하여 [새 릴리스 초안 작성](https://github.com/rust-lang/book/releases/new)을 클릭하고 기존 태그를 선택하는 대신 새 태그를 입력해 새 태그를 생성한다
- `cargo run --bin release_listings`를 실행하면 `tmp/listings.tar.gz`가 생성된다
- 초안 릴리스의 GitHub UI에 `tmp/listings.tar.gz`를 업로드한다
- 릴리스를 게시한다

## 새 리스팅 추가하기

모든 리스팅에 `rustfmt`를 실행하고, 컴파일러가 업데이트될 때 출력을 업데이트하며, 리스팅에 대한 전체 프로젝트가 포함된 릴리스 아티팩트를 생성하는 스크립트를 촉진하기 위해, 가장 간단한 것 이상의 모든 리스팅은 파일로 추출해야 한다. 이를 위해:

- `listings` 디렉토리에서 새 리스팅이 위치할 곳을 찾는다.
  - 각 장마다 하나의 하위 디렉토리가 있다
  - 번호가 있는 리스팅은 디렉토리 이름으로 `listing-[장 번호]-[리스팅 번호]`를 사용해야 한다.
  - 번호가 없는 리스팅은 `no-listing-`으로 시작하고 장의 다른 번호 없는 리스팅에 상대적인 위치를 나타내는 번호를 사용한 다음, 찾고자 하는 코드를 식별할 수 있는 짧은 설명을 추가한다.
  - 코드 출력만 표시하는 리스팅(예: "x 대신 y를 작성했다면 다음과 같은 컴파일러 오류가 발생한다"라고 말하지만 실제로 코드 x를 보여주지 않는 경우)은 `output-only-`로 시작하고 장의 다른 출력 전용 리스팅에 상대적인 위치를 나타내는 번호를 사용한 다음, 작성자나 기여자가 찾고자 하는 코드를 식별할 수 있는 짧은 설명을 추가한다.
  - **주변 리스팅 번호를 적절히 조정하는 것을 잊지 말자!**
- 해당 디렉토리에 `cargo new`를 사용하거나 다른 리스팅을 복사하여 전체 Cargo 프로젝트를 생성한다.
- 완전히 작동하는 예제를 만들기 위해 필요한 코드와 주변 코드를 추가한다.
- 파일의 일부만 표시하려면 앵커 주석(`// ANCHOR: some_tag`와 `// ANCHOR_END: some_tag`)을 사용하여 표시하려는 파일의 부분을 표시한다.
- Rust 코드의 경우, 텍스트의 코드 블록 내에서 `{{#rustdoc_include [filename:some_tag]}}` 지시문을 사용한다. `rustdoc_include` 지시문은 `mdbook test` 목적으로 `rustdoc`에 표시되지 않는 코드를 제공한다.
- 다른 모든 것은 `{{#include [filename:some_tag]}}` 지시문을 사용한다.
- 텍스트에 명령 출력도 표시하려면 다음과 같이 리스팅 디렉토리에 `output.txt` 파일을 생성한다:
  - `cargo run`이나 `cargo test`와 같은 명령을 실행하고 모든 출력을 복사한다.
  - 첫 번째 줄이 `$ [실행한 명령]`인 새 `output.txt` 파일을 생성한다.
  - 방금 복사한 출력을 붙여넣는다.
  - `./tools/update-rustc.sh`를 실행한다. 이는 컴파일러 출력에 대한 일부 정규화를 수행해야 한다.
  - `{{#include [filename]}}` 지시문으로 텍스트에 출력을 포함한다.
  - output.txt를 추가하고 커밋한다.
- 출력을 표시하고 싶지만 어떤 이유로 스크립트로 생성할 수 없는 경우(예: 사용자 입력이나 웹 요청과 같은 외부 이벤트 때문에), 출력을 인라인으로 유지하되 `manual-regeneration`과 인라인 출력을 수동으로 업데이트하는 지침이 포함된 주석을 만든다.
- 이 예제가 `rustfmt`에 의해 형식화되는 것을 원하지 않는 경우(예: 예제가 의도적으로 구문 분석되지 않기 때문에), 리스팅 디렉토리에 `rustfmt-ignore` 파일을 추가하고 형식화되지 않는 이유를 해당 파일의 내용으로 작성한다(rustfmt 버그일 경우 언젠가 수정될 수 있으므로).

## 렌더링된 책에 대한 변경 효과 확인하기

`mdbook` 업데이트나 파일 포함 방식 변경과 같은 테스트하려는 변경의 효과를 확인하려면:

- 테스트하려는 변경 전에 `mdbook build -d tmp/book-before`를 실행하여 빌드된 책을 생성한다
- 테스트하려는 변경을 적용하고 `mdbook build -d tmp/book-after`를 실행한다
- `./tools/megadiff.sh`를 실행한다
- `tmp/book-before`와 `tmp/book-after`에 남아 있는 파일은 선호하는 차이점 보기 메커니즘으로 수동으로 검사할 수 있는 차이점이 있다

## No Starch를 위한 새 마크다운 파일 생성하기

- `./tools/nostarch.sh`를 실행한다
- 스크립트가 `nostarch` 디렉토리에 생성한 파일을 확인한다
- 편집 작업을 시작하는 경우 git에 커밋한다

## 비교를 위해 docx에서 마크다운 생성하기

- docx 파일을 `tmp/chapterXX.docx`로 저장한다.
- Word에서 검토 탭으로 이동하여 "모든 변경 사항 수락 및 추적 중지"를 선택한다
- docx를 다시 저장하고 Word를 닫는다
- `./tools/doc-to-md.sh`를 실행한다
- 이 스크립트는 `nostarch/chapterXX.md`를 작성해야 한다. 필요한 경우 `tools/doc-to-md.xsl`의 XSL을 조정하고 `./tools/doc-to-md.sh`를 다시 실행한다.

## Graphviz dot 생성하기

책의 일부 다이어그램에는 [Graphviz](http://graphviz.org/)를 사용한다. 이러한 파일의 소스는 `dot` 디렉토리에 있다. 예를 들어 `dot/trpl04-01.dot` 파일을 `svg`로 변환하려면 다음을 실행한다:

```bash
$ dot dot/trpl04-01.dot -Tsvg > src/img/trpl04-01.svg
```

생성된 SVG에서 `svg` 요소의 width와 height 속성을 제거하고 `viewBox` 속성을 `0.00 0.00 1000.00 1000.00` 또는 이미지가 잘리지 않는 다른 값으로 설정한다.

## GitHub Pages에 미리보기 게시하기

진행 중인 미리보기를 위해 GitHub Pages에 게시하는 경우가 있다. 권장하는 게시 흐름은 다음과 같다:

- `pip install ghp-import`(또는 [pipx][pipx]를 사용하여 `pipx install ghp-import`)를 실행하여 `ghp-import` 도구를 설치한다.
- 루트에서 `tools/generate-preview.sh`를 실행한다

[pipx]: https://pipx.pypa.io/stable/#install-pipx