# Information Retrival

- LiYang, CS-AI, Shandong University
- Sep 15th, 2021 Created

---

## Content

### Expriment 1 (2021.9.14 -- 2021.10.13)

1. 在tweets数据集上构建inverted index

2. 实现Boolean Retrieval Model,使用TREC 2014 test topics进行测试
https://trec.nist.gov/data/microblog/2014/topics.desc.MB171-225.txt

3. Boolean Retrieval Model:
   - Input:a query (like Ron and Weasley)
   - Output: print the qualified tweets. 
   - 支持and, or ,not(查询优化可以选做)

4. 对于tweets与queries使用相同的预处理