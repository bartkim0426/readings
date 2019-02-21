# 읽기 쉬운 코드가 쉬운 코드다 (The Art of Readable Code)


## 1장. 코드는 이해하기 쉬워야 한다

### 가독성의 기본 정리 (The Fundamental Theorem of Readability)

**KEY IDEA: 코드는 다른 사람이 그것을 이해하는 데 들이는 시간을 최소화하는 방식으로 작성되어야 한다**

이해를 위한 시간 (time-till-understanding)을 최소화. 1인 프로젝으라도 6개월 뒤의 내가 그 다른 사람이 될 수 있음


# PART ONE. 표면적 수준에서의 개선

surface-level: 좋은 이름, 설명, 코드를 보기 좋게 정렬 => 반영이 쉽다.

## 2장. 이름에 정보 담기

**KEY_IDEA: 이름에 정보를 담아내라**

### 특정한 단어 고르기

구체적인 단어를 선택하여 '무의미한' 단어를 피하기

```
def GEtPage(url):
    ...
```
- local cache, database, 인터넷 페이지? 
- 페이지를 가져오는 것이라면 `FetchPage()` or `DownloadPage()`

```
class BinaryTree {
    int Size();
    ...
}
```
- `Size()`는 트리의 height인지, 메모리 사용량인지, 노드의 개수인지 애매. 
- Height(), NumNodes(), MemoryBytes() 등이 더 의미있음

```
class Thread {
    void Stop();
    ...
}
```
- 메소드명은 괜찮지만 수행하는 일에 따라 더 의미있게
- 되돌릴 수 없는 최종 동작이라면 `Kill()`. `Resume()`으로 돌이킨다면 `Pause`

- 화려한 단어 선택: 유의어 색인집을 찾거나 동료에게 이름을 물어보기
- 재치보다는 명확하고 간결한 이름


#### 예시

- v15_www 리팩토링 예시

```python
def program_list_view(request, category_slug):
    ...
    page_title = get_page_title(category_slug)

    return render(request, "webapp/program_list.html", context={
    ...
    })

...

def get_page_title(category_slug):
	"""
	category_slug => (조건에 따라) "Korean {category_slug} - OnDemandKorea" 로 title 포매팅
	"""
    tmp_title = _(category_slug.title())
    if any(keyword in tmp_title for keyword in ["Drama", "Variety", "Documentary"]):
        tmp_title = f"Korean {tmp_title}"

    return f"{tmp_title} - OnDemandKorea"
```

- page_title을 가져오는 `get_page_title`?
- `page_title`이 모호? html title tag를 명확히 나타내주지 못함
- get? 어디서 가져오는지, 기존에 존재하는 값인지 등이 모호함
- generate, create / 아니면 단순 포메팅이기 때문에 format, trim 도 괜찮을 듯 하지만 헷갈릴 우려도 있음
- `(category_slug)`를 인자로 받으므로 suffix로 `_from`을 넣어주는 것도 좋을듯
- `page_title` 대신 `html_page_title`, `html_title`도 고려 (실제로는 기존에 쓰는 값이 `page_title`이기 때문에 통일성을 고려)

그래서 나온 후보군은

```
# generate이지만 완전 생성은 아님
generate_html_title_from(category_slug)

# 포멧 => 초기화의 느낌이 조금 남
format_html_title_from(category_slug)

# trim => 단어가 직관적이지 않음
trim_html_title_from(category_slug)
```

