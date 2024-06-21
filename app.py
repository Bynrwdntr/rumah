from flask import Flask, render_template # type: ignore
import pandas as pd # type: ignore

app = Flask(__name__)

@app.route('/dataset')
def dataset():
    # Read data from CSV
    data = pd.read_csv('data.csv')

    # Rename columns for consistency with your data
    data.columns = ['Usia', 'Pendapatan', 'Status_Pernikahan', 'Jumlah_Anak', 'Membeli_Rumah']

    # Initialize an empty dictionary to hold percentages
    percentages = {}

    # Define columns to calculate percentages for
    columns = ['Usia', 'Pendapatan', 'Status_Pernikahan', 'Jumlah_Anak']

    for column in columns:
        # Group data by the current column and calculate counts for 'Ya' and 'Tidak'
        counts = data.groupby([column, 'Membeli_Rumah']).size().unstack(fill_value=0)
        counts['Ya'] = counts.get('Ya', 0)
        counts['Tidak'] = counts.get('Tidak', 0)
        
        # Calculate P(Ya) and P(Tidak)
        counts['P(Ya)'] = counts['Ya'] / (counts['Ya'] + counts['Tidak'])
        counts['P(Tidak)'] = counts['Tidak'] / (counts['Ya'] + counts['Tidak'])

        # Round percentages to two decimal places
        counts['P(Ya)'] = counts['P(Ya)'].apply(lambda x: round(x, 2))
        counts['P(Tidak)'] = counts['P(Tidak)'].apply(lambda x: round(x, 2))

        # Reset index to turn the groupby result into a regular DataFrame
        percentages[column] = counts.reset_index().to_dict(orient='records')

    # Convert the entire DataFrame to HTML for display
    data_html = data.to_html(classes='table table-striped table-bordered table-hover', index=False)

    return render_template('dataset.html', data_html=data_html, percentages=percentages)

if __name__ == '__main__':
    app.run(debug=True)
