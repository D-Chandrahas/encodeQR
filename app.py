import qrcode
import numpy as np
from flask import Flask


app = Flask(__name__)

DEFAULT_TEXT = "https://github.com/D-Chandrahas/encodeQR"

@app.route("/", methods=["GET"])
@app.route("/<path:text>", methods=["GET"])
def return_qr(text = DEFAULT_TEXT):

    # generate qr code as binary matrix
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=1,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    qr = qr.make_image(fill_color="black", back_color="white")
    qr = np.array(qr)


    # if height of qr code is odd, append one row of zeros
    # since each block character is 2x1 (height x width)
    if (qr.shape[0]%2 == 1):
        qr = np.vstack((qr, np.zeros((1, qr.shape[1]), dtype=bool)))

    res_str = []

    # print the qr code using block unicode chars ('▄','█','▀',' ')
    for i in range(0, qr.shape[0], 2):

        for j in range(qr.shape[1]):

            if qr[i,j] == True and qr[i+1,j] == True:
                res_str.append("█")

            elif qr[i,j] == True and qr[i+1,j] == False:
                res_str.append("▀")

            elif qr[i,j] == False and qr[i+1,j] == True:
                res_str.append("▄")

            else:
                res_str.append(" ")

        res_str.append("\n")

    return "".join(res_str)
