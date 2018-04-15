// includes all of the standard template library
#include <bits/stdc++.h>

using namespace std;

// typedefs for code shortening
typedef long long ll;
typedef pair<int, int> pi;
typedef vector<int> vi;

// macros for code shortening
// strings in the code are changed before the compilation
#define FOR(n) for (int i = 0; i < n; i++)
//#define FOR(a, b) for (int i = a; i <= b; i++)


// input / output
int get_n()
{
    int n;
    cin >> n;
    return n;
}
template <typename T1, typename T2> void fill_nm(T1& t1, T2& t2)
{
    cin >> t1 >> t2;
}
template <typename T> void fill_vector(std::vector<T> &arr, int n)
{   
    arr.reserve(n);
    copy_n(istream_iterator<T>(cin), n, back_inserter(arr));
}   

// friendly printing functions for debugging
template <typename T> void print_vector(std::vector<T> arr)
{
    for(auto value : arr) {
        cout << value << ' '; 
    }
    cout << '\n';
}
template <typename T1, typename T2> void print_map(std::map<T1, T2> M)
{
    for (auto& kv : M) {
        std::cout << '[' << kv.first << ": " << kv.second << "]\n";
    }
}
template <typename T> void print_vector_pairs(std::vector<T> arr)
{
    printf("[");
    for (auto& value : arr) {
        printf("[%d, %d], ", get<0>(value), get<1>(value));
    }
    printf("]\n");
}

// function to sort by the Mth element
template <typename T1> void sort_vector_tuples_by0(std::vector<T1> &v) {    
    std::sort(begin(v), end(v), [](auto const &t1, auto const &t2) 
        { return get<0>(t1) < get<0>(t2); });
}
template <typename T1> void sort_vector_tuples_by1(std::vector<T1> &v) {    
    std::sort(begin(v), end(v), [](auto const &t1, auto const &t2) 
        { return get<1>(t1) < get<1>(t2); });
}
template <typename T1> void sort_vector_tuples_by2(std::vector<T1> &v) {    
    std::sort(begin(v), end(v), [](auto const &t1, auto const &t2) 
        { return get<2>(t1) < get<2>(t2); });
}


int main() {

    // makes input and output more efficient
    ios::sync_with_stdio(0);
    cin.tie(0);
    
    // setup ~
    int n = get_n();
    vector<tuple<int, int, int>> ranges;
    int start_square = 1;
    
    // meat
    FOR(n) {
        int start, stop;
        fill_nm(start, stop);
        ranges.push_back(make_tuple(start, stop, i));
    }
    sort_vector_tuples_by0(ranges);
    vector<pi> answers;
    for (auto value : ranges) {
        while(start_square * start_square < get<0>(value)) {
            start_square++;
        }
        int count = 0;
        int tmp = start_square;
        while(tmp * tmp <= get<1>(value)) {
            count++;
            tmp++;
        }
        answers.push_back(make_pair(count, get<2>(value)));
    }
    sort_vector_tuples_by1(answers);
    for (auto value : answers) {
        printf("%d\n", get<0>(value));
    }
}

