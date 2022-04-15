채팅 서비스

- 웹브라우저에서 동작.
- 웹에서 채팅창에 접속해서 채팅 가능.
- PWA를 사용해서 알람이나 메시지도 받을 수 있다.

happy_chat.net 접속하면

- 채팅방 목록이 나온다?

->

- 행복한 채팅 주제들이 나열되어 있다. 그 주제 중 하나를 선택해서 들어간다.
- All by all 채팅. 수백명이 들어있을 수도...
- 비속어 순화
- 특정 단어를 사용할 때마다, 별풍선 쏘듯이 화면에 효과 나타내기.

- limit maximum users per room (20)

->

minimum set?

1. 로그인 기능? 최대한 간소하게.
2. 채팅 주제는 관리자가 생성. 회원은 제안 가능.
3. 1~2개 나열.
4. 방에 들어갔을 때, 채팅이 되는 것
5. 한번에는 하나의 방만 들어갈 수 있다.

채팅방에 들어온 사람에 대한 식별. (익명)

---

어떤 기술 스택을 쓸지 정한다.

최대 동시 입장 수.
Queueing service 고려해야 함.
기술 진입 장벽이 낮은.

Queue는, 사용자가 많을 때 처리를 한번에 할 수 없다.

A talks ---> addTalk(msg, room) ---> API endpoint ---> A가 구독하는 방에

- 사용자 A가 메시지를 보낸다: addTalkToChattingRoom(msg, room) -> API endpoint -> (해당 채팅방을 구독하는 모든 사용자에게 메시지를 뿌린다)
- 사용자는 해당 채팅방에 뿌려지 메시지를 동기적으로 확인한다. (polling)

Queue에서는 무슨 일이 일어날까?

[room, user]

routing_key[room1.toracle]

addTalk(who, message, when, room)

- message key를 빌드 (ex. `room1.*` except `room1.toracle`)
- fan out, fan in, direct,

room1에 현재 누가 참여하고 있는지 목록

개인마다 사서함

room1.toracle

- 안녕하세요 (by toracle)
- 안녕하세요 (by 홍길동)
- 아 그러셨구나 (by 정은경)

각자 어디까지 가져갔는지가 다르니, 개인 사서함이 있어야겠다.

채팅 메세지

- 누가
- 어떤 메세지를
- 언제

