import plotly.graph_objs as go


def scatter_layout(title: str, x_name: str, y_name: str) -> go.Layout:
    """
    Scatter type Layout for plots.
    :param title: str.
    :param x_name: str. Name to be used in plot.
    :param y_name: str. Name to be used in plot.
    :return: go.Layout.
    """
    return go.Layout(title=title,
                     xaxis={'title': x_name},
                     yaxis={'title': y_name},
                     hovermode='closest')