> Alfred powerpack을 사용중이라면 synonyms/antonyms 검색하는 `alfred-powerthesaururs` workflow (https://github.com/clarencecastillo/alfred-powerthesaurus) 사용해봐도 좋을듯


### tmp나 retval같은 보편적인 이름 피하기

#### tmp
- tmp, retval, foo 같은 이름보다는 변수의 목적이나 담은 값을 설명해 주어야 함
- 보편적인 이름이 필요한 순간들도 있다
- 변수 자체가 임시 저장소 역할을 한다면 tmp 사용 좋음

```
if (right < left) {
	tmp = right;
	right = left;
	left = tmp;
}
```

> tmp는 대상이 짧게 임시적으로 존재하고, 임시적 존재 자체가 변수의 가장 중요한 용도일 때 한해서만 사용

#### 루프반복자

- `i, j, iter, it` 등의 이름은 보편적이지만 "나는 반복자입니다" 의미 충분히 전달
- 다른 목적으로 사용하면 혼동
- 여러개를 사용하면 헷갈림 => i, j, k 보다 `club_i`, `member_i`, `user_i` (or ci, mi, ui) 등의 이름이 더 낫다 (디버깅시)


### 추상적인 이름보다 구체적인 이름을 선호하라

- 구글의 예시
- `DISALLOW_EVIL_CONSTRUCTOR` => `evil`이 지나치게 강한 표현. disallow 하는 대상이 없음. 
- `DISALLOW_COPY_AND_ASSIGN`으로 대체

- `--run_locally` 예시
- 해당 플래그의 목적 파악 힘듦
- 디버그의 용도라면 `--extra logging` / `--use_local_database` 처럼 명시적으로 사용하는게 좋음

### 추가적인 정보를 이름에 추가하기

- 변수의 이름은 작은 설명문: 중요한 정보를 추가적인 단어로 만들어서 이름 붙이는게 좋음


**단위를 포함하는 값들**
- 시간의 양, 바이트의 수 등의 단위를 변수명에 포함시킨느게 좋음

**다른 중요한 속성 포함하기**
- 어떤 변수에 위험요소 / 나중에 놀랄만한 내용이 있다면 포함시키는게 좋음

|상황|변수명|더 나은 이름|
|패스워드가 'plaintext'에 있고 암호화 필요| password | plaintext_password |
| 설명문이 화면에 나오기 전에 escaped 되어야함 | comment | unescaped_comment |
| 입력 데이터가 url encoded 되었다 | data | data_urlenc |

> 누군가 변수를 잘못 이해했을 때 보안 등 심각한 결과를 낳을 가능성이 있을 때 중요한 의미
> 헝가리언 표기법? 이름에 추가적인 속성을 붙이는 공식적인 시스템. ms에서 사용 (한번 읽어보면 좋을듯)

### 이름은 얼마나 길어야 하는가?

길면 기억하기 어렵고 줄 많이 차지 / 너무 짧으면 안됨

**좁은 범위에서는 짧은 이름이 괜찮다**
- scope가 좁으면 이름에 많은 정보를 담을 필요 없음
- 이름이 큰 범위를 갖는다면 이를 분명하게 만들기 위한 정보를 포함해야함

**긴 이름 - 더이상 문제가 되지 않는다**
- 자동완성 기능

**약어와 축약형**
- 득정 프로젝트에 국한된 의미 => 새로 합류한 사람에게 비밀스럽고 위협 (`WpAll, WpMeta.....`)
- 새로 합류한 사람이 의미를 이해할 수 있을까? 그렇다면 괜찮


### 이름 포맷팅으로 의미를 전달

- 문법적 차이가 드러나게 이름에 각각 다른 포맷팅 방식을 적용 => 코드를 읽기 쉽게 해줌
- 어떤 관습이 다른 사람에게는 이상해 보일 수 있음
- 언어/프로젝트별로 관습 있을 수 있다 ex) jquery `$all_image`, html `id="test_id" class="test_clas"` 등...
- 파이썬 관습은? 찾아보기
- 회사의 관습은 뭐가 있는지?

> 파이썬 관습: pep8 [naming convention](https://www.python.org/dev/peps/pep-0008/#naming-conventions)
> [pep8 naimng conventinos 정리]()
- reserved keyword인 경우 trailing underscore 권장
- dunder (`__foo__`)는 피하기
등등..



---

이야기거리
- 회사의 포매팅 관습?

