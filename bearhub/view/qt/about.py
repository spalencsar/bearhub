import os
from glob import glob
from typing import Optional

from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtGui import QIcon, QPixmap, QCursor, QDesktopServices, QFont
from PyQt5.QtWidgets import (
    QVBoxLayout, QDialog, QLabel, QWidget, QHBoxLayout, QSizePolicy,
    QApplication, QFrame, QPushButton, QGridLayout,
)

from bearhub import __version__, ROOT_DIR
from bearhub.context import generate_i18n
from bearhub.view.util import resource

DISPLAY_NAME = 'Bearhub'
PROJECT_URL = 'https://github.com/spalencsar/bearhub'
LICENSE_URL = 'https://raw.githubusercontent.com/spalencsar/bearhub/main/LICENSE'
ISSUES_URL = 'https://github.com/spalencsar/bearhub/issues'
STARS_URL = 'https://github.com/spalencsar/bearhub'


def _open_url(url: str) -> None:
    QDesktopServices.openUrl(QUrl(url))


def _logo_path() -> str:
    png = resource.get_path('img/logo.png')
    if os.path.isfile(png):
        return png
    return resource.get_path('img/logo.svg')


def _scaled_logo(size: int) -> QPixmap:
    pm = QPixmap(_logo_path())
    if pm.isNull():
        return pm
    return pm.scaled(QSize(size, size), Qt.KeepAspectRatio, Qt.SmoothTransformation)


