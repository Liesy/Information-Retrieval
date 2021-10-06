# Information Retrival

- LiYang, CS-AI, Shandong University
- Sep 15th, 2021 Created

---

## Content

### Expriment 1 (2021.9.14 -- 2021.10.13)

[reference code](https://blog.csdn.net/qq_43738932/article/details/112648411)

[nltk doc](https://www.cnblogs.com/chen8023miss/p/11458571.html)

1. 在tweets数据集上构建inverted index

2. 实现Boolean Retrieval Model,使用TREC 2014 test topics进行测试
   https://trec.nist.gov/data/microblog/2014/topics.desc.MB171-225.txt

3. Boolean Retrieval Model:
    - Input:a query (like Ron and Weasley)
    - Output: print the qualified tweets.
    - 支持and, or ,not(查询优化可以选做)

4. 对于tweets与queries使用相同的预处理

### Expriment 2 (2021.10.13 -- 2021.11.9)

1. 在Expriment 1 的基础上实现最基本的Ranked retrieval model
    - Input: a query (like Ron and Weasley)
    - Output: return the top K (eg., K=100) relevant tweets.
    - 使用SMART notation: lnc.ltn
    - Document: logarithmic tf (l as first character), no idf and cosine normalization
    - Query: logarithmic tf (l in leftmost column), idf (t in second column), no normalization

2. 改进inverted index
    - 在Dictionary中存储每个term的DF
    - 在posting list中存储term在每个doc中的TF with pairs (docID, tf)

3. 选做：支持所有的SMART Notations

### Expriment 3 (2021.11.9 -- 2021.12.8)

1. 实现以下指标评价，并对Experiment2的检索结果进行评价
    - Mean Average Precision (MAP)
    - Mean Reciprocal Rank (MRR)
    - Normalized Discounted Cumulative Gain (NDCG)
    - [dataset](https://trec.nist.gov/data/microblog/2014/qrels2014.txt)