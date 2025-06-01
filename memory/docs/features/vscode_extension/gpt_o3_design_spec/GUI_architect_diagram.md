```mermaid
graph TD
    User["User (VS Code Window)"]

    subgraph VSCodeExtension ["VS Code Extension (Node.js)"]
        direction LR
        SidebarProvider["sidebarProvider.ts (Static TreeView)"]
        ExtensionTS["extension.ts (Activation & Command Logic)"]
        UtilsTS["utils.ts (Helpers: getRuleSets, openTerminal, confirmModal)"]
    end

    subgraph VSCodeHost ["VS Code Host Services"]
        direction LR
        VSCodeAPI_UI["VS Code UI APIs (QuickPick, Modals, Messages)"]
        VSCodeAPI_Terminal["VS Code Terminal API (createTerminal, sendText)"]
        IntegratedTerminal["Integrated Terminal"]
    end

    subgraph PythonBackend ["Python Backend"]
        direction LR
        ManageRulesPy_Sync["manage_rules.py (list-rules via spawnSync)"]
        ManageRulesPy_Terminal["manage_rules.py (Interactive in Terminal)"]
        FileSystem["Filesystem (Workspace Root)"]
    end

    User -- "(1.) Clicks TreeItem" --> SidebarProvider
    SidebarProvider -- "(2.) Triggers VS Code Command" --> ExtensionTS

    ExtensionTS -- "3a. Uses for rule listing (via Utils)" --> UtilsTS
    ExtensionTS -- "3b. Uses for UI (modals, pickers)" --> VSCodeAPI_UI
    ExtensionTS -- "3c. Uses to run script in terminal (via Utils)" --> UtilsTS

    UtilsTS -- "4a. getRuleSets() calls" --> ManageRulesPy_Sync
    UtilsTS -- "4b. confirmModal() uses" --> VSCodeAPI_UI
    UtilsTS -- "4c. openTerminalAndRun() uses" --> VSCodeAPI_Terminal

    VSCodeAPI_Terminal -- "(5.) Creates & Shows" --> IntegratedTerminal
    IntegratedTerminal -- "(6.) Runs & Forwards I/O for" --> ManageRulesPy_Terminal
    
    ManageRulesPy_Terminal -- "7a. Outputs to / Prompts in" --> IntegratedTerminal
    IntegratedTerminal -- "7b. Displays output to / Gets input from User" --> User
    ManageRulesPy_Terminal -- "7c. Reads/Writes" --> FileSystem

    %% Styling (optional, but can improve readability)
    classDef ext fill:#007ACC,stroke:#000,stroke-width:1px,color:#fff;
    classDef vscode_host fill:#5C2D91,stroke:#000,stroke-width:1px,color:#fff;
    classDef backend fill:#FFD43B,stroke:#000,stroke-width:1px,color:#000;
    classDef user_io fill:#E0E0E0,stroke:#000,stroke-width:1px,color:#000;

    class SidebarProvider,ExtensionTS,UtilsTS ext;
    class VSCodeAPI_UI,VSCodeAPI_Terminal,IntegratedTerminal vscode_host;
    class ManageRulesPy_Sync,ManageRulesPy_Terminal,FileSystem backend;
    class User user_io;