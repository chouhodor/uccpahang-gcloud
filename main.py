
import os
import json
import gspread
import pprint
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, abort, redirect, url_for
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'uccpahangtopsecret'

try:
    #live test
    scopes = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    json_creds = os.getenv("GOOGLE_SHEETS_CREDS_JSON")

    creds_dict = json.loads(json_creds)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
    client = gspread.authorize(creds)

    pkrc_list = []
    with open('/app/app/pkrc.json') as f:
        pkrc_list = json.load(f)

    hospital_list = []
    with open('/app/app/hospital.json') as g:
        hospital_list = json.load(g)
    #live test


except:
    #local test
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('ucc-pahang.json', scope)
    client = gspread.authorize(creds)

    pkrc_list = []
    with open('pkrc.json') as f:
        pkrc_list = json.load(f)

    hospital_list = []
    with open('hospital.json') as g:
        hospital_list = json.load(g)
    #local test


###UCC Bed Watcher###
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/14vFutdJuHcszQKIpAcqyQ106AtBSebeghrRxTp9ittQ")
sheet = spreadsheet.sheet1

spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/14vFutdJuHcszQKIpAcqyQ106AtBSebeghrRxTp9ittQ")
sheet_grand = spreadsheet.worksheet('Sheet2')

###UCC Statistics###
spreadsheet_uccstats = client.open_by_url("https://docs.google.com/spreadsheets/d/1qUglpzUaioqgCg_PMunjRIq4r0hu9RdcsVBhFazWhyg")
sukpa_stats_sh = spreadsheet_uccstats.worksheet("sukpa")
ilkkm_stats_sh = spreadsheet_uccstats.worksheet("ilkkm")
ump_stats_sh = spreadsheet_uccstats.worksheet("ump")
ikpkt_stats_sh = spreadsheet_uccstats.worksheet("ikpkt")
kuipsas_stats_sh = spreadsheet_uccstats.worksheet("kuipsas")
maran_stats_sh = spreadsheet_uccstats.worksheet("maran")
uniten_stats_sh = spreadsheet_uccstats.worksheet("uniten")
temerloh_stats_sh = spreadsheet_uccstats.worksheet("temerloh")
ipglipis_stats_sh = spreadsheet_uccstats.worksheet("ipglipis")
rompin_stats_sh = spreadsheet_uccstats.worksheet("rompin")

master_stats_sh = spreadsheet_uccstats.worksheet("master")

####BRANCH####


def maxhour (h):
    if h > 48:
        return 48
    else:
         return h

def bor_color (color):
    red = 'red'
    orange = 'orange'
    white = 'white'
    yellow = 'yellow'

    if color >= 90:
        return red
    elif 75 <= color <= 89.9:
        return orange
    elif 50 <= color <= 74.9:
        return yellow
    else:
        return white

@app.route('/', methods=['POST','GET'])
def index():
    '''
    maxhours=maxhour
    bor_colors = bor_color
      
    dict_sheet = sheet.get_all_records()
    dict_sh_grand = sheet_grand.get_all_records()
    date_times = (datetime.now() + timedelta(hours=8)).strftime("%d/%m/%Y %H:%M:%S")
    
    return render_template('index.html',  
    dict_sheet = dict_sheet,
    dict_sh_grand=dict_sh_grand,
    date_times=date_times,
    maxhours=maxhours,
    bor_colors=bor_colors,
    )
    '''
    return render_template('endlife.html')

@app.route('/hospital', methods=['POST','GET'])
def hospital():
    '''
    maxhours=maxhour
    bor_colors = bor_color
      
    dict_sheet = sheet.get_all_records()
    dict_sh_grand = sheet_grand.get_all_records()
    date_times = (datetime.now() + timedelta(hours=8)).strftime("%d/%m/%Y %H:%M:%S")
    
    return render_template('hospital.html',  
    dict_sheet = dict_sheet,
    dict_sh_grand=dict_sh_grand,
    date_times=date_times,
    maxhours=maxhours,
    bor_colors=bor_colors,
    )
    '''
    return render_template('endlife.html')
    
