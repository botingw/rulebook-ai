this file document contradiction of docs about mode-specific rules and the real result from UI operation.
STATUS: this contradition not resolved in code yet.

.roomodes

customModes:
  - slug: hello-guy
    name: Hello-guy
    description: you always say hello to users
    roleDefinition: you always say hello to users
    customInstructions: no matter what user says, always say hello to him
    groups:
      - read
      - edit
    source: project

.kilocodemodes

customModes:
  - slug: say-hello
    name: say-hello
    description: you always say hello
    roleDefinition: you always say hello
    customInstructions: you always say hello no matter what user say
    groups:
      - read
      - edit
      - browser
      - command
      - mcp
    source: project
  - slug: say-hello-2
    name: say-hello-2
    description: you always say hello
    roleDefinition: you always say hello
    customInstructions: you always say hello no matter what user say
    groups:
      - read
      - edit
      - browser
      - command
      - mcp
    source: project