import panel as pn

LOGO = "https://avatars.githubusercontent.com/u/57169982?s=200&v=4"
ACCENT = "#db2777"
MERMAID_JS_URL = "https://mermaid.js.org/"
PANEL_MERMAID_URL = "https://github.com/awesome-panel/panel-mermaid"
EXAMPLES = {
    "Default": """\
graph LR
    A[Hello] --> B[fa:fa-chart-simple Panel] --> E[World]
    A-->C(fa:fa-diagram-project Mermaid) --> E ;
""",
    "Architecture": """\
architecture-beta
    group api(cloud)[API]

    service db(database)[Database] in api
    service disk1(disk)[Storage] in api
    service disk2(disk)[Storage] in api
    service server(server)[Server] in api

    db:L -- R:server
    disk1:T -- B:server
    disk2:T -- B:db
""",
}

BOOTSTRAP_CSS_URL = (
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css"
)


def get_json_theme():
    if pn.config.theme == "dark":
        return "dark"
    return "light"


def get_code_editor_theme():
    if pn.config.theme == "dark":
        return "chaos"
    return "crimson_editor"
