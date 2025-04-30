import java.io.*;
import java.util.*;

public class Main {
    public static boolean findPairWithDiff(int[] arr, int n, int k) {
        // Using HashSet for O(n) solution
        HashSet<Integer> set = new HashSet<>();
        
        for(int i = 0; i < n; i++) {
            // Check if arr[i] - k exists in set
            if(set.contains(arr[i] - k)) {
                return true;
            }
            // Check if arr[i] + k exists in set
            if(set.contains(arr[i] + k)) {
                return true;
            }
            // Add current element to set
            set.add(arr[i]);
        }
        return false;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int T = sc.nextInt();  // number of test cases
        
        while(T-- > 0) {
            int N = sc.nextInt();  // size of array
            int K = sc.nextInt();  // required difference
            
            int[] arr = new int[N];
            for(int i = 0; i < N; i++) {
                arr[i] = sc.nextInt();
            }
            
            System.out.println(findPairWithDiff(arr, N, K));
        }
        sc.close();
    }
}