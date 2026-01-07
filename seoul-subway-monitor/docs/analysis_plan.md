# Data Analysis Plan for Seoul Subway Monitoring

This document outlines the analytical approaches for monitoring the Seoul Subway system using real-time position data.

## 1. 배차 간격 정기성 분석 (Interval Regularity Analysis)
**Goal**: Detect bunching (trains too close) or gaps (trains too far apart) in service.

**Method**:
1. Group data by `line_id`, `station_id`, and `direction_type`.
2. Sort chronological arrivals (using `created_at` or `last_rec_time`).
3. Calculate time difference ($\Delta t$) between consecutive train arrivals at the same station.
4. **Anomaly Detection**: Use Z-score to identify intervals that deviate significantly from the mean for that time of day.

**Expected Output**:
- Time-series chart of arrival intervals.
- Alerts for "Bunching" events (Interval < 2 min where expected is 5 min).

## 2. 지연 발생구간 탐지 (Delay Hotspots)
**Goal**: Identify stations where trains dwell longer than expected.

**Method**:
1. Filter for events where `train_status` changes from `1` (Arrival) to `2` (Departure).
2. Calculate `dwell_time` = time(Departure) - time(Arrival).
3. Aggregate average dwell time by station and hour.

**Expected Output**:
- Heatmap of stations colored by average dwell time.
- Top 10 "Bottleneck" stations list.

## 3. 회차 효율성 분석 (Turnaround Efficiency)
**Goal**: Measure operation efficiency at terminal stations.

**Method**:
1. Identify trains arriving at their `dest_station_id`.
2. Match with the next departing train from that station in the opposite direction.
   - *Note*: Requires heuristic matching if Train No changes.
3. Calculate turnaround time.

**Expected Output**:
- Distribution of turnaround times by terminal station.

## 4. 급행/일반 열차 간섭 분석 (Congestion/Overtake Analysis)
**Goal**: Optimize the mix of Express (`is_express=1`) and Local (`is_express=0`) trains.

**Method**:
1. Track distance/time between an Express train and the Local train ahead of it.
2. Identify segments where the Local train speed drops significantly when an Express train is behind (indicating signal delays).

**Expected Output**:
- map visualization of "Interference Zones".
