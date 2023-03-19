import qrcode
img = qrcode.make('1231212312123121231212312')
img.save('simpleqrcode.jpg')
#img.show()

# qr = qrcode.QRCode(
#     version=2,
#     error_correction=qrcode.constants.ERROR_CORRECT_L,
#     box_size=10,
#     border=4,
# )

# qr.add_data('1231212312123121231212312')

# qr.make(fit=True)
# img = qr.make_image()
# filename = 'qrcode_dome.png'
# img.save(filename)