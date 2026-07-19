# VISION_MAP — The whole company, on one page

**For you — the CEO — to look at any time and instantly remember: what this is, where we
stand, and what's blocking growth.** Green = done. Yellow = in progress. Red = blocked on
you, not on code. Grey = not started yet, on purpose.

**How to view this:** if you're reading this on GitHub.com, the picture below renders
automatically. If you're reading it in a plain text editor, paste the code block (everything
between the ` ```mermaid ` lines) into **mermaid.live** to see it as a picture instead of
text.

_Last updated: 2026-07-19_

```mermaid
flowchart TB
    classDef done fill:#8fce9e,stroke:#2f7d43,color:#000,font-weight:bold
    classDef inprogress fill:#ffe38f,stroke:#c99400,color:#000,font-weight:bold
    classDef blocked fill:#ff9f9f,stroke:#b33030,color:#000,font-weight:bold
    classDef todo fill:#e0e0e0,stroke:#888888,color:#000
    classDef vision fill:#a9c9ff,stroke:#2a5db0,color:#000,font-weight:bold

    VISION["VISION<br/>Decision-quality Acquisition OS<br/>for 2-10 person US real-estate investment teams<br/><br/>Mission: make every acquisition decision<br/>as good as the best investor's best day"]:::vision

    subgraph LEGEND["Legend"]
        direction LR
        L1["Done"]:::done
        L2["In progress"]:::inprogress
        L3["Blocked - needs YOU"]:::blocked
        L4["Not started yet, on purpose"]:::todo
    end

    subgraph MARKET["Market and Competitors"]
        M1["Wedge market size:<br/>150 to 400 million dollars per year<br/>about 55,000 active flip investors"]
        M2["PropStream - biggest player<br/>just a data lookup tool, no real decisions"]
        M3["REsimpli - markets 9 AI agents<br/>publishes zero accuracy numbers"]
        M4["BatchLeads / DealMachine<br/>compliance risk pushed onto the customer"]
        M5["OUR EDGE: we publish our accuracy<br/>and our data model is actually correct -<br/>Property, Owner, Lead, Deal are 4 separate things"]
    end

    subgraph BLOCKERS["What Is Actually Blocking Growth Right Now - not code"]
        direction LR
        B1["Team size decision<br/>ADR-006"]:::blocked
        B2["Vendor data contract<br/>not started"]:::blocked
        B3["15 customer interviews<br/>0 done so far"]:::blocked
        B4["5 design partners signed<br/>0 signed so far"]:::blocked
    end

    subgraph PRODUCT["Product Features - the full plan"]
        direction TB
        P1["Login and team accounts"]:::done
        P2["Owner records"]:::done
        P3["Property and owner data feed"]:::blocked
        P4["Import your old spreadsheets"]:::todo
        P5["Pipeline board - visual deal tracker"]:::todo
        P6["AI: Which 20 leads deserve a call today"]:::todo
        P7["AI: What's it worth, what should I pay"]:::todo
        P8["AI: Don't let a lead go cold"]:::todo
        P9["Texting and email inbox"]:::todo
        P10["Deal and offer tracking"]:::todo
        P11["Did we actually make money - outcome tracking"]:::todo
        P12["Bulk marketing campaigns"]:::blocked
        P13["Search everything"]:::todo
        P14["Reports and dashboards"]:::todo
        P15["Billing"]:::todo
    end

    subgraph MONEY["How We Make Money"]
        MO1["Pricing: $299 or $599 or $1,199 per month"]
        MO2["Target: 75 percent plus gross margin"]
        MO3["Fastest path to first dollar:<br/>backtest demo on 1 real person's old deals,<br/>then get them to pay something small"]
    end

    subgraph LEGAL["Biggest Legal Risk"]
        LG1["TCPA law: texting/calling without proper<br/>consent tracking can cost 500 to 1,500 dollars<br/>PER message, no upper limit.<br/>This is why bulk campaigns wait."]:::blocked
    end

    subgraph ROADMAP["The 18-Sprint Roadmap"]
        direction LR
        R1["Sprint 1<br/>Foundation - security and login"]:::done
        R2["Sprint 2<br/>Ontology - Owner, Contact, Lead, Deal"]:::inprogress
        R3["Sprint 3-6<br/>Real data plus imports"]:::blocked
        R4["Sprint 6-10<br/>Underwriting AI engine"]:::todo
        R5["Sprint 7-13<br/>Conversations plus campaigns plus agents"]:::todo
        R6["Sprint 14-18<br/>Hardening plus launch"]:::todo
        R1 --> R2 --> R3 --> R4 --> R5 --> R6
    end

    VISION --> MARKET
    VISION --> MONEY
    MARKET --> PRODUCT
    BLOCKERS -. blocks .-> R3
    BLOCKERS -. blocks .-> P3
    LEGAL -. delays .-> P12
    PRODUCT --> ROADMAP
    MONEY --> ROADMAP
```

## The one-paragraph version, in case the picture doesn't load

You're building software that tells small real-estate investment teams what to buy, what to
pay, and who to call — and proves its numbers are right, which nobody else in this space
does. Foundation (login, security, first piece of the data model) is built and tested. The
entire rest of the product is not built yet, on purpose, because it's sequenced behind three
things only you can do: decide your team size, sign a data contract, and talk to 15 real
investors. Once those move, engineering has a long but clear 18-sprint runway to follow.
