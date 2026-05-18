# One-Pass Cross-Discipline Strategy Cases

## Case 1: HR Thesis Near Target

Input:

```yaml
discipline: human_resource_management
current_aigc_rate: 20.31%
target_aigc_rate: 15%
current_similarity_rate: already_passed
report_bands:
  red: 0
  orange: present
  purple: present
  black: many
  gray: headings_english_references
user_requirement: lower_aigc_only_no_word_count_limit
```

Expected:

```yaml
strategy: near_threshold_pushdown
discipline_profile: management_profile
primary_actions:
  - process_orange_by_compression_or_structure_rewrite
  - purple_mandatory_light_rebalance
  - freeze_black
  - freeze_gray
forbidden_actions:
  - broad_full_text_rewrite
  - add_length_for_word_count
  - rewrite_gray
  - generic_management_polishing
```

## Case 2: Computer Science High AIGC

Input:

```yaml
discipline: software_engineering
current_aigc_rate: 72%
target_aigc_rate: 25%
report_bands:
  red: many
  orange: many
  purple: present
protected:
  - code
  - api_paths
  - table_fields
  - parameters
  - test_results
```

Expected:

```yaml
strategy: high_risk_first_pass_reconstruction
discipline_profile: computer_science_profile
red_orange_coverage: 100_percent_or_valid_freeze
preferred_move: rewrite_surrounding_explanations_around_modules_and_tests
forbidden_actions:
  - change_code
  - change_api_paths
  - change_table_fields
  - invent_logs_or_metrics
```

## Case 3: Medical Conservative Handling

Input:

```yaml
discipline: nursing
current_aigc_rate: 58%
target_aigc_rate: 30%
report_bands:
  red: few
  orange: present
  purple: present
protected:
  - clinical_terms
  - dosage
  - sample_data
  - ethics_statement
```

Expected:

```yaml
discipline_profile: medicine_profile
strategy: orange_purple_joint_repair
humanization_level: conservative
preferred_move: de_template_abstract_discussion_without_colloquialism
forbidden_actions:
  - change_clinical_data
  - weaken_medical_register
  - add_subjective_claims
```

