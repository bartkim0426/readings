/* 유도속성을 사용하지 않고 나이를 구하는 class */
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

int main() {
    Person seul;
    seul.setYearOfBirth(1992);
    int age = seul.getAge();
    std::cout << "My age is " << age << "\n";
    return 0;
}
