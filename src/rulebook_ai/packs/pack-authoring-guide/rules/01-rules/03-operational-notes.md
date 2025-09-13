## Operational Notes

- **File Paths**: When using filesystem tools like `read_file` or `write_file`, always resolve file paths to their absolute form. Use the current working directory as the base for resolution if needed. Tool documentation specifies this, and failing to provide absolute paths will cause errors.
