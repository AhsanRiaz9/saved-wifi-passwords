# Saved Wifi Passowrds
You can list all wifi passwords saved in windows. 
All passwords will be saved in a text file.


## Build
You can use GNU C++ compiler to build the program.

```
g++ -std=c++11 wifi.cpp -o wifi.exe
```

## Usage

```
wifi
```

Output will be saved in a the file `saved-wifi-passwords.txt`.

**Note:** It will replace the contents of output file, not append it.
