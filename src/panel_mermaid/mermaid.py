
import panel as pn
import param
from panel.custom import JSComponent
from panel.widgets import WidgetBase

VERSION = 11

THEME_MAP = {"default": "default", "dark": "dark"}


def _get_default_theme(panel_theme: str) -> str:
    return THEME_MAP.get(panel_theme, "default")


# See https://mermaid.js.org/schemas/config.schema.json
class MermaidConfiguration(pn.viewable.Viewer, WidgetBase):
    """\
    An interactive Widget for editing the Mermaid JS configuration.

    See https://mermaid.js.org/schemas/config.schema.json

    Example:
    ```python
    config = MermaidConfiguration()
    ```

    You can use it as a *reference value* for the MermaidDiagram:

    ```python
    diagram = MermaidDiagram(
        object="...",
        configuration=config,
        ...
    )
    """

    value: dict = param.Dict(
        constant=True,
        doc="""The mermaid configuration as described in https://mermaid.js.org/schemas/config.schema.json.""",
    )

    look: str = param.Selector(
        default="classic",
        objects=["classic", "handDrawn"],
        doc="""Defines which main look to use for the diagram.""",
    )
    theme: str = param.Selector(
        default="default",
        objects=["default", "base", "dark", "forest", "neutral"],
        doc="""Theme, the CSS style sheet.\nYou may also use `themeCSS` to override this value.\n""",
    )

    def __init__(self, **params):
        if "theme" not in params:
            params["theme"] = _get_default_theme(pn.config.theme)
        super().__init__(**params)

    @param.depends("look", "theme", watch=True, on_init=True)
    def _update_value(self):
        value = {"look": self.look, "theme": self.theme}
        value = {
            key: value
            for key, value in value.items()
            if value and value != self.param[key].default
        }

        with param.edit_constant(self):
            self.value = value

    def __panel__(self):
        return pn.Column(
            pn.pane.Markdown(
                """### Mermaid Configuration
            """,
                margin=(0, 5, 0, 5),
            ),
            self.param.look,
            self.param.theme,
        )


class MermaidDiagram(JSComponent):
    '''\
    An interactive `MermaidDiagram` pane based on [Mermaid JS](https://mermaid.js.org/).

    Example:

    ```python
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
    ```

    If you want to use Font-Awesome icons prefixed with `fa:`, you
    can do this by including the Font-Awesome CSS in your application:

    ```python
    pn.extension(
        ...
        css_files=[
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css"
        ],
    )
    ```
    '''

    object = param.String(
        default="",
        allow_refs=True,
        doc="""A mermaid diagram string like
            graph LR
                A --- B
                B-->C[forbidden]
                B-->D[allowed];""",
    )
    configuration = param.Dict(
        {},
        allow_refs=True,
        doc="""The mermaid configuration as described in https://mermaid.js.org/schemas/config.schema.json.""",
    )
    event: dict = param.Dict(
        allow_refs=False, doc="""An event from interacting with the diagram"""
    )
    event_configuration: list = param.List(
        item_type=tuple,
        doc="""List of (event name, query selector string) tuples to subscribe to.
        For example [("click", ".node")] or [("mouseover", ".node")].""",
        allow_refs=True,
    )

    _esm = "mermaid.esm.js"
    _styles = (
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css"
    )

    _importmap = {
        "imports": {
            "mermaid": f"https://cdn.jsdelivr.net/npm/mermaid@{VERSION}/dist/mermaid.esm.min.mjs"
        }
    }
