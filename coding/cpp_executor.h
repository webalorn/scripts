#include <fstream>
#include <string>
#include <iostream>
#include <cstdlib>
#include <iomanip>
#include <chrono>
#include <ctime>
#include <vector>

class CppExecutor {
private:
	std::string m_version;
	std::vector<std::string> args;

	std::string inFile = "in1";
	std::string fileName = "main.cpp";

	int bash(std::string);
	void use_args();

public:
	CppExecutor();
	CppExecutor(std::string version_id);

	void set_version(std::string version_id);
	void give_args(int nbArg, char** argTab);

	int exec();
};

// Init
CppExecutor::CppExecutor() {
	set_version("g++11");
}

CppExecutor::CppExecutor(std::string version_id) {
	set_version(version_id);
}

void CppExecutor::set_version(std::string version_id) {
	m_version = version_id;
}

void CppExecutor::give_args(int nbArg, char** argTab) {
	args.resize(nbArg-1);
	for (int iArg = 0; iArg < nbArg-1; iArg++) {
		args[iArg] = argTab[iArg+1];
	}
}

// Execution

int CppExecutor::bash(std::string command) {
    return std::system(command.c_str());
}

void CppExecutor::use_args() {
	for (uint iArg = 0; iArg < args.size(); iArg++) {
		std::string arg_value = args[iArg];
		switch (iArg) {
			case 0:
				inFile = arg_value;
				break;
			case 1:
				fileName = arg_value;
		}
	}
}

int CppExecutor::exec() {
	using namespace std;

	use_args();
    
    ifstream file(fileName.c_str());
    if 	(!file){
        cout << "Ce fichier c++ n'existe pas !" << endl;
        return EXIT_FAILURE;
    }
    file.close();
    
    /* Compilation */
    cout << "---------- Compilation (" << m_version << ")" << endl;
    if (bash("g++ "+fileName+" -o exeOut -Wall -std=" + m_version)) {
        cout << endl << endl << "La compilation a echouée" << endl;
        return EXIT_FAILURE;
    }
    cout << endl << "=> compilation success" << endl;
    
    /* Execution */
    cout << "--------- Execution" << endl;
    
    clock_t c_start = clock();
    auto t_start = chrono::high_resolution_clock::now();
    
    int exeCode = bash("./exeOut < "+inFile+" > cpp_executor.out");
    
    clock_t c_end = clock();
    auto t_end = chrono::high_resolution_clock::now();
    
    cout << endl << endl;
    
    /* Output */
    cout << "---------- Output: " << endl;
    bash("cat cpp_executor.out && rm cpp_executor.out");
        
    if (exeCode != 0) {
        cout << endl << endl << "<=====> Le programme a échoué <=====>" << endl;
    }
    
    cout << endl << endl << "---------- Execution Detail: " << endl << endl;
    
    cout << "Return code: " << exeCode << endl;
    cout << fixed << setprecision(2) << "CPU time used: "
              << 1000.0 * (c_end-c_start) / CLOCKS_PER_SEC << " ms\n"
              << "Wall clock time passed: "
              << chrono::duration<double, milli>(t_end-t_start).count()
              << " ms\n";
    
    
    bash("rm exeOut");
    return EXIT_SUCCESS;
}