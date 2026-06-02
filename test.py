from report_generator import (
    ReportGenerator
)

report = ReportGenerator()

summary = """
This paper explores the use of
Generative AI in education.
"""

analysis = {

    "objectives":
        "Improve learning",

    "methodology":
        "Survey Method",

    "dataset":
        "Student Dataset",

    "results":
        "Positive outcomes",

    "limitations":
        "Small sample size",

    "future_work":
        "Larger studies"
}

citations = {

    "APA":
        "APA Citation Example",

    "MLA":
        "MLA Citation Example",

    "IEEE":
        "IEEE Citation Example",

    "Chicago":
        "Chicago Citation Example"
}

files = (
    report.export_complete_report(
        summary,
        analysis,
        citations
    )
)

print(files)