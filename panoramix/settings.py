makedocs_settings = {
    "subs": [(r"\\paragraph\*?\{(?P<titre>.*?)\}", r"\\textbf{\g<titre>~:}")]
}

homeconf_settings = {
    "files": [
        ".zshrc",
        ".vimrc",
        ".config/argos/cpu.py"
    ]
}
