# near-by-station

매물의 위치를 기준으로 반경 3km 내 가장 가까운 지하철역 정보를 조회하는 API 프로젝트입니다.

## 목적

필지 또는 매물의 입지를 판단할 때 단순 좌표 대신 사용자가 이해하기 쉬운 **가까운 지하철역, 거리, 예상 도보 시간**을 제공하기 위해 작성했습니다.

## Request

```json
{
  "pnu": "String"
}
```

## Response

```json
{
  "results": [
    {
      "pnu": "String",
      "nearbyStation": [
        {
          "name": "String",
          "line": "String",
          "distance": 0.0,
          "consumingTime": 0
        }
      ]
    }
  ]
}
```

`nearbyStation`은 거리 오름차순으로 정렬됩니다.

## 응답 필드

| Field | Description |
| --- | --- |
| `pnu` | 필지를 식별하는 PNU |
| `name` | 지하철역 이름 |
| `line` | 노선 |
| `distance` | 매물과 지하철역 사이 거리 |
| `consumingTime` | 예상 도보 소요 시간 |

## 배경

실제 부동산 탐색 서비스 개발 과정에서 매물 주변의 대중교통 접근성을 사용자에게 제공하기 위한 문제를 작은 API 단위로 분리해 구현한 예제입니다.
