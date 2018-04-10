#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <iterator>
#include <algorithm>
using namespace std;


int get_n()
{
    int n;
    cin >> n;
    return n;
}

template <typename T> void fill_vector(std::vector<T> &arr, int n)
{   
    arr.reserve(n);
    copy_n(istream_iterator<T>(cin), n, back_inserter(arr));
}   

template <typename T> void print_vector(std::vector<T> arr)
{
    for(auto value : arr) {
        cout << value << ' '; 
    }
    cout << '\n';
}

int main() {
    
    int n = get_n();
    std::vector<int> arr;
    fill_vector(arr, n); 
    print_vector(arr);

}




