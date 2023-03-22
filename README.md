**Compression Algorithm Design**

I chose to implement the Huffman coding algorithm to compress an array of bytes. 
This algorithm assigns codes to each unique value in the data and then uses these codes as a map to the original codes.
The most frequently occurring values are assigned codes that have fewer bits than less frequently occurring values. 
The codes that are generated from the algorithm are variable in length and have unique prefixes, making it a lossless algorithm. 
The 3 main reasons that I selected this method are:

* **Characteristics of input:** It is common that the input contains repeated values. This algorithm assigns a code to each UNIQUE value. Therefore, if there are a lot of repeated values, fewer codes will be required, and less information will need to be stored. 
* **Maintainability:** One of the criteria was maintainability. This implementation is easy to understand and therefore, would require less overhead for developers to maintain it. I considered using Arithmetic Encoding, but that algorithm is harder to understand and implement, thus decreasing maintainability. 
* **Lossless:** This is a lossless algorithm, meaning that no data is lost when the encoding happens and that the data can be decoded to its original form.

The time complexity of this implementation is O(n). It takes O(n) time to produce the frequency table and O(nlogn) to complete the encoding binary tree. 

The space complexity is O(m + k), where m is the # of bits in the encoded output, and k is the number of unique values in the data (map of codes to values). 

**TO RUN ALGORITHM**
* Type `python3 compression.py` into the command line or run [compression.py](compression.py) from an IDE.
* In the main function on line 161, byte_compress() is called and takes a byte array as input.

I have created a test suite in [tests.py](tests.py) for each function in the algorithm. To run these tests, uncomment lines 157 & 158 (compression.py) in the main function.

The function [byte_compress()](compression.py) takes an array of bytes and returns an encoded version of this array. I have included some sample data in the file [test_data.py](test_data.py) to see how the algorithm handles both small and large arrays.
byte_compress() first does a validation check on the data to ensure that it is an array of bytes and the array is greater than length 1. If the array only has one element in it, this algorithm will not be useful. 
After the validation check, the function calls multiple helper functions to work through the encoding. I have added a check at the end to make sure that the algorithm was successfully lossless. I have also provided a visual of the 
binary tree that the algorithm creates in the encoding process. This is commented out on line 134 (compression.py).

I calculated a compression ratio, which gives the # of compressed bytes per raw byte. When the function is executed, a few metrics will print out, such as, size of the data before and after encoding, the compression ratio, and the run time.

Resources I used:
* https://dzone.com/articles/crunch-time-10-best-compression-algorithms
* https://www.derczynski.com/papers/archive/BPE_Gage.pdf
* https://stackoverflow.com/questions/2675756/efficient-array-storage-for-binary-tree
* https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/ 
* https://arxiv.org/pdf/1109.0216.pdf#:~:text=Our%20implemented%20results%20show%20that,easier%20than%20the%20Arithmetic%20coding
* http://site.iugaza.edu.ps/jroumy/files/Arithmetic-Coding.pdf
* https://neptune.ai/blog/lossless-data-compression-using-arithmetic-encoding-in-python-and-its-applications-in-deep-learning#:~:text=Overview%20of%20the%20lossless%20algorithm%20(Arithmetic%20Encoding)&text=Lossless%20algorithms%20reconstruct%20original%20data,of%20bits%20to%20compress%20data





