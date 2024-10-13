from panel.custom import Child, JSComponent

CSS = """
.split {
    display: flex;
    flex-direction: row;
    height: 100%;
    width: 100%;
}

.gutter {
    background-color: var(--light-border-subtle);
    background-repeat: no-repeat;
    background-position: 50%;
}

.gutter.gutter-horizontal {
    background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAeCAYAAADkftS9AAAAIklEQVQoU2M4c+bMfxAGAgYYmwGrIIiDjrELjpo5aiZeMwF+yNnOs5KSvgAAAABJRU5ErkJggg==');
    cursor: col-resize;
}
"""


# Inspired by https://panel.holoviz.org/how_to/custom_components/esm/custom_layout.html
class Splitter(JSComponent):

    left = Child()
    right = Child()

    _esm = """
    import Split from 'https://esm.sh/split.js@1.6.5'

    export function render({ model }) {
      const splitDiv = document.createElement('div');
      splitDiv.className = 'split';

      const split0 = document.createElement('div');
      splitDiv.appendChild(split0);

      const split1 = document.createElement('div');
      splitDiv.appendChild(split1);

      const split = Split([split0, split1])

      model.on('remove', () => split.destroy())

      split0.append(model.get_child("left"))
      split1.append(model.get_child("right"))
      return splitDiv
    }"""

    _stylesheets = [CSS]
