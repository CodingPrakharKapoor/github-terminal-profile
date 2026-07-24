<!--
    THIS FILE IS AUTO-GENERATED.
    DO NOT EDIT README.md DIRECTLY.
-->

```text
{{ ascii }}
```

# {{ name }}

> {{ title }}

{{ subtitle }}

---

## 👤 About

{% if sections.show_age %}
- **Age:** {{ age }}
{% endif %}

- **Location:** {{ location }}

{% if website %}
- **Website:** {{ website }}
{% endif %}

{% if email %}
- **Email:** {{ email }}
{% endif %}

---

## 📊 GitHub Statistics

```text
Repositories.............. {{ github.repositories }}
Contributed Repositories.. {{ github.contributed_repositories }}
Followers................. {{ github.followers }}
Following................. {{ github.following }}
Stars..................... {{ github.stars }}
Contributions............. {{ github.contributions }}

Commits................... {{ statistics.commits }}
Lines Added............... {{ "{:,}".format(statistics.additions) }}
Lines Deleted............. {{ "{:,}".format(statistics.deletions) }}
Net Lines................. {{ "{:,}".format(statistics.additions - statistics.deletions) }}
```

---

## 💻 Languages

{% for language in languages.split(", ") %}
- {{ language }}
{% endfor %}

---

## 🚀 Frameworks

{% for framework in frameworks.split(", ") %}
- {{ framework }}
{% endfor %}

---

## 🗄 Databases

{% for database in databases.split(", ") %}
- {{ database }}
{% endfor %}

---

## 🛠 Tools

{% for tool in tools.split(", ") %}
- {{ tool }}
{% endfor %}

---

## 📂 Current Projects

{% for project in projects %}
- {{ project }}
{% endfor %}

---

## 🏆 Achievements

{% for achievement in achievements %}
- {{ achievement }}
{% endfor %}

---

## 🌐 Social Links

{% for key, value in socials.items() %}
{% if value %}
- **{{ key|capitalize }}:** {{ value }}
{% endif %}
{% endfor %}

---

_Last updated automatically by GitHub Actions._