#include <boost/algorithm/string.hpp>
#include <iostream>
#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string/classification.hpp>

using namespace std;
int main() {
    char cmdLine[128];
    fgets(cmdLine, 128, stdin);
    vector<string> strs;
    vector<string> output;
    string line(cmdLine);
    boost::split(strs, line, boost::is_any_of("\t"), boost::token_compress_on);
    cout << line << endl;
    //cout << strs << endl;
    for (vector<string>::iterator it = strs.begin(); it != strs.end(); ++it) {
        cout << *it << endl;
        output.push_back(boost::trim_left_copy(boost::trim_right_copy(*it)));
    }
    for (vector<string>::iterator it = output.begin(); it != output.end(); ++it) {
        cout << *it <<endl;
    }
}
