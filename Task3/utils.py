import pandas as pd
import plotly.graph_objects as go

# Calculate percentage change
def calculate_percentage_change(df):
    df['Percentage Change'] = df['Close'].pct_change() * 100
    return df

# Plotting function
def plot_data(df1, df2, title="Stock vs Currency Trends"):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df1.index, y=df1['Percentage Change'], mode='lines', name='Exchange Rate Change'))
    fig.add_trace(go.Scatter(x=df2.index, y=df2['Percentage Change'], mode='lines', name='Stock Price Change'))

    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Percentage Change',
        template="plotly_dark"
    )
    fig.show()

# Alert System (simple email alert for now)
def send_alert(message, to_email="your_email@example.com"):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    sender_email = "your_email@example.com"
    password = "your_password"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = 'Currency Impact Alert'
    
    msg.attach(MIMEText(message, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    text = msg.as_string()
    server.sendmail(sender_email, to_email, text)
    server.quit()
