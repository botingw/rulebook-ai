# Context for Task 2.2: Create Dedicated View Container (Sidebar)

This task involves configuring the extension's `package.json` file to create a dedicated view container in the VS Code sidebar (Activity Bar) and a view within that container. This serves as the host for the extension's graphical user interface.

The configuration is done within the `contributes` section of the `package.json`.

## Defining a View Container

A view container is defined in the `contributes.viewsContainers` section. This creates a new icon in the VS Code Activity Bar.
```
json
"contributes": {
    "viewsContainers": {
        "activitybar": [
            {
                "id": "aiRuleManager",
                "title": "AI Rule Manager",
                "icon": "media/rule-manager-icon.svg" // Specify the path to your icon
            }
        ]
    }
}
```
*   **`activitybar`**: Specifies that the view container should be placed in the Activity Bar.
*   **`id`**: A unique identifier for the view container (e.g., `aiRuleManager`). This ID will be referenced when defining views that belong to this container.
*   **`title`**: The human-readable title that will appear as a tooltip when hovering over the Activity Bar icon.
*   **`icon`**: (Optional but recommended) The path to an SVG icon that will be displayed in the Activity Bar. The path is relative to the extension's root directory. You'll need to create this icon file.

## Defining a View within the Container

Once a view container is defined, you can define views that will appear within it. This is done in the `contributes.views` section.
```
json
"contributes": {
    // ... viewsContainers section ...
    "views": {
        "aiRuleManager": [ // This key must match the view container's ID
            {
                "id": "aiRuleManagerView",
                "name": "AI Rule Manager"
            }
        ]
    }
}
```
*   The key under `views` (`"aiRuleManager"`) must match the `id` of the view container you want this view to belong to.
*   **`id`**: A unique identifier for the view itself (e.g., `aiRuleManagerView`). This ID will be used to programmatically interact with the view (e.g., to populate it with content).
*   **`name`**: The human-readable name that will appear as the title of the view within the sidebar panel.

## Result

After adding these configurations to your `package.json` and running the extension in the Extension Development Host, you should see a new icon in the Activity Bar. Clicking this icon will open a sidebar panel with a view titled "AI Rule Manager". At this stage, the view will be empty. The content of the view (the actual GUI elements) will be implemented in subsequent tasks, likely using a Webview.