from flask import Flask, render_template, request

app = Flask(__name__)

# Your existing class and function definitions

class Zones:
    def __init__(self, zone2, zone5, zone7):
        self.zone2 = zone2
        self.zone5 = zone5
        self.zone7 = zone7

class Volume:
    def __init__(self, week1, week2, week3, week4, week1z2, week1hi, week2z2, week2hi, week3z2, week3hi, week4z2, week4hi):
        self.week1 = week1
        self.week2 = week2
        self.week3 = week3
        self.week4 = week4
        self.week1z2 = week1z2
        self.week1hi = week1hi
        self.week2z2 = week2z2
        self.week2hi = week2hi
        self.week3z2 = week3z2
        self.week3hi = week3hi
        self.week4z2 = week4z2
        self.week4hi = week4hi
    def intervals_30s(self, time):
        if time<=1:
            return 10
        else:
            n=(time-(5/6))/(1/60)
            if n<=30:
                return n
            else:
                return 30


    def intervals_4min(self, time):
        if time<=1:
            return 2
        else:

            n=(time-(2/3))/(2/15)
            if n<=8:
                return n
            else:
                return 8

# Generating the workout plan for 4 weeks and 7 days per week
def generate_workout_plan(ftp, hours):
    zones = get_zone(ftp)
    volume=calculate_weekly_volume(hours)
    ftp = int(ftp)
    hours = int(hours)
    return  f"""
            week1: {convert(volume.week1)}\n
            M:rest day\n
            T:4min intervals({convert(volume.week1hi/2)}): 20 warmup|(4min @ {zones.zone5} + 4min rest)x{round(volume.intervals_4min((volume.week1hi)/2))}|20min cooldown\n
            W:zone2: {convert((volume.week1z2)/4)} @ {zones.zone2}\n
            T:rest day\n
            F:30s intervals ({convert(volume.week1hi/2)}): 20 warmup|(30s @ {zones.zone7} + 30s rest)x{round((volume.intervals_30s((volume.week1hi)/2))/2)}|2 sets||20min cooldown \n
            S:zone2: {convert((volume.week1z2)/4)} @ {zones.zone2}\n
            S:zone2: {convert((volume.week1z2)/2)} @ {zones.zone2}\n
            \n
            week2: {convert(volume.week2)}\n
            M:rest day\n
            T:4min intervals({convert(volume.week2hi/2)}): 20 warmup|(4min @ {zones.zone5} + 4min rest)x{round(volume.intervals_4min((volume.week2hi)/2))}|20min cooldown\n
            W:zone2: {convert((volume.week2z2)/4)} @ {zones.zone2}\n
            T:rest day\n
            30s intervals ({convert(volume.week2hi/2)}): 20 warmup|(30s @ {zones.zone7} + 30s rest)x{round((volume.intervals_30s((volume.week2hi)/2)/2))}|2 sets||20min cooldown \n
            S:zone2: {convert((volume.week2z2)/4)} @ {zones.zone2}\n
            S:zone2: {convert((volume.week2z2)/2)} @ {zones.zone2}\n
            \n
            week3: {convert(volume.week3)}\n
            M:rest day\n
            T:4min intervals({convert(volume.week3hi/2)}): 20 warmup|(4min @ {zones.zone5} + 4min rest)x{round(volume.intervals_4min((volume.week3hi)/2))}|20min cooldown\n
            W:zone2: {convert((volume.week3z2)/4)} @ {zones.zone2}\n
            T:rest day\n
            F:30s intervals ({convert(volume.week3hi/2)}): 20 warmup|(30s @ {zones.zone7} + 30s rest)x{round((volume.intervals_30s((volume.week3hi)/2)/2))}|2 sets||20min cooldown \n
            S:zone2: {convert((volume.week3z2)/4)} @ {zones.zone2}\n
            S:zone2: {convert((volume.week3z2)/2)} @ {zones.zone2}\n
            \n
            week4: {convert(volume.week4)}\n
            M:rest day\n
            T:4min intervals({convert(volume.week4hi/2)}): 20 warmup|(4min @ {zones.zone5} + 4min rest)x{round(volume.intervals_4min((volume.week4hi)/2))}|20min cooldown\n
            W:zone2: {convert((volume.week4z2)/4)} @ {zones.zone2}\n
            T:rest day\n
            F:30s intervals ({convert(volume.week4hi/2)}): 20 warmup|(30s @ {zones.zone7} + 30s rest)x{round(volume.intervals_30s((volume.week4hi)/2))}|20min cooldown \n
            S:zone2: {convert((volume.week4z2)/4)} @ {zones.zone2}\n
            S:zone2: {convert((volume.week4z2)/2)} @ {zones.zone2}\n
            """
  
def calculate_weekly_volume(hours):
    x = int(hours) / 1.025

    week1 = x
    week2 = 1.2 * x
    week3 = 1.4 * x
    week4 = 0.5 * x

    week1z2=week1*0.8
    week1hi=week1*0.2
    week2z2=week2*0.8
    week2hi=week2*0.2
    week3z2=week3*0.8
    week3hi=week3*0.2
    week4z2=week4*0.8
    week4hi=week4*0.2

    return Volume(week1, week2, week3, week4, week1z2, week1hi, week2z2, week2hi, week3z2, week3hi, week4z2, week4hi)



def get_zone(ftp):
    zone2 = f"{round(int(ftp) * 0.55)} to {round(int(ftp) * 0.75)} watts"
    zone5 = f"{round(int(ftp) * 1.1)} to {round(int(ftp) * 1.25)} watts"
    zone7 = f"{round(int(ftp)*1.3)} to {round(int(ftp)*1.8)} watts"
    return Zones(zone2,zone5,zone7)

def convert(total_hours):

    whole_hours = int(total_hours)
    minutes = int((total_hours - whole_hours) * 60)

    if whole_hours == 0:
        return f"{minutes} min"
    elif minutes == 0:
        return f"{whole_hours} h"
    else:
        return f"{whole_hours} h {minutes} min"
@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        ftp = request.form["ftp"]
        hours = request.form["hours"]
        output = generate_workout_plan(ftp, hours)
    return render_template("index.html", output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

