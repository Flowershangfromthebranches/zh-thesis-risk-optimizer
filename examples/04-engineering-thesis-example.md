# Example 04: Engineering Thesis Protection

## User Intent

处理工科系统设计段落，保护接口、表名和字段名。

## Before

系统通过用户管理模块实现用户信息的维护，并通过数据管理模块完成数据存储。相关模块共同构成完整闭环，从而提升系统运行效率。

Protected items supplied by user:

- API: `/api/user/profile`
- Table: `health_record`
- Fields: `heart_rate`, `blood_oxygen`, `record_time`

## Diagnosis

| Risk | Reason |
| --- | --- |
| AIGC 风险 | “共同构成完整闭环”为空泛套话 |
| 工程细节不足 | 未说明接口和表字段如何承担功能 |
| 保护项 | API、表名、字段名不可改 |

## After

用户信息维护主要由 `/api/user/profile` 接口承担，接口返回的数据只覆盖账号资料和角色信息，不直接写入健康记录。健康数据单独落在 `health_record` 表中，其中 `heart_rate`、`blood_oxygen` 和 `record_time` 分别用于记录心率、血氧和采集时间。这样划分后，用户资料变更不会影响历史健康记录，后续按时间查询异常数据也更直接。

## Technical Integrity

- API 原样保留。
- 表名和字段名原样保留。
- 未新增不存在的字段。
- 未声称已有性能测试。
