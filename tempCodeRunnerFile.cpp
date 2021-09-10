#include <iostream>
#include<cstring>
using namespace std;
int main()
{
short num = 16;
short& ref = num;
++ref;
cout << ref << " " << num << endl;
}