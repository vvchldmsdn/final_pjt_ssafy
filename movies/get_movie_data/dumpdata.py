import json
import requests
from copy import deepcopy
from pprint import pprint

spoken_language_dict = dict()
s_idx = 1
collection_dict = {
    '시리즈 없음': 0
}
production_countries_dict = dict()
p_idx = 1


# 영화 정보 받아오기
movie_results = []
spoken_languages_results = []
production_coutries_results = []
collections_result = []

Base_URL = "https://api.themoviedb.org/3"
path = "/discover/movie"
params = {
    "api_key": "d1a4feab78e87ac758f0b64d63f14214",
    "language": "ko-KR",
}

for page in range(2, 4):
    params_tmp = deepcopy(params)
    params_tmp["page"] = page

    response = requests.get(Base_URL + path, params=params_tmp).json()
    data = response.get("results")

    # 영화 하나 당 정보 찾기 시작 for 문
    for movie in data:
        # 영화 정보 하나 당 detail 페이지에서 spoken_language, production_countries, belongs_to_collections 정보 받아와야 함
        movie_id = movie.get("id")

        detail_response = requests.get(
            Base_URL + f"/movie/{movie_id}", params=params
        ).json()
        collection = detail_response.get("belongs_to_collection")  # 딕셔너리 형태
        countries = detail_response.get("production_countries")  # 리스트 형태 / 각 요소는 딕셔너리
        languages = detail_response.get("spoken_languages")  # 리스트 형태 / 각 요소는 딕셔너리

        # 내가 정해주는 pk(id)값 담을 배열
        language_ids = []
        countries_ids = []
        collection_ids = 0

        # spoken_language id값 설정
        for language in languages:
            if language["english_name"] not in spoken_language_dict:
                spoken_language_dict[language["english_name"]] = s_idx
                language_ids.append(spoken_language_dict[language["english_name"]])
                s_idx += 1
            else:
                language_ids.append(spoken_language_dict[language["english_name"]])

        # production_countries id값 설정
        for country in countries:
            if country["name"] not in production_countries_dict:
                production_countries_dict[country["name"]] = p_idx
                countries_ids.append(production_countries_dict[country["name"]])
                p_idx += 1
            else:
                countries_ids.append(production_countries_dict[country["name"]])

        # belongs_to_collection id 값 설정
        if collection != None:
            if collection["name"] not in collection_dict:
                collection_dict[collection["name"]] = collection["id"]
                collection_ids = collection.get("id")

        movie_dict = {
            "model": "movies.movie",
            "pk": movie_id,
            "fields": {
                "title": movie.get("title"),
                "poster_path": movie.get("poster_path"),
                "overview": movie.get("overview"),
                "genre_ids": movie.get("genre_ids"),
                "language_ids": language_ids,
                "productioncountry_ids": countries_ids,
                "collection_ids": collection_ids,
            },
        }
        movie_results.append(movie_dict)

with open("movies.json", "w", encoding="UTF-8") as file:
    file.write(json.dumps(movie_results, ensure_ascii=False))


# 2. 장르 정보 쓰기
data = [
    {"id": 28, "name": "액션"},
    {"id": 12, "name": "모험"},
    {"id": 16, "name": "애니메이션"},
    {"id": 35, "name": "코미디"},
    {"id": 80, "name": "범죄"},
    {"id": 99, "name": "다큐멘터리"},
    {"id": 18, "name": "드라마"},
    {"id": 10751, "name": "가족"},
    {"id": 14, "name": "판타지"},
    {"id": 36, "name": "역사"},
    {"id": 27, "name": "공포"},
    {"id": 10402, "name": "음악"},
    {"id": 9648, "name": "미스터리"},
    {"id": 10749, "name": "로맨스"},
    {"id": 878, "name": "SF"},
    {"id": 10770, "name": "TV 영화"},
    {"id": 53, "name": "스릴러"},
    {"id": 10752, "name": "전쟁"},
    {"id": 37, "name": "서부"},
]

result = []

for genre in data:
    genre_dict = {
        "model": "movies.genre",
        "pk": genre.get("id"),
        "fields": {"name": genre.get("name")},
    }
    result.append(genre_dict)

with open("genres.json", "w", encoding="UTF-8") as file:
    file.write(json.dumps(result, ensure_ascii=False))


# 3. 사용 언어 정보 받기
for language in spoken_language_dict:
    language_dict = {
        "model": "movies.spokenlanguage",
        "pk": spoken_language_dict[language],
        "fields": {"name": language},
    }
    spoken_languages_results.append(language_dict)

with open("spokenlanguages.json", "w", encoding="UTF-8") as file:
    file.write(json.dumps(spoken_languages_results, ensure_ascii=False))


# 4. 제작 국가 정보 받기
for country in production_countries_dict:
    country_dict = {
        "model": "movies.productioncountry",
        "pk": production_countries_dict[country],
        "fields": {"name": country},
    }
    production_coutries_results.append(country_dict)

with open("productioncountries.json", "w", encoding="UTF-8") as file:
    file.write(json.dumps(production_coutries_results, ensure_ascii=False))


# 5. collection 정보 받기
for collection in collection_dict:
    c_dict = {
        "model": "movies.collection",
        "pk": collection_dict[collection],
        "fields": {"name": collection},
    }
    collections_result.append(c_dict)

with open("collections.json", "w", encoding="UTF-8") as file:
    file.write(json.dumps(collections_result, ensure_ascii=False))

# pprint(movie_results)
# print('===============')
# print('===============')
# pprint(spoken_languages_results)
# print('===============')
# print('===============')
# pprint(production_coutries_results)
# print('===============')
# print('===============')
# # pprint(collection_dict)
# pprint(collections_result)
