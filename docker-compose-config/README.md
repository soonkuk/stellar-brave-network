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
$ python make_env.py <config file> <docker-compose name>
```

`docker-compose name`과 같은 이름의 폴더가 생기고 폴더아래 docker-compose 설정파일이 생성

## shell script 실행

$ . ./list_colum_in_database.sh

```
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
```
stellar database table명 확인

$ . ./get_database.sh <table name>

`table name` 폴더에 node별 database의 csv파일 생성 
