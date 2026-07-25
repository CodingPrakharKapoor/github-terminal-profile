from pathlib import Path

USERNAME = "prakhar@kapoor"

OS = "Windows 11, Android 14, Linux"
AGE = "22 years, 5 months, 29 days"
HOST = "GLA University"
KERNEL = "Software Engineer"
IDE = "VS Code"

PROGRAMMING_LANGUAGES = "Java, Python, C++, JavaScript"
COMPUTER_LANGUAGES = "HTML, CSS, JSON, YAML"
REAL_LANGUAGES = "English, Hindi"

SOFTWARE_HOBBIES = "Competitive Programming"
HARDWARE_HOBBIES = "PC Building"

EMAIL_PERSONAL = "abc@gmail.com"
EMAIL_WORK = "abc@company.com"
WEBSITE = "prakhar.dev"
LINKEDIN = "PrakharKapoor"
DISCORD = "codingprakhar"

REPOS = 36
CONTRIBUTED_REPOS = 0
STARS = 2
COMMITS = 91
FOLLOWERS = 7

LOC = 135240
LOC_ADD = 168421
LOC_DEL = 33181

TOTAL_WIDTH = 56


def make_dots(label: str, value) -> str:
    value = str(value)
    return "." * max(1, TOTAL_WIDTH - len(label) - len(value))


# --------------------------------------------------
# GitHub stats
# --------------------------------------------------

STAR_DOTS = make_dots("Stars:", STARS)

star_section = f"Stars:{STAR_DOTS}{STARS}"

repo_dots = "." * max(
    1,
    TOTAL_WIDTH
    - len("Repos:")
    - len(str(REPOS))
    - len(f" {{Contributed: {CONTRIBUTED_REPOS}}} | ")
    - len(star_section)
)

REPO_DOTS = repo_dots


FOLLOWER_DOTS = make_dots("Followers:", FOLLOWERS)

follower_section = f"Followers:{FOLLOWER_DOTS}{FOLLOWERS}"

commit_dots = "." * max(
    1,
    TOTAL_WIDTH
    - len("Commits:")
    - len(str(COMMITS))
    - len(" | ")
    - len(follower_section)
)

COMMIT_DOTS = commit_dots


LOC_DOTS = make_dots(
    "Lines of Code on GitHub:",
    LOC,
)

LOC_DEL_DOTS = " " * max(
    1,
    len(str(LOC_ADD)) - len(str(LOC_DEL))
)

replacements = {

    "USERNAME": USERNAME,

    "OS": OS,
    "OS_DOTS": make_dots("OS:", OS),

    "AGE": AGE,
    "AGE_DOTS": make_dots("Uptime:", AGE),

    "HOST": HOST,
    "HOST_DOTS": make_dots("Host:", HOST),

    "KERNEL": KERNEL,
    "KERNAL_DOTS": make_dots("Kernel:", KERNEL),

    "IDE": IDE,
    "IDE_DOTS": make_dots("IDE:", IDE),

    "PROGRAMMING_LANGUAGES": PROGRAMMING_LANGUAGES,
    "PROLANG_DOTS": make_dots(
        "Languages.Programming:",
        PROGRAMMING_LANGUAGES,
    ),

    "COMPUTER_LANGUAGES": COMPUTER_LANGUAGES,
    "COMPLANG_DOTS": make_dots(
        "Languages.Computer:",
        COMPUTER_LANGUAGES,
    ),

    "REAL_LANGUAGES": REAL_LANGUAGES,
    "REALLANG_DOTS": make_dots(
        "Languages.Real:",
        REAL_LANGUAGES,
    ),

    "SOFTWARE_HOBBIES": SOFTWARE_HOBBIES,
    "SOFT_HOBBIES_DOTS": make_dots(
        "Hobbies.Software:",
        SOFTWARE_HOBBIES,
    ),

    "HARDWARE_HOBBIES": HARDWARE_HOBBIES,
    "HARD_HOBBIES_DOTS": make_dots(
        "Hobbies.Hardware:",
        HARDWARE_HOBBIES,
    ),

    "EMAIL_PERSONAL": EMAIL_PERSONAL,
    "PERSONAL_EMAIL_DOTS": make_dots(
        "Email.Personal:",
        EMAIL_PERSONAL,
    ),

    "EMAIL_WORK": EMAIL_WORK,
    "WORK_EMAIL_DOTS": make_dots(
        "Email.Work:",
        EMAIL_WORK,
    ),

    "WEBSITE": WEBSITE,
    "WEBSITE_DOTS": make_dots(
        "Website:",
        WEBSITE,
    ),

    "LINKEDIN": LINKEDIN,
    "LINKEDIN_DOTS": make_dots(
        "LinkedIn:",
        LINKEDIN,
    ),

    "DISCORD": DISCORD,
    "DISCORD_DOTS": make_dots(
        "Discord:",
        DISCORD,
    ),

    "REPOS": REPOS,
    "REPO_DOTS": REPO_DOTS,

    "CONTRIBUTED_REPOS": CONTRIBUTED_REPOS,

    "STARS": STARS,
    "STAR_DOTS": STAR_DOTS,

    "COMMITS": COMMITS,
    "COMMIT_DOTS": COMMIT_DOTS,

    "FOLLOWERS": FOLLOWERS,
    "FOLLOWER_DOTS": FOLLOWER_DOTS,

    "LOC": LOC,
    "LOC_DOTS": LOC_DOTS,

    "LOC_ADD": LOC_ADD,

    "LOC_DEL": LOC_DEL,
    "LOC_DEL_DOTS": LOC_DEL_DOTS,
}


class SVGRenderer:

    def __init__(
        self,
        template="terminal.svg",
        output_svg="README.svg",
        output_readme="README.md",
    ):
        self.template = Path(template)
        self.output_svg = Path(output_svg)
        self.output_readme = Path(output_readme)

    def render(self):

        svg = self.template.read_text(encoding="utf-8")

        for key, value in replacements.items():
            svg = svg.replace(
                f"{{{{{key}}}}}",
                str(value),
            )

        self.output_svg.write_text(
            svg,
            encoding="utf-8",
        )

        readme = f"""<p align="center">
  <img src="{self.output_svg.name}" alt="GitHub Terminal Profile">
</p>
"""

        self.output_readme.write_text(
            readme,
            encoding="utf-8",
        )


if __name__ == "__main__":
    SVGRenderer().render()