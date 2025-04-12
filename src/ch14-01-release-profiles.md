## 릴리스 프로필로 빌드 설정하기

Rust에서 _릴리스 프로필_은 미리 정의된 설정 프로필로, 프로그래머가 코드 컴파일 시 다양한 옵션을 세부적으로 제어할 수 있게 해준다. 각 프로필은 독립적으로 설정된다.

Cargo에는 두 가지 주요 프로필이 있다. `cargo build`를 실행할 때 사용하는 `dev` 프로필과 `cargo build --release`를 실행할 때 사용하는 `release` 프로필이다. `dev` 프로필은 개발 환경에 적합한 기본값으로 설정되어 있고, `release` 프로필은 릴리스 빌드에 적합한 기본값으로 설정되어 있다.

이 프로필 이름은 빌드 출력에서 이미 익숙할 것이다:

```console
$ cargo build
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
$ cargo build --release
    Finished `release` profile [optimized] target(s) in 0.32s
```

`dev`와 `release`는 컴파일러가 사용하는 서로 다른 프로필이다.

Cargo는 프로젝트의 _Cargo.toml_ 파일에 `[profile.*]` 섹션을 명시적으로 추가하지 않았을 때 적용되는 기본 설정을 각 프로필에 대해 가지고 있다. 커스터마이징하고 싶은 프로필에 `[profile.*]` 섹션을 추가하면 기본 설정의 일부를 재정의할 수 있다. 예를 들어, `dev`와 `release` 프로필의 `opt-level` 설정 기본값은 다음과 같다:

<span class="filename">파일명: Cargo.toml</span>

```toml
[profile.dev]
opt-level = 0

[profile.release]
opt-level = 3
```

`opt-level` 설정은 Rust가 코드에 적용할 최적화 수준을 제어하며, 0부터 3까지의 범위를 가진다. 더 많은 최적화를 적용하면 컴파일 시간이 길어진다. 따라서 개발 중에 코드를 자주 컴파일해야 한다면, 결과물이 느리더라도 컴파일 속도를 높이기 위해 최적화 수준을 낮게 유지하는 것이 좋다. 그래서 `dev` 프로필의 기본 `opt-level`은 `0`이다. 코드를 릴리스할 준비가 되면, 컴파일 시간을 더 투자하는 것이 좋다. 릴리스 모드에서는 한 번만 컴파일하지만, 컴파일된 프로그램을 여러 번 실행하게 되므로, 릴리스 모드는 컴파일 시간을 늘리는 대신 실행 속도를 높인다. 그래서 `release` 프로필의 기본 `opt-level`은 `3`이다.

_Cargo.toml_에서 다른 값을 추가해 기본 설정을 재정의할 수 있다. 예를 들어, 개발 프로필에서 최적화 수준 1을 사용하고 싶다면 프로젝트의 _Cargo.toml_ 파일에 다음 두 줄을 추가하면 된다:

<span class="filename">파일명: Cargo.toml</span>

```toml
[profile.dev]
opt-level = 1
```

이 코드는 기본 설정인 `0`을 재정의한다. 이제 `cargo build`를 실행하면, Cargo는 `dev` 프로필의 기본값에 더해 `opt-level`에 대한 커스터마이징을 적용한다. `opt-level`을 `1`로 설정했기 때문에, Cargo는 기본값보다는 더 많은 최적화를 적용하지만, 릴리스 빌드만큼은 아니다.

각 프로필의 전체 설정 옵션과 기본값 목록은 [Cargo 문서](https://doc.rust-lang.org/cargo/reference/profiles.html)를 참조한다.


