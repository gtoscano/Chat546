from celery import shared_task
import markdown2
import bleach
from bs4 import BeautifulSoup
import time

import markdown
from markdown.extensions import Extension
from markdown.extensions import fenced_code
from markdown.extensions import tables
from markdown.extensions import codehilite
from markdown.extensions import attr_list
from markdown.extensions import smarty
from markdown.extensions import meta
from markdown.extensions import admonition
#from markdown.extensions.math import MathExtension
from bs4 import BeautifulSoup
import bleach
import re

def preprocess_markdown(markdown_code):
    # Replace \[...\] with $$...$$
    markdown_code = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', markdown_code, flags=re.DOTALL)
    # Replace \(...\) with $...$
    markdown_code = re.sub(r'\\\((.*?)\\\)', r'$\1$', markdown_code, flags=re.DOTALL)
    return markdown_code


def convert_markdown_to_html(markdown_code):
    return convert_markdown_to_html5(markdown_code)

def convert_markdown_to_html2(markdown_code):
   # Process the response
   html_translate = markdown2.markdown(
           markdown_code,
            extras=["fenced-code-blocks", "code-friendly", "tables"]  # Added "tables" extra
   )
   print(html_translate)


   # Parse the HTML with BeautifulSoup
   soup = BeautifulSoup(html_translate, 'html.parser')
   
   # Remove <span> tags inside <code> elements
   for code_tag in soup.find_all('code'):
       for span in code_tag.find_all('span'):
           # Replace the span tag with its contents
           span.unwrap()
   
   # Define a mapping from tags to Tailwind CSS/DaisyUI classes, including table elements
   tag_class_mapping = {
       'p': 'mb-4',
       'h1': 'text-3xl font-bold mb-4',
       'h2': 'text-2xl font-bold mb-3',
       'h3': 'text-xl font-bold mb-2',
       'h4': 'text-l font-bold mb-1',
       'ol': 'list-decimal list-inside mb-4',
       'ul': 'list-disc list-inside mb-4',
       'li': 'mb-1',
       'hr': 'border-t border-base-300 my-4',
       'pre': 'bg-base-200 p-4 rounded mb-4 overflow-x-auto',
       'code': 'bg-base-300 p-1 rounded text-gray-800',
       'blockquote': 'border-l-4 border-base-300 pl-4 italic mb-4',
       'strong': 'font-bold',
       'em': 'italic',
       'table': 'table-auto border-collapse border border-base-300 mb-4',
       'thead': 'bg-base-200',
       'th': 'border border-base-300 px-4 py-2 text-left font-semibold',
       'td': 'border border-base-300 px-4 py-2',
       'tr': 'hover:bg-base-100',
       'br': 'my-4',
   }
   
   # Add classes to the elements
   for tag in soup.find_all(True):
       if tag.name in tag_class_mapping:
           existing_classes = tag.get('class', [])
           new_classes = tag_class_mapping[tag.name].split()
           tag['class'] = existing_classes + new_classes

   # Convert the modified soup back to a string
   html_without_spans = str(soup)

   allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union([
       'p', 'pre', 'code', 'blockquote', 'h1', 'h2', 'h3', 'h4', 'hr',
       'ul', 'ol', 'li', 'strong', 'em', 'div', 'span',
       'table', 'thead', 'tbody', 'th', 'tr', 'td', 'br'  # Added table-related tags
   ])

   allowed_attributes = {
       '*': ['class'],
       'code': ['class']
   }

   clean_html = bleach.clean(
       html_without_spans,
       tags=allowed_tags,
       attributes=allowed_attributes,
       strip=False 
   )
   print(clean_html)

   return clean_html



def convert_markdown_to_html3(markdown_code):
    return convert_markdown_to_html5(markdown_code)

def convert_markdown_to_html4(markdown_code):
    # Preprocess markdown to replace \[...\] and \(...\)
    markdown_code = preprocess_markdown(markdown_code)

    # Convert markdown to HTML with math support
    html_translate = markdown2.markdown(
        markdown_code,
        extras=[
            "fenced-code-blocks", 
            "code-friendly", 
            "tables", 
            "mathjax"
        ]
    )

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_translate, 'html.parser')
    
    # Remove <p> tags that wrap display math (i.e., $$...$$)
    for p_tag in soup.find_all('p'):
        # Get the text inside the <p> tag
        text = ''.join(p_tag.stripped_strings).strip()
        if text.startswith('$$') and text.endswith('$$'):
            # Unwrap the <p> tag
            p_tag.unwrap()
    
    # Remove <span> tags inside <code> elements
    for code_tag in soup.find_all('code'):
        for span in code_tag.find_all('span'):
            # Replace the span tag with its contents
            span.unwrap()

    for li_tag in soup.find_all('li'):
        p_tags = li_tag.find_all('p', recursive=False)
        for p_tag in p_tags:
            p_tag.unwrap()
    
    # Define a mapping from tags to Tailwind CSS/DaisyUI classes
    tag_class_mapping = {
        'p': 'mb-4',
        'h1': 'text-3xl font-bold mb-4',
        'h2': 'text-2xl font-bold mb-3',
        'h3': 'text-xl font-bold mb-2',
        'h4': 'text-l font-bold mb-1',
        'ol': 'list-decimal list-inside mb-4',
        'ul': 'list-disc list-inside mb-4',
        'li': 'mb-1',
        'pre': 'bg-base-200 p-4 rounded mb-4 overflow-x-auto',
        'code': 'bg-base-300 p-1 rounded text-gray-800',
        'blockquote': 'border-l-4 border-base-300 pl-4 italic mb-4',
        'strong': 'font-bold',
        'em': 'italic',
        'hr': 'border-t border-base-300 my-4',
        'table': 'table-auto border-collapse border border-base-300 mb-4',
        'thead': 'bg-base-200',
        'th': 'border border-base-300 px-4 py-2 text-left font-semibold',
        'td': 'border border-base-300 px-4 py-2',
        'tr': 'hover:bg-base-100',
        'br': 'my-4',
        # MathJax spans
        'span': '',
    }
    
    # Add classes to the elements
    for tag in soup.find_all(True):
        if tag.name in tag_class_mapping:
            existing_classes = tag.get('class', [])
            new_classes = tag_class_mapping[tag.name].split()
            tag['class'] = existing_classes + new_classes

    # Convert the modified soup back to a string
    html_without_spans = str(soup)

    # Include MathJax-related tags and attributes
    allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union([
        'p', 'pre', 'code', 'blockquote', 'h1', 'h2', 'h3','h4', 'hr',
        'ul', 'ol', 'li', 'strong', 'em', 'div', 'span',
        'table', 'thead', 'tbody', 'th', 'tr', 'td','br',
        # MathJax-related tags
        'script', 'noscript', 'style'
    ])

    allowed_attributes = {
        '*': ['class', 'id', 'style'],
        'code': ['class'],
        'span': ['class', 'style'],
        'div': ['class', 'id', 'style'],
        'script': ['type', 'src'],
    }

    clean_html = bleach.clean(
        html_without_spans,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=False 
    )
    print("Cleaned HTML after removing unwanted tags:")
    print(clean_html)

    return clean_html



