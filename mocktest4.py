from flask import Flask,render_template,request

app = Flask(__name__)

@app.route("/copy")
@app.route("/home")
def home():
    return render_template("test4.html")

import re
def change_date_format(dt):
        return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', dt)

@app.route("/result",methods = ['POST',"GET"])
def result():

            import imp
            import gspread
            import pandas as pd
            from oauth2client.service_account import ServiceAccountCredentials
            import requests
            import fastapi

            # define the scope
            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

            # add credentials to the account
            creds = ServiceAccountCredentials.from_json_keyfile_name('upbeat-flame-354806-7edf413824bf.json', scope)

            # authorize the clientsheet 
            client = gspread.authorize(creds)

            # get the instance of the Spreadsheet
            sheet = client.open('sample1')

            # get the first sheet of the Spreadsheet
            sheet_instance = sheet.get_worksheet(0)

            # get all the records of the data
            records_data = sheet_instance.get_all_records()

            # convert the json to dataframe
            records_df = pd.DataFrame.from_dict(records_data)

            # view the top records
            res = records_df.head()

            # selecting columns
            clubs = pd.DataFrame(records_data, columns=['Date', 'League', 'Club 1', 'Club 2', 'Copy'])
            print(clubs)

            # get the second sheet of the Spreadsheet
            sheet_updt = sheet.get_worksheet(1)

            # to print date and decision
            output = request.form.to_dict()

            name = output["name"]
            if name !='':             
                dt = change_date_format(output["name"])
                clubs = clubs[clubs['Date'] >= dt] 
                print(clubs.to_json())  
           
            optionSelected = output["optionSelected"]
            if optionSelected == 'y' or optionSelected == 'n' :
                clubs = clubs[(clubs['Copy'] == optionSelected)] 
                print(clubs.to_json())

            Question = output["decision"]
            if Question == ("Yes"):
                sheet_updt.append_rows(clubs.values.tolist())
           
                return render_template("test4.html",name = name )
            else:
                return render_template("test4.html")

if __name__ == '__main__':
    # app.run(debug= True, port=5001)
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)