import panel as pn

from panel_mermaid import MermaidDiagram

pn.extension()

MermaidDiagram(
    object=(
        """
        graph LR
            A[Hello] --- B[World]
        """
    )
).servable()