@app.route('/private', methods=['POST','GET'])
def private():

    maxhours=maxhour
    bor_colors = bor_color
      
    dict_sheet = sheet.get_all_records()
    dict_sh_grand = sheet_grand.get_all_records()
    date_times = (datetime.now() + timedelta(hours=8)).strftime("%d/%m/%Y %H:%M:%S")
    
    return render_template('private.html',  
    dict_sheet = dict_sheet,
    dict_sh_grand=dict_sh_grand,
    date_times=date_times,
    maxhours=maxhours,
    bor_colors=bor_colors,
    )
    
    
@app.route('/result_pkrc', methods = ['POST'])
def result_pkrc():

    date_times = (datetime.now() + timedelta(hours=8)).strftime("%d/%m/%Y %H:%M:%S")
    pkrc = request.form['pkrc']
    a_male = int(request.form['a_male'])
    a_female = int(request.form['a_female'])
    discharge = request.form['discharge']
    capacity = int(request.form['capacity'])
    passkey = request.form['passkey']
    admin = '5079'

    pkrc_dict = { 'sukpa' : 0 ,
     'ilkkm' : 1,
     'ilkkm_covid': 2,
     'maran': 3,
     'kuipsas' : 4 ,
     'ump' : 5,
     'azzahra' : 6,
     'sulaiman_t' : 7,
     'ipglipis' : 8,
     'temerloh' : 9,
     'uniten' : 10,
     'ancasa' : 11,
     'sg_kiol' : 12,
     'panderas' : 13,
     'sg_koyan' : 14,
     'rompin' : 15 
     }
    pkrc_centre = pkrc_list
    
    def update_func():
        sheet.update(pkrc_centre[pkrc_dict[pkrc]]['a_male_dict'] , a_male)
        sheet.update(pkrc_centre[pkrc_dict[pkrc]]['a_female_dict'] , a_female)
        sheet.update(pkrc_centre[pkrc_dict[pkrc]]['discharge_dict'] , discharge)
        sheet.update(pkrc_centre[pkrc_dict[pkrc]]['capacity_dict'] , capacity)
        sheet.update(pkrc_centre[pkrc_dict[pkrc]]['date_times_dict'], date_times)
    
    def update_func2():
        sheet.update(pkrc_centre[pkrc_dict[pkrc]]['a_male_dict'] , a_male)
        sheet.update(pkrc_centre[pkrc_dict[pkrc]]['a_female_dict'] , a_female)
        sheet.update(pkrc_centre[pkrc_dict[pkrc]]['capacity_dict'] , capacity)
        sheet.update(pkrc_centre[pkrc_dict[pkrc]]['date_times_dict'], date_times)
    
    if discharge == '':
        if passkey == pkrc_centre[pkrc_dict[pkrc]]['passkey_dict']:
            update_func2()
            status = 'Success'

        elif passkey == admin:
            update_func2()
            status = 'Success'
        else:
            status = 'Error'
    else:
        if passkey == pkrc_centre[pkrc_dict[pkrc]]['passkey_dict']:
            update_func()
            status = 'Success'

        elif passkey == admin:
            update_func()
            status = 'Success'
        else:
            status = 'Error'


    return render_template('result.html',
    date_times = date_times,
    pkrc=pkrc,
    pkrc_centre=pkrc_centre,
    pkrc_dict=pkrc_dict,
    a_male=a_male,
    a_female=a_female, 
    #booking=booking,
    capacity=capacity,
    passkey=passkey,
    status=status,
    admin=admin
    )

