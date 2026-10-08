# Граф Wordraft — справочная схема

```mermaid
flowchart LR
  Q["Q task route"] --> P["P procedures"]
  P --> A["A active canonical assertions"]
  A --> S["S support edges"] --> I["I assertion instances"] --> F["F source fragments"] --> V["V revision"] --> D["D document"]
  P --> K["K advisory practices"] --> R["R external resources"]
  P --> J["J decisions / governance"]
  R -. research gap .-> P17["P17 research escalation"]
  P17 --> P00["P00 safe source intake"] --> R
  R -. promote .-> P18["P18 knowledge promotion"] --> D
  C["C eval cases"] -. test .-> Q
  P --> P16["P16 preservation audit"]
  A -->|has_exception / refines / conflicts_with / supersedes| A
```

## Главное

- A/S/I/F/V/D — доказуемая policy.
- P/Q — executive function редактора.
- K/R — внешняя expertise без автоматического превращения в policy.
- J — explicit precedence/safety/preservation.
- C — regression harness.
