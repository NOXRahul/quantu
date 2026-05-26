# QuantU — Architecture Overview

## Design Philosophy

QuantU follows a **layered modular architecture** inspired by scientific computing frameworks:

```
┌─────────────────────────────────────────────┐
│              Dashboard (Streamlit)           │
│      Interactive UI + Real-time Viz          │
├─────────────────────────────────────────────┤
│           Visualization Layer               │
│      Plotly · Matplotlib · Color Maps       │
├──────────┬──────────┬───────────────────────┤
│   Core   │  Fields  │  Relativity  Propulsion│
│ Physics  │  Engine  │  Modules     Modules   │
├──────────┴──────────┴───────────────────────┤
│           Math Engine                       │
│    Solvers · Tensors · Symbolic · Curvature │
├─────────────────────────────────────────────┤
│           Constants & Utilities             │
│         Physical Constants (SI)             │
└─────────────────────────────────────────────┘
```

## Module Dependency Graph

```
constants.py ← math_engine/ ← core/ ← fields/
                    ↑              ↑
                    └── relativity/  propulsion/
                           ↑            ↑
                           └── viz/ ────┘
                                ↑
                            dashboard/
```

## Integration Patterns

- **Bottom-up**: Constants → Solvers → Physics → Fields → Visualization → Dashboard
- **No circular deps**: Each layer only imports from layers below
- **Pure computation**: Physics modules return NumPy arrays; visualization is separate
- **Streamlit caching**: Heavy computations use `@st.cache_data` for responsiveness
