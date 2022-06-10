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

---

저장을 어떻게 할까? 뭘 저장해야 하나?

속도 측면에서 RDB보다는 NoSQL을 쓰는 경우가 많다고 한다.

- 누가 (User, WebSocket ID)
- 어디에서 (Room, IP)
- 무엇을
- 언제

Who generates id?

- receiver, sender
- server, client (distribted)
- ----> <uuid>
- <uuid> ---->

uuid.uuid4()
uuid.uuid4()
uuid.uuid4()
uuid.uuid4()

DB replication. cluster.
ZooKeeper: ID generation server

- 아파치 주키퍼는 아파치 소프트웨어 재단 프로젝트중의 한 소프트웨어 프로젝트로서 공개 분산형 구성 서비스, 동기 서비스 및 대용량 분산 시스템을 위한 네이밍 레지스트리를 제공한다. 주키퍼는 하둡의 한 하위 프로젝트이었으나 지금은 독립적인 상위 프로젝트이다.

MySQL storage engine. disk. PK sorting.
InnoDB PK

1
2
3
4
5

[ ] [ ] [ ] [ ] [ ]

1
3
4
6
2

[ ] [ ] [ ] [ ]

[ ] [^] [ ] [ ] [ ]

[memory]
[ disk ]

RDB (SQLite. file. has memory engine also)
MongoDB (DB)

Redis (cache, k/v) -- memory

Query --> [ ResultSet <-- Disk ]
<Cursor>
cursor.next() -

Server-side cursor, Client-side cursor

python mysql driver
pymysql
mysql-client, mysqldb (mysqlclient C module)
https://mysqlclient.readthedocs.io/user_guide.html
https://docs.djangoproject.com/en/4.0/ref/databases/#server-side-cursors

qs = Message.objects.filter(room=1)
for message in qs:

qs.count() > 100000

for message in qs: <--- eval on qs.
qs.\_resultset
<- model Message() \* 100000
memory, CPU
server down. severe CPU. 10min. -> crash. DB.
<---------------->
x DB [create instances in memory]

for message in qs.iterator():
<--- doesn't make qs.\_resultset

table. know how large it will grow.

User 1m

Log.

User .
Room .
Message

!= N+1

---

## Room

1 | test1 |
2 | test2 |

## Message

1 | 1 | hello world
2 | 1 | hi!
3 | 1 | hi

(1) \* 3 = 6
1 + N row

## Message + Room name

qs = Message.filter(room=1)

for message in qs:
print(message.room.name, message.content)

---

emoji.

- DATABASES.

- MySQL . CREATE DATABASE heppy_chat DEFAULT CHARACTER SET utf8. var. ASCII 1byte. CJK 2byte. Emoji 3byte. utf8 mb4

AbstractUser

- id
- username
- password
- joined_at
- email

Message

- id (system id) --- integer, incremental, predictable GET /messages/{uuid}/ - security. distributed.
- uuid (logical id)
- sender
- room
- content
- created_at

Room

- id (system id)
- uuid (logical id)
- name
- participant_count
- message_count
- created_at

RoomManager

- id (system id)
- room
- member
- created_at
- deleted_at

/\*
UserSocket

- User
- WebSocket ID
  \*/
