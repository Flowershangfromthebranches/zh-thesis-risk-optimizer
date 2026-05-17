# Discipline Strategy Router Cases

## Case 1: Management

Input: `人力资源管理`

Expected:

```yaml
selected_profile: management_profile
profile_file: discipline_profiles/management.md
```

## Case 2: Computer Science

Input: `计算机科学`

Expected:

```yaml
selected_profile: computer_science_profile
profile_file: discipline_profiles/computer_science.md
```

## Case 3: Medicine

Input: `护理学`

Expected:

```yaml
selected_profile: medicine_profile
level_4_allowed: false
```

## Case 4: Law

Input: `民商法`

Expected:

```yaml
selected_profile: law_profile
protect: 法条, 判例, 引文, 条款编号
```
