/* 유도속성을 사용하지 않고 월급을 구하는 class */
# include <iostream>

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


int main() {
    Worker seul;
    seul.setWorkandWage(20, 200);
    std::cout << "My salary is " << seul.getSalary() << "\n";
    return 0;
}
