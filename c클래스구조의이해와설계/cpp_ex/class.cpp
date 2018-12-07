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
