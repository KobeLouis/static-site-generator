class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag if tag is not None else ""
        self.value = value if value is not None else ""
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    
    def to_html(self):
        raise NotImplementedError("Subclasses must implement the to_html method")
    
    def props_to_html(self):
        if not self.props:
            return ""
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return f"HTMLNode(tag='{self.tag}', value='{self.value}', children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=[], props=props)
    
    def to_html(self):
        if not self.value:
            raise ValueError("Invalid HTML: no value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag='{self.tag}', value='{self.value}', props={self.props})"