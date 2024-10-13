import mermaid from 'mermaid';

// Helper function to render Mermaid diagram as SVG
async function generateMermaidSVG(graphObject) {
    if (!graphObject) return null;
    const { svg } = await mermaid.render('graphDiv', graphObject);
    return svg;
}

// Initializes Mermaid configuration
function initializeMermaidConfiguration(config) {
    console.log(config)
    const mermaidConfig = { ...config, startOnLoad: false, securityLevel: 'loose' };
    mermaid.initialize(mermaidConfig);
}

// Adds event listeners to SVG elements based on model configuration
function addEventListeners(svgElement, eventConfig, model) {
    if (!svgElement) return;

    eventConfig.forEach(([eventName, className]) => {
        svgElement.querySelectorAll(className).forEach(node => {
            const nodeId = node.id;
            if (nodeId) {
                function handleEvent(event) {
                    const timestamp = new Date().toISOString();
                    model.event = { type: eventName, class: className, id: nodeId, timestamp };
                }
                node.addEventListener(eventName, handleEvent);
            }
        });
    });
}

// Updates the Mermaid object (diagram) and renders it into the element
async function updateDiagram(el, model) {
    if (!model.object) return;
    const svg = await generateMermaidSVG(model.object);
    el.innerHTML = svg;
    const svgElement = el.firstChild;
    addEventListeners(svgElement, model.event_configuration, model);
}

// Main render function exported for use
export async function render({ model, el }) {
    // Initialize Mermaid configuration and render the diagram
    initializeMermaidConfiguration(model.configuration);
    await updateDiagram(el, model);

    // Handle property changes and update the diagram
    model.on('object', () => updateDiagram(el, model));
    model.on('configuration', () => {
        initializeMermaidConfiguration(model.configuration);
        updateDiagram(el, model);
    });
    model.on('event_configuration', () => updateDiagram(el, model));
}
