import panel as pn
import param
from panel.widgets import WidgetBase

NO_EXAMPLE = ""


# Inspired by https://www.gradio.app/docs/gradio/examples
class ExamplePicker(pn.viewable.Viewer, WidgetBase):
    value = param.Parameter()

    options = param.ClassSelector(class_=(list, dict))
    components = param.Parameter(allow_refs=False)

    def __init__(self, **kwargs):
        if "value" in kwargs and "options" in kwargs:
            value = kwargs["value"]
            options = kwargs["options"]
            if value in options and value not in options.values():
                kwargs["value"] = options[value]

        super().__init__(**kwargs)
        self._selector = pn.widgets.Select(
            value=NO_EXAMPLE, options=self._options, margin=(-10, 10, 10, 10)
        )
        pn.bind(self._update_value, self._selector.param.value, watch=True)()

        if "value" in kwargs:
            self.param.trigger("value")

        self._layout = pn.Column(
            pn.pane.Markdown("**Pick an Example 👇**", margin=(0, 10)), self._selector
        )

    @param.depends("options")
    def _options(self):
        options = self.options
        if isinstance(options, dict):
            return {NO_EXAMPLE: NO_EXAMPLE} | options
        return [NO_EXAMPLE] + self.options

    def _update_value(self, value):
        if value == NO_EXAMPLE:
            return

        if self.value != value:
            self.value = value
        else:
            self.param.trigger("value")

        self._selector.value = None

    @param.depends("value", watch=True)
    def _update_components(self):
        components = self.components
        if not components:
            return
        value = self.value
        if isinstance(components, list):
            raise NotImplementedError
        if hasattr(components, "object"):
            components.object = value
        elif hasattr(components, "value"):
            components.value = value
        else:
            raise ValueError(
                "Error. Component does not have an object or value attribute."
            )

    def __panel__(self):
        return self._layout
