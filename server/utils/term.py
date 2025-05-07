def term_to_num(term: str) -> float:
    #Like 25F is 2025.2
    year = int("20" + term[:2])
    season = term[2]
    season_map = {"W": 0.0, "S": 0.1, "F": 0.2}
    return year + season_map.get(season, 0.0)