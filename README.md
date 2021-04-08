# 가장 가까운 지하철 역 조회 API
매물에서 3킬로 반경 내 지하철역 조회

Request:
```json
{
  "pnu":String
}
```

Response:
```json
{
	"results" : [
	{
		"pnu": String,
		"nearbyStation": // distance ASC 로 정렬
		[
			{
				"name" : String, // 역 이름
				"line" : String, // 호선 
				"distance" : Double, // 거리
				"consumingTime" : Int // 도보 소요시간
			},
			// ...
		]
	},
	// ...
}
```
