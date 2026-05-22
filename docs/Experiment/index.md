# Experimental Design
As a part of this project, we designed an experiment using JSPsych on Cognition.run, and this is where we dicuss how to run our experiment.

## Select The Participants

The participants are linked in a circular chain — each person's selection stimulus becomes the next person's yoked stimulus, with Person n feeding back to Person 1.

```mermaid
flowchart LR
    subgraph p1["Person 1"]
        direction LR
        Y1["Yoked"] ~~~ S1["Selection"]
    end
    subgraph p2["Person 2"]
        direction LR
        Y2["Yoked"] ~~~ S2["Selection"]
    end
    subgraph p3["Person 3"]
        direction LR
        Y3["Yoked"] ~~~ S3["Selection"]
    end
    subgraph mid["Other Participants"]
        dots["···"]
    end
    subgraph pn["Person n"]
        direction LR
        Yn["Yoked"] ~~~ Sn["Selection"]
    end

    S1 --> Y2
    S2 --> Y3
    S3 --> dots
    dots --> Yn
    Sn --> Y1
```

When unrolled in time, the cycle begins with Person 1 completing only the Selection task, each subsequent participant completing Yoked then Selection, and the cycle closes when Person 1 returns to complete the Yoked task using Person n's selection.

```mermaid
flowchart LR
    subgraph p1a["Person 1"]
        S1["Selection"]
    end
    subgraph p2["Person 2"]
        direction LR
        Y2["Yoked"] ~~~ S2["Selection"]
    end
    subgraph p3["Person 3"]
        direction LR
        Y3["Yoked"] ~~~ S3["Selection"]
    end
    subgraph mid["Other Participants"]
        dots["···"]
    end
    subgraph pn["Person n"]
        direction LR
        Yn["Yoked"] ~~~ Sn["Selection"]
    end
    subgraph p1b["Person 1"]
        Y1b["Yoked"]
    end

    S1 --> Y2
    S2 --> Y3
    S3 --> dots
    dots --> Yn
    Sn --> Y1b
```

## How Categorization Works

The stimulus space runs from a perfect square to a perfect circle. A hidden category boundary divides the space into shapes that are **Not Safe** (sharp corners) and **Safe** (rounded corners) for children. 

What exactly counted as save varied between experiments, but were consistant across the multiple loops in one experiment. Thus, each participant only had to identify two separate boundaries, one for their [selection experiment](./selection_code.md) and one for their [yoked experiment](./yoked_code.md).

``` mermaid
block-beta
    columns 31
    sq["Square"]:2
    ns["Not Safe"]:13
    b[" "]:1
    s["Safe"]:13
    ci["Circle"]:2

    style sq fill:none,stroke:none
    style ci fill:none,stroke:none
    style ns fill:#f5c2c2,stroke:#c45b50
    style b fill:#8b3a2e,stroke:#8b3a2e,color:#fff
    style s fill:#f2dfd0,stroke:#c4a898
```

``` mermaid
block-beta
    columns 31
    sq["Square"]:2
    ns["Not Safe"]:6
    b[" "]:1
    s["Safe"]:20
    ci["Circle"]:2

    style sq fill:none,stroke:none
    style ci fill:none,stroke:none
    style ns fill:#f5c2c2,stroke:#c45b50
    style b fill:#8b3a2e,stroke:#8b3a2e,color:#fff
    style s fill:#f2dfd0,stroke:#c4a898
```

``` mermaid
block-beta
    columns 31
    sq["Square"]:2
    ns["Not Safe"]:20
    b[" "]:1
    s["Safe"]:6
    ci["Circle"]:2

    style sq fill:none,stroke:none
    style ci fill:none,stroke:none
    style ns fill:#f5c2c2,stroke:#c45b50
    style b fill:#8b3a2e,stroke:#8b3a2e,color:#fff
    style s fill:#f2dfd0,stroke:#c4a898
```

## Running The Experiment

The process of running an experiment is a fairly manual one, and is described below. The how these tests are run is described in more detail by the [Selection Code](./selection_code.md) and [Yoked Code](./yoked_code.md) sections, but here we are more concerned with this manual aspect.

As previously noted, each participant is expected to run two both the selection experiment and the yoked experiment, although the order they are taken can be swapped for all but the first participant. Thus, the process of running an experiment has been split into these two parts with the assumption that you will do both for each participant.

### Selection Experiment

```mermaid
flowchart TD
    A(["Get A Participant"])
    B["Have them take the Selection Experiment"]
    C["Download the resulting CSV from Cognition.run"]
    D["Save as raw_sel_data.csv (or edit the Jupyter notebook)"]
    E["Run interpret_selection.ipynb to extract results"]
    F[("Save results to results/saved_selection_data.csv")]
    G["Print Config Code to run a yoked experiment"]

    A --> B --> C --> D --> E
    E --> F
    E --> G
```

### Yoked Experiment

```mermaid
flowchart TD
    A(["Get A Participant"])
    A2["Get Previous Participant's Selection Data"]
    B["Have them take the Yoked Experiment"]
    C["Download the resulting CSV from Cognition.run"]
    D["Save as raw_yol_data.csv (or edit the Jupyter notebook)"]
    E["Run interpret_yolked.ipynb to extract results"]
    F[("Save results to results/saved_yolked_data.csv")]

    A --> B
    A2 --> B
    B --> C --> D --> E --> F
```

## The Infrastructure
The Javascript code used to run the experiment is setup and explained here.

[Selection Experiment](./selection_code.md){.md-button .md-button--primary}
[Yoked Experiment](./yoked_code.md){.md-button .md-button--primary}
