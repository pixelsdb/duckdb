#include <iostream>
#include "duckdb.hpp"
#include "utils/ConfigFactory.h"
#include <sys/stat.h> // For checking file existence with stat()


using namespace duckdb;

// Function to check if a file exists (C++11-compatible)
bool fileExists(const std::string& filename) {
    struct stat buffer;
    return (stat(filename.c_str(), &buffer) == 0);
}

int main() {
    DuckDB db(nullptr);
    Connection con(db);

    // Get the base directory from the configuration
    std::string baseDir = ConfigFactory::Instance().getPixelsSourceDirectory();

    // Try the first file path
    std::string demo = baseDir + "cpp/tests/data/example.pxl";

    // If the first path does not exist, try the second path
    if (!fileExists(demo)) {
        std::cout << "File not found at: " << demo << "\nTrying alternative path...\n";
        demo = baseDir + "tests/data/example.pxl";
    }

    // If neither path exists, throw an error
    if (!fileExists(demo)) {
        throw std::runtime_error("File not found in both paths.");
    }

    // Execute the query and print the result
    auto result = con.Query("SELECT * from '" + demo + "';");
    result->Print();
}