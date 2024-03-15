from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path

env = Environment(
    loader=FileSystemLoader(["templates", "inputs"]),
    autoescape=select_autoescape(['html', 'xml'])
)

INPUT_DIR = Path("inputs")
OUTPUT_DIR = Path("docs")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


for input_file in INPUT_DIR.rglob("*.html"):
    relative_path = input_file.relative_to(INPUT_DIR)
    output_file = OUTPUT_DIR / relative_path

    output_file.parent.mkdir(parents=True, exist_ok=True)

    template = env.get_template(str(relative_path))
    rendered_content = template.render()

    output_file.write_text(rendered_content, encoding='utf-8')

    print(f"Generated {output_file}")

