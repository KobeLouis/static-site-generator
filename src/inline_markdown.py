import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown: unmatched delimiter '{delimiter}' in text '{node.text}'")
        
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[i], text_type))

    return new_nodes

def extract_markdown_images(text):
    pattern = r'!\[([^\[\]]*)\]\(([^\(\)]*)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)'
    matches = re.findall(pattern, text)
    return matches

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        images = extract_markdown_images(text)
        if not images:
            new_nodes.append(node)
            continue
        
        for alt_text, url in images:
            split = text.split(f'![{alt_text}]({url})')

            if len(split) != 2:
                raise ValueError(f"Invalid markdown: image section unclosed")
            
            if split[0] != "":
                new_nodes.append(TextNode(split[0], TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            text = split[1]

        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        links = extract_markdown_links(text)
        if not links:
            new_nodes.append(node)
            continue
        
        
        for link_text, url in links:
            split = text.split(f'[{link_text}]({url})')
            
            if len(split) != 2:
                raise ValueError(f"Invalid markdown: link section unclosed")
            
            if split[0] != "":
                new_nodes.append(TextNode(split[0], TextType.TEXT))
            
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            text = split[1]
            
        
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = []
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes