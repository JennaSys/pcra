from common.pyreact import createElement as el, Fragment, useContext
from common.pymui import Menu, MenuItem
from main import UserCtx


def LandingPageMenu(props):
    mainMenu = props['mainMenu']
    mainMenuClose = props['mainMenuClose']
    aboutModalOpen = props['aboutModalOpen']

    ctx = useContext(UserCtx)
    logout = ctx['logout']
    isLoggedIn = ctx['isLoggedIn']

    def handleAbout():
        mainMenuClose()
        aboutModalOpen()

    def handleLogout():
        mainMenuClose()
        logout()

    return el(Fragment, None,
              el(Menu, {'id': 'main-menu',
                        'anchorEl': mainMenu,
                        'keepMounted': True,
                        'open': bool(mainMenu),
                        'onClose': mainMenuClose,
                        },
                 el(MenuItem, {'onClick': handleAbout}, "About"),
                 el(MenuItem, {'onClick': handleLogout,
                               'disabled': not isLoggedIn}, "Logout"),
                 ),
              )
