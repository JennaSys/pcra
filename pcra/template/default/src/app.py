# __pragma__ ('skip')
def require(lib): return lib

class document:
    getElementById = None
    addEventListener = None
# __pragma__ ('noskip')


pythonlogo = require('../python_logo.png')
reactlogo = require('../react_logo.png')
styles = require('../app.css')
React = require('react')
ReactDOM = require('react-dom')

el = React.createElement


def App():
    return (
        el('div', {'className': "App"},
           el('header', {'className': 'App-header'},
              el('div', {'className': 'image-container'},
                 el('img', {'src': pythonlogo, 'className': 'App-logo', 'alt': "python logo"}),
                 el('span', {'className': 'overlay-image'},
                    el('img', {'src': reactlogo, 'className': 'App-logo Spin-logo', 'alt': "react logo"})
                    )
                 ),
              el('p', None, "Edit ", el('code', None, "src/app.py"), " and save to reload."),
              el('a', {'className': 'App-link',
                       'href': "https://reactjs.org",
                       'target': "_blank",
                       'rel': "noopener noreferrer"
                       },
                 "React"
                 ),
              el('a', {'className': 'App-link',
                       'href': "https://material-ui.com",
                       'target': "_blank",
                       'rel': "noopener noreferrer"
                       },
                 "Material-UI"
                 ),
              el('a', {'className': 'App-link',
                       'href': "https://www.transcrypt.org",
                       'target': "_blank",
                       'rel': "noopener noreferrer"
                       },
                 "Transcrypt"
                 ),
              el('a', {'className': 'App-link',
                       'href': "https://pyreact.com",
                       'target': "_blank",
                       'rel': "noopener noreferrer"
                       },
                 "React to Python"
                 )
              )
           )
    )


def render():
    ReactDOM.render(
        React.createElement(App, None),
        document.getElementById('root')
    )


document.addEventListener("DOMContentLoaded", render)
