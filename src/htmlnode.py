class HTMLNode():
    def __init__(
            self, tag: str = None, value: str = None,
            children: list[object] = None,
            props: dict[str, str] = None) -> None:
        self.tag        = tag
        self.value      = value
        self.children   = children
        self.props      = props
    
    def to_html(self) -> str:
        raise NotImplementedError("HTMLNode, to_html(): method not implemented")
    
    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        
        html_props = ""
        for prop in self.props:
            html_props += f" {prop}=\"{self.props[prop]}\""
        return html_props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
            self, tag: str, value: str,
            props: dict[str, str] = None) -> None:
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode, to_html(): no value found")
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(
            self, tag: str, children: list[object],
            props: dict[str, str] = None) -> None:
        super().__init__(tag, None, children, props)
    
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode, to_html(): no tag found")
        if self.children is None:
            raise ValueError("ParentNode, to_html(): no children nodes found")
        
        child_html = ""
        for node in self.children:
            child_html += node.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
