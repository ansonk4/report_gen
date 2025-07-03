import plotly.graph_objects as go


def double_bar_chart(
        x_values, school_values:dict, avg_values:dict, 
        title, xtitle, x1name, 
        x2name, output_path):

    school_values = [school_values[value] for value in x_values]
    avg_values = [avg_values[value] for value in x_values]

    fig = go.Figure(data=[
        go.Bar(name=x1name, x=x_values, y=school_values),
        go.Bar(name=x2name, x=x_values, y=avg_values)
    ])

    fig.update_layout(
        barmode='group',
        title=title,
        xaxis_title=xtitle,
        yaxis_title='Percentage',
    )

    fig.write_image(output_path)

