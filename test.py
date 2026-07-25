from svg_renderer import renderer

renderer.add_ascii([
"      /\\_/\\\\",
"     ( o.o )",
"      > ^ <",
])

renderer.title("Prakhar Kapoor")
renderer.subtitle("CodingPrakharKapoor")

renderer.blank_right()

renderer.section(
    "System",
    [
        ("OS", "Windows 11"),
        ("Editor", "VS Code"),
        ("Shell", "PowerShell"),
        ("Terminal", "Windows Terminal"),
    ],
)

renderer.section(
    "GitHub",
    [
        ("Repositories", 36),
        ("Followers", 7),
        ("Stars", 2),
        ("Commits", 91),
    ],
)

renderer.section_heading("Statistics")

renderer.statistic("Additions", "+24,581")
renderer.statistic("Deletions", "-8,143")
renderer.statistic("Net LOC", "+16,438")

renderer.save()