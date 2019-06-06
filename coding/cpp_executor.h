#include <fstream>
#include <string>
#include <iostream>
#include <cstdlib>
#include <iomanip>
#include <chrono>
#include <ctime>
#include <vector>

#ifdef _WIN32
#include <intrin.h>
#else
#include <x86intrin.h>
#endif

class CppExecutor {
private:
	std::string m_version;
	std::vector<std::string> args;

	std::string inFile = "in1";
	std::string fileName = "main.cpp";
    bool helpMode = false;

	int bash(std::string);
	void use_args();

public:
	CppExecutor();
	CppExecutor(std::string version_id);

	void set_version(std::string version_id);
	void give_args(int nbArg, char** argTab);

	int exec();
    void print_help();
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

        if (iArg == 0 && (arg_value == "-h" || arg_value == "--help")) {
            helpMode = true;
            return;
        }

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

    if (helpMode) {
        print_help();
        return 0;
    }
    
    ifstream file(fileName.c_str());
    if 	(!file){
        cout << "Ce fichier c++ (" << fileName << ") n'existe pas !" << endl;
        return EXIT_FAILURE;
    }
    file.close();
    
    /* Compilation */
    cout << "---------- Compilation (" << m_version << ")" << endl;
    if (bash("g++ "+fileName+" -o exeOut -Wall -Don_local -std=" + m_version)) {
        cout << endl << endl << "La compilation a echouée" << endl;
        return EXIT_FAILURE;
    }
    cout << endl << "=> compilation success" << endl;
    
    /* Execution */
    cout << "--------- Execution" << endl;
    
    clock_t c_start = clock();
    auto t_start = chrono::high_resolution_clock::now();
    
    int exeCode = 0;
    if (inFile == "0") {
        exeCode = bash("./exeOut > cpp_executor.out");
    } else {
        exeCode = bash("time ./exeOut < "+inFile+" > cpp_executor.out");
    }
    
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
    cout << fixed << setprecision(2) //<< "CPU time used: "
              << "CPU time used is user + sys at the end of 'execution'\n"
              //<< 1000.0 * (c_end-c_start) / CLOCKS_PER_SEC << " ms\n"
              << "Wall clock time passed: "
              << chrono::duration<double, milli>(t_end-t_start).count()
              << " ms\n";
    
    
    bash("rm exeOut");
    return EXIT_SUCCESS;
}

void CppExecutor::print_help() {
    std::cout << "Usage : <command name> [input_file_name] [code_file_name]\n"
        << "All arguments are facultatives and have the given default values:\n"
        << "    - input_file_name : " << inFile << "\n"
        << "    - code_file_name : " << fileName << "\n"
        << "\n"
        << "This command compile the code in 'exeOut' using gcc with this c++ version : " << m_version << "\n"
        << "The program is then executed. The default output and error output are separated\n"
        << "\n"
        << "\n"
        << "Special behavior : to not use input file but just standard input, use 0 instead of input_file_name\n";
}