class AboutDialog(QDialog):
    """
    Bearhub About — structured layout (not the old bauh stack of centered labels).

    Sections:
      1. Header: logo left + title/version right
      2. Product blurb
      3. Source matrix (icon + name per backend)
      4. Action row (GitHub / Issues / License)
      5. Footer close
    """

    def __init__(self, app_config: dict):
        super(AboutDialog, self).__init__()
        self.setObjectName('about_dialog')
        self.i18n = generate_i18n(app_config, resource.get_path('locale/about'))
        i18n = self.i18n

        self.setWindowTitle(f"{i18n['about.title']} — {DISPLAY_NAME}")
        self.setWindowIcon(QIcon(_logo_path()))
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── 1. Header band ──────────────────────────────────────────────
        header = QWidget(self)
        header.setObjectName('about_header')
        header_l = QHBoxLayout(header)
        header_l.setContentsMargins(24, 22, 24, 18)
        header_l.setSpacing(18)

        logo = QLabel(header)
        logo.setObjectName('logo')
        logo.setFixedSize(88, 88)
        logo.setAlignment(Qt.AlignCenter)
        pm = _scaled_logo(88)
        if not pm.isNull():
            logo.setPixmap(pm)
        header_l.addWidget(logo, 0, Qt.AlignVCenter)

        title_col = QVBoxLayout()
        title_col.setSpacing(4)
        title_col.setContentsMargins(0, 4, 0, 4)

        name = QLabel(DISPLAY_NAME, header)
        name.setObjectName('app_name')
        name_font = QFont(name.font())
        name_font.setPointSize(max(16, name_font.pointSize() + 4))
        name_font.setBold(True)
        name.setFont(name_font)
        title_col.addWidget(name)

        tagline = QLabel(i18n.get('about.info.tagline', 'Arch package hub'), header)
        tagline.setObjectName('app_tagline')
        title_col.addWidget(tagline)

        version = QLabel(f"{i18n.get('about.version', 'Version')} {__version__}", header)
        version.setObjectName('app_version')
        title_col.addWidget(version)
        title_col.addStretch(1)

        header_l.addLayout(title_col, 1)
        root.addWidget(header)

        # ── 2. Body ─────────────────────────────────────────────────────
        body = QWidget(self)
        body.setObjectName('about_body')
        body_l = QVBoxLayout(body)
        body_l.setContentsMargins(24, 16, 24, 8)
        body_l.setSpacing(14)

        section_what = self._section_title(i18n.get('about.section.what', 'What is Bearhub?'), body)
        body_l.addWidget(section_what)

        desc = QLabel(i18n.get('about.info.desc', ''), body)
        desc.setObjectName('app_description')
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        desc.setMinimumWidth(400)
        body_l.addWidget(desc)

        section_src = self._section_title(i18n.get('about.section.sources', 'Package sources'), body)
        body_l.addWidget(section_src)

        sources = self._build_sources_grid(body)
        body_l.addWidget(sources)

        root.addWidget(body)

        # ── 3. Actions ──────────────────────────────────────────────────
        actions = QWidget(self)
        actions.setObjectName('about_actions')
        actions_l = QHBoxLayout(actions)
        actions_l.setContentsMargins(24, 8, 24, 8)
        actions_l.setSpacing(10)

        actions_l.addWidget(self._link_button(
            i18n.get('about.action.github', 'GitHub'),
            PROJECT_URL,
            'about_btn_github'))
        actions_l.addWidget(self._link_button(
            i18n.get('about.action.issues', 'Issues'),
            ISSUES_URL,
            'about_btn_issues'))
        actions_l.addWidget(self._link_button(
            i18n.get('about.action.license', 'License'),
            LICENSE_URL,
            'about_btn_license'))
        actions_l.addStretch(1)

        root.addWidget(actions)

        # ── 4. Footer ───────────────────────────────────────────────────
        footer = QWidget(self)
        footer.setObjectName('about_footer')
        footer_l = QHBoxLayout(footer)
        footer_l.setContentsMargins(24, 12, 24, 16)
        footer_l.setSpacing(12)

        note = QLabel(i18n.get('about.footer.fork', ''), footer)
        note.setObjectName('about_footer_note')
        note.setWordWrap(True)
        note.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        footer_l.addWidget(note, 1)

        bt_close = QPushButton(i18n.get('about.close', 'Close'), footer)
        bt_close.setObjectName('about_close')
        bt_close.setCursor(QCursor(Qt.PointingHandCursor))
        bt_close.setDefault(True)
        bt_close.clicked.connect(self.hide)
        footer_l.addWidget(bt_close, 0, Qt.AlignRight | Qt.AlignVCenter)

        root.addWidget(footer)

        self.adjustSize()
        w = max(480, self.sizeHint().width())
        h = self.sizeHint().height()
        self.setFixedSize(w, h)

    def _section_title(self, text: str, parent: QWidget) -> QLabel:
        lbl = QLabel(text, parent)
        lbl.setObjectName('about_section')
        f = QFont(lbl.font())
        f.setBold(True)
        f.setPointSize(max(10, f.pointSize()))
        lbl.setFont(f)
        return lbl

    def _link_button(self, label: str, url: str, object_name: str) -> QPushButton:
        bt = QPushButton(label, self)
        bt.setObjectName(object_name)
        bt.setProperty('about_action', True)
        bt.setCursor(QCursor(Qt.PointingHandCursor))
        bt.clicked.connect(lambda _=False, u=url: _open_url(u))
        return bt

    def _build_sources_grid(self, parent: QWidget) -> QWidget:
        """Icon + label tiles for each gem (not a bare icon row)."""
        wrap = QWidget(parent)
        wrap.setObjectName('about_sources')
        grid = QGridLayout(wrap)
        grid.setContentsMargins(0, 4, 0, 0)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(10)

        # Friendly labels for known backends
        labels = {
            'arch': self.i18n.get('about.source.arch', 'Arch / AUR'),
            'flatpak': self.i18n.get('about.source.flatpak', 'Flatpak'),
            'appimage': self.i18n.get('about.source.appimage', 'AppImage'),
            'web': self.i18n.get('about.source.web', 'Web apps'),
        }

        available = []
        for gem_path in sorted(glob(f'{ROOT_DIR}/gems/*')):
            if gem_path.endswith('.py') or gem_path.endswith('__pycache__'):
                continue
            name = gem_path.split('/')[-1]
            icon_path = f'{gem_path}/resources/img/{name}.svg'
            if os.path.isfile(icon_path):
                available.append((name, icon_path, labels.get(name, name.capitalize())))

        gem_px = 32
        cols = 2
        for idx, (name, icon_path, label) in enumerate(available):
            tile = QFrame(wrap)
            tile.setObjectName('about_source_tile')
            tile.setProperty('gem', name)
            tl = QHBoxLayout(tile)
            tl.setContentsMargins(10, 8, 12, 8)
            tl.setSpacing(10)

            ic = QLabel(tile)
            ic.setObjectName('gem_logo')
            ic.setFixedSize(gem_px, gem_px)
            ic.setPixmap(QIcon(icon_path).pixmap(gem_px, gem_px))
            tl.addWidget(ic)

            name_lbl = QLabel(label, tile)
            name_lbl.setObjectName('about_source_name')
            tl.addWidget(name_lbl, 1)

            r, c = divmod(idx, cols)
            grid.addWidget(tile, r, c)

        return wrap

    def closeEvent(self, event):
        event.ignore()
        self.hide()
