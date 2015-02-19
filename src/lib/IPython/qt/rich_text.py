""" Defines classes and functions for working with Qt's rich text system.
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
import io
import os
import re

# System library imports
from IPython.external.qt import QtGui

# IPython imports
from IPython.utils import py3compat

#-----------------------------------------------------------------------------
# Constants
#-----------------------------------------------------------------------------

# A regular expression for an HTML paragraph with no content.
EMPTY_P_RE = re.compile(r'<p[^/>]*>\s*</p>')

# A regular expression for matching images in rich text HTML.
# Note that this is overly restrictive, but Qt's output is predictable...
IMG_RE = re.compile(r'<img src="(?P<name>[\d]+)" />')

#-----------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------

class HtmlExporter(object):
    """ A stateful HTML exporter for a Q(Plain)TextEdit.

    This class is designed for convenient user interaction.
    """

    def __init__(self, control):
        """ Creates an HtmlExporter for the given Q(Plain)TextEdit.
        """
        assert isinstance(control, (QtGui.QPlainTextEdit, QtGui.QTextEdit))
        self.control = control
        self.filename = 'ipython.html'
        self.image_tag = None
        self.inline_png = None

    def export(self):
        """ Displays a dialog for exporting HTML generated by Qt's rich text
        system.

        Returns
        -------
        The name of the file that was saved, or None if no file was saved.
        """
        parent = self.control.window()
        dialog = QtGui.QFileDialog(parent, 'Save as...')
        dialog.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        filters = [
            'HTML with PNG figures (*.html *.htm)',
            'XHTML with inline SVG figures (*.xhtml *.xml)'
        ]
        dialog.setNameFilters(filters)
        if self.filename:
            dialog.selectFile(self.filename)
            root,ext = os.path.splitext(self.filename)
            if ext.lower() in ('.xml', '.xhtml'):
                dialog.selectNameFilter(filters[-1])

        if dialog.exec_():
            self.filename = dialog.selectedFiles()[0]
            choice = dialog.selectedNameFilter()
            html = py3compat.cast_unicode(self.control.document().toHtml())

            # Configure the exporter.
            if choice.startswith('XHTML'):
                exporter = export_xhtml
            else:
                # If there are PNGs, decide how to export them.
                inline = self.inline_png
                if inline is None and IMG_RE.search(html):
                    dialog = QtGui.QDialog(parent)
                    dialog.setWindowTitle('Save as...')
                    layout = QtGui.QVBoxLayout(dialog)
                    msg = "Exporting HTML with PNGs"
                    info = "Would you like inline PNGs (single large html " \
                        "file) or external image files?"
                    checkbox = QtGui.QCheckBox("&Don't ask again")
                    checkbox.setShortcut('D')
                    ib = QtGui.QPushButton("&Inline")
                    ib.setShortcut('I')
                    eb = QtGui.QPushButton("&External")
                    eb.setShortcut('E')
                    box = QtGui.QMessageBox(QtGui.QMessageBox.Question,
                                            dialog.windowTitle(), msg)
                    box.setInformativeText(info)
                    box.addButton(ib, QtGui.QMessageBox.NoRole)
                    box.addButton(eb, QtGui.QMessageBox.YesRole)
                    layout.setSpacing(0)
                    layout.addWidget(box)
                    layout.addWidget(checkbox)
                    dialog.setLayout(layout)
                    dialog.show()
                    reply = box.exec_()
                    dialog.hide()
                    inline = (reply == 0)
                    if checkbox.checkState():
                        # Don't ask anymore; always use this choice.
                        self.inline_png = inline
                exporter = lambda h, f, i: export_html(h, f, i, inline)

            # Perform the export!
            try:
                return exporter(html, self.filename, self.image_tag)
            except Exception as e:
                msg = "Error exporting HTML to %s\n" % self.filename + str(e)
                reply = QtGui.QMessageBox.warning(parent, 'Error', msg,
                    QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)

        return None

#-----------------------------------------------------------------------------
# Functions
#-----------------------------------------------------------------------------

def export_html(html, filename, image_tag = None, inline = True):
    """ Export the contents of the ConsoleWidget as HTML.

    Parameters
    ----------
    html : unicode,
        A Python unicode string containing the Qt HTML to export.

    filename : str
        The file to be saved.

    image_tag : callable, optional (default None)
        Used to convert images. See ``default_image_tag()`` for information.

    inline : bool, optional [default True]
        If True, include images as inline PNGs.  Otherwise, include them as
        links to external PNG files, mimicking web browsers' "Web Page,
        Complete" behavior.
    """
    if image_tag is None:
        image_tag = default_image_tag

    if inline:
        path = None
    else:
        root,ext = os.path.splitext(filename)
        path = root + "_files"
        if os.path.isfile(path):
            raise OSError("%s exists, but is not a directory." % path)

    with io.open(filename, 'w', encoding='utf-8') as f:
        html = fix_html(html)
        f.write(IMG_RE.sub(lambda x: image_tag(x, path = path, format = "png"),
                           html))


def export_xhtml(html, filename, image_tag=None):
    """ Export the contents of the ConsoleWidget as XHTML with inline SVGs.

    Parameters
    ----------
    html : unicode,
        A Python unicode string containing the Qt HTML to export.

    filename : str
        The file to be saved.

    image_tag : callable, optional (default None)
        Used to convert images. See ``default_image_tag()`` for information.
    """
    if image_tag is None:
        image_tag = default_image_tag

    with io.open(filename, 'w', encoding='utf-8') as f:
        # Hack to make xhtml header -- note that we are not doing any check for
        # valid XML.
        offset = html.find("<html>")
        assert offset > -1, 'Invalid HTML string: no <html> tag.'
        html = (u'<html xmlns="http://www.w3.org/1999/xhtml">\n'+
                html[offset+6:])

        html = fix_html(html)
        f.write(IMG_RE.sub(lambda x: image_tag(x, path = None, format = "svg"),
                           html))


def default_image_tag(match, path = None, format = "png"):
    """ Return (X)HTML mark-up for the image-tag given by match.

    This default implementation merely removes the image, and exists mostly
    for documentation purposes. More information than is present in the Qt
    HTML is required to supply the images.

    Parameters
    ----------
    match : re.SRE_Match
        A match to an HTML image tag as exported by Qt, with match.group("Name")
        containing the matched image ID.

    path : string|None, optional [default None]
        If not None, specifies a path to which supporting files may be written
        (e.g., for linked images).  If None, all images are to be included
        inline.

    format : "png"|"svg", optional [default "png"]
        Format for returned or referenced images.
    """
    return u''


def fix_html(html):
    """ Transforms a Qt-generated HTML string into a standards-compliant one.

    Parameters
    ----------
    html : unicode,
        A Python unicode string containing the Qt HTML.
    """
    # A UTF-8 declaration is needed for proper rendering of some characters
    # (e.g., indented commands) when viewing exported HTML on a local system
    # (i.e., without seeing an encoding declaration in an HTTP header).
    # C.f. http://www.w3.org/International/O-charset for details.
    offset = html.find('<head>')
    if offset > -1:
        html = (html[:offset+6]+
                '\n<meta http-equiv="Content-Type" '+
                'content="text/html; charset=utf-8" />\n'+
                html[offset+6:])

    # Replace empty paragraphs tags with line breaks.
    html = re.sub(EMPTY_P_RE, '<br/>', html)

    return html
