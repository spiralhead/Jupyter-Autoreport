# from docx import Document
# from docx.shared import Pt
import comtypes.client
import os


def search_and_replace_in_word(app, search_str, replace_str):
    wdFindContinue = 1
    wdReplaceAll = 2
    replace_str = replace_str.replace("\n", "^p\n")
    app.Selection.Find.Execute(
        search_str,
        False,
        False,
        False,
        False,
        False,
        True,
        wdFindContinue,
        False,
        replace_str,
        wdReplaceAll,
    )


wdFormatPDF = 17


def annotate_docx(word_file, replace_dict):
    """replace all occurrences of `find_str` w/ `replace_str` in `word_file`"""
    transfer_dict = {}
    for key in replace_dict.keys():
        transfer_dict[f"<<{key}>>"] = replace_dict[key]
    replace_dict = transfer_dict

    # Dispatch() attempts to do a GetObject() before creating a new one.
    # DispatchEx() just creates a new one.

    app = comtypes.client.CreateObject("Word.Application", dynamic=True)
    doc = app.Documents.Open(os.path.abspath(word_file))

    # expression.Execute(FindText, MatchCase, MatchWholeWord,
    #   MatchWildcards, MatchSoundsLike, MatchAllWordForms, Forward,
    #   Wrap, Format, ReplaceWith, Replace)
    try:
        for key, val in replace_dict.items():
            if len(val) > 250:
                val = [
                    val[i : i + 250 - 2 * len(key)]
                    for i in range(0, len(val), 250 - 2 * len(key))
                ]
                for chunk in val[:-1]:
                    search_and_replace_in_word(app, key, chunk + key)
                search_and_replace_in_word(app, key, val[-1])
            else:
                search_and_replace_in_word(app, key, val)
            for section in app.ActiveDocument.Sections:
                for header in section.Headers:
                    for shape in header.Shapes:
                        if shape.TextFrame.HasText:
                            if key in shape.TextFrame.TextRange.Text:
                                shape.TextFrame.TextRange.Text = (
                                    shape.TextFrame.TextRange.Text.replace(key, val)
                                )
        doc.SaveAs(
            os.path.splitext(os.path.abspath(word_file))[0] + ".pdf", wdFormatPDF
        )

    finally:
        app.Quit(False)


if __name__ == "__main__":
    pass
