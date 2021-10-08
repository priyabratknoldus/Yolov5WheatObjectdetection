import os
from csv import DictWriter

from PIL import Image

from countwheatgrains import count
from detect import parse_opt, main
from predict import ricegrains

# class PostProcessing:
#     def __init__(self):
#         self.filename = "inputImage.jpg"
#         self.classifier = ricegrains(self.filename)


parent_directory = '/home/knoldus/Desktop/Dataset_A/from_APPLE_Dataset_A/50_GRAM'
env_dirs = os.listdir(parent_directory)
upload_folder = os.path.join('/home/knoldus/Downloads/objectdetectionwheat/yolov5/static/')


def processFiles():
    dict = {}
    return_dict = {}

    for env in env_dirs:
        img_dirs = ''
        extraPath = ''
        if env == 'SUNLIGHT':
            extraPath = '/PAPER/'
        else:
            extraPath = '/FLASH ON/PAPER/'

        img_dirs = parent_directory + '/' + env + extraPath

        for img in os.walk(img_dirs):
            dict[img[0]] = img[2]

    for key in dict:
        for img in dict[key]:
            imgPath = key + img
            print('Image Path- ', imgPath)
            riceGrainModel = ricegrains(imgPath)
            predict_result = riceGrainModel.predictionricegrains()
            print(predict_result[3])

            # 'image_name,A/B,S or A,50/100/150,W/I/O,On/Off,H/P,Broken,Damaged,Foreign Matter,Healthy,Immature,Potiya,Shrivelled,Wevilled \n'
            split_arr = imgPath.split('/')
            result_dict = {}
            result_dict['image_name'] = split_arr[-1]
            result_dict['A/B'] = split_arr[4]
            result_dict['S or A'] = split_arr[5].split('_')[1]
            result_dict['50/100/150'] = split_arr[6].split('_')[0]
            result_dict['W/I/O'] = split_arr[7]
            if imgPath.__contains__('SUNLIGHT'):
                result_dict['On/Off'] = 'N/A'
                result_dict['H/P'] = split_arr[8]
            else:
                result_dict['On/Off'] = split_arr[8]
                result_dict['H/P'] = split_arr[9]
            result_dict['Broken'] = predict_result[3]['Broken'] * 100
            result_dict['Damaged'] = predict_result[3]['Damaged'] * 100
            result_dict['Foreign Matter'] = predict_result[3]['ForeignMatters'] * 100
            result_dict['Healthy'] = predict_result[3]['Healthy'] * 100
            result_dict['Immature'] = predict_result[3]['Immature'] * 100
            result_dict['Potiya'] = predict_result[3]['Potiya'] * 100
            result_dict['Shrivelled'] = predict_result[3]['Shrivled'] * 100
            result_dict['Wevilled'] = predict_result[3]['Weevilled'] * 100

            return_dict[split_arr[-1]] = result_dict

    return return_dict


def predictRoute(path):
    image = Image.open(path)
    opt = parse_opt()
    damaged = main(opt)

    # decodeImage(image, clApp.filename)
    try:
        result = ricegrains.predictionricegrains()
        full_filename = os.path.join(upload_folder, 'inputImage.jpg')
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


#         return predict="Low Probability Score", cnt = "No Count",
#         user_image = "Image is not Available", result = "No Result", damaged = "No Result"
#
#
# return predict=predict, cnt = cnt, user_image = full_filename, result = result,
# grainWeight = grainWeight, damaged = damaged

def writecsv(header, dict):
    # Open your CSV file in append mode
    # Create a file object for this file

    os.remove("/home/knoldus/Downloads/objectdetectionwheat/yolov5/Result.csv")

    with open('Result.csv', 'a') as f_object:
        # Pass the file object and a list
        # of column names to DictWriter()
        # You will get a object of DictWriter
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)
        dictwriter_object.writeheader()

        # Pass the dictionary as an argument to the Writerow()
        for key in dict:
            dictwriter_object.writerow(dict[key])

        # Close the file object
        f_object.close()


if __name__ == "__main__":
    # clApp = PostProcessing()
    dict = processFiles()
    field_names = ['image_name', 'A/B', 'S or A', '50/100/150', 'W/I/O', 'On/Off', 'H/P', 'Broken', 'Damaged',
                   'Foreign Matter', 'Healthy', 'Immature', 'Potiya', 'Shrivelled', 'Wevilled']

    writecsv(field_names, dict)

    csv = 'image_name,A/B,S or A,50/100/150,W/I/O,On/Off,H/P,Broken,Damaged,Foreign Matter,Healthy,Immature,Potiya,Shrivelled,Wevilled \n'

# riceGrainModel = ricegrains('/home/knoldus/Downloads/objectdetectionwheat/yolov5/static/inputImage.jpg')
# predict_result = riceGrainModel.predictionricegrains()
# print(predict_result[3])
