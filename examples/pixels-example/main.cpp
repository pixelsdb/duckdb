#include "duckdb.hpp"
#include <iostream>
#include "utils/ConfigFactory.h"

using namespace duckdb;

int main() {
	DuckDB db(nullptr);
	Connection con(db);
	std::string demo = ConfigFactory::Instance().getPixelsSourceDirectory() + "cpp/tests/data/example.pxl";
//    std::string demo = ConfigFactory::Instance().getPixelsSourceDirectory() + "cpp/cppout/1734406571.pxl";
	auto result = con.Query("SELECT * from '" + demo + "';");
	result->Print();
}
