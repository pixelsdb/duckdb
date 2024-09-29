//
// Created by whz on 9/29/24.
//
#include "duckdb.hpp"
#include <iostream>
//#include "utils/ConfigFactory.h"

using namespace duckdb;

int main() {
	DuckDB db(nullptr);
	Connection con(db);
//	std::string demo = ConfigFactory::Instance().getPixelsSourceDirectory() + "cpp/tests/data/example.pxl";
	std::string demo="/home/whz/dev/pixels/cpp/pixels-duckdb/data/parquet-testing/candidate.parquet";
	auto result = con.Query("SELECT * from '" + demo + "';");
	result->Print();
}