@app.route('/result_hospital', methods = ['POST'])
def result_hospital():

    date_times = (datetime.now() + timedelta(hours=8)).strftime("%d/%m/%Y %H:%M:%S")
    hospital = request.form['hospital']
    a_male = request.form['a_male']
    a_female = request.form['a_female']
    a_total = int(request.form['a_total'])
    #booking = request.form['booking']
    capacity = int(request.form['capacity'])
    passkey = request.form['passkey']
    admin = '5079'

    hospital_dict = { 'htaa_icu' : 0 , 'htaa_gen' : 1, 'hoshas_icu': 2, 'hoshas_gen': 3, 'hklipis_icu' : 4 , 'hklipis_gen' : 5 ,'hms': 6, 'hjka' : 7 ,  'hbentong' : 8 , 'hraub' : 9 , 'hoshka' : 10 }
    hospital_centre = hospital_list
    
    def update_func2():
        sheet.update(hospital_centre[hospital_dict[hospital]]['a_male_dict'] , a_male)
        sheet.update(hospital_centre[hospital_dict[hospital]]['a_female_dict'] , a_female)
        sheet.update(hospital_centre[hospital_dict[hospital]]['a_total_dict'] , a_total)
        sheet.update(hospital_centre[hospital_dict[hospital]]['capacity_dict'] , capacity)
        sheet.update(hospital_centre[hospital_dict[hospital]]['date_times_dict'], date_times)
    
    if passkey == hospital_centre[hospital_dict[hospital]]['passkey_dict']:
        update_func2()
        status = 'Success'

    elif passkey == admin:
        update_func2()
        status = 'Success'
    else:
        status = 'Error'
    
       
    return render_template('result2.html',
    date_times = date_times,
    hospital=hospital,
    hospital_centre=hospital_centre,
    hospital_dict=hospital_dict,
    a_male=a_male,
    a_female=a_female, 
    a_total=a_total,
    #booking=booking,
    capacity=capacity,
    passkey=passkey,
    status=status,
    admin=admin
    )

@app.route('/fullview', methods=['POST','GET'])
def fullview():

    maxhours=maxhour
    bor_colors = bor_color
      
    dict_sheet = sheet.get_all_records()
    date_times = (datetime.now() + timedelta(hours=8)).strftime("%d/%m/%Y %H:%M:%S")
    
    return render_template('fullview.html',  
    dict_sheet = dict_sheet,
    date_times=date_times,
    maxhours=maxhours,
    bor_colors=bor_colors,
    )

@app.route('/statistic', methods=['POST','GET'])
def statistic():
    def jumlah(item):
        item = [i[1] for i in item]
        item.pop(0)
        item = list(map(int, item))
        item = item[-15:]
        return item

    def jumlah_2(item):
        item = [i[1] for i in item]
        item.pop(0)
        item = list(map(int, item))
        item = item[-5:]
        return item

    def lelaki(item):
        item = [i[2] for i in item]
        item.pop(0)
        item = list(map(int, item))
        item = item[-15:]
        return item

    def perempuan(item):
        item = [i[3] for i in item]
        item.pop(0)
        item = list(map(int, item))
        item = item[-15:]
        return item

    master_list = master_stats_sh.get_all_values()
    sukpa_list = sukpa_stats_sh.get_all_values()
    ilkkm_list= ilkkm_stats_sh.get_all_values()
    ikpkt_list = ikpkt_stats_sh.get_all_values()
    kuipsas_list = kuipsas_stats_sh.get_all_values()
    maran_list = maran_stats_sh.get_all_values()
    ump_list = ump_stats_sh.get_all_values()
    uniten_list = uniten_stats_sh.get_all_values()
    temerloh_list = temerloh_stats_sh.get_all_values()
    ipglipis_list = ipglipis_stats_sh.get_all_values()
    rompin_list = rompin_stats_sh.get_all_values()
   
    tarikh = [i[0] for i in master_list]
    tarikh.pop(0)
    tarikh = tarikh[-15:]

    tarikh_2 = [i[0] for i in master_list]
    tarikh_2.pop(0)
    tarikh_2 = tarikh_2[-5:]
        
    date_times = (datetime.now() + timedelta(hours=8)).strftime("%d/%m/%Y %H:%M:%S")
    
    
    return render_template('statistic.html',  
    date_times=date_times,
    tarikh=tarikh,
    tarikh_2=tarikh_2,
    master_list=master_list,
    sukpa_list=sukpa_list,
    ilkkm_list=ilkkm_list,
    ump_list=ump_list,
    ikpkt_list=ikpkt_list,
    kuipsas_list=kuipsas_list,
    maran_list=maran_list,
    uniten_list=uniten_list,
    temerloh_list=temerloh_list,
    ipglipis_list=ipglipis_list,
    rompin_list=rompin_list,
    jumlah=jumlah,
    jumlah_2=jumlah_2,
    lelaki=lelaki,
    perempuan=perempuan
    )

@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500



if __name__ == '__main__':
    app.run(debug=False)