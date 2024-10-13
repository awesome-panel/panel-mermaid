import textwrap
from io import StringIO

import panel as pn
from config import (
    ACCENT,
    BOOTSTRAP_CSS_URL,
    EXAMPLES,
    LOGO,
    get_code_editor_theme,
    get_json_theme,
)
from example_picker import ExamplePicker
from panel_modal import Modal
from splitter import Splitter

from panel_mermaid import MermaidConfiguration, MermaidDiagram

# Panel Configuration
pn.extension(
    "codeeditor", "modal", sizing_mode="stretch_width", css_files=[BOOTSTRAP_CSS_URL]
)

# Component Definitions
initialization = MermaidConfiguration(name="Initialization")
example = ExamplePicker(value="Default", options=EXAMPLES)
code = pn.widgets.CodeEditor(
    value=example.value,
    theme=get_code_editor_theme(),
    sizing_mode="stretch_both",
    on_keyup=False,
)
diagram = MermaidDiagram(
    object=code.value,
    update_value=True,
    configuration=initialization,
    event_configuration=[("click", ".node")],
    margin=10,
)
run = pn.widgets.Button(
    name="▷ Run",
    sizing_mode="fixed",
    width=100,
    button_type="primary",
    description="Click Run to update the diagram",
    margin=(10, 10, 10, 20),
)
value_download = pn.widgets.FileDownload(
    file=pn.bind(StringIO, diagram.param.value),
    filename="diagram.svg",
    button_type="primary",
    button_style="outline",
)
event = pn.pane.JSON(
    object=diagram.param.event, name="Config Dict", theme=get_json_theme()
)
events = pn.Column(
    diagram.param.event_configuration,
    event,
    name="Events",
)

docs_modal = Modal()
docs_section = pn.Column(
    pn.widgets.Button.from_param(
        docs_modal.param.open,
        name="Show Documentation",
        button_type="primary",
        button_style="outline",
        description="Click here to show the MermaidDiagram documentation",
    ),
    docs_modal,
)


# Callback Definitions
@pn.depends(run, code, watch=True)
def _update_diagram(event=None, value=""):
    diagram.object = value


@pn.depends(example, watch=True)
def _update_code(value):
    code.value = value
    _update_diagram(value=value)


@pn.depends(docs_modal.param.open)
def docs_content(event=None):
    return pn.Column(
        pn.pane.Markdown(
            textwrap.dedent(diagram.__doc__)
            + "\n### Parameters\n\n"
            + diagram.param._repr_html_(),
        ),
        height=500,
        scroll=True,
    )


# Layout Setup
docs_modal[:] = [docs_content]

value_section = pn.Column(
    pn.widgets.TextAreaInput.from_param(diagram.param.value, disabled=True, height=100),
    diagram.param.update_value,
    value_download,
    name="Value",
)

sidebar = [
    example,
    docs_section,
    pn.Accordion(
        initialization,
        events,
        value_section,
        margin=(10, 15, 10, 5),
    ),
]

main_content = pn.Column(
    run,
    pn.pane.Markdown(
        "Click *run* or press *CTRL+Enter* in the editor to update the diagram.",
        margin=(-20, 15, -25, 15),
    ),
    Splitter(
        left=code,
        right=diagram,
        sizing_mode="stretch_both",
        margin=(10, 10, 50, 10),
    ),
)

# Template Setup
pn.template.FastListTemplate(
    title="Panel Mermaid | Diagram Editor",
    logo=LOGO,
    sidebar=sidebar,
    main=[main_content],
    main_layout=None,
    accent=ACCENT,
).servable()
