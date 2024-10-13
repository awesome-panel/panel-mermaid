import textwrap

import panel as pn
from config import (
    ACCENT,
    BOOTSTRAP_CSS_URL,
    EXAMPLES,
    LOGO,
    MERMAID_JS_URL,
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
config = MermaidConfiguration()
example = ExamplePicker(value="Default", options=EXAMPLES)
code = pn.widgets.CodeEditor(
    value=example.value,
    theme=get_code_editor_theme(),
    sizing_mode="stretch_both",
    on_keyup=False,
)
diagram = MermaidDiagram(
    object=code.value,
    configuration=config,
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
event_label = pn.pane.Markdown("### Mermaid Events", margin=(0, 5, 0, 5))
event = pn.pane.JSON(
    object=diagram.param.event, name="Config Dict", theme=get_json_theme()
)
events = pn.Column(
    event_label,
    diagram.param.event_configuration,
    event,
)

docs_modal = Modal()
docs_section = pn.Column(
    pn.pane.Markdown("### Mermaid Documentation", margin=(0, 5, 0, 5)),
    pn.widgets.Button.from_param(
        docs_modal.param.open,
        name="Show",
        button_type="primary",
        button_style="outline",
        description="Click here to show the Mermaid Parameter documentation",
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
            textwrap.dedent(diagram.__doc__) + "\n" + diagram.param._repr_html_(),
        ),
        height=500,
        scroll=True,
    )


# Layout Setup
docs_modal[:] = [docs_content]

sidebar = [
    example,
    config,
    events,
    docs_section,
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
    site="Panel-Mermaid",
    logo=LOGO,
    site_url=MERMAID_JS_URL,
    sidebar=sidebar,
    main=[main_content],
    main_layout=None,
    accent=ACCENT,
).servable()
