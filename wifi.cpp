#include <iostream>
#include <fstream>
#include <string.h>
#include <stdexcept>
#include <stdio.h>
#include <string>
#include <vector>

using namespace std;

string exec(const char* cmd) {
    char buffer[128];
    string result = "";
    FILE* pipe = _popen(cmd, "r");
    if (!pipe) throw runtime_error("_popen() failed!");
    try {
        while (fgets(buffer, sizeof buffer, pipe) != NULL) {
            result += buffer;
        }
    } catch (...) {
        _pclose(pipe);
        throw;
    }
    _pclose(pipe);
    return result;
}

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
	vector<string> output;
	while(getline(ifs,data))
	{
		temp="netsh wlan show profile \"";
		temp+=data;
		temp+="\" key=clear";
		output.push_back(exec(temp.data()));
	}
	ifs.close();
	remove("out.txt");

	ofstream ofs("saved-wifi-passwords.txt");
	for (string str: output)
		ofs << str;
	ofs.close();
	
	return 0;
}
