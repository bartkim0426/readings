django를 사용하면서 자주 사용하는 클래스 구조. 이해 없이 사용했지만 최근 javascript 스터디를 하면서 클래스로 이런저런 프로젝트르 진행하게 되었고, 덕분에 OOP의 기본인 클래스에 대해 관심이 생겨 이 책을 추천받게 되었다.

읽고 나서는 클래스에 대한 개념이 어느정도 잡혔으면.

## Todo

- [ ]  UML 활용해서 직접 짜보기
- [ ]  C++ 프로젝트 디렉토리 만들기(예시용)
- [ ]  C++ 클래스 기본 개념 공부하기 (책읽을수 있는 정도만)

# 1장. 객체지향 개념

- `UML` : Unified Modeling Language - 객체지향 방법론 프로젝트에서 표준적으로 사용하는 표기법. 실제 UML을 활용해서 프로젝트 모델링을 짜보면 좋을것
- C++ 언어에서의 메세지 전송(?)

# 2장. 클래스

## 유스케이스 기반 클래스 도출

실제로 클래스 도출할때 이런식으로 생각하면서 도출하면 될듯.

- 경계 클래스: 인터페이스 역할. actor(사용자)와 시스템.
- 실체 클래스: 영속적인 정보, 실제 db인듯
- 제어 클래스: control logic, business logic. django에서 view단

## 검토방법

- 오직 하나의 대상과 개념만을 나타내는지?
- 높은 응집도, 낮은 결합도
- 구체적, 명확한 이름

⇒ 실제로 이를 활용하여 db 구성을 해보자

**경계클래스**

메인페이지

회원가입, 로그인 (아이디찾기 등)

마이페이지

회원변경? (개인-기업회원간)

주문(프로젝트 결제)

예치금 충전

결제

**실체클래스**

User

Project

Board

Point

AppliedProject? (Order)

예치금

**제어클래스 → django 사용하면 큰 의미가 없는듯?**

(정확히 어떤건지 잘 모르겠지만)

로그인, 회원가입 기능

문자(카톡), 메일 전송 기능

주문 기능 

예치금 (포인트) 결제 기능

⇒ 실제 필요한 클래스로 정리 ⇒ 이건 클래스가 아니라 app단위, class를 짜보자

User

UserDate

Auth?

Project
ProjectData

Board

Point

Balance (Deposit?)

Order (Investments)

Stock (Wallet) (개인 지갑??) ⇒ deposit이 아니라 투자하여 발행된 주식 token

# 3장. 속성

속성이란?

- 클래스가 나타내는 객체들이 저장하는 데이터

## UML에서 속성 표현

`[가시성] 이름 [:타입][다중성][=초기값]`

1. 가시성: public, private, protect, package가 있는듯 (패키지는 어떤개념?)
2. 이름: 고유한 이름. 약어는 웬만하면 안쓰는게 좋다 (표준약어는 괜찮음)
3. 다중성: 여러개를 가질수있는지?
4. 타입: 실제 가질수있는 값. C++의 경우에는 char*, int등의 기본타입을 이용하던지 String, Integer 등 클래스를 정의하고 사용해야함. ⇒ 개발자가 정의한 클래스도 사용 가능. 
5. 초기값: 객체에 따라 다른 초기값이 필요한 경우에는 cosntructor를 이용해아함

```cpp
# include <string>
# include <iostream>
using namespace std;

class Student {
    private:
        string id;
        string name;
        string address[2];
        /* Department department; */
        int year;
    public:
        Student() {
            year = 1;
        }
        string publicname;
        void printname()
        {
            std::cout << "Public name is: " << publicname;
        }
};


int main() 
{
    Student Seul;
    Seul.publicname = "seul";
    Seul.printname();
    return 0;
}
```


**속성과 객체**

- 속성은 값 자체를 의미하고 독립적인 존재로서 의미는 없다!
- 객체는 기본적으로 고유하다 ⇒ 특별한 방법 없이 구분이 필요 : 아이디를 속성으로 기술할 필요가 있음

## 고급 속성

**인스턴스 범위의 속성** (instance scope attribute)

- 속성 값이 각 객체별로 의미가 있는 경우. 일반적인 속성들

**클래스 범위의 속성** (class scope attribute)

- 클래스에 대해서 정의된 속성: 모든 객체들이 공유할 수 있는 정보?
- ex) 전체 등록된 강좌의 총 수 등

**C++ example**

- class 내부에 `static` 키워드를 사용하여 정의
- `int Course::total = 0;`으로 직접 데이터 멤버를 정의해주어야함


```cpp
# include <iostream>

class Course {
    private:
        char* id;
        char* name;
        int credit;
    public:
        static int total;
        void printtotal()
        {
            std::cout << "Count number is " << total << "\n";
        }
};

int Course::total = 0;

int main() 
{
    Course python;
    python.printtotal();
    std::cout << "(not function) Count number is " << python.total << "\n";
    return 0;
}
```

**유도 속성** (derived attribute)

- 다른 속성들에 의해서 결정될 수 있는 속성
- ex) 생년월일 ⇒ 나이값 유도
- 엄밀히 말하면 이는 다른 속성값으로 계산될 수 있으므로 반드시 필요한 것은 아님! 다음과 같은 상황에서 사용
1. 모델의 이해도를 향상 : 명시적으로 유도속성 기술
2. 성능 향상 : 매번 계산하면 비효율적

**c++ ex)**

- person의 생년월일 ⇒ 나이
- 직원의 일급, 근무일수 ⇒ 월급

    
    
```cpp
/* 유도속성을 사용하지 않고 월급을 구하는 class */
# include <iostream>


class Person {
    private:
        char* name;
        char* address;
        int yearOfBirth;
    public:
        void setYearOfBirth(int year) {
            yearOfBirth = year;
        }
        int getAge() {
            int currentYear = 2018;
            return currentYear - yearOfBirth;
        }
};

class Worker {
    private:
        char* name;
        char* address;
        int dayOfWork;
        int dailyWage;
    public:
        void setWorkandWage(int day, int wage) {
            dayOfWork = day;
            dailyWage = wage;
        }
        int getSalary() {
            return dayOfWork * dailyWage;
        }
};

/* 유도속성을 사용하여 성능 향상 */
class Worker {
    private:
        char* name;
        char* address;
        int dayOfWork;
        int dailyWage;
        /* 유도속성 사용 */
        int salary;
        void computeSalary() {
            salary = dayOfWork * dailyWage;
        }
    public:
        void setWorkandWage(int day, int wage) {
            dayOfWork = day;
            dailyWage = wage;
            computeSalary();
        }
        int getSalary() {
            return salary;
        }
};
```


# 4장. 연산
