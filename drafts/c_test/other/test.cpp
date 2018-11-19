#include <iostream>
#include <vector>
#include <time.h>
#include "IntCell.hpp"
using namespace std;

// Broken binarySearch because of call-by-value
 int binarySearch( const vector<int> &arr, int x ) {
     int low = 0, high = arr.size( ) - 1;
     while( low <= high ) {
         int mid = ( low + high ) / 2;
         if( arr[ mid ] == x )
         return mid;
     else if( x < arr[ mid ] )
         high = mid - 1;
     else
         low = mid + 1;
     }
     return -1; // not found
 }

 int binarySearch( vector<int> *arr, int x ) {
     int low = 0, high = arr->size( ) - 1;
     while( low <= high ) {
         int mid = ( low + high ) / 2;
         if( (*arr)[ mid ] == x )
         return mid;
     else if( x < (*arr)[ mid ] )
         high = mid - 1;
     else
         low = mid + 1;
     }
     return -1; // not found
 }
 int main( ) {
     IntCell a(2);
     IntCell b(5);
     IntCell c;
     c = a + b;
     cout << a.getValue() << endl;
     cout << b.getValue() << endl;
     cout << c.getValue() << endl;
  }