def convert_markdown_to_html5(markdown_code):
    # Preprocess markdown to replace \[...\] and \(...\)
    markdown_code = preprocess_markdown(markdown_code)

    # Convert markdown to HTML with math support
    html_translate = markdown2.markdown(
        markdown_code,
        extras=[
            "fenced-code-blocks",
            "code-friendly",
            "tables",
            "mathjax",
            "cuddled-lists",  # Add this extra
        ],
    )
    #print("HTML after markdown conversion:")
    #print(html_translate)

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_translate, "html.parser")

    # Unwrap <p> tags that only contain display math (i.e., $$...$$)
    for p_tag in soup.find_all("p"):
        # Get the contents inside the <p> tag
        contents = p_tag.contents
        if len(contents) == 1 and contents[0].name == "span":
            span_tag = contents[0]
            if span_tag.get("class") == ["math"]:
                # Check if it's display math (i.e., $$...$$)
                math_content = ''.join(span_tag.strings)
                if math_content.startswith("$$") and math_content.endswith("$$"):
                    # Unwrap the <p> and span tags
                    span_tag.unwrap()
                    p_tag.unwrap()

    # Remove <span> tags inside <code> elements
    for code_tag in soup.find_all("code"):
        for span in code_tag.find_all("span"):
            # Replace the span tag with its contents
            span.unwrap()

    # Unwrap <p> tags inside <li> elements
    for li_tag in soup.find_all("li"):
        p_tags = li_tag.find_all("p", recursive=False)
        for p_tag in p_tags:
            p_tag.unwrap()

    # Define a mapping from tags to Tailwind CSS/DaisyUI classes
    tag_class_mapping = {
        "p": "mb-4",
        "h1": "text-3xl font-bold mb-4",
        "h2": "text-2xl font-bold mb-3",
        "h3": "text-xl font-bold mb-2",
        "h4": "text-l font-bold mb-1",
        "ol": "list-decimal list-inside mb-4",
        "ul": "list-disc list-inside mb-4",
        "li": "mb-1",
        "pre": "bg-base-200 p-4 rounded mb-4 overflow-x-auto",
        "code": "bg-base-300 p-1 rounded text-gray-800",
        "blockquote": "border-l-4 border-base-300 pl-4 italic mb-4",
        "strong": "font-bold",
        "em": "italic",
        "hr": "border-t border-base-300 my-4",
        "table": "table-auto border-collapse border border-base-300 mb-4",
        "thead": "bg-base-200",
        "th": "border border-base-300 px-4 py-2 text-left font-semibold",
        "td": "border border-base-300 px-4 py-2",
        "tr": "hover:bg-base-100",
        'br': 'my-4',
        # Exclude adding classes to 'span' to avoid affecting MathJax spans
    }

    # Add classes to the elements
    for tag in soup.find_all(True):
        if tag.name in tag_class_mapping:
            existing_classes = tag.get("class", [])
            new_classes = tag_class_mapping[tag.name].split()
            tag["class"] = existing_classes + new_classes

    # Convert the modified soup back to a string
    html_without_spans = str(soup)

    # Include MathJax-related tags and attributes
    allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union(
        [
            "p",
            "pre",
            "code",
            "blockquote",
            "h1",
            "h2",
            "h3",
            "h4",
            "hr",
            "ul",
            "ol",
            "li",
            "strong",
            "em",
            "div",
            "span",
            "table",
            "thead",
            "tbody",
            "th",
            "tr",
            "td",
            "br",
            # MathJax-related tags
            "script",
            "noscript",
            "style",
        ]
    )

    allowed_attributes = {
        "*": ["class", "id", "style"],
        "code": ["class"],
        "span": ["class", "style"],
        "div": ["class", "id", "style"],
        "script": ["type", "src"],
    }

    clean_html = bleach.clean(
        html_without_spans, tags=allowed_tags, attributes=allowed_attributes, strip=False
    )
    #print("Cleaned HTML after removing unwanted tags:")
    #print(clean_html)

    return clean_html
