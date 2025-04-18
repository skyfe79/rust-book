# 프로그래밍의 공통 개념

이 장에서는 거의 모든 프로그래밍 언어에서 등장하는 개념과 이를 Rust에서 어떻게 구현하는지 알아본다. 대부분의 프로그래밍 언어는 핵심적으로 많은 공통점을 가지고 있다. 이 장에서 소개하는 개념은 Rust에만 국한된 것이 아니지만, Rust의 문맥에서 이를 설명하고 이러한 개념을 사용할 때의 관례를 다룬다.

특히 변수, 기본 타입, 함수, 주석, 그리고 제어 흐름에 대해 배울 것이다. 이러한 기초 개념은 모든 Rust 프로그램에 포함되며, 이를 일찍 익히면 강력한 기초를 다지는 데 도움이 될 것이다.

> #### 키워드
>
> Rust 언어는 다른 언어와 마찬가지로 언어 자체에서만 사용할 수 있는 _키워드_ 집합을 가지고 있다. 이 단어들은 변수나 함수의 이름으로 사용할 수 없다는 점을 명심해야 한다. 대부분의 키워드는 특별한 의미를 가지며, Rust 프로그램에서 다양한 작업을 수행하는 데 사용된다. 몇몇 키워드는 현재 기능과 연결되어 있지 않지만, 향후 Rust에 추가될 수 있는 기능을 위해 예약되어 있다. 키워드 목록은 [부록 A][appendix_a]에서 확인할 수 있다.

[appendix_a]: appendix-01-keywords.md


