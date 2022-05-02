# group-project-s22-furious-five

Relevant links
- Assignment handout: https://github.com/ckaestne/seai/blob/S2022/assignments/project.md
- Recitation 2 (Kafka): [https://github.com/ckaestne/seai/tree/S2022/recitations/02_kafka](https://github.com/ckaestne/seai/tree/S2022/recitations/02_kafka)
- Notion: https://www.notion.so/f2620d75dbe245e5914afe5bac33b165?v=580c48b57ec44112abda718bf00450ec
- Shared Drive Folder - https://drive.google.com/drive/folders/1HuB7o-MEjlaJWel_OlCx55E0skNOm90O?usp=sharing

Using kcat/kafka
```
pip install kafka-python
brew install kcat
kcat -b localhost -t movielog12 > movies.txt
```

Data from stream

- Watch data: 2021-12-30T20:52:08,763687,GET /data/m/men+in+black+1997/12.mpg
    - UserID: 763687
    - MovieID: men+in+black+1997
- Rate data: 2022-01-04T02:46:26,850894,GET /rate/showgirls+1995=4
    - UserID: 850894
    - MovieID: showgirls+1995
    - Rating: 4

Data from API

- [http://128.2.204.215:8080/movie/](http://128.2.204.215:8080/movie/star+trek+2009)<movie_id>: [http://128.2.204.215:8080/movie/star+trek+2009](http://128.2.204.215:8080/movie/star+trek+2009)
- [http://128.2.204.215:8080/user/](http://128.2.204.215:8080/user/505573)<user_id>: [http://128.2.204.215:8080/user/505573](http://128.2.204.215:8080/user/505573)

