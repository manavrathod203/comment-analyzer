import asyncio
import subprocess
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
import base64
import os

async def execute_script_async(input_data):
    # Execute the external Python script with the input data
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'main.py'))
    command = ['python', script_path, input_data]
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False,  # Set text to False for bytes output
    )

    stdout, stderr = await process.communicate()

    # Check if the script executed successfully
    if process.returncode == 0:
        script_output = stdout.decode()  # Convert bytes to a string
    else:
        script_output = f"Error: {stderr.decode()}"  # Convert bytes to a string

    return script_output

def execute_script(request):
    script_output = None

    if request.method == 'POST':
        input_data = request.POST.get('input_data')
        if input_data:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            script_output = loop.run_until_complete(execute_script_async(input_data))
            loop.close()

    # Rest of your view code remains the same
    # ...---------------------------------

    # Read CSV files into pandas DataFrames
    df1 = pd.read_csv('positive_comments.csv')
    df2 = pd.read_csv('neutral_comments.csv')
    df3 = pd.read_csv('negative_comments.csv')
    

    # Convert DataFrames to HTML tables
    positive_table = df1.to_html(
        classes='table table-bordered border border-dark border-3 table-success ', index=False)
    neutral_table = df2.to_html(
        classes='table table-bordered border border-dark border-3 table-warning ', index=False)
    negative_table = df3.to_html(
        classes='table table-bordered border border-dark border-3 table-danger ', index=False)

    image_path = os.path.abspath('..\\test1\\sentiment_pie_chart.png')
    
    # Read the image file
    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    # Convert the image bytes to a base64 string
    image_base64 = base64.b64encode(image_bytes)

    # Return the HTML for the image tag
    image_html = '<img src="data:image/png;base64,{}">'.format(image_base64.decode())

    # ------------------------------------
    return render(request, 'index.html', {
        'script_output': script_output,
        'positive_table': positive_table,
        'neutral_table': neutral_table,
        'negative_table': negative_table,
        'image_html': image_html,
    })

