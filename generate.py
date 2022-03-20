import argparse
from typing import List
from me_reader import MeFile, read_me_file
from recipe import ResumeRecipe

def generate_pdf(me: MeFile, path: str, recipe: ResumeRecipe, tex_path: None | str = None):
    doc = me.create_document(recipe)
    doc.generate_pdf(path, compiler="pdflatex", compiler_args=["-include-directory=.."])
    if tex_path is not None:
        doc.generate_tex(tex_path)

if __name__ == "__main__":
    # Create and configure argparser
    parser = argparse.ArgumentParser(description="A utility that creates my resume.")
    parser.add_argument("-i", "--include-tags", help="include tags in resume", dest="include_tags")
    parser.add_argument("-eI", "--exclude-items", action="store", type=str, default="", help="exclude tags from resume", dest="exclude_items")
    parser.add_argument("-eT", "--exclude-tags", action="store", type=str, default="", help="exclude tags from resume", dest="exclude_tags")
    parser.add_argument("-eC", "--exclude-contact", action="store", type=str, default="", help="exclude contact info from resume", dest="exclude_contact")
    parser.add_argument("-r", "--recipe-file", help="create resume from recipe file")
    parser.add_argument("-t", "--output-tex", action="store", dest="tex_path", default=None, help="outputs a .tex file")
    parser.add_argument("-o", "--output-file", default="./pdf/resume", action="store", dest="pdf_path", help="outputs a .tex file")

    # Parse arguments
    args = parser.parse_args()

    # Parse path information
    pdf_path = args.pdf_path
    # Remove unnecessary .pdf extension
    if pdf_path.endswith(".pdf"):
        pdf_path = pdf_path[:-4]

    # Create recipe
    recipe = ResumeRecipe()
    recipe.exclude_items = args.exclude_items.lower().split(",")
    recipe.exclude_tags = args.exclude_tags.lower().split(",")
    recipe.exclude_contact = args.exclude_contact.lower().split(",")
    tex_path = args.tex_path
    if tex_path is not None and tex_path.endswith(".tex"):
        tex_path = tex_path[:-4]

    generate_pdf(read_me_file(), pdf_path, recipe, tex_path)
