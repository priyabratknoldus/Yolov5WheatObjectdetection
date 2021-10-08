import os

from PIL import Image
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin

from countwheatgrains import count
from detect import parse_opt, main
from predict import ricegrains

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)


# @cross_origin()
class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = ricegrains(self.filename)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index6.html')


PEOPLE_FOLDER = os.path.join('/home/knoldus/Downloads/objectdetectionwheat/yolov5/static/')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER


@app.route("/predictRoute", methods=['POST'])
@cross_origin()
def predictRoute():
    # if os.path.exists('/home/knoldus/Downloads/rice-quality-analysis-master (1)/Rice-Grain-Image-Classification-master/static/inputImage.jpg'): os.remove(
    #     '/home/knoldus/Downloads/rice-quality-analysis-master (1)/Rice-Grain-Image-Classification-master/static/inputImage.jpg')
    if request.method == 'POST':

        # image = request.json['filename']
        file = request.files['filename']
        # Read the image via file.stream
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'inputImage.jpg'))
        image = Image.open(file.stream)
        file.close()
        opt = parse_opt()
        damaged = main(opt)
        print(damaged)
        # decodeImage(image, clApp.filename)
        try:
            result = clApp.classifier.predictionricegrains()
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'inputImage.jpg')
            cnt = count()

            print('test2')

            float_number = round(float(result[2][0][0] * 100), 2)
            print(float_number)
            # finalresult = print("Broken: " + str(float(result[2][0][0])) + "; Damaged: " + str(float(result[2][0][1])) + "; FM: " + str(float(result[2][0][2])))
            finalresult = "Broken: " + str(round(float(result[2][0][0] * 100), 2)) + "%; Damaged: " + str(
                round(float(result[2][0][1] * 100), 2)) + "\n" \
                                                          "%; ForeignMatters: " + str(
                round(float(result[2][0][2] * 100), 2)) + "%; Healthy: " + str(round(float(result[2][0][3] * 100), 2)) + \
                          "%; Immature: " + str(round(float(result[2][0][4] * 100), 2)) + "%; Potiya: " + str(
                round(float(result[2][0][5] * 100), 2)) + \
                          "%; Shriveled: " + str(round(float(result[2][0][6] * 100), 2)) + "%; Weevilled: " + str(
                round(float(result[2][0][7] * 100), 2)) + "\n" \
                                                          "%"

            # print(finalresult)

            predict = result[0]['image']
            # cnt = result[1]
            # el1 = data['array'][0]
            result = finalresult
            grainWeight = cnt * .065
            damaged = damaged



        except Exception as e:
            print(e)
            return render_template('index6.html', predict="Low Probability Score", cnt="No Count",
                                   user_image="Image is not Available", result="No Result", damaged="No Result")

    return render_template('index6.html', predict=predict, cnt=cnt, user_image=full_filename, result=result,
                           grainWeight=grainWeight, damaged=damaged)


# port = int(os.getenv("PORT"))
if __name__ == "__main__":
    clApp = ClientApp()
    # app.run(host='0.0.0.0', port=port)
    app.run(host='0.0.0.0', port=8000, debug=True)
