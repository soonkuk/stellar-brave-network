## json 형식의 config 파일

```
{
    "groups":
    {
        "g1": ["1", "2", "3"],
        "g2": ["4", "5", "6", "7"]
    },
    "binary_link":
    [
        [ ["8"], ["3", "4"] ],
        [ ["9"], ["3", "6"] ]
    ],
    "unary_link":
    [
        [ ["9"], ["1"] ]
    ],
    "horizon":
    {
        "h1": "2",
        "h2": "7"
    }
}
```
groups은 모든 노드가 서로 바라보는 쿼럼구성

binary_link는 양방향 validator 설정

unary_link는 단방향 validator 설정

horizon은 horizon 갯수 지정과 연결된 stellar core 표시

## 구동

```
$ python install ruamel.yaml
$ python make_env.py <config file>
```

`config file`의 setting과 같은 이름의 폴더가 생기고 폴더아래 docker-compose 설정파일이 생성됨

ex)config-12.json -> docker-compose-12 

## docker-compose 실행 후 shell script 실행

```
$ cd <docker-compose folder>
$ . ./account.sh   				

account 3개에 대한 public key와 address를 각각 변수에 지정 

$ . ./init_account.sh				

account 3개의 account 생성하고 10240 입금

$ . ./balance.sh <number of horizon>		

각 account 잔고에 대하여 number of horizon의 갯수 만큼 확인

$ . ./list_colum_in_database.sh
             List of relations
 Schema |     Name      | Type  |  Owner   
--------+---------------+-------+----------
 public | accountdata   | table | postgres
 public | accounts      | table | postgres
 public | ban           | table | postgres
 public | ledgerheaders | table | postgres
 public | offers        | table | postgres
 public | peers         | table | postgres
 public | publishqueue  | table | postgres
 public | pubsub        | table | postgres
 public | scphistory    | table | postgres
 public | scpquorums    | table | postgres
 public | signers       | table | postgres
 public | storestate    | table | postgres
 public | trustlines    | table | postgres
 public | txfeehistory  | table | postgres
 public | txhistory     | table | postgres
(15 rows)

stellar database table명 확인

$ . ./get_database.sh <table name>

`table name` 폴더에 node별 database의 csv파일 생성
```
