# Python Naming Conventinos (PEP8)

## Descriptive: Naming Styles

- `b`, `B`, `lowercases`, `lower_case_with_underscores`, `UPPERCASE`, `UPPER_CASE_WITH_UNDERSCORES`, `CapWords`, `mixedCase` ...
- `_single_leading_underscore`: 약한 "internal use" 인디케이터. `from M import *`는 `_*`를 호출하지 않음
- `single_trailing_underscore_`: 충돌 피하기 위해서 사용됨. `Tkinter.Toplevel(master, class_='ClassName')`
- `__double_leading_underscore`: 클랫에서 사용되면 던더바랑 헷갈림, 사용자제
- `double_leading_and_trailing_underscoree__`: "magic" objects live in user-controlled namespaces. doucumented 된 이름만 사용하고 절대 새로만들지 말아라 ex) `__init__`, `__import__` ...

## Perscriptive: Naming Conventions

### Names to Avoid

변수명으로 `I`, `O`, `l` 단일 캐틱터 사용 금지 (몇몇 폰트에서 0 / 1로 보임). 쓸거면 `L`

### ASCII Compatibility

- standard library리에 쓰이는 Identifiers는 ASCII compatible 해야함
- [PEP-3131](https://www.python.org/dev/peps/pep-3131/#policy-specification) 참고
- non-ASCII 테스팅 하거나 저자명에만 (저자명의 경우에는 Latin alphabet 번역 추가)

### Packages and Module Names
- short, all-lowercase name 사용
- 가독성 향상을 위해 Underscore 사용 가능

### Class Names
- `CapWords` 컨벤션 주로 사용

### Type Variable Names
- [PEP 484](https://www.python.org/dev/peps/pep-0484/)에서 소개된 type variable 이름은 보통 `CapWord`에 짧게 사용

### Exceptions Name
- 예외는 class여야 하므로 클래스명 컨벤션이 여기 적용 (`CapWord`)
- suffix로 `Error` 붙여야함 (예외가 실제로 에러인경우)

### Global Variable Name
(한 모듈 안에서만 사용된다고 가정)
- function과 동일

### Function and Variable Nmaes
- 함수명은 lowerclass. 가독성 위해서 중간에 underscore 사용가능
- mixedCase는 이미 그런 스타일이 널리 사용될 때 retain 하기 위할때만 가능

### Function and Method Arguments
- instance method 안에 첫번째 argument로는 항상 `self`
- class method 안에 첫번째 argument로는 항상 `cls`

### Method Names and Instance Variables
- function naming rule을 사용
- non-public method / 변수에는 leading underscore (`_my_method`)
- dunder (`__my_method`)로 이름을 지으면 `Foo.__my_method`로 호출 할 수 없다.

### Constants
- 보통 all capital + underscore로 ex) `MAX_OVERFLOW`

### Designing for Inheritance

Pythonic guidelines
- Public attribute는 언더스코어로 시작하면 안된다
- reserved keyword와 겹친다면 뒤에 언더스코어를 붙이기
- accessor/mutator method 없이 attribute name만 노출하는게 좋음: 파이썬은 쉽게 추후 강화가 가능 (`@property` 등으로)
=> property는 new-style classes에서만 동작 / avoid using properties fofr computationally expensive operation
- 사용하지 않는 subclass가 있다면 `__Subclass()` 사용
