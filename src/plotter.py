import plotly.graph_objects as go


def format_label(label: list[str]) -> list[str]:
    label = [s.capitalize() for s in label]
    return [s.replace("_", " ") for s in label]

def double_bar_chart(
        x_values, school_values:dict, avg_values:dict, 
        title, xtitle, x1name, 
        x2name, output_path):

    school_values = [school_values[value] for value in x_values]
    avg_values = [avg_values[value] for value in x_values]
    x_values = format_label(x_values)
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

def pie_chart(labels: list[str], values: dict[str, float], title: str, output_path: str):

    values = [values[label] for label in labels]
    labels = format_label(labels)
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            textinfo='label+percent',
            textposition='inside',
            automargin=True,
            pull=[0.02]*len(labels)  # Slightly pull out all slices for better separation
        )
    ])
    fig.update_layout(
        title=title,
        legend=dict(orientation="v", x=1, y=0.5),
        margin=dict(t=60, b=60, l=60, r=120)  # Add more right margin for labels
    )
    fig.write_image(output_path)
