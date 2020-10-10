#include<iostream>
using namespace std;
#include<fstream>
#include<string.h>
void saveProfileNames()
{
	system("t.cmd");
	system("cls");
	//save all profiles name in out.txt
}
int main()
{
	saveProfileNames();
	ifstream ifs("out.txt");
	string data;
	string temp;
	while(getline(ifs,data))
	{
		temp="netsh wlan show profile \"";
		temp+=data;
		temp+="\" key=clear >> swp.txt";
		system(temp.data());
	}
	ifs.close();
	remove("temp.txt");
	rename("swp.txt","saved-wifi-passwords.txt");
	return 0;
}
