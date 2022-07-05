# Amazon-Products-Co-Purchased-Network
Explore the characteristics of the network and discover the most influential determinants in co-purchased item sales
\
Team: Xin Zhao, Ruixi Wang, Xinyi Chen, Xintian Shen

## Dataset

Amazon product co-purchasing network metadata data sctructure:

![image](https://user-images.githubusercontent.com/73065775/177401293-6b885572-4a01-4445-a374-9673f97ca5e4.png)



### Data_Preparation.py:
(This program transfer string file into a csv and extracted necessary infromation with regex)

Data source: http://snap.stanford.edu/data/amazon-meta.html \

data_preparation.py average running time: 1 hr 15 min, RAM allocate: 1.5 G. intel i7 \

To speed up the process, try Running Python script on GPU by using package: from numba import jit, cuda \

Output file is csv object that will be used in DataFrame_preparation.py

### DataFrame_preparation.py:
(This program transfer csv file from previous step into edge list file and attributes file)

![image](https://user-images.githubusercontent.com/73065775/177402032-76637094-fedb-4859-92c9-2a916a674cbe.png)

## Network Gephi visualization
- Node: Amazon products
- Tie: Co-purchased relations
- Color: Categories
  - Pink: Books
  - Green: Video tapes
  - Orange: Music
![network](https://user-images.githubusercontent.com/73065775/177402329-20f8d6e3-cfd8-4138-b97f-cf4909961e98.png)

## Network characteristics
### amazon_meta_network.R

![image](https://user-images.githubusercontent.com/73065775/177402982-1f8079a7-e16f-482f-8c31-73118423454c.png)

## Network Degree > 28

![image](https://user-images.githubusercontent.com/73065775/177403692-592ba9c9-2260-44c5-9778-9c2a1982a06a.png)

Degree:
- Highly centralized in degree centrality

Eigenvector
- Not centralized in eigenvector centrality
- High degree products know no influential neighbors

Conclusion
- A local but giant hub in the scoped network is surprisingly not a significant bridge


## Regression model Data Exploratory Analysis

Available network features:

![image](https://user-images.githubusercontent.com/73065775/177404123-6373948a-ff3a-4a20-ad48-a99712878d0a.png)

LassoLarsIC features selection:
- Avg_rating
- Degree
- Closnesscentrality

## Regression model result
![image](https://user-images.githubusercontent.com/73065775/177404532-2fa84007-cc3c-4feb-96fb-013d91704c1d.png)

### High sales products have high degrees but a low closeness centrality


## Regression model result explanation 

![image](https://user-images.githubusercontent.com/73065775/177404675-f66f8685-e870-4e83-9c05-6df7d77c3a6d.png)

The size of the node is ranked by degree. The color of the node is category. The example product is a book called negotiating agreement without giving, the avg rating is 4.5, the sales rank is 220 out of 500k products. The degree is 158, and closenesscentrality is 0.1579. The degree of the product shows that it has 158 co-purchased products, but its co-purchased products’ degree is very low. It means that the co-purchased products are barely co-purchased with other products. Accordingly, this product has a high degree with a low closenesscentrality.
