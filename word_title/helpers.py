from IPython.display import Latex, display
import pandas as pd
from pandas import RangeIndex
from re import sub


row_color = "D3D3D3"


def disp_tex(x: str):
    x = Latex(x)
    latex_x = x._repr_latex_()
    latex_x = (
        latex_x[:2].replace("$$", "\[")
        + latex_x[2:-2]
        + latex_x[-2:].replace("$$", "\]")
    )
    x._repr_latex_ = lambda: latex_x
    display(x)


def _color_if_even(s):
    return [
        f"background-color: #{row_color}" if (int(s.name) + 1) % 2 == 0 else ""
        for val in s
    ]


class TABLE_LATEX_REPR(object):
    def __init__(
        self,
        df: pd.DataFrame,
        column_format: list[int] | dict[int, str] | str | None = None,
        caption: str = "",
        debug: bool = False,
    ):
        self.df = df
        self.column_format = column_format
        self.caption = caption
        self.debug = debug

    def gen_column_formater(self):
        if isinstance(self.column_format, str):
            # add more recent setting to table_styles
            return
        elif isinstance(self.column_format, dict):
            _original_columns = self.df.columns
            self.df.columns = RangeIndex(stop=len(self.df.columns))
            numeric_cols = self.df._get_numeric_data().columns.to_list()
            self.df.columns = _original_columns
            orig_formatter = ""
            for ci, _ in enumerate(self.df.columns):
                orig_formatter += "r" if ci in numeric_cols else "l"
            orig_formatter = [*orig_formatter]
            for i in self.column_format.keys():
                try:
                    orig_formatter[
                        i
                    ] = f"{orig_formatter[i].upper()}{{{self.column_format[i]:.2g}cm}}"
                except TypeError:
                    self.column_format = None
                    return
            self.column_format = "".join(orig_formatter)
            # create a default: set float, complex, int cols to 'r' ('S'), index to 'l'

    def _repr_html_(self):
        if self.debug:
            print(self.debug)
            print(self._repr_latex_())
        return self.df.to_html()

    def __repr__(self):
        return self.df.__repr__()

    def _repr_latex_(self):
        # self.column_format()
        self.gen_column_formater()
        formatter = lambda s: "{:.3G}".format(s) if isinstance(s, float) else s
        output = (
            self.df.style.format(formatter=formatter)
            .apply(_color_if_even, axis=1)
            .hide(axis="index")
            .to_latex(
                hrules=True,
                caption=self.caption,
                position="H",
                column_format=self.column_format,
                environment="longtable",
                convert_css=True,
            )
        )

        output = self.remove_lt_excess(output)
        return output

    def remove_lt_excess(self, output_str):
        output_str = sub(
            r"\\multicolumn\{.*\}\{Continued on next page\} \\\\\n\\midrule",
            "",
            output_str,
        )
        return output_str.replace(
            f"{{\\cellcolor[HTML]{{{row_color}}}}} ",
            f"{{\\cellcolor[HTML]{{{row_color}}}}}",
        )


def display_pd_table(*args, **kwargs):
    return display(TABLE_LATEX_REPR(*args, **kwargs))


def annotate_tex(replace_dict: dict[str, str]):
    with open("annotation_template.tex", "r", encoding="utf8") as f:
        content = f.read()

    for key, value in replace_dict.items():
        content = content.replace(f"???{key}???", value)

    with open("annotation.tex", "w", encoding="utf8") as f:
        f.write(content)


if __name__ == "__main__":
    import pandas as pd

    disp_tex("$$x^2$$")
