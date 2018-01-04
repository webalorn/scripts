#include <fstream>
#include <string>
#include <iostream>
#include <cstdlib>
#include <iomanip>
#include <chrono>
#include <ctime>
 
using namespace std;

int main(int nbArg, char** argTab)
{
    string inFile = "in1";
    string fileName = "main.cpp";

    if (nbArg >= 2) {
        inFile = argTab[1];
    }
    if (nbArg >= 3) {
        string fileName = argTab[2  ];
    }
    
    ifstream file(fileName.c_str());
    if(!file){
        std::cout << "Ce fichier c++ n'existe pas !" << std::endl;
        return 0;
    }
    file.close();
    
    string command;
    
    //string command = "echo \"---------compilation...\" && g++ "+fileName+".cpp -o exeOut -Wall && ./exeOut && 
    //string command = "cp "+fileName+"-"+inNum+".in "+fileName+".in";
    //std::system(command.c_str());
    
    command = "g++ "+fileName+" -o exeOut -Wall -std=c++11";
    cout << "---------- Compilation..." << endl;
    if (std::system(command.c_str())) {
        cout << endl << endl << "La compilation a echouee" << endl;
        return 0;
    }
    cout << endl << "=> compilation success" << endl;
    
    command = "./exeOut < "+inFile+" > g++11.out";
    cout << "--------- Execution..." << endl;
    
    std::clock_t c_start = std::clock();
    auto t_start = std::chrono::high_resolution_clock::now();
    
    int exeCode = std::system(command.c_str());
    
    std::clock_t c_end = std::clock();
    auto t_end = std::chrono::high_resolution_clock::now();
    
    cout << endl << endl;
    

    cout << "---------- Output: " << endl;
    command = "cat g++11.out && rm g++11.out";
    std::system(command.c_str());
        
    if (exeCode != 0) {
        cout << endl << endl << "<=====> Le programme a échoué <=====>" << endl;
    }
    
    cout << endl << endl << "---------- Execution Detail: " << endl << endl;
    
    cout << "Return code: " << exeCode << endl;
    std::cout << std::fixed << std::setprecision(2) << "CPU time used: "
              << 1000.0 * (c_end-c_start) / CLOCKS_PER_SEC << " ms\n"
              << "Wall clock time passed: "
              << std::chrono::duration<double, std::milli>(t_end-t_start).count()
              << " ms\n";
    
    
    //command = "rm exeOut"; std::system(command.c_str());
}
