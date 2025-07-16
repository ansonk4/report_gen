# import plotly.graph_objects as go


# def format_label(label: list[str]) -> list[str]:
#     label = [s.capitalize() for s in label]
#     return [s.replace("_", " ") for s in label]


# def double_bar_chart(
#         x_values, school_values:dict, avg_values:dict, 
#         title, xtitle, x1name, 
#         x2name, output_path):

#     school_values = [school_values[value] for value in x_values]
#     avg_values = [avg_values[value] for value in x_values]
#     x_values = format_label(x_values)

#     fig = go.Figure(data=[
#         go.Bar(name=x1name, x=x_values, y=school_values),
#         go.Bar(name=x2name, x=x_values, y=avg_values)
#     ])

#     fig.update_layout(
#         barmode='group',
#         title=title,
#         xaxis_title=xtitle,
#         yaxis_title='Percentage',
#     )

#     fig.write_image(output_path)

# def pie_chart(labels: list[str], values: dict[str, float], title: str, output_path: str):

#     values = [values[label] for label in labels]
#     labels = format_label(labels)
#     fig = go.Figure(data=[
#         go.Pie(
#             labels=labels,
#             values=values,
#             textinfo='label+percent',
#             textposition='inside',
#             automargin=True,
#             pull=[0.02]*len(labels)  # Slightly pull out all slices for better separation
#         )
#     ])
#     fig.update_layout(
#         title=title,
#         legend=dict(orientation="v", x=1, y=0.5),
#         margin=dict(t=60, b=60, l=60, r=120)  # Add more right margin for labels
#     )
#     fig.write_image(output_path)

# def bar_chart(x_values: list[str], y_values: list[float], title: str, xtitle: str, ytitle: str, output_path: str):
#     # Sort by y_values descending
#     x_values = format_label(x_values)
#     sorted_pairs = sorted(zip(x_values, y_values), key=lambda x: x[1], reverse=False)
#     x_values, y_values = zip(*sorted_pairs)
#     x_values = format_label(list(x_values))
#     fig = go.Figure(data=[
#         go.Bar(
#             x=y_values,
#             y=x_values,
#             orientation='h',
#             text=[f"{v:.2f}%" for v in y_values],
#             textposition='auto'
#         )
#     ])
#     fig.update_layout(
#         title=title,
#         xaxis_title=ytitle,
#         yaxis_title=xtitle,
#     )
#     fig.write_image(output_path)


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

    # Define explicit colors for better visibility
    colors = ['#1f77b4', '#ff7f0e']  # Blue and orange
    
    fig = go.Figure(data=[
        go.Bar(name=x1name, x=x_values, y=school_values, marker_color=colors[0]),
        go.Bar(name=x2name, x=x_values, y=avg_values, marker_color=colors[1])
    ])

    fig.update_layout(
        barmode='group',
        title=title,
        xaxis_title=xtitle,
        yaxis_title='Percentage',
        template='plotly_white',  # Use white template for better contrast
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # Write with explicit settings for better color handling
    fig.write_image(output_path, format='png', scale=2)

def pie_chart(labels: list[str], values: dict[str, float], title: str, output_path: str):

    values = [values[label] for label in labels]
    labels = format_label(labels)
    
    # Define a color palette for pie chart
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF']
    
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            textinfo='label+percent',
            textposition='inside',
            automargin=True,
            pull=[0.02]*len(labels),  # Slightly pull out all slices for better separation
            marker=dict(colors=colors[:len(labels)])  # Apply color palette
        )
    ])
    fig.update_layout(
        title=title,
        legend=dict(orientation="v", x=1, y=0.5),
        margin=dict(t=60, b=60, l=60, r=120),  # Add more right margin for labels
        template='plotly_white',
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    fig.write_image(output_path, format='png',scale=2)

def bar_chart(x_values: list[str], y_values: list[float], title: str, xtitle: str, ytitle: str, output_path: str):
    # Sort by y_values descending
    x_values = format_label(x_values)
    sorted_pairs = sorted(zip(x_values, y_values), key=lambda x: x[1], reverse=False)
    x_values, y_values = zip(*sorted_pairs)
    x_values = format_label(list(x_values))
    
    fig = go.Figure(data=[
        go.Bar(
            x=y_values,
            y=x_values,
            orientation='h',
            text=[f"{v:.2f}%" for v in y_values],
            textposition='auto',
            marker_color='#1f77b4'  # Explicit blue color
        )
    ])
    fig.update_layout(
        title=title,
        xaxis_title=ytitle,
        yaxis_title=xtitle,
        template='plotly_white',
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    fig.write_image(output_path, format='png', scale=2)