# Tamapy: a Python3 Tamagotchi.

A simple tick‑based Tamagotchi you can play in the terminal.

Based on the original one (see picture below) but simpler.


![Tamagotchi instructions](instruction.png)

## Features

- Stats range 0–6
- Hidden “poo” mechanic affects sickness and cleanliness
- Poo is **not shown** to the user and **not saved**
- Medicine now **cures sickness** by resetting poo
- Age increases only while playing (+1 pet year every 5 minutes)
- State saved in JSON
- 6‑square stat bars
- Fully interactive CLI



## How to run
```python tamagotchi.py```

If you want to start a new tamapy, just delete the tamapy_state.json file.


## System Design

### State machine definition

Tamapy is fundamentally a finite‑state machine whose state is defined by four visible stats and one hidden stat:
Visible state variables (0–6):
- happy
- full
- clean
- healthy

Hidden state variable (0–6): poo (not shown to the user, not saved)

Meta‑state variables:
- age_years (integer)
- last_age_update (timestamp)
- tick_count (integer)
- now (timestamp)
- start (timestamp)

The Tamapy is dead when:
```happy == 0 AND full == 0 AND clean == 0 AND health == 0```

This is the only absorbing state in the machine.



### State transitions

Every user action and every tick moves the Tamapy from one state to another.
User‑driven transitions, each action modifies exactly one stat:

| Action|Effect|
|---|---|
|feed|full +1|
|play|happy +1|
|clean|clean +1, poo -1|
|medicine|health +1, poo reset to 0|

All increments are capped at 6.



### Tick‑driven transitions

Every loop iteration triggers a tick, which applies:

    Age update  
    Every 5 minutes → age_years +1.

    Poo accumulation  
    Every 2 ticks → poo +1 (max 6).

    Sickness logic  
    If poo ≥ 3 → health -1.

    Rotational decay  
    One stat decreases each tick in this order: happy → full → clean → health → repeat
    Health only decays in rotation if health ≤ 2.

    Dirty penalty  
    If poo == 6 → clean -1.

This creates a slow, predictable decay cycle with a hidden sickness mechanic.



### Hidden poo mechanic
Although poo is not shown to the user and not saved, it remains a core internal driver of difficulty:

    It accumulates automatically.

    It triggers sickness.

    It dirties the Tamapy when maxed.

    Cleaning reduces it.

    Medicine resets it.

This creates a feedback loop:
    
    poo ↑ → sickness ↑ → health ↓ → medicine → poo reset → cycle repeats



### Persistence model

Only long‑term state is saved:

    name, happy, full, clean, health, tick_count, age_years, last_age_update, timestamps

Not saved:

    poo (always resets to 0 on load)

This keeps the save file simple and avoids exposing hidden mechanics.



### UI model

The UI is intentionally minimal:

    Shows age as: Age: X 🐾

    Shows four stat bars (6 squares each)

    Does not show poo

    Does not show internal sickness state

    Does not show tick count

This keeps the game readable and cute while hiding complexity.



### Game loop

The main loop follows a simple pattern:
```
load state
while alive:
    show status
    get user action
    apply action
    tick()
    save state
```
This ensures:
- Every action advances time
- Every action triggers decay
- State is always saved after each turn



### Design philosophy

The design intentionally blends:

#### Simplicity
- Only four visible stats.
- One hidden stat.
- One terminal condition.
- One tick per action.

#### Depth
- Hidden sickness mechanic.
- Rotational decay.
- Age progression.
- Medicine curing sickness.
- Cleaning reducing hidden poo.

#### Predictability
- Decay is deterministic.
- Sickness is deterministic.
- Age progression is deterministic.

#### Player Feedback
- The player sees the consequences (health dropping, clean dropping) without seeing the hidden cause (poo).
- This creates a subtle “mystery” effect similar to early Tamagotchis.



### Component architecture diagram

```mermaid
flowchart TD
    subgraph UI["USER INTERFACE LAYER"]
        UI1[CLI Menu]
        UI2[Status Renderer]
        UI3[Stat Bars]
        UI4[Age Display]
    end

    subgraph GC["GAME CONTROLLER (main loop)"]
        GC1[Load State]
        GC2[Show Status]
        GC3[Read Input]
        GC4[Dispatch Actions]
        GC5[Tick]
        GC6[Save State]
    end

    subgraph TM["TAMAGOTCHI MODEL"]
        direction TB
        subgraph SV["State Variables"]
            SV1["happy, full, clean, health 0–6"]
            SV2["poo (hidden)"]
            SV3[age_years]
            SV4[tick_count]
            SV5[timestamps]
        end
        subgraph AC["Actions"]
            AC1["feed()"]
            AC2["play()"]
            AC3["clean_poo()"]
            AC4["take_medicine()"]
        end
        subgraph TE["Tick Engine"]
            TE1["update_age()"]
            TE2[poo accumulation]
            TE3[sickness logic]
            TE4[rotational decay]
            TE5[cleanliness penalty]
        end
        subgraph DC["Death Check"]
            DC1["is_dead()"]
        end
    end

    subgraph PL["PERSISTENCE LAYER"]
        subgraph SER["Serialization"]
            SER1["to_dict()"]
            SER2["from_dict()"]
        end
        subgraph ST["Storage"]
            ST1["JSON File: tamapy_state.json"]
        end
        subgraph RL["Rules"]
            RL1[poo NOT saved]
            RL2[poo resets on load]
        end
    end

    UI --> GC
    GC --> TM
    TM --> PL

    %% Top-level layers (UI, GC keep original color; TM, PL take sub-group color)
    classDef bigLayer fill:#C9BDD0,stroke:#534AB7,stroke-width:1px,color:#26215C
    class UI,GC bigLayer

    classDef swappedLayer fill:#FDF1F2,stroke:#D4537E,stroke-width:1px,color:#72243E
    class TM,PL swappedLayer

    %% Sub-groupings (SV, AC, TE, DC, SER, ST, RL take top-level layer color)
    classDef swappedGroup fill:#C9BDD0,stroke:#534AB7,stroke-width:1px,color:#26215C
    class SV,AC,TE,DC,SER,ST,RL swappedGroup

    %% Smallest boxes: individual items
    classDef smallItem fill:#FFB2D0,stroke:#993556,stroke-width:1px,color:#4B1528
    class UI1,UI2,UI3,UI4,GC1,GC2,GC3,GC4,GC5,GC6,SV1,SV2,SV3,SV4,SV5,AC1,AC2,AC3,AC4,TE1,TE2,TE3,TE4,TE5,DC1,SER1,SER2,ST1,RL1,RL2 smallItem
```