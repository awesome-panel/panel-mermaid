from panel_mermaid import MermaidConfiguration, MermaidDiagram


def test_configuration():
    configuration = MermaidConfiguration()
    MermaidDiagram(configuration=configuration)
