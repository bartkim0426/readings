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
