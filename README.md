2024년 2학기 대학글쓰기1 과제3을 위한 데이터 전처리와 데이터 분석에 사용된 코드\n\n

공공데이터 포털에서 모은 헬스장, 영화관, 공공도서관의 좌표값을 가지고 각 문화시설 별 밀도를 계산하는 방식\n
자세한 방법은 다음과 같음\n
특정 도시 내 특정 문화시설(도서관)이 $n$개 있고 이들을 각각 $X_1, \ldots, X_n$이라 할 때 $i = 1,2,\ldots, n$에 대해
$\delta_i = min\{ |X_1 - X_i|, |X_2 - X_i|, \ldots, |X_n - X_i|\}$라 하면 $D = {\delta_1, \delta_2, \ldots, \delta_n}$을 구할 수 있다.\n
여기서 $\bar{D} = \frac{1}{n} \sum\limits^{n}_{i=1} \delta_i$이라 하면 각 문화시설별 $\bar{D}$를 비교해 각 문화시설 별 밀도를 구할 수 있다.
가설은 '공공도서관의 밀도가 다른 문화시설 보다 유의미하게 낮아 접근성이 떨어지고 이는 곧 공공도서관을 잘 이용하지 않는 이유이다'였으나...\n
실제로 데이터를 구해 계산해보니 유의미한 차이를 보이지 않아서 멸망해버린 프로젝트
