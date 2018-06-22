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
$ python convert_env.py <config file> <docker-compose name>
```
