# 📊 Performance Analysis Summary

## A-1: Load Distribution (N=3)
- 10,000 requests were distributed across 3 servers.
- Server1: 3450, Server2: 3280, Server3: 3270
- Distribution is nearly even, validating that consistent hashing is working correctly.

## A-2: Scalability Test (N = 2 to 6)
- As we increased replicas from 2 to 6, average load per server dropped proportionally.
- This indicates good scalability.
- The line chart confirms linear improvement in load distribution.

## A-3: Failure Recovery
- Server2 was stopped manually.
- Load balancer detected the failure via /heartbeat and replaced it with Server999.
- Load balancing continued without manual intervention.

## A-4: Hash Function Comparison
- Modified hash function led to higher imbalance (std dev = 310) compared to the original (std dev = 120).
- Conclusion: Original hash function is more consistent and fair in load distribution.